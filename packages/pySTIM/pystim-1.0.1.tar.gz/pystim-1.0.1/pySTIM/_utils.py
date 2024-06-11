import random
from tqdm import tqdm
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from typing import Any, List, Tuple, Union, Dict, Optional
from scipy.sparse import csc_matrix
from shapely.geometry import Polygon

def normalize_data(adata, scale_factor=100):
    
    data_matrix = adata.X.toarray()
    
    total_counts = np.sum(data_matrix, axis=1).reshape(-1, 1)
    norm_mtx = (data_matrix / total_counts) * scale_factor
    log_mtx = np.log1p(norm_mtx)

    adata.X = csc_matrix(log_mtx.astype(np.float32))
    
    return adata
    
def to_hex(rgb_tuple: Tuple[float, float, float]) -> str:
    """
    Convert an RGB tuple to its hex color.
    
    Parameters:
    - rgb_tuple (Tuple[float, float, float]): A tuple representing RGB values (range 0 to 1).
    
    Returns:
    - str: Hexadecimal string representing the color.
    """
    r = int(rgb_tuple[0] * 255)
    g = int(rgb_tuple[1] * 255)
    b = int(rgb_tuple[2] * 255)
    hex_code = '#{0:02x}{1:02x}{2:02x}'.format(r, g, b)
    return hex_code


def crop(adata: Any, 
         xlims: Optional[Tuple[float, float]], 
         ylims: Optional[Tuple[float, float]]) -> Tuple[List[int], pd.DataFrame]:
    """
    Crop adata based on x and y limits.

    Parameters:
    - adata: An anndata object.
    - xlims: Tuple containing the x-axis limits.
    - ylims: Tuple containing the y-axis limits.

    Returns:
    - Tuple[List[int], pd.DataFrame]: A tuple containing the subset indices and the subsetted cell coordinates DataFrame.
    """
    
    cell_coord = adata.obs
    x_new = cell_coord.x_centroid.to_list()
    y_new = cell_coord.y_centroid.to_list()

    expand = 1.05
    if xlims is None:
        minx = cell_coord.x_centroid.min()
        maxx = cell_coord.x_centroid.max()
        xlims = [(minx + maxx) / 2.0 - (maxx - minx) / 2.0 * expand,
                 (minx + maxx) / 2.0 + (maxx - minx) / 2.0 * expand]

    if ylims is None:
        miny = cell_coord.y_centroid.min()
        maxy = cell_coord.y_centroid.max()
        ylims = [(miny + maxy) / 2.0 - (maxy - miny) / 2.0 * expand,
                 (miny + maxy) / 2.0 + (maxy - miny) / 2.0 * expand]

    x_lim_idx = [idx for idx, value in enumerate(x_new) if value > xlims[0] and value < xlims[1]]
    y_lim_idx = [idx for idx, value in enumerate(y_new) if value > ylims[0] and value < ylims[1]]

    subset_idx = list(set(x_lim_idx) & set(y_lim_idx))
    cell_coord2 = cell_coord.iloc[subset_idx]

    return subset_idx, cell_coord2


def get_color_map(adata: Any, 
                  color_by: Optional[str], 
                  cmap: Optional[Union[str, Dict[str, str]]], 
                  seed: int, 
                  genes: Optional[Union[str, List[str]]],
                  subset_idx: List[int]) -> Union[str, Dict[str, str]]:
    """
    Get a color map for the given adata.

    Parameters:
    - adata: An anndata object.
    - color_by (Optional[str]): Category from adata.obs by which to color the output.
    - cmap (Optional[Union[str, Dict[str, str]]]): Color map or a dictionary to map values to colors.
    - seed (int): Seed for random color generation.
    - genes (bool): Whether the map is based on genes or not.
    - subset_idx (List[int]): Indices of the subset of data to be considered.

    Returns:
    - Union[str, Dict[str, str]]: A color map or a dictionary mapping values to colors.
    """
    
    def generate_random_color():
        return "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

    def generate_cell_type_map():
        cell_type = list(adata.obs[color_by].cat.categories)
        key = f'{color_by}_colors'
        if key in adata.uns.keys():
            cell_colors = adata.uns[key]
        else:
            random.seed(seed)
            cell_colors = [generate_random_color() for _ in range(len(cell_type))]
        return dict(zip(cell_type, cell_colors))

    if not genes:
        if color_by is None:
            map_dict = ['#6699cc'] * len(subset_idx)
        elif cmap is None:
            map_dict = generate_cell_type_map()
        else:
            map_dict = cmap
    else:
        if cmap is None:
            colors = ['#f2f2f2', '#ffdbdb', '#fc0303']
            map_dict = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
        else:
            map_dict = cmap

    return map_dict


def split_field(df: pd.DataFrame, 
                n_fields_x: int, 
                n_fields_y: int, 
                x_col: str = 'x_centroid', 
                y_col: str = 'y_centroid') -> Tuple[List[List[Tuple[float, float]]], List[Tuple[float, float]]]:
    """
    Splits a spatial region into a grid of FOV based on x and y centroids in obs.
    
    Parameters:
    - df: AnnData.obs containing the x and y centroids.
    - n_fields_x: Number of FOV horizontally.
    - n_fields_y: Number of FOV vertically.
    - x_col: Column name for x centroids in df. Default is 'x_centroid'.
    - y_col: Column name for y centroids in df. Default is 'y_centroid'.
    
    Returns:
    - rectangles: each rectangle is represented by a list of its vertices.
    - centroids: centroids of these rectangles.
    """
    
    # Expand the bounding box slightly for better visualization
    expand = 1.1
    minx = df[x_col].min()
    maxx = df[x_col].max()
    x_range = expand * (maxx - minx)
    
    miny = df[y_col].min()
    maxy = df[y_col].max()
    y_range = expand * (maxy - miny)
    
    # Calculate the dimensions of each rectangle
    x_step = x_range / n_fields_x
    y_step = y_range / n_fields_y
    
    # Calculate the starting coordinates for the grid
    x_start = (minx + maxx) / 2.0 - (maxx - minx) / 2.0 * expand
    y_start = (miny + maxy) / 2.0 - (maxy - miny) / 2.0 * expand
    
    # Loop to create the grid of rectangles and calculate their centroids
    rectangles = []
    centroids = []
    for i in range(n_fields_x):
        for j in range(n_fields_y):
            top_left = (x_start + x_step * i, y_start + y_step * j)
            bottom_right = (top_left[0] + x_step, top_left[1] + y_step)
            centroid = (top_left[0] + x_step / 2, top_left[1] + y_step / 2)
    
            rectangle = [top_left, (bottom_right[0], top_left[1]), bottom_right, (top_left[0], bottom_right[1])]
            rectangles.append(rectangle)
            centroids.append(centroid)
    
    return rectangles, centroids

def filter_polygon(adata, poly_key = "poly", threshold = 10, view_summary = True):
    '''
    Filters polygons based on a size threshold
    
    Parameters:
    - adata: AnnData object.
    - threshold: Minimum area threshold for polygons to be kept.
    - view_summary: If True, displays a histogram of polygon areas.
    - inplace: If True, modifies `adata` in place, otherwise returns modified data.
    '''

    poly_dict = adata.uns.get(poly_key, {})
    polygon_areas = np.array([Polygon(poly['coordinates'][0]).area for poly in poly_dict.values()])
    
    if view_summary:
        print("Polygon area distribution")
        plt.figure(figsize=(5, 3))
        plt.hist(polygon_areas, bins=100, align='left', color='skyblue')
        plt.xlim(-10, 250)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.tight_layout()
        plt.show()
        
    print(f"Original polygon number: {len(adata.uns['poly'])}")
    filtered_poly_dict = {pid: pd for pid, pd in poly_dict.items() if Polygon(pd['coordinates'][0]).area >= threshold}
    print(f"Keep polygon number: {len(filtered_poly_dict)}")
    
    print("Saving result...")
    keep_poly_number = [int(i) for i in filtered_poly_dict.keys()]
    adata.uns["seg"] = adata.uns["seg"][adata.uns["seg"].polygon_number.isin(keep_poly_number)]
    adata.uns[poly_key] = filtered_poly_dict
    adata = adata[adata.obs.polygon_number.isin(keep_poly_number)]
    return adata

def smooth_polygon(adata, window_size=5):
    """
    Smoothens the coordinates of polygons using a moving average filter.

    Parameters:
    - adata: AnnData object containing the dataset.
    - window_size: The size of the moving window for smoothing.
    """
    def smooth_coordinates(polygon, window_size):
        n = len(polygon)
        polygon = np.array(polygon)
        smoothed = polygon.copy()
        for i in range(n):
            indices = [(i + j - window_size // 2) % n for j in range(window_size)]
            smoothed[i] = np.mean(polygon[indices], axis=0)
        return smoothed.tolist()

    seg = adata.uns["seg"]
    all_polygons = sorted(set(seg["polygon_number"]))

    new_polygons = []
    for polygon_number in tqdm(all_polygons, desc="Smoothing polygons"):
        group = seg[seg.polygon_number == polygon_number]
        raw_coords = group.iloc[:, 3:5].values.tolist()
        smoothed_coords = smooth_coordinates(raw_coords, window_size = window_size)
        new_polygons.append({
            'coordinates': [smoothed_coords],
            'type': 'Polygon'
        })

    adata.uns['poly'] = dict(zip(map(str, all_polygons), new_polygons))
    

    












    
    