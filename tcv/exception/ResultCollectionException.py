class ResultCollectionException(Exception):
    message: str

    def __init__(self, *args):
        if len(args) > 0:
            self.message = str(args[0])
