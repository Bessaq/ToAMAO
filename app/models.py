from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

# Modelos existentes (mantidos para referência)
class HouseSystem(str, Enum):
    PLACIDUS = "placidus"
    KOCH = "koch"
    REGIOMONTANUS = "regiomontanus"
    CAMPANUS = "campanus"
    EQUAL = "equal"
    WHOLE_SIGN = "whole_sign"
    
# Mapeamento de sistemas de casas para identificadores do Kerykeion
HOUSE_SYSTEM_MAP = {
    "placidus": "P",
    "koch": "K",
    "regiomontanus": "R",
    "campanus": "C",
    "equal": "E",
    "whole_sign": "W"
}

class PlanetPosition(BaseModel):
    name: str
    sign: str
    sign_num: int
    position: float
    abs_pos: float
    house_name: str
    speed: float = 0.0
    retrograde: bool = False

class NatalChartRequest(BaseModel):
    name: Optional[str] = Field(None, description="Nome da pessoa ou evento")
    year: int = Field(..., description="Ano de nascimento")
    month: int = Field(..., description="Mês de nascimento (1-12)")
    day: int = Field(..., description="Dia de nascimento (1-31)")
    hour: int = Field(..., description="Hora de nascimento (0-23)")
    minute: int = Field(..., description="Minuto de nascimento (0-59)")
    latitude: float = Field(..., description="Latitude do local de nascimento")
    longitude: float = Field(..., description="Longitude do local de nascimento")
    tz_str: str = Field(..., description="String de fuso horário (ex: 'America/Sao_Paulo')")
    house_system: HouseSystem = Field(HouseSystem.PLACIDUS, description="Sistema de casas a ser usado")

class TransitRequest(BaseModel):
    year: int = Field(..., description="Ano do trânsito")
    month: int = Field(..., description="Mês do trânsito (1-12)")
    day: int = Field(..., description="Dia do trânsito (1-31)")
    hour: int = Field(..., description="Hora do trânsito (0-23)")
    minute: int = Field(..., description="Minuto do trânsito (0-59)")
    latitude: float = Field(..., description="Latitude do local para cálculo do trânsito")
    longitude: float = Field(..., description="Longitude do local para cálculo do trânsito")
    tz_str: str = Field(..., description="String de fuso horário (ex: 'America/Sao_Paulo')")
    house_system: HouseSystem = Field(HouseSystem.PLACIDUS, description="Sistema de casas a ser usado")
    name: Optional[str] = Field(None, description="Nome opcional para o trânsito (ex: 'Trânsitos 2025')")

# Novo modelo para requisição de SVG combinado
class SVGCombinedChartRequest(BaseModel):
    """
    Modelo para requisição de gráfico SVG combinado de mapa natal e trânsitos.
    """
    natal_chart: NatalChartRequest = Field(..., description="Dados do mapa natal")
    transit_chart: TransitRequest = Field(..., description="Dados do trânsito")
    
    class Config:
        schema_extra = {
            "example": {
                "natal_chart": {
                    "name": "João",
                    "year": 1997,
                    "month": 10,
                    "day": 13,
                    "hour": 22,
                    "minute": 0,
                    "latitude": -3.7172,
                    "longitude": -38.5247,
                    "tz_str": "America/Fortaleza",
                    "house_system": "placidus"
                },
                "transit_chart": {
                    "name": "Trânsitos 2025",
                    "year": 2025,
                    "month": 6,
                    "day": 2,
                    "hour": 12,
                    "minute": 0,
                    "latitude": -3.7172,
                    "longitude": -38.5247,
                    "tz_str": "America/Fortaleza",
                    "house_system": "placidus"
                }
            }
        }
