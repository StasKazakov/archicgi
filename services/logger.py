import logging
import os

os.makedirs("data", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join("data", "logs.txt"))
    ]
)

# Disable httpx default logging
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)