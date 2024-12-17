from decimal import Decimal
from pathlib import PosixPath

from srt import Subtitle

from src.client.ffmpeg_client import extract_frames_from_video
from src.model.dji_metadata import convert_dji_metadata_to_exif_tags
from src.service.exif_tools_service import set_metadata
from src.service.file_finder import get_frames_for_video, get_subtitle_file_for_video_file
from src.service.srt_subtitle_service import parse_srt_subtitle_file, find_subtitle, \
    convert_srt_subtitle_to_dji_metadata
from src.service.video_frame_service import get_file_time


class VideoToImagesService:
    fps = Decimal(1)

    def __init__(self, output_directory: PosixPath):
        self.output_directory = output_directory

    def _build_and_get_frames(self, video_path: PosixPath) -> list[PosixPath]:
        extract_frames_from_video(video_path, self.output_directory, self.fps)
        return get_frames_for_video(video_path, self.output_directory)

    def _get_frames_for_video(self, video_path: PosixPath) -> list[PosixPath]:
        return get_frames_for_video(video_path, self.output_directory)

    @staticmethod
    def _find_subtitles(video_path: PosixPath) -> list[Subtitle]:
        subtitle_file = get_subtitle_file_for_video_file(video_path)
        return parse_srt_subtitle_file(subtitle_file)

    def find_and_add_frame_metadata(self, frame: PosixPath, subtitles: list[Subtitle]):
        time_for_frame = get_file_time(frame, self.fps)
        subtitle = find_subtitle(time_for_frame, subtitles)
        frame_metadata = convert_srt_subtitle_to_dji_metadata(subtitle)
        exif_metadata = convert_dji_metadata_to_exif_tags(frame_metadata)
        set_metadata(str(frame), exif_metadata)

    def process_video(self, video_path: PosixPath, frames_exist=False):
        subtitles = self._find_subtitles(video_path)
        if frames_exist:
            frames = self._get_frames_for_video(video_path)
        else:
            frames = self._build_and_get_frames(video_path)
        for frame in frames:
            self.find_and_add_frame_metadata(frame, subtitles)
