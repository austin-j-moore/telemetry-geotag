import exiftool


def get_metadata(image_path: str) -> dict:
    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(image_path)
    return metadata[0]


def set_metadata(image_path: str, new_metadata: dict):
    with exiftool.ExifToolHelper() as et:
        et.set_tags(image_path, new_metadata)

