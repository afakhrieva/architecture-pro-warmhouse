МАППИНГ API МОНОЛИТА -> НОВЫЕ СЕРВИСЫ
```
    1. GET /api/v1/sensors
       → GET /api/devices?type=sensor
       
    2. GET /api/v1/sensors/:id
       → GET /api/devices/{id}
       
    3. POST /api/v1/sensors
       → POST /api/devices
         {
           "name": "...",
           "type": "sensor",
           "homeId": ...,
           "capabilities": ["temperature"]
         }
       
    4. PUT /api/v1/sensors/:id
       → PATCH /api/devices/{id}
       
    5. DELETE /api/v1/sensors/:id
       → DELETE /api/devices/{id}
       
    6. PATCH /api/v1/sensors/:id/value
       → POST /api/devices/{id}/commands
         {
           "type": "set_value",
           "params": {"value": ...}
         }
       → Также сохраняем в Telemetry Service:
         POST /api/telemetry/{id}/temperature
    */
}
```