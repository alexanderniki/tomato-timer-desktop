class Logger:

    level = "DEBUG"
    active = True

    def __init__(self):
        pass

    def debug(self, *items):
        text = ""
        for item in items:
            text += str(item) + " "
        print("[DEBUG] " + text)

    def info(self, *items):
        text = ""
        for item in items:
            text += str(item) + " "
        print("[INFO] " + text)

    def warning(self, *items):
        text = ""
        for item in items:
            text += str(item) + " "
        print("[WARNING] " + text)

    def error(self, *items):
        text = ""
        for item in items:
            text += str(item) + " "
        print("[ERROR] " + text)

    def critical(self, *items):
        text = ""
        for item in items:
            text += str(item) + " "
        print("[CRITICAL] " + text)


log = Logger()