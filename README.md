# Einfaches Python MySQL Repository Pattern

## Ordner- und Dateistruktur

### Benennung der Tabellen und Klassen

Weit verbreitet ist die Benennung von Tabellen und Klassen im Singular.
In Python werden alle Eigenschaften einer Klasse immer klein geschrieben.
Es bietet sich daher an die Tabellenspalten im Datenbankserver ebenfalls so
zu schreiben. Damit erhält man eine einfache Zuordnung und Übersicht zwsichen
Tabelle und Klasse.

> _Ob die Tabellen und Klassen deutsche oder englische Namen erhalten spielt hier
keine Rolle. Es sollte nur im gesamten Programm einheitlich sein._

### Beispiel Fahrzeuge

Die Tabelle die für die Fahrzeuge zuständig ist erhält den Namen `fahrzeug` oder
`vehicle`. Die Klasse im Ordner `models` erhällt dann den Namen `fahrzeug.py` oder 
`vehicle.py`.

`vehicle`:
```sql
CREATE TABLE `vehicle` (
    `id` INT PRIMARY KEY AUTO_INCREMENT
    , `name` NVARCHAR(250) NOT NULL
    , `license_plate` NVARCHAR(30) NOT NULL
    , `registration_no` NVARCHAR(MAX) NOT NULL
)
```

`models/vehicle.py`:
```py
class Vehicle:
    def __init__(self) -> None:
        self.id = None
        self.name = ""
        self.license_plate = ""
        self.registration_no = ""
```

### Models

Alle Klassen für die Tabellen in der Datenbank. Gängige Praxis ist eine Klasse
je Tabelle zu haben.

Diese Models sind reine Daten Objekte. Die gesamte Logik um dieses Model herum 
wird in anderen Klassen und Funktionen ausgelagert.

In einigen Fällen enthalten diese Models die Validierungslogik für die einzelnen
Properties.

### Repository

Ein Repository ist eine Klasse die alle notwendigen Methoden enthält um ein 
Model nach den gestellten Anforderungen aus der Datenbank zu lesen, schreiben,
bearbeiten oder zu löschen. Umgangssprachlich nennt man das CRUD (Create, 
Read, Update, Delete).

Diese Klasse erhalt eine bereits konfigurierte Datenbankverbindung als 
`__init__` Parameter. Diese Datenbankverbindung wird in der `Unit of Work`
aufgebaut.

`vehicle_repository.py`:
```py
class VehicleRepository:
    def __init__(self, connection):
        self._connection = connection
```

### Unit of Work

Eine `Unit of Work` ermöglicht das Zusammenfassen mehrer Repositories. Diese 
Klasse organisiert die notwendige Verbindung zur Datenquelle. In unserem Fall
ist die eine SQL Verbindung. Es kann sich hierbei aber auch um eine Netzwerkverbindung zu einem Datenspeicher handeln oder einer anderen Art von 
Datenquelle.

Im Regelfall benötigt man zum Verarbeiten von Anfragen mehr als eine Tabelle um
die gewünschten Antworten wieder an den Benutzer zu senden.

So gibt es zum Beispiel Fahrer, Autos, Fahrentenbücher, Werkstatthistorie und 
weitere Daten die zu einem Auto in einem Fuhrpark gehören.

Um sich das manuelle Aufbauen und Schließen der Verbindung zu ersparen wird 
eine `Unit of Work` immer `__enter__` und `__exit__` implementiert. Dies ist 
die Implementierung eines sogenannten Kontext. So einen Kontext wird mit `with` 
aufgerufen. Dies macht man auch wenn man mit Dateien arbeitet.


```py
with open('no_content.txt') as file:
    # do something with the file
```

Diese Methoden ermöglichen das automatische Öffnen und Schließen der Verbindung
bei Initialisierung der Klasse. So erhält man ein autmatische 
Resourcenverwaltung die einem das Leben erleichtert. 

`repositories/car_fleet_unit_of_work.py`:
```py
class CarFleetUnitOfWork:
    def __init__(self, connection_string: string) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback) -> None:
        pass
```

`main.py`:
```py
from repositories.car_fleet_unit_of_work import CarFleetUnitOfWork


if __name__ == "__main__":
    config = {"user": "root", "password": "$up3rSecre7!", "host": "127.0.0.1"}

    with CarFleetUnitOfWork(config) as uow:
        all_vehicles = uow.vehicles.all()

        single_vehicle = uow.vehicles.get(23)
```