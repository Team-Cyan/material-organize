import logging
from utils.file_helper import FileHelper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    target: str = "20251012"
    source = FileHelper("/Users/lancer/import")
    source.extract_raw(f"/Users/lancer/materials/{target}/photo")
    source.extract_mp4(f"/Users/lancer/materials/{target}/video")
