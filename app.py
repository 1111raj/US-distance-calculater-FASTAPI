# app.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import pgeocode
import math
from typing import Optional

app = FastAPI(title="ZIP Distance (Haversine)", version="1.0")

nomi = pgeocode.Nominatim("US")

class ZipPair(BaseModel):
    zip1: str
    zip2: str
    units: Optional[str] = "miles"  # "miles" or "km"

def lookup_latlon(zip_code: str):
    zip_code = (zip_code or "").strip()
    if not zip_code:
        raise HTTPException(status_code=400, detail="ZIP code is empty")
    zip5 = zip_code[:5]
    info = nomi.query_postal_code(zip5)
    # pgeocode returns NaN for missing lat/lon
    if info is None or math.isnan(info.latitude) or math.isnan(info.longitude):
        raise HTTPException(status_code=404, detail=f"ZIP code not found: {zip_code}")
    return float(info.latitude), float(info.longitude)

def haversine_km(lat1, lon1, lat2, lon2):
    # returns distance in kilometers
    rlat1, rlon1, rlat2, rlon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = rlat2 - rlat1
    dlon = rlon2 - rlon1
    a = math.sin(dlat/2)**2 + math.cos(rlat1) * math.cos(rlat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    R = 6371.0088
    return R * c

@app.post("/distance")
def distance_post(payload: ZipPair):
    lat1, lon1 = lookup_latlon(payload.zip1)
    lat2, lon2 = lookup_latlon(payload.zip2)

    km = haversine_km(lat1, lon1, lat2, lon2)
    miles = km * 0.62137119

    result = {
        "zip1": payload.zip1,
        "zip2": payload.zip2,
        "coords": {
            "zip1": {"lat": lat1, "lon": lon1},
            "zip2": {"lat": lat2, "lon": lon2}
        },
        "distance_km": round(km, 4),
        "distance_miles": round(miles, 4)
    }

    # preferred single-value field
    if (payload.units or "miles").lower() == "km":
        result["distance"] = {"value": round(km, 4), "units": "km"}
    else:
        result["distance"] = {"value": round(miles, 4), "units": "miles"}

    return result

@app.get("/distance")
def distance_get(zip1: str = Query(...), zip2: str = Query(...), units: Optional[str] = Query("miles")):
    payload = ZipPair(zip1=zip1, zip2=zip2, units=units)
    return distance_post(payload)
