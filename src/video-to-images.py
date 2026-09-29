import os
from pathlib import PosixPath

from src.service.file_finder import get_mp4_files
from src.service.video_to_image_service import VideoToImagesService

OUTPUT_DIRECTORY = os.environ['OUTPUT_DIRECTORY']
INPUT_DIRECTORY = os.environ['INPUT_DIRECTORY']

def main():
    video_and_image_service = VideoToImagesService(
        output_directory=PosixPath(OUTPUT_DIRECTORY)
    )
    for video_file in get_mp4_files(PosixPath(INPUT_DIRECTORY)):
        video_and_image_service.process_video(video_file)


if __name__ == '__main__':
    main()
