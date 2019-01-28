class InitialDataException(Exception):
    def __init__(self):

        super().__init__("Error getting initial Data")
