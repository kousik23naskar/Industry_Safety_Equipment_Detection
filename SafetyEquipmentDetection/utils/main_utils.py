import os.path
import sys
import yaml
import base64
from pathlib import Path
from SafetyEquipmentDetection.exception import AppException
from SafetyEquipmentDetection.logger import logging


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            logging.info("Read yaml file successfully")
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise AppException(e, sys) from e
    



def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(content, file)
            logging.info("Successfully write_yaml_file")

    except Exception as e:
        raise AppException(e, sys)
    



def decodeImage(imgstring, fileName):
    try:
        imgdata = base64.b64decode(imgstring)
        file_path = f"./data/{fileName}"
        with open(file_path, 'wb') as f:
            f.write(imgdata)
        logging.info(f"Image successfully saved to {file_path}")
    except Exception as e:
        raise AppException(e, sys)


def encodeImageIntoBase64(croppedImagePath):
    try:
        with open(croppedImagePath, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        logging.info(f"Image successfully encoded to base64 from {croppedImagePath}")
        return encoded_string
    except Exception as e:
        logging.error(f"Failed to encode image to base64: {e}")
        raise

def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"    
    