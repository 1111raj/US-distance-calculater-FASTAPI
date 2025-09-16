# ZIP Distance API (FastAPI)

A simple **FastAPI** service that calculates the distance between two US ZIP codes using the **Haversine formula** and `pgeocode`.

---

## Features
- Get the latitude and longitude for US ZIP codes.
- Calculate distances between two ZIP codes.
- Supports **miles** and **kilometers**.
- Exposes both **POST** and **GET** endpoints.

---

## Requirements
- Python 3.9+
- Dependencies listed in `requirements.txt`:
  - `fastapi`
  - `uvicorn`
  - `pgeocode`

Install dependencies:

```bash
pip install -r requirements.txt
