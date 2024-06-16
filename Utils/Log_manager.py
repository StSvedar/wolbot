from datetime import datetime

class Log_manager:
    def __init__(self, file_name = "log.txt"):
        self.log_file = open(file_name, "w")

    def __del__(self):
        self.log("Closing log file")
        self.log_file.close()

    def log(self, message):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{time}] {message}"
        self.log_file.write(message + "\n")
        print(message)
