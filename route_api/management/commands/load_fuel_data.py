import pandas as pd
import requests
import time
from django.core.management.base import BaseCommand
from route_api.models import FuelStation


def geocode_address(address, city, state):
    query = f"{address}, {city}, {state}, USA"
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }

    response = requests.get(url, params=params, headers={
        "User-Agent": "fuel-optimizer-app"
    })

    if response.status_code == 200:
        data = response.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])

    return None, None


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        df = pd.read_excel("./fuel-prices-for-be-assessment.xlsx")

        FuelStation.objects.bulk_create([
            FuelStation(
                opis_id=row["OPIS Truckstop ID"],
                name=row["Truckstop Name"],
                address=row["Address"],
                city=row["City"],
                state=row["State"],
                rack_id=row["Rack ID"],
                price_per_gallon=row["Retail Price"],
            )
            for _, row in df.iterrows()
        ])

        self.stdout.write("Fuel data loaded successfully")
