"""Skeleton of a handler."""

from typing import Tuple

import os
import numpy

from rasterio.io import MemoryFile

from rio_tiler import main
from rio_tiler_mvt.mvt import encoder as mvtEncoder

from urllib.request import urlopen

from lambda_proxy.proxy import API

APP = API(name="satellite-3d")


@APP.route(
    "/<int:z>/<int:x>/<int:y>.pbf",
    methods=["GET"],
    cors=True,
    payload_compression_method="gzip",
    binary_b64encode=True,
)
def tiler(
    z: int,
    x: int,
    y: int,
    tilesize: int = 128,
    feature_type: str = "polygon"
) -> Tuple:
    """Handle tile requests."""
    if isinstance(tilesize, str):
        tilesize = int(tilesize)

    address = f"https://elevation-tiles-prod.s3.amazonaws.com/geotiff/{z}/{x}/{y}.tif"
    tile, mask = main.tile(address, x, y, z, tilesize=tilesize)

    token = os.environ["MAPBOX_ACCESS_TOKEN"]
    address = f"https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.jpg?access_token={token}"
    imgdata = urlopen(address).read()
    with MemoryFile(imgdata) as memfile:
        with memfile.open() as dataset:
            rgb_tile = dataset.read(out_shape=(3, tilesize, tilesize))

    tile = numpy.concatenate([tile, rgb_tile], axis=0)
    return (
        "OK",
        "application/x-protobuf",
        mvtEncoder(
            tile,
            mask,
            ["elevation", "R", "G", "B"],
            "satellite-3d",
            feature_type=feature_type,
        ),
    )