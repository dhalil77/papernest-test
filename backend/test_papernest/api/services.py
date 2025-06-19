import requests
import logging
from typing import Optional, Tuple
from math import radians, cos, sin, asin, sqrt
from django.conf import settings

logger = logging.getLogger('api')

class GeocodingService:
    """Service de géocodage simple"""
    
    API_URL = "https://api-adresse.data.gouv.fr/search/"
    TIMEOUT = 10
    
    def get_coordinates(self, address: str) -> Optional[Tuple[float, float]]:
        """Récupère les coordonnées d'une adresse"""
        try:
            params = {
                "q": address.strip(),
                "limit": 1,
                "autocomplete": 0
            }
            
            response = requests.get(
                self.API_URL,
                params=params,
                timeout=self.TIMEOUT
            )
            
            if response.status_code != 200:
                logger.warning(f"Erreur API géocodage {response.status_code} pour: {address}")
                return None
            
            data = response.json()
            features = data.get("features", [])
            
            if not features:
                logger.warning(f"Aucun résultat pour: {address}")
                return None
            
            # Vérifier le score
            feature = features[0]
            score = feature.get("properties", {}).get("score", 0)
            
            if score < 0.5:
                logger.warning(f"Score trop faible ({score:.3f}) pour: {address}")
                return None
            
            coords = feature["geometry"]["coordinates"]
            logger.info(f"Géocodage de l'adresse: '{address}' -> {coords[0]:.6f}, {coords[1]:.6f}")
            return coords[0], coords[1]  # lon, lat
            
        except Exception as e:
            logger.error(f"Erreur géocodage pour '{address}': {e}")
            return None

def calcul_distance(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    R = 6371  # Rayon de la Terre en km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * asin(sqrt(a))

def calculate_coverage(lon: float, lat: float, antenna_data) -> dict:
    """Calcule la couverture réseau pour des coordonnées données"""

    ranges = getattr(settings, 'TECHNOLOGY_RANGES', {"2G": 30, "3G": 5, "4G": 10})
    coverage = {}
    
    for operator in antenna_data['Operateur'].unique():
        op = antenna_data[antenna_data['Operateur'] == operator]

        status = {"2G": False, "3G": False, "4G": False}
        
        for _, row in op.iterrows():
            try:
                distance = calcul_distance(lon, lat, row['lon'], row['lat'])
                
                for tech in ['2G', '3G', '4G']:
                    
                    if row[tech] and distance <= ranges[tech]:
                        status[tech] = True
                        
            except Exception as e:
                logger.warning(f"Erreur calcul distance: {e}")
                continue
        
        coverage[operator] = status
    
    return coverage