import logging
import os
import datetime

# Ensure logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure Logger
log_file = f"logs/app_{datetime.date.today()}.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("SistemaVentas")

def log_info(msg):
    logger.info(msg)
    print(f"[INFO] {msg}")

def log_error(msg, error=None):
    if error:
        logger.error(f"{msg}: {str(error)}", exc_info=True)
        print(f"[ERROR] {msg}: {str(error)}")
    else:
        logger.error(msg)
        print(f"[ERROR] {msg}")
