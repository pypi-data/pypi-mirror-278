import random
import string
import sys

from logger_local.LoggerLocal import Logger

from .Connector import get_connection
from .constants import OBJECT_TO_INSERT_CODE

logger = Logger.create_logger(object=OBJECT_TO_INSERT_CODE)
# after 100 times of trying to generate a random number that does not already exist in the database, raise an exception
MAX_NUMBER_OF_TRIES = 100


# TODO Shall move NumberGenerator and IdentityGenerator to database-mysql (new name database-sql) ?

class NumberGenerator:
    @staticmethod
    # TODO: Add new parameters to define new logic region: Region, entity_type: EntityType
    def get_random_number(schema_name: str, view_name: str, number_column_name: str = "number") -> int:
        logger.start(object={"schema_name": schema_name, "view_name": view_name,
                             "number_column_name": number_column_name})
        connector = get_connection()
        cursor = connector.cursor()

        random_number = None

        # Try 100 times to get a random number that does not already exist in the database
        for _ in range(MAX_NUMBER_OF_TRIES):
            random_number = random.randint(1, sys.maxsize)
            logger.info(object={f"Random {number_column_name} generated": random_number})

            query_get = (f"SELECT `{number_column_name}` FROM `{schema_name}`.`{view_name}` "
                         f"WHERE `{number_column_name}` = %s LIMIT 1")
            cursor.execute(query_get, (random_number,))
            row = cursor.fetchone()
            if not row:
                logger.info(f"{number_column_name} {random_number} does not already exist in database")
                break
            else:
                logger.info(f"{number_column_name} {random_number} already exists in database")

        if random_number is None:
            error_message = f"Could not generate a random {number_column_name} that does not already exist in the database"
            logger.error(error_message)
            logger.end(object={"error_message": error_message})
            raise Exception(error_message)
        logger.end(object={"random_number": random_number})
        return random_number

    @staticmethod
    def generate_random_string(length: int) -> str:
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(length))

    # TODO: reuse get_random_number with generator function as parameter
    @staticmethod
    def get_random_identifier(schema_name: str, view_name: str, identifier_column_name: str,
                              length: int = 20) -> str:
        logger.start(object={"schema_name": schema_name, "view_name": view_name,
                             "identifier_column_name": identifier_column_name})
        connector = get_connection()
        cursor = connector.cursor()

        random_identifier = None

        for _ in range(MAX_NUMBER_OF_TRIES):
            random_identifier = NumberGenerator.generate_random_string(length=length)
            logger.info(object={"Random identifier generated": random_identifier})

            query_get = (f"SELECT `{identifier_column_name}` FROM `{schema_name}`.`{view_name}` "
                         f"WHERE `{identifier_column_name}` = %s LIMIT 1")
            cursor.execute(query_get, (random_identifier,))
            row = cursor.fetchone()
            if not row:
                logger.info(f"Identifier {random_identifier} does not already exist in database")
                break
            else:
                logger.info(f"Identifier {random_identifier} already exists in database")

        if random_identifier is None:
            error_message = "Could not generate a random identifier that does not already exist in the database"
            logger.error(error_message)
            logger.end(object={"error_message": error_message})
            raise Exception(error_message)

        logger.end(object={"random_identifier": random_identifier})
        return random_identifier
