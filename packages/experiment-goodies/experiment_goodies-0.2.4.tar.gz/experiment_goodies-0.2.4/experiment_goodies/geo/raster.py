from typing import Any, Literal

import affine
import numpy as np
import rasterio
from geopandas import GeoSeries
from rasterio.mask import mask
from rasterio.merge import merge
from rasterio.warp import Resampling, calculate_default_transform, reproject
from rio_cogeo import cog_translate
from shapely import Polygon, box


def compute_affine_transform(
    min_x: float, max_y: float, resolution_x: float, resolution_y: float
) -> affine.Affine:
    """Creates the affine transform for given coordinates and resolution"""
    return affine.Affine(
        resolution_x,
        0,
        min_x,
        0,
        resolution_y,
        max_y,
    )


def get_raster_metadata(input_path: str) -> dict[str, Any]:
    """Retrieves metadata from raster stored in disk"""
    with rasterio.open(input_path) as src:
        return src.meta


def get_raster_extent(input_path: str) -> GeoSeries:
    """Retrieves the extent (bounding box) of the raster as GeoSeries in the same CRS as the raster"""
    with rasterio.open(input_path) as src:
        geom = box(*src.bounds)
        return GeoSeries.from_wkt(data=[geom.wkt], crs=src.crs)


def get_raster_footprint(input_path: str) -> GeoSeries:
    """Retrieves the footprint of the raster file as a GeoSeries of polygons in WGS84

    Args:
        input_path (str): path to raster from which to extract footprint

    Returns:
        GeoSeries: footprint of raster
    """
    with rasterio.open(input_path) as src:
        # read dataset valid mask
        mask = src.dataset_mask()

        # Extract feature shapes and values from the array.
        footprint = []
        for geom, val in rasterio.features.shapes(mask, transform=src.transform):
            # skip masks that are not valid
            if val != 255:
                continue

            # Transform shapes from the dataset's own coordinate
            # reference system to CRS84 (EPSG:4326).
            geom = rasterio.warp.transform_geom(src.crs, "EPSG:4326", geom, precision=6)
            for g in geom["coordinates"]:
                footprint.append(Polygon(g))
        return GeoSeries(footprint, crs="EPSG:4326")


def mask_raster_pixels_by_geometries(
    geometries: GeoSeries,
    raster_path: str,
    output_path: str,
    invert: bool = False,
    fill_value: int = 0,
):
    """Masks raster according to given geometries. Pixel values outside of geometries will be replaced
    by given `fill_value`, unless `inverted=True` in which case it's the opposite. This function is a wrapper
    around rasterio.mask.mask

    Args:
        geometries (geopandas.GeoSeries): masking geometries
        raster_path (str): path to input raster
        output_path (str): path to output masked raster
        invert (bool, optional): set to True if pixels inside geometries should be replaced. Defaults to False.
        fill_value (int, optional): value to replace. Defaults to 0.
    """
    with rasterio.open(raster_path) as src:
        profile = src.profile
        prj_geometries = geometries.to_crs(src.crs)
        masked_array, out_transform = mask(
            src,
            prj_geometries,
            invert=invert,
            nodata=fill_value,
        )
        profile.update(
            {
                "height": masked_array.shape[1],
                "width": masked_array.shape[2],
                "transform": out_transform,
            }
        )
    with rasterio.open(output_path, "w", **profile) as dst:
        dst.write(masked_array)


def merge_rasters_into_mosaic(
    raster_paths: list[str],
    mosaic_path: str,
    method: Literal["first", "last", "min", "max"] = "max",
):
    """Merges a list of rasters into a single mosaic. Assumes all input rasters are in the same CRS
    This function is a simple wrapper around rasterio.merge.merge, see https://rasterio.readthedocs.io/en/stable/api/rasterio.merge.html
    for more complex functionalities.

    Args:
        paths (list[str]): list of rasters to merge
        mosaic_path (str): output mosaic path
        method (str): which method to use for merging. Defaults to "max"
    """
    mosaic, output_trf = merge(raster_paths, method=method)
    with rasterio.open(raster_paths[0]) as ref_src:
        ref_meta = ref_src.meta
    output_meta = ref_meta.copy()
    output_meta.update(
        {
            "driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": output_trf,
        }
    )
    with rasterio.open(mosaic_path, "w", **output_meta) as dst:
        dst.write(mosaic)


def transform_to_cog(raster_path: str, output_path: str):
    """Translates a GeoTIFF raster to Cloud Optimized GeoTIFF (COG) format. It is a simple wrapper around
    cog_translate function from rio-cogeo library. Use https://cogeotiff.github.io/rio-cogeo/ if you need more
    control.


    Args:
        raster_path (str): path to raster to transform
        output_path (str): path to cog destination
    """
    with rasterio.open(raster_path) as src:
        src_profile = src.profile
    src_profile.update(
        {
            "GTIFF": "IF_SAFER",
            "interleave": "pixel",
            "compress": "DEFLATE",
            "tiled": True,
            "blockxsize": 256,
            "blockysize": 256,
        }
    )

    config = dict(
        GDAL_NUM_THREADS="ALL_CPUS",
        GDAL_TIFF_INTERNAL_MASK=True,
        GDAL_TIFF_OVR_BLOCKSIZE="128",
    )
    cog_translate(raster_path, output_path, src_profile, config=config, in_memory=False)


def clip_raster_borders(
    raster_path: str, boundary_cut_m: int, nodata: Any = 0
) -> tuple[np.ndarray, dict[str, Any]]:
    """Clips borders of a raster by given distance in meters. Returns the clipped array and georeference metadata

    Args:
        raster_path (str): path to raster to clip
        boundary_cut_m (int): clipping distance from border, in meters

    Returns:
        tuple[np.ndarray, dict[str, Any]]: clipped raster array and metadata
    """
    with rasterio.open(raster_path) as src:
        bounds = src.bounds
        clipping_geom = GeoSeries(
            Polygon(
                [
                    (bounds.left, bounds.top),
                    (bounds.right, bounds.top),
                    (bounds.right, bounds.bottom),
                    (bounds.left, bounds.bottom),
                ]
            ),
            crs=src.crs,
        )
        clipping_geom = clipping_geom.buffer(distance=-boundary_cut_m)
    clipped_raster, meta = clip_raster_by_geom(
        raster_path, clipping_geom, nodata=nodata
    )
    return clipped_raster, meta


def clip_raster_by_geom(
    raster_path: str, geom: GeoSeries, nodata: int = 0, all_touched: bool = True
) -> tuple[np.ndarray, dict[str, Any]]:
    """Clips a raster by given geometry. Returns the clipped array and georeference metadata. Uses rasterio.mask.mask
    underneath

    Args:
        raster_path (str): path to raster
        geom (GeoDataFrame): clipping geometry
        nodata (int, optional): value for nodata in raster. Defaults to 0.
        all_touched (bool, optional): whether to consider all pixels touched by the geometry. Defaults to True.

    Returns:
        tuple[np.ndarray, dict[str, Any]]: clipped array and raster metadata
    """
    with rasterio.open(raster_path) as src:
        # clipping geometry must have the same CRS as raster
        geometry_src_crs = geom.to_crs(src.crs)
        out, out_transform = mask(
            src,
            shapes=geometry_src_crs.geometry,
            crop=True,
            all_touched=all_touched,
            nodata=nodata,
        )
        # update metadata
        out_meta = src.meta
        out_meta.update(
            {
                "driver": "GTiff",
                "height": out.shape[1],
                "width": out.shape[2],
                "transform": out_transform,
                "nodata": nodata,
            }
        )
    return out, out_meta


def mask_file_to_vector_file(
    mask_path: str,
    output_path: str,
    mask_value: int = 1,
    simplify: bool = False,
    simplify_tol: float = 1.0,
):
    """Converts a raster file containing an integer mask to a vector file with constituent polygons.
    The projection of the polygons will match that of the input raster. User can optionally simplify the
    resulting geometries via the Douglas Peucker algorithm.

    Args:
        mask_path (str): path to raster from where polygons will be extracted
        output_path (str): file path to save polygons as vector file
        mask_value (int, optional): the method will look for pixel values equal to this parameter
        for creating the geometries. Defaults to 1.
        simplify (bool, optional): whether to simplify the geometries. Defaults to False.
        simplify_tol (float, optional): tolerance (in raster projection units) for simplification. Defaults to 1.0.
    """
    with rasterio.open(mask_path) as src:
        mask = src.read()
        mask[mask != mask_value] = 0
        mask[mask == mask_value] = 1
        crs = src.crs
        transform = src.transform
    polygons = mask_to_polygons(mask, crs, transform)
    if simplify:
        polygons = polygons.simplify(simplify_tol)
    polygons.to_file(output_path)


def mask_to_polygons(mask: np.ndarray, crs: str, transform: np.ndarray) -> GeoSeries:
    """Converts a binary mask into a GeoSeries of polygons.

    Args:
        mask (np.ndarray): binary mask
        crs (str): coordinate reference system of the mask
        transform (np.ndarray): geo transform of the mask

    Returns:
        GeoSeries: polygons extracted from the mask
    """
    polygons = []
    for geom, val in rasterio.features.shapes(mask, transform=transform):
        if val == 0:
            continue
        for g in geom["coordinates"]:
            polygons.append(Polygon(g))
    polygons = GeoSeries(polygons, crs=crs)
    return polygons


def reproject_raster(
    raster_path: str,
    output_path: str,
    dst_crs: str,
    float_output: bool = True,
    resampling_method: Resampling = Resampling.nearest,
):
    """Reprojects a raster into given CRS

    Args:
        raster_path (str): input raster path
        output_path (str): output reprojected raster path
        dst_crs (str): destination coordinate reference system
        float_output (bool, optional): transform output raster to float and use NaN as nodata for output raster.
        Rasterio reprojection doesn't handle nodata well, so it is recommended to keep this value true. Defaults to True.
        resampling_method (Resampling, optional): resampling method for interpolating reprojected raster pixels. Defaults to Resampling.nearest.
    """
    with rasterio.open(raster_path) as src:
        # calculate the transform matrix for the output
        dst_transform, width, height = calculate_default_transform(
            src.crs,
            dst_crs,
            src.width,
            src.height,
            *src.bounds,  # unpacks outer boundaries (left, bottom, right, top)
        )
        # set properties for output
        dst_kwargs = src.meta.copy()
        dst_kwargs.update(
            {
                "crs": dst_crs,
                "transform": dst_transform,
                "width": width,
                "height": height,
            }
        )
        if float_output:
            dst_kwargs.update({"nodata": np.nan, "dtype": np.float32})

        with rasterio.open(output_path, "w", **dst_kwargs) as dst:
            # iterate through bands
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=dst_transform,
                    dst_crs=dst_crs,
                    resampling=resampling_method,
                )
