from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DjiMetadataHeader(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    sort_count: int | None = Field(alias="SrtCnt")
    diff_time: int | None = Field(alias="DiffTime")
    time_stamp: datetime | None = Field(alias="timestamp")


class DjiMetadata(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    header: DjiMetadataHeader

    iso: int | None
    shutter_speed: str | None = Field(alias="shutter")
    fnum: int | None
    exposure_value: float | None = Field(alias="ev")
    color_temperature: int | None = Field(alias="ct")
    color_mode: str | None = Field(alias="color_md")
    focal_length: float | None = Field(alias="focal_len")
    latitude: Decimal
    longitude: Decimal
    relative_altitude: Decimal | None = Field(alias="rel_alt")
    absolute_altitude: Decimal | None = Field(alias="abs_alt")

def convert_dji_metadata_to_exif_tags(dji_metadata: DjiMetadata) -> dict[str, Any]:
    metadata = {}
    if dji_metadata.iso is not None:
        metadata["EXIF:ISO"] = dji_metadata.iso
    if dji_metadata.fnum is not None:
        metadata["EXIF:FNumber"] = float(dji_metadata.fnum)
    if dji_metadata.shutter_speed is not None:
        metadata["EXIF:ShutterSpeedValue"] = dji_metadata.shutter_speed
    if dji_metadata.latitude is not None:
        metadata["EXIF:GPSLatitude"] = str(dji_metadata.latitude)
        metadata["EXIF:GPSLatitudeRef"] = "N"
    if dji_metadata.longitude is not None:
        metadata["EXIF:GPSLongitude"] = str(dji_metadata.longitude)
        metadata["EXIF:GPSLongitudeRef"] = "W"
    if dji_metadata.relative_altitude is not None:
        metadata["EXIF:GPSAltitude"] = str(dji_metadata.absolute_altitude)
    if dji_metadata.header.time_stamp is not None:
        metadata["EXIF:DateTimeOriginal"] = dji_metadata.header.time_stamp.strftime('%Y:%m:%d %H:%M:%S.%f')
    if dji_metadata.focal_length is not None:
        metadata["EXIF:FocalLength"] = dji_metadata.focal_length

    return metadata

# EXIF:ISO: int
# EXIF:FNumber: float
# EXIF:ExposureTime: float
# EXIF:ShutterSpeedValue: float
# EXIF:GPSLatitude: float
# EXIF:GPSLatitudeRef: str
# EXIF:GPSLongitude: float
# EXIF:GPSLongitudeRef: str
# EXIF:GPSAltitude: float
# EXIF:GPSAltitudeRef: int
# EXIF:GPSMapDatum: float
# EXIF:DateTimeOriginal: str
# EXIF:FocalLength: float