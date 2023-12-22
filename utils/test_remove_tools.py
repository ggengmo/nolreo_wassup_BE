import os
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent

# 미디어 폴더 삭제하는 함수
def remove_media_folder():
    path = os.path.join(BASE_DIR, 'media')
    shutil.rmtree(path)