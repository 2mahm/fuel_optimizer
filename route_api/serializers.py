from rest_framework import serializers


class OptimizeRouteRequestSerializer(serializers.Serializer):
    start = serializers.ListField(
        child=serializers.FloatField(),
        min_length=2,
        max_length=2
    )
    end = serializers.ListField(
        child=serializers.FloatField(),
        min_length=2,
        max_length=2
    )

    def validate_start(self, value):
        lng, lat = value
        if not (-180 <= lng <= 180 and -90 <= lat <= 90):
            raise serializers.ValidationError(
                "Invalid longitude/latitude values for start"
            )
        return value

    def validate_end(self, value):
        lng, lat = value
        if not (-180 <= lng <= 180 and -90 <= lat <= 90):
            raise serializers.ValidationError(
                "Invalid longitude/latitude values for end"
            )
        return value
class FuelStopSerializer(serializers.Serializer):
    name = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    price_per_gallon = serializers.FloatField()


class RouteSerializer(serializers.Serializer):
    total_distance_miles = serializers.FloatField()


class OptimizeRouteResponseSerializer(serializers.Serializer):
    route = RouteSerializer()
    fuel_stops = FuelStopSerializer(many=True)
    total_fuel_cost = serializers.FloatField()
