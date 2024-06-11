import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import math
from mpl_toolkits.axes_grid1 import make_axes_locatable
import random
from descartes import PolygonPatch
import scanpy as sc
from ._utils import to_hex, crop, get_color_map, split_field
from typing import Any, List, Optional, Union, Dict, Tuple

def plot_polygon(adata: Any, 
                 plot_type: str = "cell", 
                 xlims: Optional[Tuple[float, float]] = None, 
                 ylims: Optional[Tuple[float, float]] = None, 
                 color_by: Optional[str] = None, 
                 genes: Optional[Union[str, List[str]]] = None, 
                 seed: int = 123, 
                 alpha: float = 0.8,
                 cmap: Optional[Union[str, Dict[str, str]]] = None, 
                 ptsize: float = 0.01, 
                 ticks: bool = False, 
                 dpi: int = 300,
                 width: int = 5, 
                 height: int = 5, 
                 edgecolor: str = "#808080", 
                 linewidth: float = 0.2,
                 legend_col = 1) -> None:
    """
    Plot polygons based on the provided adata.

    Parameters:
    - adata: A anndata object.
    - plot_type: The type of plot ('cell', 'gene', or 'transcript').
    - xlims: Tuple containing the x-axis limits.
    - ylims: Tuple containing the y-axis limits.
    - color_by: Category from adata.obs by which to color the output.
    - genes: Genes to be considered for 'gene' or 'transcript' plots.
    - seed: Seed for random color generation.
    - alpha: Opacity of polygons.
    - cmap: Color map or a dictionary to map values to colors.
    - ptsize: Size of points in the scatter plot.
    - ticks: Whether to display axis ticks.
    - dpi: Resolution.
    - width: Width of the figure.
    - height: Height of the figure.
    - edgecolor: Color of the polygon edge.
    - linewidth: Width of the polygon edge line.

    Returns:
    None: Displays the desired plot based on the given parameters.
    """
    
    try:
        adata.uns['poly']
    except AttributeError:
        print('Please create polygons first! To create polygons, please use the create_polygons function.')
    else:
        poly_dict = {idx + 1: adata.uns['poly'][key] for idx, key in enumerate(adata.uns['poly'].keys())}
        new_lib = [*poly_dict.values()]

        subset_idx, new_coord = crop(adata, xlims, ylims)

        print("Total number of polygons: ", len(new_coord))

        if plot_type == "cell":
            if color_by is None:
                cols = ['#6699cc'] * len(subset_idx)
            else:
                map_dict = get_color_map(adata, color_by, cmap, seed, genes, subset_idx)
                cols = list(new_coord[color_by].map(map_dict))

            fig, ax = plt.subplots(dpi=dpi, figsize=(width, height))
            if not ticks:
                plt.tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)
            [ax.add_patch(PolygonPatch(new_lib[i], fc=cols[j], ec=edgecolor, alpha=alpha, zorder=0.5, linewidth=linewidth)) for j, i in
             enumerate(subset_idx)]
            ax.axis('scaled')
            ax.grid(False)
            ax.invert_yaxis()
            
            scalebar = AnchoredSizeBar(ax.transData,
                       25, ' ', 'lower right', 
                       pad=0.5,
                       sep=5,
                       color='black',
                       frameon=False,
                       size_vertical=2,
                       fontproperties=fm.FontProperties(size=12))


            ax.add_artist(scalebar)
                
            if color_by is not None:
                markers = [plt.Line2D([0, 0], [0, 0], color=color, marker='o', linestyle='') for color in
                           map_dict.values()]
                ax.legend(markers, map_dict.keys(),
                          numpoints=1, loc='center left', bbox_to_anchor=(1, 0.5),
                          frameon=False, ncol=legend_col)
            plt.show()

        elif plot_type == "gene":
            if isinstance(genes, str):
                genes = [genes]

            def create_gene_plot(ax, gene, counts, cmap, subset_idx, alpha, edgecolor, ticks):
                # c_max = np.quantile(counts, 0.99)
                c_max = max(counts)
                bar_colors = [cmap(c / c_max) for c in counts]
                bar_colors = np.clip(bar_colors, 0, 1)
                all_colors = [to_hex(i) for i in bar_colors]
                cols = [all_colors[i] for i in subset_idx]
                if not ticks:
                    ax.tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)

                ax.set_title(gene)
                [ax.add_patch(
                    PolygonPatch(new_lib[i], fc=cols[j], ec=edgecolor, alpha=alpha, zorder=0.1, linewidth=linewidth)) for j, i
                    in enumerate(subset_idx)]
                ax.axis('scaled')
                ax.grid(False)
                ax.invert_yaxis()
                
                scalebar = AnchoredSizeBar(ax.transData,
                       25, ' ', 'lower right', 
                       pad=0.5,
                       sep=5,
                       color='black',
                       frameon=False,
                       size_vertical=2,
                       fontproperties=fm.FontProperties(size=12))


                ax.add_artist(scalebar)
                norm = matplotlib.colors.Normalize(vmin=min(counts), vmax=c_max)

                return norm

            n_rows = math.ceil(len(genes) / 3)
            if len(genes) < 4:
                n_cols = len(genes)
            else:
                n_cols = 3

            fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(n_cols * width, n_rows * height), dpi=dpi)
            # plt.subplots_adjust(hspace=0.5)

            if len(genes) == 1:
                counts = sc.get.obs_df(adata, keys=genes[0]).to_list()
                norm = create_gene_plot(axs, genes[0], counts, cmap, subset_idx, alpha, edgecolor, ticks)
                divider = make_axes_locatable(axs)
                cax = divider.append_axes("right", size="5%", pad=0.05)
                fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), ax = axs, cax=cax)
            else:
                axs = axs.flatten()
                for gene, ax in zip(genes, axs):
                    counts = sc.get.obs_df(adata, keys=gene).to_list()
                    norm = create_gene_plot(ax, gene, counts, cmap, subset_idx, alpha, edgecolor, ticks)
                    divider = make_axes_locatable(ax)
                    cax = divider.append_axes("right", size="5%", pad=0.05)
                    plt.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, cax=cax)

            if len(genes) < n_rows * n_cols:
                for idx in range(len(genes), n_rows * n_cols):
                    fig.delaxes(axs[idx])

            plt.tight_layout()
            plt.show()

        elif plot_type == "transcript":

            mol_data = adata.uns['transcript']
            cell_id_keep = new_coord.cell_id.tolist()
            mol_data2 = mol_data[mol_data.cell_id.isin(cell_id_keep) & mol_data.feature_name.isin(genes)]
            if cmap is None:
                random.seed(seed)
                tx_col = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                          for i in range(len(genes))]
                map_dict = {genes[i]: tx_col[i] for i in range(len(genes))}
            else:
                map_dict = cmap

            all_tx = mol_data2['feature_name'].to_list()
            all_tx = pd.DataFrame(all_tx, columns=['colors'])
            all_tx = all_tx.replace({'colors': map_dict})

            fig, ax = plt.subplots(dpi=dpi, figsize=(width, height))
            if not ticks:
                plt.tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)
            [ax.add_patch(PolygonPatch(new_lib[i], fc='#fcfcfa', ec=edgecolor, alpha=alpha, zorder=0.5, linewidth=linewidth)) for j, i in
             enumerate(subset_idx)]
            scalebar = AnchoredSizeBar(ax.transData,
                       25, ' ', 'lower right', 
                       pad=0.5,
                       sep=5,
                       color='black',
                       frameon=False,
                       size_vertical=2,
                       fontproperties=fm.FontProperties(size=12))


            ax.add_artist(scalebar)
            
            ax.scatter(mol_data2.x_location, mol_data2.y_location, c=all_tx.colors, s=ptsize)
            ax.axis('scaled')
            ax.grid(False)
            ax.invert_yaxis()
            markers = [plt.Line2D([0, 0], [0, 0], color=color, marker='o', linestyle='') for color in map_dict.values()]
            ax.legend(markers, map_dict.keys(),
                      numpoints=1, loc='center left', bbox_to_anchor=(1, 0.5),
                      frameon=False, ncol=legend_col)
            plt.show()
            

def plot_scatter(adata: sc.AnnData, 
                 xlims: Optional[tuple] = None, 
                 ylims: Optional[tuple] = None, 
                 color_by: Optional[str] = None, 
                 genes: Optional[Union[str, List[str]]] = None, 
                 seed: int = 123, 
                 alpha: float = 0.8, 
                 cmap: Optional[str] = None, 
                 ptsize: float = 0.1, 
                 ticks: bool = False, 
                 dpi: int = 300, 
                 width: int = 5, 
                 height: int = 5, 
                 legend_loc: str = "center left", 
                 legend_col: int = 2, 
                 bbox_to_anchor: tuple = (1.0, 0.5), 
                 save: Optional[str] = None) -> None:
    """
    Plot scatter plots based on AnnData object.

    Parameters:
    - adata: A anndata object.
    - xlims, ylims: The x and y limits for cropping.
    - color_by: The column to color by.
    - genes: Gene(s) to plot.
    - seed: Random seed.
    - alpha: Transparency level.
    - cmap: Colormap.
    - ptsize: Point size.
    - ticks: Whether to show ticks.
    - dpi: Dots per inch.
    - width, height: Width and height of plot.
    - legend_loc: Legend location.
    - legend_col: Number of columns in the legend.
    - bbox_to_anchor: Legend bbox_to_anchor.
    - save: Filename to save the plot to.

    Returns:
    None
    """
    
    def plot(ax: plt.Axes, 
             group: str, 
             new_coord: pd.DataFrame, 
             alpha: float = 0.8, 
             ptsize: float = 0.01, 
             ticks: bool = False) -> None:
        """
        Helper function to create the scatter plot.
        """
        if not ticks:
            plt.tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)
            ax.axis("off")

        ax.scatter(np.array(new_coord.x_centroid), np.array(new_coord.y_centroid), marker='o', linewidth=0,
                   alpha=alpha, color=np.array(new_coord['color']), s=ptsize)

        ax.set_title(group)
        ax.axis('scaled')
        ax.grid(False)
        ax.invert_yaxis()

    group = list(adata.obs.ident.cat.categories)

    n_rows = math.ceil(len(group) / 6)
    if len(group) < 6:
        n_cols = len(group)
    else:
        n_cols = 6

    fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(n_cols * width, n_rows * height), dpi=dpi,
                            layout='constrained')

    if not genes:
        if len(group) == 1:
            subset_idx, new_coord = crop(adata, xlims, ylims)
            map_dict = get_color_map(adata, color_by, cmap, seed, genes, subset_idx)
            new_coord['color'] = new_coord[color_by].map(map_dict)
            plot(axs, group[0], new_coord, alpha, ptsize, ticks)
        else:
            axs = axs.flatten()
            for g, ax in zip(group, axs):
                tmp = adata[adata.obs.ident == g]
                subset_idx, new_coord = crop(tmp, xlims, ylims)
                map_dict = get_color_map(adata, color_by, cmap, seed, genes, subset_idx)
                new_coord['color'] = new_coord[color_by].map(map_dict)
                plot(ax, g, new_coord, alpha, ptsize, ticks)
        
            for ax in axs[len(group):]:
                ax.axis("off")
                ax.set_visible(False)
            
        markers = [plt.Line2D([0, 0], [0, 0], color=color, marker='o', linestyle='') for color in map_dict.values()]
        fig.legend(markers, map_dict.keys(), numpoints=1, loc=legend_loc, bbox_to_anchor=bbox_to_anchor, frameon=False,
                   ncol=legend_col)
        if save:
            plt.savefig(save, transparent=True, bbox_inches='tight')
            
        plt.show()

    else:
        if isinstance(genes, str):
            genes = [genes]

        if len(group) == 1:
            counts = sc.get.obs_df(adata, keys=genes[0]).to_list()
            subset_idx, new_coord = crop(adata, xlims, ylims)

            cmap = get_color_map(adata, color_by, cmap, seed, genes, subset_idx)

            # c_max = max(counts)
            c_max = np.quantile(counts, 0.99)
            c_min = min(counts)
            bar_colors = [cmap(c / c_max) for c in counts]
            bar_colors = np.clip(bar_colors, 0, 1)
            all_colors = [to_hex(i) for i in bar_colors]

            new_coord['color'] = [all_colors[i] for i in subset_idx]
            plot(axs, group[0], new_coord, alpha, ptsize, ticks)
            norm = matplotlib.colors.Normalize(vmin=c_min, vmax=c_max)
            cbar_ax = fig.add_axes([0.96, 0.2, 0.02, 0.6])
            fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbar_ax)
        else:
            c_max_list = []
            c_min_list = []
            
            axs = axs.flatten()
            for g, ax in zip(group, axs):
                tmp = adata[adata.obs.ident == g]
                counts = sc.get.obs_df(tmp, keys=genes[0]).to_list()
                c_max_list.append(np.quantile(counts, 0.99))
                c_min_list.append(min(counts))

            c_max = max(c_max_list)
            c_min = min(c_min_list)

            for g, ax in zip(group, axs.flatten()):
                tmp = adata[adata.obs.ident == g]
                counts = sc.get.obs_df(tmp, keys=genes[0]).to_list()
                subset_idx, new_coord = crop(tmp, xlims, ylims)

                cmap = get_color_map(adata, color_by, cmap, seed, genes, subset_idx)

                bar_colors = [cmap(c / c_max) for c in counts]
                bar_colors = np.clip(bar_colors, 0, 1)
                all_colors = [to_hex(i) for i in bar_colors]

                new_coord['color'] = [all_colors[i] for i in subset_idx]
                plot(ax, g, new_coord, alpha, ptsize, ticks)
            
            for ax in axs[len(group):]:
                ax.axis("off")
                
            norm = matplotlib.colors.Normalize(vmin=c_min, vmax=c_max)
            cbar_ax = fig.add_axes([1.02, 0.2, 0.005, 0.6])
            cb = fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbar_ax, orientation='vertical')
            '''
            if n_rows == 1:
                fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), ax=axs[:], shrink=0.6, location="right")
            else:
                fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), ax=axs[:, :], shrink=0.6, location="right")
            '''
        if save:
            plt.savefig(save)
            
        plt.show()

        
def plot_fov(data: "AnnData", 
             n_fields_x: int, 
             n_fields_y: int, 
             x_col: str = "x_centroid", 
             y_col: str = "y_centroid",
             group_label: Optional[str] = None, 
             highlight_cell: Optional[str] = None, 
             highlight_color: str = '#FC4B42',
             fill: bool = True, 
             point_size: float = 0.8, 
             alpha: float = 0.3,
             font_size: Optional[float] = None, 
             resolution: int = 200, 
             plot_width: int = 5, 
             plot_height: int = 5) -> None:
    """
    Plot field of view (FoV) with optional cell highlighting and field partitioning.
    
    Parameters:
    - adata: An anndata object.
    - n_fields_x, n_fields_y: Number of fields in x and y dimensions to partition the plot.
    - x_col, y_col: Column names indicating x and y coordinates in the data.
    - group_label: Column name to use for grouping and highlighting cells.
    - highlight_cell: Cell group label to be highlighted.
    - highlight_color: Color for highlighted cells.
    - fill: Whether to fill the polygons representing fields.
    - point_size: Size of the plotted cell points.
    - alpha: Transparency level for the polygons and cell points.
    - font_size: Font size for the field numbers. Calculated based on n_fields_x and n_fields_y if not provided.
    - resolution: Resolution of the plot in dpi.
    - plot_width, plot_height: Figure size.
    
    Returns:
    None
    """
    
    coord = data.obs.copy()
    
    rectangles, centroids = split_field(coord, n_fields_x, n_fields_y, x_col=x_col, y_col=y_col)
    
    # Convert rectangles to DataFrame for easier manipulation
    rectangle_df = pd.concat([pd.DataFrame(rect, columns=['x', 'y']).assign(id=idx) for idx, rect in enumerate(rectangles)])
    
    # Create polygons for plotting
    polygons = [{'coordinates': [group[['x', 'y']].values.tolist()], 'type': 'Polygon'} for _, group in rectangle_df.groupby('id')]
    
    if fill:
        fill_color = "#D3D3D3"
    else:
        fill_color = 'None'
    
    if font_size is None:
        font_size = 120 / (n_fields_x + n_fields_y)
    
    fig, ax = plt.subplots(dpi=resolution, figsize=(plot_width, plot_height))
    plt.tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)
    
    if isinstance(group_label, str) and highlight_cell:
        coord['highlight'] = coord[group_label].apply(lambda x: highlight_color if x == highlight_cell else '#BFBFBF')
        [ax.plot(group_data[x_col], group_data[y_col], 'o', markersize=point_size, markerfacecolor=color, markeredgecolor='none', alpha=alpha) for color, group_data in coord.groupby('highlight')]
    else:
        ax.plot(coord[x_col].tolist(), coord[y_col].tolist(), 'o', markersize=point_size, markerfacecolor='#bfbfbf', markeredgecolor='none', alpha=alpha)
    
    for polygon in polygons:
        ax.add_patch(PolygonPatch(polygon, fc=fill_color, ec='black', alpha=alpha, linewidth=0.5))
    
    for idx, (x, y) in enumerate(centroids):
        ax.text(x, y, str(idx), fontsize=font_size, ha='center', va='center', weight='bold')
    
    ax.axis('scaled')
    ax.grid(False)
    ax.invert_yaxis()
    ax.set_frame_on(False)
    plt.show()
    
    
def subset_fov(adata: "AnnData", 
               fov: List[int], 
               n_fields_x: int, 
               n_fields_y: int, 
               x_col: str = 'x_centroid', 
               y_col: str = 'y_centroid') -> Tuple[float, float, float, float]:
    """
    Extract the coordinates that define the boundary of the specified field of view (FoV) from an AnnData object.

    Parameters:
    - adata: An anndata object.
    - fov: List of field of view indices to be considered.
    - n_fields_x, n_fields_y: Number of fields in x and y dimensions used to partition the plot.
    - x_col, y_col: Column names indicating x and y coordinates in the data.

    Returns:
    (xmin, xmax, ymin, ymax): Boundary coordinates in the format.
    """

    df = adata.obs.copy()
    rectangles, _ = split_field(df, n_fields_x, n_fields_y, x_col=x_col, y_col=y_col)
    
    selected_rectangles = [rectangles[i] for i in fov]
    min_pt = np.min(np.min(selected_rectangles, axis=0), axis=0)
    max_pt = np.max(np.max(selected_rectangles, axis=0), axis=0)
    
    return min_pt[0], max_pt[0], min_pt[1], max_pt[1]