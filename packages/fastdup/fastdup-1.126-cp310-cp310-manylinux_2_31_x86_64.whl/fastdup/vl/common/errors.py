from fastdup.vl.common.settings import Settings

def too_many_files_error() -> str:
    return f"Error: Dataset Exceeds Maximum Image Limit ({Settings.MAX_NUM_OF_IMAGES})"

def too_little_files_error(num_images: int) -> str:
    return f'"Error: Insufficient number of valid images in dataset ({num_images}). ' \
           f'Minimum required images: {Settings.MIN_NUM_OF_IMAGES}". ' \
           f'Please note that only the following image formats are supported: {Settings.SUPPORTED_IMG_FORMATS}'