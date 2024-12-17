from datetime import timedelta, datetime
import xml.etree.ElementTree as ElementTree
import re
from decimal import Decimal
from pathlib import PosixPath

from srt import Subtitle
import srt

from src.model.dji_metadata import DjiMetadata, DjiMetadataHeader


def parse_srt_subtitle_file(srt_subtitle_file: PosixPath) -> list[Subtitle]:
    with open(str(srt_subtitle_file), 'r') as file:
        subtitles: list[Subtitle] = list(srt.parse(file.read()))
    return subtitles


def find_subtitle(time: timedelta, subtitles: list[Subtitle]) -> Subtitle:
    for subtitle in subtitles:
        if subtitle.start <= time <= subtitle.end:
            return subtitle
    raise ValueError(f"No subtitle found for {time=}")


def _remove_xml_tags(content: str) -> str:
    return ElementTree.fromstring(content).text


def _extract_timestamp(content: str) -> str | None:
    timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+)', content)
    if timestamp_match:
        return timestamp_match.group(1)
    return None


def _extract_fields(content: str) -> dict[str, str | None]:
    pattern = r'(\w+)\s*:\s*([\w./\-]+)'
    matches = re.findall(pattern, content)
    result = {key.strip(): value.strip() for key, value in matches}
    return result


def _convert_diff_time(diff_time: str) -> int:
    if diff_time.endswith("ms"):
        return int(diff_time[:-2])
    return int(diff_time)


def convert_content_payload_to_metadata(content: str) -> DjiMetadata:
    dexmlified_content: str = _remove_xml_tags(content)
    time_stamp: str | None = _extract_timestamp(dexmlified_content)
    fields: dict[str, str | None] = _extract_fields(dexmlified_content)

    header = DjiMetadataHeader(
        sort_count=int(fields.get('SrtCnt')) if fields.get('SrtCnt') else None,
        diff_time=_convert_diff_time(fields.get('DiffTime')) if fields.get('DiffTime') else None,
        time_stamp=datetime.strptime(time_stamp, '%Y-%m-%d %H:%M:%S.%f') if time_stamp else None
    )
    return DjiMetadata(
        header=header,
        iso=int(fields.get('iso')) if fields.get('iso') else None,
        shutter_speed=fields.get('shutter'),
        fnum=int(fields.get('fnum')) if fields.get('fnum') else None,
        exposure_value=int(fields.get('ev')) if fields.get('ev') else None,
        color_temperature=int(fields.get('ct')) if fields.get('ct') else None,
        color_mode=fields.get('color_md'),
        focal_length=int(fields.get('focal_len')) if fields.get('focal_len') else None,
        latitude=Decimal(fields['latitude']),
        longitude=Decimal(fields['longitude']),
        relative_altitude=Decimal(fields.get('rel_alt')) if fields.get('rel_alt') else None,
        absolute_altitude=Decimal(fields.get('abs_alt')) if fields.get('abs_alt') else None
    )


def convert_srt_subtitle_to_dji_metadata(srt_subtitle: Subtitle) -> DjiMetadata:
    content: str = srt_subtitle.content
    return convert_content_payload_to_metadata(content)
