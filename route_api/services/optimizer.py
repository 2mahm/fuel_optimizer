import math
from route_api.models import FuelStation


class FuelOptimizer:
    MAX_RANGE = 500  
    MPG = 10         

    @staticmethod
    def optimize(total_miles: float):


        if total_miles <= 0:
            return {
                "stops": [],
                "total_cost": 0
            }

        total_gallons_needed = total_miles / FuelOptimizer.MPG

        stops_needed = math.floor(total_miles / FuelOptimizer.MAX_RANGE)

        if stops_needed <= 0:

            cheapest_station = (
                FuelStation.objects
                .order_by("price_per_gallon")
                .first()
            )

            if not cheapest_station:
                raise Exception("No fuel stations available")

            total_cost = total_gallons_needed * cheapest_station.price_per_gallon

            return {
                "stops": [{
                    "name": cheapest_station.name,
                    "city": cheapest_station.city,
                    "state": cheapest_station.state,
                    "price_per_gallon": cheapest_station.price_per_gallon
                }],
                "total_cost": round(total_cost, 2)
            }

        cheapest_stations = list(
            FuelStation.objects
            .order_by("price_per_gallon")[:stops_needed]
        )

        if not cheapest_stations:
            raise Exception("No fuel stations available")

        gallons_per_full_tank = FuelOptimizer.MAX_RANGE / FuelOptimizer.MPG

        total_cost = 0
        stops = []

        for station in cheapest_stations:
            cost = gallons_per_full_tank * station.price_per_gallon
            total_cost += cost

            stops.append({
                "name": station.name,
                "city": station.city,
                "state": station.state,
                "price_per_gallon": station.price_per_gallon
            })

        remaining_miles = total_miles % FuelOptimizer.MAX_RANGE
        if remaining_miles > 0:
            remaining_gallons = remaining_miles / FuelOptimizer.MPG
            cheapest_price = cheapest_stations[0].price_per_gallon
            total_cost += remaining_gallons * cheapest_price

        return {
            "stops": stops,
            "total_cost": round(total_cost, 2)
        }
