import requests
from django.conf import settings


class RoutingService:

    @staticmethod
    def get_route(start, end):
        api_key = getattr(settings, "ORS_API_KEY", None)

        if not api_key:
            raise Exception(
                "ORS_API_KEY is not set. Get a free key at "
                "https://openrouteservice.org/dev/#/signup and add it to your .env"
            )

        url = "https://api.openrouteservice.org/v2/directions/driving-car"

        body = {
            "coordinates": [
                start,
                end
            ],
            "instructions": False,          
            "geometry_simplify": True       
        }

        response = requests.post(
            url,
            headers={
                "Authorization": api_key,
                "Content-Type": "application/json"
            },
            json=body,
            timeout=10
        )

        if response.status_code != 200:
            raise Exception(response.text)

        data = response.json()

        if "routes" not in data:
            raise Exception(f"Routing API error: {data}")

        route = data["routes"][0]

        distance_meters = route["summary"]["distance"]
        geometry = route.get("geometry")  

        distance_miles = distance_meters * 0.000621371

        return {
            "distance_miles": distance_miles,
            "geometry": geometry
        }
