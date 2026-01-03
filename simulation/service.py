from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import joblib
import pandas as pd

from .schemas import RoomInput, RoomOutput

router = APIRouter(tags=['ML Simuation'])

try:
    clf = joblib.load(os.path.join(os.path.dirname(__file__), 'models', 'rf_model.pkl'))
    le = joblib.load(os.path.join(os.path.dirname(__file__), 'models', 'label_encoder.pkl'))
    metrics_map = joblib.load(os.path.join(os.path.dirname(__file__), 'models', 'status_metrics_map.pkl'))
    print("✅ Models loaded successfully!")
except FileNotFoundError as e:
    print(f"❌ Error: {e}")
    print("Run training first: python 06_training.py")
    raise


@router.get("/status")
def health_check():
    """Health check"""
    return {
        "message": "ML Simulation",
        "status": "aman bro",
    }

@router.post("/ml_simulation", response_model=RoomOutput)
def simulation_predict(room: RoomInput):
    """
    Prediksi status ruangan

    Input: occupancy, temp, hum, lux, noise, luas
    Output: status, pmv, ppd, energy_kwh
    """
    try:

        input_data = pd.DataFrame([{
            'occupancy': room.occupancy,
            'temp': room.temp,
            'hum': room.hum,
            'lux': room.lux,
            'noise': room.noise,
            'luas': room.luas
        }])

        
        status_encoded = clf.predict(input_data)[0]
        status = le.inverse_transform([status_encoded])[0]


        metrics = metrics_map[status]

        return RoomOutput(
            status=status,
            pmv=round(metrics['pmv_mean'], 2),
            ppd=round(metrics['ppd_mean'], 2),
            energy_kwh=round(metrics['kwh_mean'], 4)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
