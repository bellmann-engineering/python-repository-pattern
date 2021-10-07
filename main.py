from models.vehicle import Vehicle
from repositories.car_fleet_unit_of_work import CarFleetUnitOfWork


if __name__ == "__main__":
    config = {"user": "root", "password": "$up3rSecre7!", "host": "127.0.0.1"}

    # Initialisiert eine SQL Verbindung
    with CarFleetUnitOfWork(config) as uow:
        # Liste alle Fahrzeuge
        all_vehicles = uow.vehicles.all()

        # Einfahrzeug mit der Id 23 aus der Tabelle vehicles laden
        single_vehicle = uow.vehicles.get(23)

        single_vehicle.name = "Neuer Name"

        # Änderung des Namens in der Datenbank speichern
        uow.vehicles.update(single_vehicle)

        # Lösch Fahrzeug mit der Id 2315
        to_delete = uow.vehicles.get(2315)
        uow.vehicles.delete(to_delete)

        # Erstell ein neues Fahrzeug
        passat = Vehicle()
        passat.name = "VW Passat"
        passat.registration_no = "wksdj2093847dbcc1UZ"
        passat.license_plate = "WOB PA 5547"

        # Fügt das Fahrzeug in die Tabelle ein und gibt es mit der generierten
        # Id als ergebnis aus
        passat = uow.vehicles.create(passat)

    # Hier ist die Verbindung wieder geschlossen
    # Alle Änderungen wurden mit einem commit an die Datenbank gesendet
