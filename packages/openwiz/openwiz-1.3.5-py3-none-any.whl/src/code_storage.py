from src.logger import Logger

class CodeStorage:
    def __init__(self, logger: Logger):
        self.logger = logger

    def save_code(self, file_name, code):
        with open(file_name, "w") as f:
            f.write(code)
        print(f"\n> Code saved to {file_name}")
        self.logger.log(f"Code saved to {file_name}")
