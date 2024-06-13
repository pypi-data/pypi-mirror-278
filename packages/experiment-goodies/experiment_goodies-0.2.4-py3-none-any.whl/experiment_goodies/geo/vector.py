import math
import random

import geopandas
import numpy as np
import pandas as pd
import shapely
from geopandas import GeoDataFrame, GeoSeries
from pyproj import Transformer
from rasterio.features import rasterize
from shapely import Geometry, affinity


def load_geometries_from_paths(
    file_paths: list[str], target_crs: str | int = 4326
) -> GeoSeries:
    """Loads geometries from given paths into same CRS and returns them as a GeoSeries

    Args:
        file_paths (list[str]): paths to vector files containing geometries to load
        target_crs (str | int, optional): destination Coordinate Reference System (CRS). Defaults to 4326 (WGS).

    Returns:
        geopandas.GeoSeries: loaded geometries
    """
    valid_zones = []
    for path in file_paths:
        valid_zones.append(
            geopandas.read_file(path).make_valid().geometry.to_crs(target_crs)
        )
    valid_zones: geopandas.GeoSeries = pd.concat(valid_zones)
    return valid_zones


def geometries_to_mask(
    geometries: list[Geometry],
    affine_transform: list[int],
    out_shape: tuple[int],
    mask_value: int = 1,
) -> np.ndarray:
    """Transform georeferenced geometries into a mask with geometries filled in. Simple wrapper around
    rasterio.features.rasterize, see https://rasterio.readthedocs.io/en/stable/api/rasterio.features.html for
    more information.

    Args:
        geometries (list[Geometry]): list of geometries in geo-coordinates
        affine_transform (list[int]): transform from geo-coordinates into image coordinates
        out_shape (tuple[int]): shape of output mask
        mask_value (int, optional): value to burn into geometries. Defaults to 1.

    Returns:
        np.ndarray: generated mask
    """
    if len(geometries) == 0:
        return np.zeros(out_shape, dtype=np.uint8)
    rasterized_geoms = rasterize(
        shapes=geometries, out_shape=out_shape, transform=affine_transform
    )
    rasterized_geoms = (rasterized_geoms * mask_value).astype(np.uint8)
    return rasterized_geoms


def randomly_translate_geometries(
    geometries: GeoSeries,
    x_off_range: tuple[int],
    y_off_range: tuple[int],
    random_seed: int = None,
) -> GeoSeries:
    """Applies random translation to x and y coordinates for each geometry according to given translation ranges.

    Args:
        geoseries (GeoSeries): geometries to translate
        x_off_range (tuple[int]): translation range for X coordinate
        y_off_range (tuple[int]): translation range for Y coordinate
        random_seed (int, optional): set it to have reproducible results. Defaults to None.

    Returns:
        GeoSeries: translated geometries
    """
    if random_seed is not None:
        random.seed(random_seed)
    geometries = geometries.apply(
        lambda geom: affinity.translate(
            geom, xoff=random.randint(*x_off_range), yoff=random.randint(*y_off_range)
        )
    )
    return geometries


def transform_pt_crs(
    x: float, y: float, src_crs: int | str, dst_crs: int | str
) -> tuple[float, float]:
    """Transforms given point coordinates from one crs to another

    Args:
        x (float): horizontal (or east-west) coordinate
        y (float): vertical coordinate (or north-south)
        src_crs (int | str): source CRS
        dst_crs (int | str): destination CRS

    Returns:
        tuple[float, float]: transformed coordinates
    """
    transformer = Transformer.from_crs(src_crs, dst_crs)
    transformed_pt = transformer.transform(x, y)
    return transformed_pt


def buffer_wgs84_points(
    points: GeoDataFrame,
    tile_size_m: int,
    cap_style: int = 3,
    drop_epsg_col: bool = True,
) -> GeoDataFrame:
    """Given a geodataframe with point geometries in WGS84, buffers them and returns the resulting tiles in WGS84

    Args:
        spots (GeoDataFrame): geodataframe with point geometries
        tile_size_m (int): tiles will be of size (tile_size_m X tile_size_m)
        cap_style (int): the shape of the ends of the buffer. Defaults to 3. See
        https://shapely.readthedocs.io/en/stable/reference/shapely.buffer.html for
        more info
        drop_epsg_col (bool): whether to drop the epsg column generated for buffering the
        geometries

    Returns:
        GeoDataFrame: geodataframe with tiles
    """
    tile_centroids = points.copy()
    tile_centroids["epsg"] = tile_centroids.geometry.apply(
        lambda pt: find_best_utm_code(pt.x, pt.y)
    )
    tile_centroids_grouped = tile_centroids.groupby("epsg")
    tiles = []
    for epsg, epsg_hotspots in tile_centroids_grouped:
        epsg_hotspots = epsg_hotspots.to_crs(epsg=epsg)
        group_tiles = epsg_hotspots.geometry.buffer(
            tile_size_m // 2, cap_style=cap_style
        )
        group_tiles = group_tiles.to_crs(epsg=4326)
        if not drop_epsg_col:
            epsg_hotspots["epsg"] = epsg
        group_tiles = GeoDataFrame(
            epsg_hotspots,
            geometry=group_tiles,
            crs=4326,
        )
        tiles.append(group_tiles)
    tiles = pd.concat(tiles)
    return tiles


def create_cell_grid(
    bounds: tuple[float, float, float, float],
    n_cells_x: int,
    n_cells_y: int,
    out_crs: str = "EPSG:4326",
) -> geopandas.GeoDataFrame:
    """Create a cell grid of size (n_cells_x,n_cells_y) within given bounds.

    Args:
        bounds (tuple[float, float, float, float]): bounds in which to create the grid in the format west, north, east, south
        n_cells_x (int): number of cells in x direction
        n_cells_y (int): number of cells in y direction
        out_crs (_type_, optional): Output Coordinate Reference System. Defaults to "EPSG:4326".

    Returns:
        geopandas.GeoDataFrame: grid cell as a geodataframe
    """
    xmin, ymin, xmax, ymax = bounds
    cell_size_x = (xmax - xmin) / n_cells_x
    cell_size_y = (ymax - ymin) / n_cells_y
    grid_cells = []
    for x0 in np.arange(xmin, xmax, cell_size_x):
        for y0 in np.arange(ymin, ymax, cell_size_y):
            x1 = x0 - cell_size_x
            y1 = y0 + cell_size_y
            grid_cells.append(shapely.geometry.box(x0, y0, x1, y1))
    return geopandas.GeoDataFrame(grid_cells, columns=["geometry"], crs=out_crs)


def find_best_utm_code(lon: float, lat: float) -> str:
    """finds the best matching UTM code for given lat-long coordinates

    Args:
        lon (float): longitude
        lat (float): ñatitude

    Returns:
        str: UTM code found
    """
    utm_band = str((math.floor((lon + 180) / 6) % 60) + 1)
    if len(utm_band) == 1:
        utm_band = "0" + utm_band
    if lat >= 0:
        epsg_code = "326" + utm_band
    else:
        epsg_code = "327" + utm_band
    return epsg_code
