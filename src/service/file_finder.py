from pathlib import PosixPath


def get_srt_files(directory: PosixPath) -> list[PosixPath]:
    return [file for file in directory.iterdir() if file.suffix.lower() == '.srt']


def get_mp4_files(directory: PosixPath) -> list[PosixPath]:
    return [file for file in directory.iterdir() if file.suffix.lower() == '.mp4']

def get_frames_for_video(video_file: PosixPath, frames_directory: PosixPath) -> list[PosixPath]:
    video_file_name = video_file.stem
    return [
        file for file in frames_directory.iterdir()
        if file.suffix.lower() == '.jpeg'
           and video_file_name in file.stem
           and not file.stem.startswith('._')
    ]

def get_base_file_name(file_name: PosixPath) -> str:
    return file_name.stem


def get_subtitle_file_for_video_file(video_file: PosixPath) -> PosixPath:
    video_file_name = video_file.stem
    video_file_directory = video_file.parent
    subtitle_files = get_srt_files(video_file_directory)
    for subtitle_file in subtitle_files:
        if video_file_name.lower() in subtitle_file.stem.lower():
            return subtitle_file
    raise FileNotFoundError(f"No subtitle file found for {video_file_name=}")
