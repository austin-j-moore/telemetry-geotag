import os
from pathlib import PosixPath

from src.service.video_to_image_service import VideoToImagesService

OUTPUT_DIRECTORY = os.environ['OUTPUT_DIRECTORY']
INPUT_DIRECTORY = os.environ['INPUT_DIRECTORY']

def main():
    video_and_image_service = VideoToImagesService(
        output_directory=PosixPath(OUTPUT_DIRECTORY)
    )
    video_file = PosixPath(INPUT_DIRECTORY).joinpath('DJI_0500.MP4')
    video_and_image_service.process_video(video_file)


if __name__ == '__main__':
    main()
