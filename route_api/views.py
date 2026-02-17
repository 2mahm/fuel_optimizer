from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from .serializers import (
    OptimizeRouteRequestSerializer,
    OptimizeRouteResponseSerializer
)
from .services.routing_service import RoutingService
from .services.optimizer import FuelOptimizer


class OptimizeRouteView(APIView):

    def post(self, request):
        request_serializer = OptimizeRouteRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        start_coords = request_serializer.validated_data["start"]
        end_coords = request_serializer.validated_data["end"]

        cache_key = f"route_{start_coords}_{end_coords}"

        cached_response = cache.get(cache_key)
        if cached_response:
            return Response(cached_response, status=status.HTTP_200_OK)

        try:
            route = RoutingService.get_route(start_coords, end_coords)

            optimization = FuelOptimizer.optimize(
                route["distance_miles"]
            )

            response_data = {
                "route": {
                    "total_distance_miles": round(route["distance_miles"], 2)
                },
                "fuel_stops": optimization["stops"],
                "total_fuel_cost": round(optimization["total_cost"], 2)
            }

            response_serializer = OptimizeRouteResponseSerializer(data=response_data)
            response_serializer.is_valid(raise_exception=True)

            cache.set(cache_key, response_serializer.data, timeout=3600)

            return Response(response_serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
