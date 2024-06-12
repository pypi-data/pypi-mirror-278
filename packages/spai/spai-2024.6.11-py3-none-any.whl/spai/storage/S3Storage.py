import pandas as pd
import json
import io
from minio import Minio
import fnmatch
from io import BytesIO
import numpy as np
import shutil
import os

from .BaseStorage import BaseStorage
from .decorators import with_rio, with_geopandas, with_rioxarray


# Ver funciones en CloudStorage si las de aquí no acaban de funcionar...


class S3Storage(BaseStorage):
    def __init__(self, url, access, secret, bucket, region=None):
        super().__init__()
        self.url = url
        self.access = access
        self.secret = secret
        self.region = region
        self.bucket = bucket

        if self.access and self.secret:
            # Create a client
            self.client = Minio(
                endpoint=self.url,
                access_key=self.access,
                secret_key=self.secret,
                secure=True if self.region else False,
                region=self.region,
            )  # because no certificate is used in the containerised version of minio
            if not self.client.bucket_exists(self.bucket):
                # Make a bucket with the credentials and the bucket_name given
                self.client.make_bucket(self.bucket)
                print(f"Bucket '{self.bucket}' created")
            else:
                print(f"'{self.bucket}' bucket ready to use")
        else:
            # TODO: create bucket in our minio server (we will need our credentials for that, do it with API request?
            print("Missing credentials")
            # Habría que preguntar si se quiere crear el bucket en nuestro cloud o decirles que introduzcan sus creds

    def get_path(self, name):
        return self.get_url(name)

    def delete(self, name):
        self.client.remove_object(self.bucket, name)

    def get_url(self, name):
        return self.client.presigned_get_object(self.bucket, name)

    def exists(self, name):
        try:
            self.client.stat_object(self.bucket, name)
            return True
        except:
            return False

    def list(self, pattern="*", recursive=True):
        return fnmatch.filter(
            [
                obj.object_name
                for obj in self.client.list_objects(self.bucket, recursive=recursive)
            ],
            pattern,
        )

    def create_from_path(self, data, name):
        if data.endswith(".json"):
            content_type = "application/json"
            self.client.fput_object(self.bucket, name, data, content_type=content_type)
            return self.get_url(name)
        if data.endswith(".tiff") or data.endswith(".tif"):
            content_type = "image/tiff"
            self.client.fput_object(self.bucket, name, data, content_type=content_type)
            return self.get_url(name)
        if data.endswith(".geojson"):
            content_type = "application/geojson"
            self.client.fput_object(self.bucket, name, data, content_type=content_type)
            return self.get_url(name)
        self.client.fput_object(self.bucket, name, data)
        return self.get_url(name)

    def create_from_image(self, data, name):
        image_bytes = BytesIO()
        # get format from file extension
        format = name.split(".")[-1]
        data.save(image_bytes, format=format)
        image_bytes.seek(0)
        self.client.put_object(
            self.bucket, name, image_bytes, len(image_bytes.getvalue())
        )
        return self.get_url(name)

    @with_rio
    def create_from_rasterio(self, rio, x, name, ds, window=None):
        transform = ds.transform if window is None else ds.window_transform(window)
        with rio.io.MemoryFile() as memfile:
            with memfile.open(
                driver="GTiff",
                count=1 if x.ndim < 3 else x.shape[0],
                height=x.shape[0] if x.ndim < 3 else x.shape[1],
                width=x.shape[1] if x.ndim < 3 else x.shape[2],
                dtype=np.uint8 if x.dtype == "bool" else x.dtype,
                crs=ds.crs,
                transform=transform,
                # nbits=1 if x.dtype == 'bool' else
            ) as dest_ds:
                bands = 1 if x.ndim < 3 else [i + 1 for i in range(x.shape[0])]
                dest_ds.write(x, bands)
            self.client.put_object(
                self.bucket, name, memfile, length=-1, part_size=10 * 1024 * 1024
            )
        return self.get_url(name)

    @with_rioxarray
    def create_from_xarray(self, rxr, data, name):
        # TODO don't save to disk
        content_type = "image/tiff"
        tmp_path = f"/tmp/{name}"
        self.create_dir(tmp_path)
        data.rio.to_raster(tmp_path)
        self.client.fput_object(
            self.bucket,
            name,
            tmp_path,
            content_type=content_type,
        )
        # shutil.rmtree(os.path.dirname(tmp_path))
        return self.get_url(name)

    def create_from_array(self, data, name):
        array_bytes = BytesIO()
        np.save(array_bytes, data)
        array_bytes.seek(0)
        self.client.put_object(
            self.bucket, name, array_bytes, len(array_bytes.getvalue())
        )
        return self.get_url(name)

    def create_from_csv(self, data, name):
        csv_bytes = BytesIO()
        data.to_csv(csv_bytes)
        csv_bytes.seek(0)
        self.client.put_object(self.bucket, name, csv_bytes, len(csv_bytes.getvalue()))
        return self.get_url(name)

    def create_from_json(self, data, name):
        json_bytes = BytesIO()
        data.to_json(json_bytes)
        json_bytes.seek(0)
        self.client.put_object(
            self.bucket, name, json_bytes, len(json_bytes.getvalue())
        )
        return self.get_url(name)

    def create_from_dict(self, data, name):
        if name.endswith(".json"):
            content_type = "application/json"
            content = json.dumps(data, ensure_ascii=False).encode("utf8")
            self.client.put_object(
                self.bucket,
                name,
                io.BytesIO(content),
                -1,
                part_size=50 * 1024 * 1024,
                content_type=content_type,
            )
            return name
        elif name.endswith(".geojson"):
            content_type = "application/geojson"
            content = json.dumps(data, ensure_ascii=False).encode("utf8")
            self.client.put_object(
                self.bucket,
                name,
                io.BytesIO(content),
                -1,
                part_size=50 * 1024 * 1024,
                content_type=content_type,
            )
            return name
        else:
            raise TypeError("Not a valid dict type extension")

    def create_from_string(self, data, name):
        content_type = "text/plain"
        prefix = "txt/"
        content = data.encode("utf8")
        self.client.put_object(
            self.bucket,
            name,
            io.BytesIO(content),
            -1,
            part_size=50 * 1024 * 1024,
            content_type=content_type,
        )
        return name

    def create_from_dataframe(self, data, name):
        if name.endswith(".csv"):
            content_type = "text/csv"
            content = data.to_csv().encode("utf8")
            self.client.put_object(
                self.bucket,
                name,
                io.BytesIO(content),
                -1,
                part_size=50 * 1024 * 1024,
                content_type=content_type,
            )
            return name
        elif name.endswith(".json") or name.endswith(".geojson"):
            type = "json" if name.endswith(".json") else "geojson"
            content_type = f"application/{type}"
            content = data.to_json().encode("utf8")
            self.client.put_object(
                self.bucket,
                name,
                io.BytesIO(content),
                -1,
                part_size=50 * 1024 * 1024,
                content_type=content_type,
            )
            return name
        else:
            raise TypeError("Not a valid dataframe type extension")

    def read_object(self, name):
        return BytesIO(self.client.get_object(self.bucket, name).read())

    def read_from_json(self, name):
        return pd.read_json(self.read_object(name))

    def read_from_array(self, name):
        return np.load(self.read_object(name))

    @with_geopandas
    def read_from_geojson(self, gpd, name):
        response = None
        try:
            response = self.client.get_object(self.bucket, name)
            data = json.load(response)
        finally:
            if response:
                response.close()
                response.release_conn()
        return gpd.GeoDataFrame.from_features(data)

    @with_rio
    def read_from_rasterio(self, rio, name):
        return rio.open(self.read_object(name))

    def read_from_csv(self, name):
        return pd.read_csv(self.read_object(name), index_col=0)
