from pydantic import BaseModel, Field

class RoomInput(BaseModel):
    """Input data sensor"""
    occupancy: int = Field(..., ge=0)
    temp: float = Field(..., ge=15.0, le=35.0)
    hum: float = Field(..., ge=20.0, le=90.0)
    lux: float = Field(..., ge=0.0)
    noise: float = Field(..., ge=0.0)
    luas: float = Field(176.0, description="Luas ruangan (m²)")

    class Config:
        json_schema_extra = {
            "example": {
                "occupancy": 15,
                "temp": 24.5,
                "hum": 55.0,
                "lux": 400.0,
                "noise": 45.0,
                "luas": 176.0
            }
        }

class RoomOutput(BaseModel):
    """Output prediksi"""
    status: str
    pmv: float
    ppd: float
    energy_kwh: float
