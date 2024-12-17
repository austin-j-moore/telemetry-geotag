import os
from decimal import Decimal
from pathlib import PosixPath

from src.service.file_finder import get_mp4_files, get_base_file_name


def _build_ffmpeg_command(video_file: PosixPath, output_directory: PosixPath, fps: Decimal) -> str:
    video_file_base_name = get_base_file_name(video_file)
    escaped_video_file = str(video_file).replace(' ', '\ ')
    output_file_pattern = str(output_directory.joinpath(video_file_base_name)).replace(' ', '\ ')
    return (f'ffmpeg -i {escaped_video_file} -vf fps={str(round(fps, 1))} -qscale:v 2 '
            f'{output_file_pattern}_%04d.jpeg')


def extract_frames_from_video(video_file: PosixPath, output_directory: PosixPath, fps: Decimal) -> None:
    command = _build_ffmpeg_command(video_file, output_directory, fps)
    os.system(command)


def extract_frames_from_all_videos(video_directory: PosixPath, output_directory: PosixPath, fps: Decimal) -> None:
    for video_file in get_mp4_files(video_directory):
        extract_frames_from_video(video_file, output_directory, fps)
