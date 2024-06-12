"""
Explore, load and download satellite imagery data
"""

import numpy as np
from typing import List, Union, Optional, Any
from datetime import datetime

from . import DOWNLOADERS, AVAILABLE_COLLECTIONS
from .utils import (
    create_aoi_geodataframe,
    get_last_month,
    add_item_extra_properties,
)

from ...storage import Storage


def load_satellite_imagery(
    aoi: Any,
    date: Optional[List[Union[str, datetime]]] = None,
    collection: str = "sentinel-2-l2a",
    clip: Optional[bool] = False,
    crs: Optional[str] = "epsg:4326",
    **kwargs,
):
    """
    Load satellite imagery data from a given area of interest (aoi) and date in memory.

    Parameters
    ----------
    aoi : Any
        Area of interest. It can be a GeoDataFrame, a list of coordinates, a bounding box, etc.
    date : Optional[List[Union[str, datetime]]], optional
        Date of the image, by default None. If None, the last available image will be loaded.
    collection : str, optional
        Satellite collection to download, by default "sentinel-2-l2a"
    clip : Optional[bool], optional
        Clip the data to the area of interest, by default False
    crs : Optional[str], optional
        Coordinate Reference System, by default "epsg:4326"
    kwargs : dict
        Extra parameters to pass to the downloader, such as bands, cloud_cover, vegetation_percentage an so on.   TODO

    Returns
    -------
    xarray.Dataset
        Satellite imagery data in memory.
    """
    gdf = create_aoi_geodataframe(aoi, crs)
    bbox = gdf.total_bounds
    if collection not in AVAILABLE_COLLECTIONS:
        raise ValueError(
            f"Collection {collection} not available. Available collections are: {AVAILABLE_COLLECTIONS}"
        )

    if not date and "dem" not in collection:
        # If no date given, search for the last available image
        # until a valid image is found
        last_available_image_date = None
        while not last_available_image_date:
            date = get_last_month(date)
            search = explore_satellite_imagery(gdf, date, collection, crs, **kwargs)
            if search:
                last_available_image_date = search[-1]["datetime"]
                date = last_available_image_date

    downloader = DOWNLOADERS[collection](bbox, date, **kwargs)
    data = downloader.load_stac()

    if clip:
        data = downloader.clip_data(data, gdf)

    return data


def download_satellite_imagery(
    storage: Storage,
    aoi: Any,
    date: Optional[List[Union[str, datetime]]] = None,
    collection: str = "sentinel-2-l2a",
    name: Optional[str] = None,
    clip: Optional[bool] = False,
    crs: Optional[str] = "epsg:4326",
    **kwargs,
) -> List[str]:
    """
    Download satellite imagery data from a given area of interest (aoi) and date to a given storage.

    Parameters
    ----------
    storage : Storage
        Storage object to save the data.
    aoi : Any
        Area of interest. It can be a GeoDataFrame, a list of coordinates, a bounding box, etc.
    date : Optional[List[Union[str, datetime]]], optional
        Date of the image, by default None. If None, the last available image will be loaded.
    collection : str, optional
        Satellite collection to download, by default "sentinel-2-l2a"
    clip : Optional[bool], optional
        Clip the data to the area of interest, by default False
    crs : Optional[str], optional
        Coordinate Reference System, by default "epsg:4326"
    kwargs : dict
        Extra parameters to pass to the downloader, such as bands, cloud_cover, vegetation_percentage an so on.   TODO

    Returns
    -------
    None
    """
    data = load_satellite_imagery(aoi, date, collection, clip, crs, **kwargs)
    if not data:
        return None
    data = data.compute()
    paths = []
    for date in data.time.values:
        date = np.datetime_as_string(date, unit="D")
        path = storage.create(
            data.sel(time=date).squeeze(),
            name=name if name else f"{collection}_{date}.tif",
        )
        paths.append(path)
    return paths if len(paths) > 1 else paths[0]


def explore_satellite_imagery(
    aoi: Any,
    date: Optional[List[Union[str, datetime]]] = None,
    collection: str = "sentinel-2-l2a",
    crs: Optional[str] = "epsg:4326",
    **kwargs,
) -> dict:
    """
    Explore satellite imagery data from a given area of interest (aoi) and date.

    Parameters
    ----------
    aoi : Any
        Area of interest. It can be a GeoDataFrame, a list of coordinates, a bounding box, etc.
    date : Optional[List[Union[str, datetime]]], optional
        Date of the image, by default None. If None, the available images of the last month will be loaded.
    collection : str, optional
        Satellite collection to download, by default "sentinel-2-l2a"
    crs : Optional[str], optional
        Coordinate Reference System, by default "epsg:4326"
    kwargs : dict
        Extra parameters to pass to the downloader, such as bands, cloud_cover, vegetation_percentage an so on.   TODO

    Returns
    -------
    dict
        Information about the available images. If no image is found, it returns None. If any extra parameter is given, it will be added to the output.
    """
    gdf = create_aoi_geodataframe(aoi, crs)
    bbox = gdf.total_bounds
    if collection not in AVAILABLE_COLLECTIONS:
        raise ValueError(
            f"Collection {collection} not available. Available collections are: {AVAILABLE_COLLECTIONS}"
        )

    if not date:
        date = get_last_month()

    downloader = DOWNLOADERS[collection](bbox, date, **kwargs)
    search = downloader.search_stac()

    if not search:
        return None

    search_list = []
    for item in search:
        item_dict = {
            "id": item.id,
            "datetime": item.datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        item_dict["thumbnail"] = (
            item.assets["thumbnail"].href if "thumbnail" in item.assets else None
        )
        # Add extra parameters from the query, such as cloud cover, etc.
        item_dict = add_item_extra_properties(item, item_dict, downloader.query, kwargs)
        search_list.append(item_dict)
    # Sort by datetime
    search_list_sorted = sorted(search_list, key=lambda x: x["datetime"])

    return search_list_sorted
