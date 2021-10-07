import mysql.connector
from mysql.connector.connection import MySQLConnection

from repositories.vehicle_repository import VehicleRepository


class CarFleetUnitOfWork:
    def __init__(self, config) -> None:
        self._config = config
        self._connection = None

        # Fahrzeuge Tabelle vehicle
        self._vehicles = None

    # Erstellt die Datenbankverbindung beim Aufruf der Klasse
    def __enter__(self):
        if self._connection:
            return self

        self._connection = mysql.connector.connector(config=self._config)

        return self

    # Sobald der with Block zu ende ist wird __exit__ aufgerufen und die
    # Verbindung wird abgebaut
    def __exit__(self, ext_type, exc_value, traceback) -> None:
        self._connection.commit()

        if self._connection:
            self._connection.close()

        self._vehicles = None
        self._connection = None

    @property
    def vehicles(self):
        if self._vehicles:
            return self.vehicles

        self._vehicles = VehicleRepository(self._connection)

        return self._vehicles
