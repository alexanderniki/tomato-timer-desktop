class Logger:

    level = "DEBUG"  # I don't use it yet
    active = True

    def __init__(self):
        pass

    def _item(self, level: str, *items, **tags) -> str:
        text: str = ''

        # Get tags
        for key, value in tags.items():
            if key == 'tag':
                text += '[' + str(value) + '] '
            else:
                pass

        # Get other args
        for item in items:
            text += str(item)

        return '[' + level + '] ' + text

    def debug(self, *items, **tags):
        if self.active:
            print(self._item('DEBUG', *items, **tags))
        else:
            pass

    def info(self, *items, **tags):
        if self.active:
            print(self._item('INFO', *items, **tags))
        else:
            pass

    def warning(self, *items, **tags):
        if self.active:
            print(self._item('WARNING', *items, **tags))
        else:
            pass

    def error(self, *items, **tags):
        if self.active:
            print(self._item('ERROR', *items, **tags))
        else:
            pass

    def critical(self, *items, **tags):
        if self.active:
            print(self._item('CRITICAL', *items, **tags))
        else:
            pass


log = Logger()