# from .download import download_satellite_image, download_dem, download_cloud_mask
# from .explore import explore_satellite_images

from .stac import (
    AWSS2L2ADownloader,
    PCS1GRDDownloader,
    PCS1RTCDownloader,
    AWSDEM30Downloader,
    AWSDEM90Downloader,
    PCESAWCDownloader,
    PCLandsat8Downloader,
    PCModisBurnedDownloader,
    PCModisSnow8Downloader,
    PCModisSnowDayDownloader,
    PCAlosPalsarAnnualDownloader,
)

DOWNLOADERS = {
    "sentinel-2-l2a": AWSS2L2ADownloader,
    "sentinel-1-grd": PCS1GRDDownloader,
    "sentinel-1-rtc": PCS1RTCDownloader,
    "cop-dem-glo-30": AWSDEM30Downloader,
    "cop-dem-glo-90": AWSDEM90Downloader,
    "esa-worldcover": PCESAWCDownloader,
    "landsat-8-c2-l2": PCLandsat8Downloader,
    "modis-burned-areas": PCModisBurnedDownloader,
    "modis-snow-cover-8": PCModisSnow8Downloader,
    "modis-snow-cover-daily": PCModisSnowDayDownloader,
    "alos-palsar-mosaic": PCAlosPalsarAnnualDownloader,
}
AVAILABLE_COLLECTIONS = list(DOWNLOADERS.keys())

from .download_stac import (
    download_satellite_imagery,
    load_satellite_imagery,
    explore_satellite_imagery,
)
