import asyncio
from .config import Config
from .uploader_service import UploaderService

def upload_folder(config: Config, folder_path: str, include_folder: bool = False, parent_folder_name: str = None, skip_extensions: list[str] = ['.log']):
    try:
        uploader_service = UploaderService(config)
        asyncio.run(uploader_service.upload_folder(folder_path, include_folder, parent_folder_name, skip_extensions))
    except Exception as e:
        print("An error occurred during the upload Folder:", str(e))