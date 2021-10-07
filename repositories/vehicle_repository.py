from models.vehicle import Vehicle


class VehicleRepository:
    def __init__(self, connection) -> None:
        self._connection = connection

    def all(self):
        vehicles = []

        cursor = self._connection.cursor()

        query = """
            SELECT
                id
                , name
                , license_plate
                , registration_no
            FROM
                `vehicle`
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        for row in rows:
            vehicles.append(self.map_to_vehicle(row))

        return vehicles

    def get(self, vehicle_id: int):
        cursor = self._connection.cursor()

        query = """
            SELECT
                id
                , name
                , license_plate
                , registration_no
            FROM
                `vehicle`
            WHERE
                id = %(id)s
        """

        cursor.execute(query, {"id": vehicle_id})

        row = cursor.fetchone()

        cursor.close()

        vehicle = self.map_to_vehicle(row)

        return vehicle

    def create(self, vehicle):
        cursor = self._connection.cursor()

        query = """
            INSERT INTO
                `vehicle`
            (
                name
                , license_plate
                , registration_no
            )
            VALUES
            (
                %(name)s
                , %(license_plate)s
                , %(registration_no)s
            ) 
        """

        cursor.execute(
            query,
            {
                "name": vehicle.name,
                "license_plate": vehicle.license_plate,
                "registration_no": vehicle.registration_no,
            },
        )

        vehicle = self.get(cursor.lastlastrowid)

        cursor.close()

        return vehicle

    def update(self, vehicle):
        cursor = self._connection.cursor()

        query = """
            UPDATE
                `vehicle`
            SET
                name = %(name)s
                , license_plate = %(license_plate)s
                , registration_no = %(registration_no)s
            WHERE
                id = %(id)s 
        """

        cursor.execute(
            query,
            {
                "id": vehicle.id,
                "name": vehicle.name,
                "license_plate": vehicle.license_plate,
                "registration_no": vehicle.registration_no,
            },
        )

        cursor.close()

    def delete(self, vehicle):
        cursor = self._connection.cursor()

        query = """
            DELETE FROM
                `vehicle`
            WHERE
                id = %(id)s
        """

        cursor.execute(query, {"id": vehicle.id})

        cursor.close()

    def map_to_vehicle(self, row):
        vehicle = Vehicle()
        vehicle.id = row[0]
        vehicle.name = row[1]
        vehicle.license_plate = row[2]
        vehicle.vehicle_registration_no = row[3]

        return vehicle
