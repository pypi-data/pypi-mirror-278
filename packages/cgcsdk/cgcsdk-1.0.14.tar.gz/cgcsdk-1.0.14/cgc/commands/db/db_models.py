from cgc.commands.cgc_models import CGCEntityList
from cgc.commands.exceptions import DatabaseCreationException


class DatabasesList(CGCEntityList):
    """List of templates in cgc-server

    :param Enum: name of template
    :type Enum: str
    """

    POSTGRESQL = "postgresql"
    WEAVIATE = "weaviate"
    # MINIO = "minio"
    MONGODB = "mongodb"
    REDIS = "redis"

    @staticmethod
    def verify(entity: str) -> str:
        if entity == "mongodb":
            raise DatabaseCreationException(
                """
Due to license agreement we can not serve MongoDB as a single click app.
If you like to use it you can spawn one as custom image.

cgc compute create custom -n name -c 4 -m 8 --image mongo
"""
            )
        elif entity == "redis":
            raise DatabaseCreationException(
                """
Due to license agreement we can not serve Redis as a single click app.
If you like to use it you can spawn one as custom image.

cgc compute create custom -n name -c 4 -m 8 --image redis
"""
            )
