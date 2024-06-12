"""
OpenStreetMapa data download module
"""
from typing import List, Optional, Union

import geopandas as gpd
import osmnx as ox
import pandas as pd
from shapely.geometry import Polygon
from shapely.validation import make_valid


def download_waterways_from_osm(
    gdf: Union[str, gpd.GeoDataFrame],
    storage,
    waterway_tags: Optional[dict] = {
        "waterway": ["river", "canal", "stream", "brook", "ditch", "drain"]
    },
) -> None:
    """
    Download the waterways from OpenStreetMap for the given area of interest

    Parameters
    ----------
    aoi : Union[str, gpd.GeoDataFrame]
        The area of interest
    storage : BaseStorage
        The storage object
    waterway_tags : dict, optional
        The waterway tags to use, by default {'waterway': ['river', 'canal', 'stream', 'brook', 'ditch', 'drain']}

    Raises
    ------
    TypeError
        If the area of interest is not a GeoDataFrame or a filepath
    """
    if isinstance(gdf, str):
        gdf = gpd.read_file(gdf)
    elif not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("AoI must be a GeoDataFrame or a filepath")

    all_waterways = get_all_osm_elements(gdf, waterway_tags)

    final_waterways_gdf = pd.concat(all_waterways, ignore_index=True)
    final_waterways_gdf = final_waterways_gdf[["geometry"]]
    final_waterways_gdf = final_waterways_gdf[
        final_waterways_gdf.geometry.type.isin(("LineString", "MultiLineString"))
    ]
    storage.create_from_parquet(final_waterways_gdf, name="waterways.parquet")


def download_roads_from_osm(
    gdf: Union[str, gpd.GeoDataFrame],
    storage,
    waterway_tags: Optional[dict] = {
        "highway": ["motorway", "trunk", "primary", "secondary", "tertiary"]
    },
) -> None:
    """
    Download the waterways from OpenStreetMap for the given area of interest

    Parameters
    ----------
    aoi : Union[str, gpd.GeoDataFrame]
        The area of interest
    storage : BaseStorage
        The storage object
    waterway_tags : dict, optional
        The waterway tags to use, by default {'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary']}

    Raises
    ------
    TypeError
        If the area of interest is not a GeoDataFrame or a filepath
    """
    if isinstance(gdf, str):
        gdf = gpd.read_file(gdf)
    elif not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("AoI must be a GeoDataFrame or a filepath")

    all_roads = get_all_osm_elements(gdf, waterway_tags)

    final_roads_gdf = pd.concat(all_roads, ignore_index=True)
    final_roads_gdf = final_roads_gdf[["geometry"]]
    final_roads_gdf = final_roads_gdf[
        final_roads_gdf.geometry.type.isin(("LineString", "MultiLineString"))
    ]
    storage.create_from_parquet(final_roads_gdf, name="roads.parquet")


def download_buildings_from_osm(gdf: Union[str, gpd.GeoDataFrame], storage):
    """
    Download the buildings from OpenStreetMap for the given area of interest

    Parameters
    ----------
    aoi : Union[str, gpd.GeoDataFrame]
        The area of interest
    storage : BaseStorage
        The storage object

    Raises
    ------
    TypeError
        If the area of interest is not a GeoDataFrame or a filepath
    """
    if isinstance(gdf, str):
        gdf = gpd.read_file(gdf)
    elif not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("AoI must be a GeoDataFrame or a filepath")

    all_buildings = []

    for _, row in gdf.iterrows():
        polygon = row.geometry

        try:
            buildings_gdf = ox.features_from_polygon(polygon, tags={"building": True})
        except ox._errors.InsufficientResponseError:
            continue

        all_buildings.append(buildings_gdf)

    final_buildings_gdf = pd.concat(all_buildings, ignore_index=True)
    final_buildings_gdf = final_buildings_gdf[["geometry"]]
    final_buildings_gdf = final_buildings_gdf[
        final_buildings_gdf.geometry.type.isin(("Polygon", "MultyPolygon"))
    ]
    final_buildings_gdf.to_crs(epsg=4326, inplace=True)
    storage.create_from_parquet(final_buildings_gdf, name="buildings.parquet")


def get_all_osm_elements(gdf: gpd.GeoDataFrame, tags: dict) -> List:
    """
    Iterate over a given AOI GeoDataFrame and get all the desired OSM elements defined in the tags

    Parameters
    ----------
    gdf: gpd.GeoDataFrame
        The GeoDataFrame of the Area of Interest
    tags: dict
        Dict with the OSM tags of the elements to download

    Returns
    -------
    all_elements: List
        List with all the required elements
    """
    all_elements = []

    for _, row in gdf.iterrows():
        # create polygon from row as shapely.geometry.Polygon
        polygon = row.geometry
        if not polygon.is_valid:
            polygon = make_valid(polygon)

        for key, values in tags.items():
            if isinstance(values, list):
                for value in values:
                    try:
                        waterway_gdf = ox.features_from_polygon(
                            polygon, tags={key: value}
                        )
                        all_elements.append(waterway_gdf)
                    except ox._errors.InsufficientResponseError:
                        continue
            else:
                try:
                    waterway_gdf = ox.features_from_polygon(polygon, tags={key: values})
                    all_elements.append(waterway_gdf)
                except ox._errors.InsufficientResponseError:
                    continue

    return all_elements
