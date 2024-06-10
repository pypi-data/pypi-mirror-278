class Data:
    def __init__(self, columns):
        self.columns = columns

    def __repr__(self):
        return f"{self.__class__.__name__} [{', '.join(self.columns)}]"

    def select(self, columns):
        return Data(columns=columns)
