import planetary_computer
from pystac_client import Client
import rasterio
import numpy as np
from datetime import datetime, timedelta
import apps.config as config

# STAC client config
CATALOG_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"

def get_available_dates(lat, lon):
    delta = config.BBOX_DELTA
    bbox = [lon - delta, lat - delta, lon + delta, lat + delta]
    end = datetime.now().strftime("%Y-%m-%d")
    start = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    catalog = Client.open(CATALOG_URL)
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=f"{start}/{end}",
        query={"eo:cloud_cover": {"lt": 10}},
        limit=100
    )
    items = list(search.items())
    dates = sorted({itm.properties["datetime"][:10] for itm in items}, reverse=True)
    return dates

def fetch_image(lat, lon, date_str):
    delta = config.BBOX_DELTA
    bbox = [lon - delta, lat - delta, lon + delta, lat + delta]
    search_time = f"{date_str}/{date_str}"
    catalog = Client.open(CATALOG_URL)

    print('catalog opened')
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=search_time,
        query={"eo:cloud_cover": {"lt": 50}},
        limit=1
    )
    items = list(search.items())
    if not items:
        return None
    item = planetary_computer.sign(items[0])
    bands = ["B04", "B03", "B02"]
    channels = []
    for b in bands:
        with rasterio.open(item.assets[b].href) as src:
            ch = src.read(1, out_shape=(512,512))
        channels.append(ch)
    rgb = np.stack(channels, axis=-1).astype(float)
    rgb /= max(rgb.max(), 1)
    rgb = np.clip(rgb * 5.0, 0, 1)
    return rgb
