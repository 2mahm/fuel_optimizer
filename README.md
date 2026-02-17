# ###################################       Fuel Optimizer API    ################################

A Django REST API that calculates optimal fuel stops and total fuel cost for long-distance routes. The service fetches driving distance from OpenRouteService, then applies local fuel-cost optimization using a dataset of ~2,000 fuel stations.



###############################################      Description       ####################################### 

Fuel Optimizer determines the cheapest fuel strategy for a trip between two coordinates. It assumes a vehicle with a 500-mile max range and 10 MPG, computes total distance via OpenRouteService, and selects the lowest-priced stations from the local database to minimize total fuel expenditure.




###############################################      Architecture Overview       ####################################### 


┌─────────────┐     POST /api/optimize-route/     ┌──────────────────┐
│   Client    │ ───────────────────────────────► │  OptimizeRouteView│
└─────────────┘                                   └────────┬─────────┘
                                                           │
                    ┌──────────────────────────────────────┼──────────────────────────────────────┐
                    │                                      │                                      │
                    ▼                                      ▼                                      ▼
           ┌────────────────┐                    ┌────────────────┐                    ┌────────────────┐
           │ Cache (1h TTL) │                    │ RoutingService │                    │ FuelOptimizer  │
           │ route_{coords} │                    │ OpenRouteService│                    │ SQLite/Stations│
           └────────────────┘                    └────────────────┘                    └────────────────┘


- **Views**: Handle HTTP, validation via serializers.
- **Services**: `RoutingService` (OpenRouteService integration), `FuelOptimizer` (cost logic).
- **Models**: `FuelStation` with indexed `price_per_gallon` for fast lookups.
- **Cache**: Optional in-memory cache; identical route requests return cached responses for 1 hour.

###############################################      Tech Stack       ####################################### 




| Component | Technology |
|-----------|------------|
| Framework | Django 6.0 |
| API | Django REST Framework |
| Database | SQLite |
| External API | OpenRouteService (Directions) |
| Data Loading | pandas, openpyxl |
| Config | python-dotenv |


###############################################      Setup Instructions       ####################################### 


### 1. Clone and Enter Project


git clone <repository-url>
cd fuel_optimizer


### 2. Create Virtual Environment


python -m venv venv
venv\Scripts\activate          



### 3. Install Dependencies


pip install -r requirements.txt



## Environment Variables

Create a `.env` file in the project root:

```env
ORS_API_KEY=your_openrouteservice_api_key
```



############################################# Database Setup #######################################

1. Apply migrations:


python manage.py migrate




## Data Loading

Place the fuel dataset (`fuel-prices-for-be-assessment.xlsx`) in the project root. It must contain columns:

- `OPIS Truckstop ID`
- `Truckstop Name`
- `Address`
- `City`
- `State`
- `Rack ID`
- `Retail Price`

Load the data:


python manage.py load_fuel_data


Expected output: `Fuel data loaded successfully`.



############################################### Running the Server ########################################


python manage.py runserver


The API is available at `http://127.0.0.1:8000/`.



###################################       API Endpoint    ######################################

### `POST /api/optimize-route/`

Computes route distance and returns optimal fuel stops and total fuel cost.



## Example Request

curl -X POST http://127.0.0.1:8000/api/optimize-route/ \
  -H "Content-Type: application/json" \
  -d '{
    "start": [-122.4194, 37.7749],
    "end": [-118.2437, 34.0522]
  }'


Coordinates are `[longitude, latitude]` (e.g., San Francisco → Los Angeles).

---

################################# Example Response ###############################


{
  "route": {
    "total_distance_miles": 382.17
  },
  "fuel_stops": [],
  "total_fuel_cost": 238.86
}


For trips exceeding 500 miles:

json
{
  "route": {
    "total_distance_miles": 1245.32
  },
  "fuel_stops": [
    {
      "name": "Station A",
      "city": "Phoenix",
      "state": "AZ",
      "price_per_gallon": 3.45
    },
    {
      "name": "Station B",
      "city": "Tucson",
      "state": "AZ",
      "price_per_gallon": 3.52
    }
  ],
  "total_fuel_cost": 1728.50
}

🧠 Optimization Strategy

1-One external routing API call.

2-Compute total gallons required (distance / 10 MPG).

3-Determine fuel stops (distance / 500 miles).

4-Select cheapest stations from local dataset.

5-Compute total cost.

6-Fuel pricing is handled locally to minimize external dependency






⚡ Performance Considerations

1-Single routing API call

2-Indexed price_per_gallon

3-Minimal response payload

4-Optional caching (1-hour TTL)

5-Local optimization (no repeated API calls)

6-Repeated identical requests are served instantly via cache






🔐 Security Considerations

1-Serializer-based input validation

2-API key stored in environment variables

3-Controlled external API usage

4-Error handling for routing failures




📈 Scalability Notes

1-For production-scale deployment:

2-Replace SQLite with PostgreSQL

3-Use Redis for distributed caching

4-Add rate limiting

5-Add structured logging

6-Consider local routing engine (OSRM)

7-Add monitoring (Sentry / Prometheus)

👨‍💻 Author

Mahmoud Mohamed Mahmoud 