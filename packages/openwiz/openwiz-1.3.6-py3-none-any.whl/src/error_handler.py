from src.logger import Logger

class ErrorHandler:
    def __init__(self, logger: Logger):
        self.logger = logger

    def handle(self, error):
        self.logger.log(f"Error: {error}")
        print(f"An error occurred: {error}")
