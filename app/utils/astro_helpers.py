"""
Módulo de utilidades para funções compartilhadas entre os routers da API de Astrologia.
Centraliza funções auxiliares para evitar duplicação de código e facilitar manutenção.
"""
from typing import Optional, Dict, Any, List
from kerykeion import AstrologicalSubject
from app.models import (
    NatalChartRequest, TransitRequest, PlanetPosition,
    HOUSE_SYSTEM_MAP
)

def create_subject(data: NatalChartRequest | TransitRequest, default_name: str) -> AstrologicalSubject:
    """
    Cria um objeto AstrologicalSubject a partir dos dados da requisição.
    
    Args:
        data: Dados do mapa natal ou trânsito
        default_name: Nome padrão a ser usado se não especificado
        
    Returns:
        Objeto AstrologicalSubject configurado
    """
    house_system_code = HOUSE_SYSTEM_MAP.get(data.house_system, "P")
    return AstrologicalSubject(
        name=getattr(data, 'name', default_name) or default_name,
        year=data.year,
        month=data.month,
        day=data.day,
        hour=data.hour,
        minute=data.minute,
        lng=data.longitude,
        lat=data.latitude,
        tz_str=data.tz_str,
        houses_system_identifier=house_system_code
    )

def get_planet_data(subject: AstrologicalSubject, planet_name_kerykeion: str, api_planet_name: str) -> Optional[PlanetPosition]:
    """
    Extrai dados de um planeta do objeto AstrologicalSubject.
    
    Args:
        subject: Objeto AstrologicalSubject contendo os dados do mapa
        planet_name_kerykeion: Nome do planeta no Kerykeion (ex: 'sun', 'moon')
        api_planet_name: Nome do planeta na API (ex: 'Sun', 'Moon')
        
    Returns:
        Objeto PlanetPosition com os dados do planeta ou None se não encontrado
    """
    try:
        p = getattr(subject, planet_name_kerykeion.lower())
        if p and p.name:
            return PlanetPosition(
                name=api_planet_name,
                sign=p.sign,
                sign_num=p.sign_num,
                position=round(p.position, 4),
                abs_pos=round(p.abs_pos, 4),
                house_name=p.house_name if hasattr(p, 'house_name') else "N/A",
                speed=round(p.speed, 4) if hasattr(p, 'speed') else 0.0,
                retrograde=p.retrograde if hasattr(p, 'retrograde') else False
            )
    except AttributeError:
        pass
    return None

# Constantes compartilhadas
HOUSE_NUMBER_TO_NAME_BASE = {
    1: "first", 2: "second", 3: "third", 4: "fourth",
    5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth",
    9: "ninth", 10: "tenth", 11: "eleventh", 12: "twelfth"
}

# Mapeamento de planetas comum a vários routers
PLANETS_MAP = {
    "sun": "Sun", "moon": "Moon", "mercury": "Mercury", "venus": "Venus",
    "mars": "Mars", "jupiter": "Jupiter", "saturn": "Saturn",
    "uranus": "Uranus", "neptune": "Neptune", "pluto": "Pluto",
    "mean_node": "Mean_Node", "true_node": "True_Node",
}
