import re
from datetime import timedelta
from decimal import Decimal
from pathlib import Path, PosixPath


def get_frame_number_from_file(file_name: PosixPath) -> int:
    file_name = Path(file_name).name
    match = re.search(r'_(\d+)\.', file_name)
    return int(match.group(1).lstrip("0"))


def convert_frame_number_to_time(frame_number: int, fps: Decimal) -> timedelta:
    return timedelta(seconds=float(frame_number / fps))


def get_file_time(file_name: PosixPath, fps: Decimal) -> timedelta:
    file_number = get_frame_number_from_file(file_name)
    return convert_frame_number_to_time(file_number, fps)
