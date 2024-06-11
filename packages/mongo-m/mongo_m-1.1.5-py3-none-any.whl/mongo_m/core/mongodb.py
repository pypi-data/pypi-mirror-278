import pymongo


class MongoDB(pymongo.MongoClient):
    """
    Initializes a new MongoDB connection.

    Parameters:
        host (str): The host address of the MongoDB server.
        port (int): The port number of the MongoDB server.
        user (str, optional): The username for authentication. Defaults to None.
        password (str, optional): The password for authentication. Defaults to None.
    """

    # MongoDB connection
    def __init__(self, host, port, user: str = None, password: str = None):
        if user is not None and password is not None:
            uri = f"mongodb://{user}:{password}@{host}:{port}/"
        else:
            uri = f"mongodb://{host}:{port}/"
        super().__init__(uri, authSource="admin")
