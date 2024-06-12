"""
STACDownloader class to download and load satellite data from a STAC API.
"""

import geopandas as gpd

from datetime import datetime
from typing import List, Union, Optional

from .decorators import with_rioxarray


class STACDownloader:
    def __init__(
        self,
        aoi: Union[str, gpd.GeoDataFrame],
        datetime: List[Union[str, datetime]],
        query: Optional[dict] = None,
    ):
        try:
            from odc.stac import configure_rio, load

            self.load = load
        except ImportError:
            raise ImportError(
                "The odc.stac package is required. Please install it with 'pip install odc-stac' and try again."
            )
        try:
            import pystac_client
        except ImportError:
            raise ImportError(
                "The pystac_client package is required. Please install it with 'pip install pystac-client' and try again."
            )
        configure_rio(cloud_defaults=True, aws={"aws_unsigned": True})

        self.aoi = aoi
        self.datetime = datetime
        self.query = query
        self.catalog = pystac_client.Client.open(self.url, modifier=self.modifier)

    def search_stac(self):
        items = self.catalog.search(
            bbox=self.aoi,
            datetime=self.datetime,
            collections=self.collection,
            query=self.query,
        ).item_collection()

        if len(items) == 0:
            print(
                f"No images found for {self.datetime} in {self.collection} collection"
            )
            return None

        return items

    def load_stac(
        self,
        groupby: Optional[str] = "solar_day",
        chunks: Optional[dict] = {"time": 5, "x": 512, "y": 512},
    ):
        items = self.search_stac()
        if not items:
            return None
        data = self.load(
            items,
            chunks=chunks,
            crs=self.crs,
            bands=self.bands,
            resolution=self.resolution,
            groupby=groupby,
            bbox=self.aoi,
        )

        return data

    @staticmethod
    @with_rioxarray
    def clip_data(data, gdf):
        return data.rio.clip(gdf.geometry.values, gdf.crs, drop=False)
