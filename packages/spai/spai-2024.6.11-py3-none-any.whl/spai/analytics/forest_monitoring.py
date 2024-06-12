import numpy as np
import geopandas as gpd

from ..processing import read_raster
from ..processing import normalised_difference
from ..processing import mask_raster
from ..processing import autocategorize1D
from ..processing import px_count
from ..processing import colorize_raster
from ..processing import save_table

from .utils import format_name

COLORS_MAPPING = {0: "orangered", 1: "yellow", 2: "lawngreen", 3: "darkgreen"}


def forest_monitoring(
    image_name,
    date,
    aoi_mask,
    storage,
    prefix="",  # prefix for the raster names
    analytics_prefix="",  # prefix for the analytics names
    names={},
    threshold=3,
    colors=["darkgreen"],
):
    default_names = {  # names for the raster files
        "ndvi": "ndvi_{date}.tif",
        "ndvi_masked": "ndvi_masked_{date}.tif",
        "ndvi_categorized": "ndvi_categorized_{date}.tif",
        "vegetation": "vegetation_{date}.tif",
        "vegetation_masked": "vegetation_masked_{date}.tif",
        "vegetation_masked_rgb": "vegetation_masked_rgb_{date}.tif",
        "quality_masked": "quality_masked_{date}.tif",
        "quality_masked_rgb": "quality_masked_rgb_{date}.tif",
        "vegetation_growth": "AOI_Vegetation_Growth.json",
        "vegetation_quality": "AOI_Vegetation_Quality.json",
    }
    names = {**default_names, **names}

    # read_raster image
    ds, raster = read_raster(image_name, storage, bands=[8, 4])

    # calculate ndvi
    ndvi = normalised_difference(raster)

    # save_raster ndvi
    raster_name_ndvi = format_name(names["ndvi"], prefix, date)
    storage.create(ndvi, raster_name_ndvi, ds=ds)

    # read_geojson aoi_mask
    aoi_mask_gdf = gpd.GeoDataFrame.from_features(aoi_mask, crs=4326)

    # mask_raster ndvi with aoi_mask
    ndvi_masked, _ = mask_raster(raster_name_ndvi, aoi_mask_gdf, storage)

    # save_raster ndvi_masked
    raster_name_ndvi_masked = format_name(names["ndvi_masked"], prefix, date)
    storage.create(ndvi_masked, raster_name_ndvi_masked, ds=ds)

    # autocategorize1D ndvi
    ndvi_categorized = autocategorize1D(ndvi)

    # save_raster ndvi_categorized
    raster_name_ndvi_categorized = format_name(names["ndvi_categorized"], prefix, date)
    storage.create(ndvi_categorized, raster_name_ndvi_categorized, ds=ds)

    # apply_threshold to ndvi_categorized
    vegetation = ndvi_categorized >= threshold
    vegetation = vegetation.astype(np.uint8)

    # save_raster vegetation
    raster_name_vegetation = format_name(names["vegetation"], prefix, date)
    storage.create(vegetation, raster_name_vegetation, ds=ds)

    # mask_raster vegetation with aoi_mask
    vegetation_masked, _ = mask_raster(raster_name_vegetation, aoi_mask_gdf, storage)

    # save_raster vegetation_masked
    raster_name_vegetation_masked = format_name(
        names["vegetation_masked"], prefix, date
    )
    storage.create(vegetation_masked, raster_name_vegetation_masked, ds=ds)

    # colorize_raster vegetation_masked
    vegetation_masked_rgb = colorize_raster(vegetation_masked, colors=colors)

    # save_raster vegetation_masked_rgb
    raster_name_vegetation_masked_rgb = format_name(
        names["vegetation_masked_rgb"], prefix, date
    )
    storage.create(vegetation_masked_rgb, raster_name_vegetation_masked_rgb, ds=ds)

    # mask_raster ndvi_categorized with aoi_mask
    quality_mask, _ = mask_raster(raster_name_ndvi_categorized, aoi_mask_gdf, storage)

    # save_raster quality_mask
    raster_name_quality_mask = format_name(names["quality_masked"], prefix, date)
    storage.create(quality_mask, raster_name_quality_mask, ds=ds)

    # colorize_raster quality_mask
    quality_mask_rgb = colorize_raster(
        quality_mask,
        colors=COLORS_MAPPING,
        colorize_zero=True,
    )

    # save_raster quality_mask_rgb
    raster_name_quality_mask_rgb = format_name(
        names["quality_masked_rgb"], prefix, date
    )
    storage.create(quality_mask_rgb, raster_name_quality_mask_rgb, ds=ds)

    # px_count vegetation_masked
    growth = px_count(vegetation_masked, values=[0, 1])

    # div growth
    growth_hectarias = np.divide(
        growth, 100, out=np.zeros_like(growth, dtype=np.float64), where=100 != 0
    )

    # save_table growth
    growth_table_name = format_name(names["vegetation_growth"], analytics_prefix, date)
    growth_columns = ["Not Vegetation Ha", "Vegetation Ha", "Total"]
    save_table(
        data=growth_hectarias,
        columns=growth_columns,
        table_name=growth_table_name,
        date=date,
        storage=storage,
    )

    # px_count quality_mask
    quality = px_count(quality_mask, values=[0, 1, 2, 3])

    # div quality
    quality_hectarias = np.divide(
        quality, 100, out=np.zeros_like(quality, dtype=np.float64), where=100 != 0
    )

    # save_table quality
    quality_table_name = format_name(
        names["vegetation_quality"], analytics_prefix, date
    )
    quality_columns = [
        "Bare Ground",
        "Sparse or Unhealthy Vegetation",
        "Healthy Vegetation",
        "Very Health Vegetation",
        "Total",
    ]
    save_table(
        data=quality_hectarias,
        table_name=quality_table_name,
        columns=quality_columns,
        date=date,
        storage=storage,
    )
