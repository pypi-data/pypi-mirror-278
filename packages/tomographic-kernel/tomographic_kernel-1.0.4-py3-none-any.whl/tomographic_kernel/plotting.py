import logging
import os
from concurrent import futures

import astropy.units as au
import numpy as np
import pylab as plt
from h5parm import DataPack
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon, Circle
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.spatial import ConvexHull, cKDTree
from scipy.spatial import Voronoi
from scipy.spatial.distance import pdist

from tomographic_kernel.tomographic_kernel import TEC_CONV

logger = logging.getLogger(__name__)

try:
    import cmocean

    phase_cmap = cmocean.cm.phase
except ImportError:
    phase_cmap = plt.cm.hsv


def add_colorbar_to_axes(ax, cmap, norm=None, vmin=None, vmax=None):
    """
    Add colorbar to axes easily.

    Args:
        ax: Axes
        cmap: str or cmap
        norm: Normalize or None
        vmin: lower limit of color if norm is None
        vmax: upper limit of color if norm is None
    """
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    if norm is None:
        norm = plt.Normalize(vmin=vmin, vmax=vmax)
    sm = plt.cm.ScalarMappable(norm, cmap=plt.cm.get_cmap(cmap))
    ax.figure.colorbar(sm, cax=cax, orientation='vertical')


def plot_vornoi_map(points, colors, ax=None, alpha=1., radius=None, norm=None, vmin=None, vmax=None, cmap=plt.cm.PuOr,
                    relim=True, colorbar=True, fov_circle=False):
    """
    Plot a Vornoi tesselation of data.

    Args:
        points: [N,2] coordinates of points
        colors: [N] values at points
        ax: None, or an Axes
        alpha: alpha of colors for blending
        radius: technical
        norm:
        vmin:
        vmax:
        cmap:
        relim:
        colorbar:

    Returns:

    """
    if cmap == 'phase':
        cmap = phase_cmap

    if norm is None:
        norm = plt.Normalize(np.nanmin(colors) if vmin is None else vmin,
                             np.nanmax(colors) if vmax is None else vmax)

    if radius is None:
        radius = np.max(np.linalg.norm(points - np.mean(points, axis=0), axis=1))

    def voronoi_finite_polygons_2d(vor, radius=radius):
        """
        Reconstruct infinite voronoi regions in a 2D diagram to finite
        regions.

        Parameters
        ----------
        vor : Voronoi
            Input diagram
        radius : float, optional
            Distance to 'points at infinity'.

        Returns
        -------
        regions : list of tuples
            Indices of vertices in each revised Voronoi regions.
        vertices : list of tuples
            Coordinates for revised Voronoi vertices. Same as coordinates
            of input vertices, with 'points at infinity' appended to the
            end.

        """

        if vor.points.shape[1] != 2:
            raise ValueError("Requires 2D input")

        new_regions = []
        new_vertices = vor.vertices.tolist()

        center = vor.points.mean(axis=0)
        # if radius is None:
        #     radius = np.max(np.linalg.norm(points - np.mean(points, axis=0),axis=1))
        #     # radius = vor.points.ptp().max()

        # Construct a map containing all ridges for a given point
        all_ridges = {}
        for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
            all_ridges.setdefault(p1, []).append((p2, v1, v2))
            all_ridges.setdefault(p2, []).append((p1, v1, v2))

        # Reconstruct infinite regions
        for p1, region in enumerate(vor.point_region):
            vertices = vor.regions[region]

            if all(v >= 0 for v in vertices):
                # finite region
                new_regions.append(vertices)
                continue

            # reconstruct a non-finite region
            ridges = all_ridges[p1]
            new_region = [v for v in vertices if v >= 0]

            for p2, v1, v2 in ridges:
                if v2 < 0:
                    v1, v2 = v2, v1
                if v1 >= 0:
                    # finite ridge: already in the region
                    continue

                # Compute the missing endpoint of an infinite ridge

                t = vor.points[p2] - vor.points[p1]  # tangent
                t /= np.linalg.norm(t)
                n = np.array([-t[1], t[0]])  # normal

                midpoint = vor.points[[p1, p2]].mean(axis=0)
                direction = np.sign(np.dot(midpoint - center, n)) * n
                far_point = vor.vertices[v2] + direction * radius

                new_region.append(len(new_vertices))
                new_vertices.append(far_point.tolist())

            # sort region counterclockwise
            vs = np.asarray([new_vertices[v] for v in new_region])
            c = vs.mean(axis=0)
            angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
            new_region = np.array(new_region)[np.argsort(angles)]

            # finish
            new_regions.append(new_region.tolist())

        return new_regions, np.asarray(new_vertices)

    # compute Voronoi tesselation
    vor = Voronoi(points)

    # plot
    regions, vertices = voronoi_finite_polygons_2d(vor)

    if ax is None:
        fig, ax = plt.subplots(1, 1)
    # colorize
    for color, region in zip(colors, regions):
        if np.size(color) == 1:
            if norm is None:
                color = cmap(color)
            else:
                color = cmap(norm(color))
        polygon = vertices[region]
        ax.fill(*zip(*polygon), color=color, alpha=alpha)

    # plt.plot(points[:,0], points[:,1], 'ko')
    if relim:
        min_bound = np.min(points, axis=0)
        max_bound = np.max(points, axis=0)
        box_size = max_bound - min_bound
        ax.set_xlim(min_bound[0] - 0.1 * box_size[0], max_bound[0] + 0.1 * box_size[0])
        ax.set_ylim(min_bound[1] - 0.1 * box_size[1], max_bound[1] + 0.1 * box_size[1])

    if colorbar:
        add_colorbar_to_axes(ax, cmap, norm=norm)

    if fov_circle:
        ax.add_patch(Circle(np.mean(points, axis=0), radius=radius, edgecolor='black', lw=2., facecolor='none'))
    return ax


class DatapackPlotter(object):
    def __init__(self, datapack):
        if isinstance(datapack, str):
            datapack = DataPack(filename=datapack, readonly=True)
        self.datapack = datapack

    def _create_polygon_plot(self, points, values=None, N=None, ax=None, cmap=plt.cm.PuOr, overlay_points=None,
                             annotations=None, title=None, polygon_labels=None, reverse_x=False):
        # get nearest points (without odd voronoi extra regions)
        k = cKDTree(points)
        dx = np.max(points[:, 0]) - np.min(points[:, 0])
        dy = np.max(points[:, 1]) - np.min(points[:, 1])
        delta = pdist(points)

        N = N or int(min(max(100, 2 * np.max(delta) / np.min(delta)), 500))
        x = np.linspace(np.min(points[:, 0]) - 0.1 * dx, np.max(points[:, 0]) + 0.1 * dx, N)
        y = np.linspace(np.min(points[:, 1]) - 0.1 * dy, np.max(points[:, 1]) + 0.1 * dy, N)
        X, Y = np.meshgrid(x, y, indexing='ij')
        # interior points population
        points_i = np.array([X.flatten(), Y.flatten()]).T
        # The match per input point
        dist, i = k.query(points_i, k=1)
        # the polygons are now created using convex hulls
        # order is by point order
        patches = []
        for group in range(points.shape[0]):
            points_g = points_i[i == group, :]
            if points_g.size == 0:
                logger.debug("Facet {} has zero size".format(group))
                poly = Polygon(points[group:group + 1, :], closed=False)
            else:
                hull = ConvexHull(points_g)
                nodes = points_g[hull.vertices, :]
                poly = Polygon(nodes, closed=False)
            patches.append(poly)
        if ax is None:
            fig, ax = plt.subplots()
            logger.info("Making new plot")
        if values is None:
            values = np.zeros(len(patches))  # random.uniform(size=len(patches))
        p = PatchCollection(patches)
        # p.set_array(values)
        ax.add_collection(p)
        # plt.colorbar(p)
        if overlay_points is not None:
            if annotations is None:
                ax.scatter(overlay_points[:, 0], overlay_points[:, 1], marker='+', c='black')
            else:
                for point, a in zip(overlay_points, annotations):
                    ax.text(point[0], point[1], a, ha='center', va='center', backgroundcolor=(1., 1., 1., 0.1))

        if reverse_x:
            ax.set_xlim([np.max(points_i[:, 0]), np.min(points_i[:, 0])])
        else:
            ax.set_xlim([np.min(points_i[:, 0]), np.max(points_i[:, 0])])
        ax.set_ylim([np.min(points_i[:, 1]), np.max(points_i[:, 1])])
        ax.set_facecolor('black')
        ax.grid(b=True, color='black')
        if title is not None:
            if reverse_x:
                ax.text(np.max(points_i[:, 0]) - 0.05 * dx, np.max(points_i[:, 1]) - 0.05 * dy, title, ha='left',
                        va='top', backgroundcolor=(1., 1., 1., 0.5))
            else:
                ax.text(np.min(points_i[:, 0]) + 0.05 * dx, np.max(points_i[:, 1]) - 0.05 * dy, title, ha='left',
                        va='top', backgroundcolor=(1., 1., 1., 0.5))
        #            Rectangle((x, y), 0.5, 0.5,
        #    alpha=0.1,facecolor='red',label='Label'))
        #            ax.annotate(title,xy=(0.8,0.8),xycoords='axes fraction')
        return ax, p

    def _create_image_plot(self, points, values=None, N=None, ax=None, cmap=plt.cm.PuOr, overlay_points=None,
                           annotations=None, title=None, reverse_x=False):
        '''
        Create initial plot, with image data instead of polygons.
        points: (ra, dec)
        values: array [n, m] or None, assumes (dec, ra) ordering ie (y,x)
        '''
        dx = np.max(points[0]) - np.min(points[0])
        dy = np.max(points[1]) - np.min(points[1])
        if values is not None:
            Ndec, Nra = values.shape
        else:
            Ndec, Nra = len(points[1]), len(points[0])
            values = np.zeros([Ndec, Nra])
        if ax is None:
            fig, ax = plt.subplots()
            logger.info("Making new plot")

        x = np.linspace(np.min(points[0]), np.max(points[0]), Nra)
        y = np.linspace(np.min(points[1]), np.max(points[1]), Ndec)
        img = ax.imshow(values, origin='lower', cmap=cmap, aspect='auto', extent=(x[0], x[-1], y[0], y[-1]))
        if overlay_points is not None:
            if annotations is None:
                ax.scatter(overlay_points[:, 0], overlay_points[:, 1], marker='+', c='black')
            else:
                for point, a in zip(overlay_points, annotations):
                    ax.text(point[0], point[1], a, ha='center', va='center', backgroundcolor=(1., 1., 1., 0.1))
        if reverse_x:
            ax.set_xlim([x[-1], x[0]])
        else:
            ax.set_xlim([x[0], x[-1]])
        ax.set_ylim([y[0], y[-1]])
        ax.set_facecolor('black')
        ax.grid(b=True, color='black')
        if title is not None:
            if reverse_x:
                ax.text(x[-1] - 0.05 * dx, y[-1] - 0.05 * dy, title, ha='left', va='top',
                        backgroundcolor=(1., 1., 1., 0.5))
            else:
                ax.text(x[0] + 0.05 * dx, y[-1] - 0.05 * dy, title, ha='left', va='top',
                        backgroundcolor=(1., 1., 1., 0.5))
        return ax, img

    def plot(self, ant_sel=None, time_sel=None, freq_sel=None, dir_sel=None, pol_sel=None, fignames=None, vmin=None,
             vmax=None, mode='perantenna', observable='phase', phase_wrap=True, log_scale=False, plot_crosses=True,
             plot_facet_idx=False, plot_patchnames=False, labels_in_radec=False, plot_arrays=False,
             solset=None, plot_screen=False, tec_eval_freq=None, per_plot_scale=False, per_timestep_scale=False,
             mean_residual=False, cmap=None,
             overlay_solset=None, **kwargs):
        """

        :param ant_sel:
        :param time_sel:
        :param freq_sel:
        :param dir_sel:
        :param pol_sel:
        :param fignames:
        :param vmin:
        :param vmax:
        :param mode:
        :param observable:
        :param phase_wrap:
        :param log_scale:
        :param plot_crosses:
        :param plot_facet_idx:
        :param plot_patchnames:
        :param labels_in_radec:
        :param show:
        :param plot_arrays:
        :param solset:
        :param plot_screen:
        :param tec_eval_freq:
        :param kwargs:
        :return:
        """
        SUPPORTED = ['perantenna']
        assert mode in SUPPORTED, "only 'perantenna' supported currently".format(SUPPORTED)
        if fignames is None:
            save_fig = False
            show = True
        else:
            save_fig = True

        if plot_patchnames:
            plot_facet_idx = False
        if plot_patchnames or plot_facet_idx:
            plot_crosses = False
        if overlay_solset is not None:
            plot_overlay = True
        else:
            plot_overlay = False

        ###
        # Set up plotting

        with self.datapack:
            self.datapack.current_solset = solset
            logger.info(
                "Applying selection: ant={},time={},freq={},dir={},pol={}".format(ant_sel, time_sel, freq_sel, dir_sel,
                                                                                  pol_sel))
            self.datapack.select(ant=ant_sel, time=time_sel, freq=freq_sel, dir=None, pol=pol_sel)
            axes = self.datapack.__getattr__(
                "axes_" + observable if 'weights_' not in observable else observable.replace('weights_', 'axes_'))
            full_patch_names, _ = self.datapack.get_directions(axes['dir'])

            self.datapack.select(ant=ant_sel, time=time_sel, freq=freq_sel, dir=dir_sel, pol=pol_sel)
            obs, axes = self.datapack.__getattr__(observable)
            # flags = np.zeros_like(obs, dtype=np.bool)
            if observable.startswith('weights_'):
                # obs = np.sqrt(np.abs(1. / obs))  # uncert from weights = 1/var
                # obs = np.sqrt(obs)  # uncert from weights = 1/var
                phase_wrap = False
            if plot_overlay:
                self.datapack.current_solset = overlay_solset
                overlay_obs, overlay_axes = self.datapack.__getattr__(observable)
                weights, _ = self.datapack.__getattr__("weights_" + observable)
                _, flag_directions = self.datapack.get_directions(overlay_axes['dir'])
                logger.info("Flagging observables based on inf uncertanties")
                flags = weights == np.inf
                self.datapack.current_solset = solset
            else:
                flags = obs.copy()
                overlay_obs = obs.copy()

            if 'pol' in axes.keys():
                # plot only first pol selected
                obs = obs[0, ...]
                flags = flags[0, ...]
                overlay_obs = overlay_obs[0, ...]

            # obs is dir, ant, freq, time
            antenna_labels, antennas = self.datapack.get_antennas(axes['ant'])
            patch_names, directions = self.datapack.get_directions(axes['dir'])

            timestamps, times = self.datapack.get_times(axes['time'])
            freq_dep = True
            try:
                freq_labels, freqs = self.datapack.get_freqs(axes['freq'])
            except:
                freq_dep = False
                obs = obs[:, :, None, :]
                overlay_obs = overlay_obs[:, :, None, :]
                flags = flags[:, :, None, :]
                freq_labels, freqs = [""], [None]

            if tec_eval_freq is not None:
                # phase_wrap = True
                obs = obs * TEC_CONV / tec_eval_freq
                overlay_obs = overlay_obs * TEC_CONV / tec_eval_freq

                if observable.startswith('weights_'):
                    obs = np.abs(obs)
                    overlay_obs = np.abs(overlay_obs)

            if log_scale:
                obs = np.log10(obs)
                overlay_obs = np.log10(overlay_obs)

            if phase_wrap:
                obs = np.arctan2(np.sin(obs), np.cos(obs))
                overlay_obs = np.arctan2(np.sin(overlay_obs), np.cos(overlay_obs))
                vmin = -np.pi
                vmax = np.pi
                cmap = phase_cmap if cmap is None else cmap
            else:
                vmin = vmin or np.nanmin(obs)
                vmax = vmax or np.nanmax(obs)
                cmap = plt.cm.PuOr if cmap is None else cmap

            norm = plt.Normalize(vmin, vmax)

            Na = len(antennas)
            Nt = len(times)
            Nd = len(directions)
            Nf = len(freqs)
            fixfreq = Nf >> 1
            logger.info("Plotting {} directions".format(Nd))
            logger.info("Plotting {} antennas".format(Na))
            logger.info("Plotting {} timestamps".format(Nt))

            _, antennas_ = self.datapack.get_antennas([self.datapack.ref_ant])

            ref_dist = np.sqrt(
                (antennas.x - antennas_.x) ** 2 + (antennas.y - antennas_.y) ** 2 + (antennas.z - antennas_.z) ** 2).to(
                au.km).value
            #            if labels_in_radec:
            ra = directions.ra.deg
            dec = directions.dec.deg
            if not plot_screen:
                ### points are normal
                points = np.array([ra, dec]).T
                if plot_crosses or plot_patchnames or plot_facet_idx:
                    overlay_points = points
                else:
                    overlay_points = None
            else:
                ### get unique ra and dec and then rearrange into correct order.
                _ra = np.unique(ra)
                _dec = np.unique(dec)
                Nra = len(_ra)
                Ndec = len(_dec)
                assert Ndec * Nra == Nd
                ### sort lexiconially
                ind = np.lexsort((ra, dec))
                points = (_ra, _dec)
                obs = obs[ind, ...]
                obs = obs.reshape((Ndec, Nra, Na, Nf, Nt))
                if plot_crosses:
                    overlay_points = None  # put the facet (ra,dec).T
                else:
                    overlay_points = None
        if plot_patchnames:
            annotations = patch_names
        elif plot_facet_idx:
            facet_inv_map = [list(full_patch_names).index(ts) for ts in patch_names]
            annotations = np.array([str(facet_inv_map[k]) for k in range(Nd)])
        else:
            annotations = None

        if fignames is not None:
            if not isinstance(fignames, (tuple, list)):
                fignames = [fignames]
        if fignames is not None:
            if Nt > len(fignames):
                fignames = fignames[:Nt]
            if Nt < len(fignames):
                logger.info("Nt<len(fignames)")
                raise ValueError("Gave too few fignames.")

        if mode == 'perantenna':

            M = int(np.ceil(np.sqrt(Na)))
            fig, axs = plt.subplots(nrows=M, ncols=M, sharex='col', sharey='row', squeeze=False, figsize=(4 * M, 4 * M))
            fig.subplots_adjust(wspace=0., hspace=0.)
            axes_patches = []
            axes_overlay = []
            c = 0
            for row in range(M):
                for col in range(M):
                    ax = axs[row, col]
                    if col == 0:
                        ax.set_ylabel("Projected North (radians)" if not labels_in_radec else "DEC (deg)")

                    if row == M - 1:
                        ax.set_xlabel("Projected East (radians)" if not labels_in_radec else "RA (deg)")

                    if c >= Na:
                        continue
                    try:
                        title = antenna_labels[c].decode()
                    except:
                        title = antenna_labels[c]
                    if plot_screen:
                        _, p = self._create_image_plot(points, values=None, N=None,
                                                       ax=ax, cmap=cmap, overlay_points=overlay_points,
                                                       annotations=annotations,
                                                       title="{} {:.1f}km".format(title, ref_dist[c]),
                                                       reverse_x=labels_in_radec)
                    else:
                        _, p = self._create_polygon_plot(points, values=None, N=None,
                                                         ax=ax, cmap=cmap, overlay_points=overlay_points,
                                                         annotations=annotations,
                                                         title="{} {:.1f}km".format(title, ref_dist[c]),
                                                         reverse_x=labels_in_radec)
                    if plot_overlay:
                        sc = ax.scatter(flag_directions.ra.deg, flag_directions.dec.deg,
                                        s=50 * np.ones(len(flag_directions)), ec=cmap(np.ones(len(flag_directions))),
                                        linewidths=1. * np.ones(len(flag_directions)),
                                        fc=cmap(np.ones(len(flag_directions))))
                        axes_overlay.append(sc)
                    axes_patches.append(p)
                    c += 1

            if not per_plot_scale:
                fig.subplots_adjust(right=0.85)
                cbar_ax = fig.add_axes([0.875, 0.15, 0.025, 0.7])
                cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbar_ax, orientation='vertical')
                # cb = ColorbarBase(cbar_ax, cmap=cmap,
                #                   norm=norm, orientation='vertical')

            for j in range(Nt):
                logger.info("Plotting {}".format(timestamps[j]))
                if not plot_screen:
                    _datum = obs[:, :, fixfreq, j]
                    _overlay_datum = overlay_obs[:, :, fixfreq, j]
                    _flagum = flags[:, :, fixfreq, j]
                else:
                    _datum = obs[:, :, :, fixfreq, j]
                    _overlay_datum = overlay_obs[:, :, :, fixfreq, j]
                    _flagum = flags[:, :, :, fixfreq, j]

                if per_timestep_scale:
                    vmin = np.nanmin(_datum)  # np.nanpercentile(_datum, 5./_datum.size*100.)
                    vmax = np.nanmax(_datum)  # np.nanpercentile(_datum,100. - 5./_datum.size*100.)
                    norm = plt.Normalize(vmin, vmax)
                    cb.update_normal(plt.cm.ScalarMappable(norm=norm, cmap=cmap))
                for i in range(Na):
                    if not plot_screen:
                        datum = _datum[:, i]
                        overlay_datum = _overlay_datum[:, i]
                        flagum = _flagum[:, i]
                    else:
                        datum = _datum[:, :, i]
                        overlay_datum = _overlay_datum[:, :, i]
                        flagum = _flagum[:, :, i]

                    if per_plot_scale:
                        vmin = np.nanmin(datum)  # np.nanpercentile(datum, 2./_datum.size*100.)
                        vmax = np.nanmax(datum)  # np.nanpercentile(datum, 100. - 2./_datum.size*100.)
                        norm = plt.Normalize(vmin, vmax)
                    colors = cmap(norm(datum))
                    if plot_overlay:
                        lws = 1. * np.ones(flagum.size)
                        lws[flagum] = 2.
                        s = 50. * np.ones(flagum.size)
                        s[flagum] = 100.
                        ecolors = cmap(norm(overlay_datum))
                        fcolors = cmap(norm(overlay_datum))
                        ecolors[..., 0][flagum] = 1.  # [1., 0., 0., 1.]
                        ecolors[..., 1][flagum] = 0.  # [1., 0., 0., 1.]
                        ecolors[..., 2][flagum] = 0.  # [1., 0., 0., 1.]
                        ecolors[..., 3][flagum] = 1.  # [1., 0., 0., 1.]
                        axes_overlay[i].set_facecolors(fcolors)
                        axes_overlay[i].set_edgecolors(ecolors)
                        axes_overlay[i].set_linewidths(lws)
                        axes_overlay[i].set_sizes(s)
                    if plot_screen:
                        axes_patches[i].set_array(colors)
                    else:
                        axes_patches[i].set_color(colors)

                axs[0, 0].set_title("{} {} : {}".format(observable, freq_labels[fixfreq], timestamps[j]))
                fig.canvas.draw()
                if save_fig:
                    plt.savefig(fignames[j])


def _parallel_plot(arg):
    datapack, time_slice, kwargs, output_folder = arg
    dp = DatapackPlotter(datapack=datapack)
    with dp.datapack:
        dp.datapack.current_solset = kwargs.get('solset', 'sol000')
        # Get the time selection desired
        dp.datapack.select(time=kwargs.get('time_sel', None))
        soltabs = dp.datapack.soltabs
        axes = {k: v for (v, k) in zip(*dp.datapack.soltab_axes(soltabs[0]))}
    # timeslice the selection
    times = axes['time']  # mjs
    # sel_list = list(range(len(times))[time_slice])#times[time_slice]
    kwargs['time_sel'] = time_slice  # sel_list
    fignames = [os.path.join(output_folder, "fig-{:04d}.png".format(j)) for j in range(len(times))[time_slice]]
    dp.plot(fignames=fignames, **kwargs)
    return fignames


def animate_datapack(datapack, output_folder, num_processes, **kwargs):
    """
    Plot the datapack in parallel, then stitch into movie.
    datapack: str the datapack filename
    output_folder: str, folder to store figs in
    num_processes: int number of parallel plotting processes to run
    **kwargs: keywords to pass to DatapackPlotter.plot function.
    """
    os.makedirs(output_folder, exist_ok=True)

    if num_processes is None:
        num_processes = 1  # psutil.cpu_count()

    if isinstance(datapack, DataPack):
        datapack = datapack.filename

    #    with DataPack(datapack) as datapack_fix:
    #        datapack_fix.add_antennas(DataPack.lofar_array)

    args = []
    for i in range(num_processes):
        args.append((datapack, slice(i, None, num_processes), kwargs, output_folder))
    with futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        jobs = executor.map(_parallel_plot, args)
        results = list(jobs)
    plt.close('all')
    make_animation(output_folder, prefix='fig', fps=4)


def make_animation(datafolder, prefix='fig', fps=4):
    '''Given a datafolder with figures of format `prefix`-%04d.png create a
    video at framerate `fps`.
    Output is datafolder/animation.mp4'''
    if os.system(
            'ffmpeg -y -framerate {} -i {}/{}-%04d.png -vf scale="trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -profile:v high -pix_fmt yuv420p -g 30 -r 30 {}/animation.mp4'.format(
                fps, datafolder, prefix, datafolder)):
        logger.info("{}/animation.mp4 exists already".format(datafolder))


def plot_phase_vs_time(datapack, output_folder, solsets='sol000',
                       ant_sel=None, time_sel=None, dir_sel=None, freq_sel=None, pol_sel=None):
    if isinstance(datapack, DataPack):
        datapack = datapack.filename

    if not isinstance(solsets, (list, tuple)):
        solsets = [solsets]

    output_folder = os.path.abspath(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    with DataPack(datapack, readonly=True) as datapack:
        phases = []
        stds = []
        for solset in solsets:
            datapack.current_solset = solset
            datapack.select(ant=ant_sel, time=time_sel, dir=dir_sel, freq=freq_sel, pol=pol_sel)
            weights, axes = datapack.weights_phase
            freq_ind = len(axes['freq']) >> 1
            freq = axes['freq'][freq_ind]
            ant = axes['ant'][0]
            phase, _ = datapack.phase
            std = np.sqrt(np.abs(weights))
            timestamps, times = datapack.get_times(axes['time'])
            phases.append(phase)
            stds.append(std)
        for phase in phases:
            for s, S in zip(phase.shape, phases[0].shape):
                assert s == S
        Npol, Nd, Na, Nf, Nt = phases[0].shape
        fig, ax = plt.subplots()
        for p in range(Npol):
            for d in range(Nd):
                for a in range(Na):
                    for f in range(Nf):
                        ax.cla()
                        for i, solset in enumerate(solsets):
                            phase = phases[i]
                            std = stds[i]
                            label = "{} {} {:.1f}MHz {}:{}".format(solset, axes['pol'][p], axes['freq'][f] / 1e6,
                                                                   axes['ant'][a], axes['dir'][d])
                            # ax.fill_between(times.mjd, phase[p, d, a, f, :] - 2 * std[p, d, a, f, :],
                            #                 phase[p, d, a, f, :] + 2 * std[p, d, a, f, :], alpha=0.5,
                            #                 label=r'$\pm2\hat{\sigma}_\phi$')  # ,color='blue')
                            ax.scatter(times.mjd, phase[p, d, a, f, :], marker='+', alpha=0.3,
                                       label=label)

                        ax.set_xlabel('Time [mjd]')
                        ax.set_ylabel('Phase deviation [rad.]')
                        ax.legend()
                        filename = "{}_{}_{}_{}MHz.png".format(axes['ant'][a], axes['dir'][d], axes['pol'][p],
                                                               axes['freq'][f] / 1e6)

                        plt.savefig(os.path.join(output_folder, filename))
        plt.close('all')


def plot_phase_vs_time_per_datapack(datapacks, output_folder, solsets='sol000',
                                    ant_sel=None, time_sel=None, dir_sel=None, freq_sel=None, pol_sel=None):
    if not isinstance(solsets, (list, tuple)):
        solsets = [solsets]

    if not isinstance(datapacks, (list, tuple)):
        datapacks = [datapacks]

    output_folder = os.path.abspath(output_folder)
    os.makedirs(output_folder, exist_ok=True)
    phases = []
    stds = []
    for solset, datapack in zip(solsets, datapacks):
        with DataPack(datapack, readonly=True) as datapack:
            datapack.current_solset = solset
            datapack.select(ant=ant_sel, time=time_sel, dir=dir_sel, freq=freq_sel, pol=pol_sel)
            weights, axes = datapack.weights_phase
            freq_ind = len(axes['freq']) >> 1
            freq = axes['freq'][freq_ind]
            ant = axes['ant'][0]
            phase, _ = datapack.phase
            std = np.sqrt(np.abs(weights))
            timestamps, times = datapack.get_times(axes['time'])
            phases.append(phase)
            stds.append(std)
    for phase in phases:
        for s, S in zip(phase.shape, phases[0].shape):
            assert s == S
    Npol, Nd, Na, Nf, Nt = phases[0].shape
    fig, ax = plt.subplots()
    for p in range(Npol):
        for d in range(Nd):
            for a in range(Na):
                for f in range(Nf):
                    ax.cla()
                    for i, solset in enumerate(solsets):
                        phase = phases[i]
                        std = stds[i]
                        label = "{} {} {} {:.1f}MHz {}:{}".format(os.path.basename(datapacks[i]), solset,
                                                                  axes['pol'][p], axes['freq'][f] / 1e6,
                                                                  axes['ant'][a], axes['dir'][d])
                        # ax.fill_between(times.mjd, phase[p, d, a, f, :] - 2 * std[p, d, a, f, :],
                        #                 phase[p, d, a, f, :] + 2 * std[p, d, a, f, :], alpha=0.5,
                        #                 label=r'$\pm2\hat{\sigma}_\phi$')  # ,color='blue')
                        ax.scatter(times.mjd, phase[p, d, a, f, :], marker='+', alpha=0.3,
                                   label=label)

                    ax.set_xlabel('Time [mjd]')
                    ax.set_ylabel('Phase deviation [rad.]')
                    ax.legend()
                    filename = "{}_{}_{}_{}MHz.png".format(axes['ant'][a], axes['dir'][d], axes['pol'][p],
                                                           axes['freq'][f] / 1e6)

                    plt.savefig(os.path.join(output_folder, filename))
        plt.close('all')


def plot_data_vs_solution(datapack, output_folder, data_solset='sol000', solution_solset='posterior_sol',
                          show_prior_uncert=False,
                          ant_sel=None, time_sel=None, dir_sel=None, freq_sel=None, pol_sel=None):
    def _wrap(phi):
        return np.angle(np.exp(1j * phi))

    if isinstance(datapack, DataPack):
        datapack = datapack.filename

    output_folder = os.path.abspath(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    solsets = [data_solset, solution_solset]
    with DataPack(datapack, readonly=True) as datapack:
        phases = []
        stds = []
        datapack.switch_solset(data_solset)
        datapack.select(ant=ant_sel, time=time_sel, dir=dir_sel, freq=freq_sel, pol=pol_sel)
        weights, axes = datapack.weights_phase
        _, freqs = datapack.get_freqs(axes['freq'])
        phase, _ = datapack.phase
        std = np.sqrt(np.abs(1. / weights))
        timestamps, times = datapack.get_times(axes['time'])
        phases.append(_wrap(phase))
        stds.append(std)

        tec_conversion = -8.4480e9 / freqs[None, None, None, :, None]

        datapack.switch_solset(solution_solset)
        datapack.select(ant=ant_sel, time=time_sel, dir=dir_sel, freq=freq_sel, pol=pol_sel)
        weights, _ = datapack.weights_tec
        tec, _ = datapack.tec
        std = np.sqrt(np.abs(1. / weights))[:, :, :, None, :] * np.abs(tec_conversion)
        phases.append(_wrap(tec[:, :, :, None, :] * tec_conversion))
        stds.append(std)

        for phase in phases:
            for s, S in zip(phase.shape, phases[0].shape):
                assert s == S
        Npol, Nd, Na, Nf, Nt = phases[0].shape
        fig, ax = plt.subplots()
        for p in range(Npol):
            for d in range(Nd):
                for a in range(Na):
                    for f in range(Nf):
                        ax.cla()
                        ###
                        # Data
                        phase = phases[0]
                        std = stds[0]
                        label = "{} {} {:.1f}MHz {}:{}".format(data_solset, axes['pol'][p], axes['freq'][f] / 1e6,
                                                               axes['ant'][a], axes['dir'][d])
                        if show_prior_uncert:
                            ax.fill_between(times.mjd, phase[p, d, a, f, :] - std[p, d, a, f, :],
                                            phase[p, d, a, f, :] + std[p, d, a, f, :], alpha=0.5,
                                            label=r'$\pm2\hat{\sigma}_\phi$')  # ,color='blue')
                        ax.scatter(times.mjd, phase[p, d, a, f, :], marker='+', alpha=0.3, color='black', label=label)

                        ###
                        # Solution
                        phase = phases[1]
                        std = stds[1]
                        label = "Solution: {}".format(solution_solset)
                        ax.fill_between(times.mjd, phase[p, d, a, f, :] - std[p, d, a, f, :],
                                        phase[p, d, a, f, :] + std[p, d, a, f, :], alpha=0.5,
                                        label=r'$\pm\hat{\sigma}_\phi$')  # ,color='blue')
                        ax.scatter(times.mjd, phase[p, d, a, f, :], label=label, marker='.', s=5.)

                        ax.set_xlabel('Time [mjd]')
                        ax.set_ylabel('Phase deviation [rad.]')
                        ax.legend()
                        filename = "{}_v_{}_{}_{}_{}_{}MHz.png".format(data_solset, solution_solset, axes['ant'][a],
                                                                       axes['dir'][d], axes['pol'][p],
                                                                       axes['freq'][f] / 1e6)
                        ax.set_ylim(-np.pi, np.pi)
                        plt.savefig(os.path.join(output_folder, filename))
        plt.close('all')


def plot_freq_vs_time(datapack, output_folder, solset='sol000', soltab='phase', phase_wrap=True, log_scale=False,
                      ant_sel=None, time_sel=None, dir_sel=None, freq_sel=None, pol_sel=None, vmin=None, vmax=None):
    if isinstance(datapack, DataPack):
        datapack = datapack.filename

    with DataPack(datapack, readonly=True) as datapack:
        datapack.switch_solset(solset)
        datapack.select(ant=ant_sel, time=time_sel, dir=dir_sel, freq=freq_sel, pol=pol_sel)
        obs, axes = datapack.__getattr__(soltab)
        if soltab.startswith('weights_'):
            obs = np.sqrt(np.abs(1. / obs))  # uncert from weights = 1/var
            phase_wrap = False
        if 'pol' in axes.keys():
            # plot only first pol selected
            obs = obs[0, ...]

        # obs is dir, ant, freq, time
        antenna_labels, antennas = datapack.get_antennas(axes['ant'])
        patch_names, directions = datapack.get_sources(axes['dir'])
        timestamps, times = datapack.get_times(axes['time'])
        freq_labels, freqs = datapack.get_freqs(axes['freq'])

        if phase_wrap:
            obs = np.angle(np.exp(1j * obs))
            vmin = -np.pi
            vmax = np.pi
            cmap = phase_cmap
        else:
            vmin = vmin if vmin is not None else np.percentile(obs.flatten(), 1)
            vmax = vmax if vmax is not None else np.percentile(obs.flatten(), 99)
            cmap = plt.cm.bone
        if log_scale:
            obs = np.log10(obs)

        Na = len(antennas)
        Nt = len(times)
        Nd = len(directions)
        Nf = len(freqs)

        M = int(np.ceil(np.sqrt(Na)))

        output_folder = os.path.abspath(output_folder)
        os.makedirs(output_folder, exist_ok=True)
        for k in range(Nd):
            filename = os.path.join(os.path.abspath(output_folder), "{}_{}_dir_{}.png".format(solset, soltab, k))
            logger.info("Plotting {}".format(filename))
            fig, axs = plt.subplots(nrows=M, ncols=M, figsize=(4 * M, 4 * M), sharex=True, sharey=True)
            for i in range(M):

                for j in range(M):
                    l = j + M * i
                    if l >= Na:
                        continue
                    im = axs[i][j].imshow(obs[k, l, :, :], origin='lower', cmap=cmap, aspect='auto', vmin=vmin,
                                          vmax=vmax,
                                          extent=(times[0].mjd * 86400., times[-1].mjd * 86400., freqs[0], freqs[1]))
            plt.tight_layout()
            fig.subplots_adjust(right=0.8)
            cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
            fig.colorbar(im, cax=cbar_ax)
            plt.savefig(filename)
        plt.close('all')


def plot_solution_residuals(datapack, output_folder, data_solset='sol000', solution_solset='posterior_sol',
                            ant_sel=None, time_sel=None, dir_sel=None, freq_sel=None, pol_sel=None):
    def _wrap(phi):
        return np.angle(np.exp(1j * phi))

    if not isinstance(datapack, str):
        datapack = datapack.filename

    output_folder = os.path.abspath(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    solsets = [data_solset, solution_solset]
    with DataPack(datapack, readonly=True) as datapack:
        datapack.switch_solset(data_solset)
        datapack.select(ant=ant_sel, time=time_sel, dir=dir_sel, freq=freq_sel, pol=pol_sel)

        phase, axes = datapack.phase
        timestamps, times = datapack.get_times(axes['time'])
        antenna_labels, antennas = datapack.get_antennas(axes['ant'])
        patch_names, directions = datapack.get_sources(axes['dir'])
        _, freqs = datapack.get_freqs(axes['freq'])
        pols, _ = datapack.get_pols(axes['pol'])
        Npol, Nd, Na, Nf, Nt = phase.shape

        datapack.switch_solset(solution_solset)
        datapack.select(ant=ant_sel, time=time_sel, dir=dir_sel, freq=freq_sel, pol=pol_sel)
        tec, _ = datapack.tec
        phase_pred = -8.448e9 * tec[..., None, :] / freqs[:, None]

        res = _wrap(_wrap(phase) - _wrap(phase_pred))
        cbar = None

        for p in range(Npol):
            for a in range(Na):

                M = int(np.ceil(np.sqrt(Nd)))
                fig, axs = plt.subplots(nrows=2 * M, ncols=M, sharex=True, figsize=(M * 4, 1 * M * 4),
                                        gridspec_kw={'height_ratios': [1.5, 1] * M})
                fig.subplots_adjust(wspace=0., hspace=0.)
                fig.subplots_adjust(right=0.85)
                cbar_ax = fig.add_axes([0.875, 0.15, 0.025, 0.7])

                vmin = -1.
                vmax = 1.
                norm = plt.Normalize(vmin, vmax)

                for row in range(0, 2 * M, 2):
                    for col in range(M):
                        ax1 = axs[row][col]
                        ax2 = axs[row + 1][col]

                        d = col + row // 2 * M
                        if d >= Nd:
                            continue

                        img = ax1.imshow(res[p, d, a, :, :], origin='lower', aspect='auto',
                                         extent=(times[0].mjd * 86400., times[-1].mjd * 86400., freqs[0], freqs[-1]),
                                         cmap=plt.cm.jet, norm=norm)
                        ax1.text(0.05, 0.95, axes['dir'][d], horizontalalignment='left', verticalalignment='top',
                                 transform=ax1.transAxes, backgroundcolor=(1., 1., 1., 0.5))

                        ax1.set_ylabel('frequency [Hz]')
                        ax1.legend()

                        mean = res[p, d, a, :, :].mean(0)
                        t = np.arange(len(times))
                        ax2.plot(times.mjd * 86400, mean, label=r'$\mathbb{E}_\nu[\delta\phi]$')
                        std = res[p, d, a, :, :].std(0)
                        ax2.fill_between(times.mjd * 86400, mean - std, mean + std, alpha=0.5,
                                         label=r'$\pm\sigma_{\delta\phi}$')
                        ax2.set_xlabel('Time [mjs]')
                        ax2.set_xlim(times[0].mjd * 86400., times[-1].mjd * 86400.)
                        ax2.set_ylim(-np.pi, np.pi)
                #                         ax2.legend()

                fig.colorbar(img, cax=cbar_ax, orientation='vertical', label='phase dev. [rad]')
                filename = "{}_v_{}_{}_{}.png".format(data_solset, solution_solset, axes['ant'][a], axes['pol'][p])
                plt.savefig(os.path.join(output_folder, filename))
                plt.close('all')


def test_vornoi():
    from scipy.spatial import Voronoi
    import pylab as plt
    from matplotlib.patches import Polygon
    from matplotlib.collections import PatchCollection
    import numpy as np

    points = np.random.uniform(size=[10, 2])
    v = Voronoi(points)
    nodes = v.vertices
    regions = v.regions

    ax = plt.subplot()
    patches = []
    for reg in regions:
        if len(reg) < 3:
            continue
        poly = Polygon(np.array([nodes[i] for i in reg]), closed=False)
        patches.append(poly)
    p = PatchCollection(patches)
    p.set_array(np.random.uniform(size=len(patches)))
    ax.add_collection(p)
    # plt.colorbar(p)
    ax.scatter(points[:, 0], points[:, 1])
    ax.set_xlim([np.min(points[:, 0]), np.max(points[:, 0])])
    ax.set_ylim([np.min(points[:, 1]), np.max(points[:, 1])])
    plt.show()


def test_nearest():
    from scipy.spatial import ConvexHull, cKDTree
    import pylab as plt
    from matplotlib.patches import Polygon
    from matplotlib.collections import PatchCollection
    import numpy as np

    points = np.random.uniform(size=[42, 2])
    k = cKDTree(points)
    dx = np.max(points[:, 0]) - np.min(points[:, 0])
    dy = np.max(points[:, 1]) - np.min(points[:, 1])
    N = int(min(max(100, points.shape[0] * 2), 500))
    x = np.linspace(np.min(points[:, 0]) - 0.1 * dx, np.max(points[:, 0]) + 0.1 * dx, N)
    y = np.linspace(np.min(points[:, 1]) - 0.1 * dy, np.max(points[:, 1]) + 0.1 * dy, N)
    X, Y = np.meshgrid(x, y, indexing='ij')
    points_i = np.array([X.flatten(), Y.flatten()]).T
    dist, i = k.query(points_i, k=1)
    patches = []
    for group in range(points.shape[0]):
        points_g = points_i[i == group, :]
        hull = ConvexHull(points_g)
        nodes = points_g[hull.vertices, :]
        poly = Polygon(nodes, closed=False)
        patches.append(poly)
    ax = plt.subplot()
    p = PatchCollection(patches)
    p.set_array(np.random.uniform(size=len(patches)))
    ax.add_collection(p)
    # plt.colorbar(p)
    ax.scatter(points[:, 0], points[:, 1])
    ax.set_xlim([np.min(points_i[:, 0]), np.max(points_i[:, 0])])
    ax.set_ylim([np.min(points_i[:, 1]), np.max(points_i[:, 1])])
    ax.set_facecolor('black')
    plt.show()
