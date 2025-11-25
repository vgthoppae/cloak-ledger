import logging
import os

class CloakLogger:
  def __init__(self, console_log=True):
    self.desc = "Cloak Loagger"
    self.console_log = console_log

  def configure(self):
    # Clean up any previous logs
    for log_file in ["logger.log", "web.log", "tunnel.log", "app.log"]:
      if os.path.exists(log_file):
        os.remove(log_file)
        print(f"🧹 Cleaned up {log_file}")

    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # --- File Handler ---
    file_handler = logging.FileHandler("logger.log")
    file_handler.setLevel(logging.DEBUG)

    # --- Formatter (shared) ---
    formatter = logging.Formatter("%(filename)s:%(lineno)s %(levelname)s:%(message)s")
    file_handler.setFormatter(formatter)

    # --- Console Handler ---
    if self.console_log:
      console_handler = logging.StreamHandler()
      console_handler.setLevel(logging.DEBUG)
      console_handler.setFormatter(formatter)

    # --- Add handlers to logger ---
    logger.addHandler(file_handler)

    # --- Console Handler ---
    if self.console_log:
      logger.addHandler(console_handler)
      logger.info("This goes to both the file and the console!")
    else:
      logger.info("This goes to only the file")

    print("✅ Logging configured")
