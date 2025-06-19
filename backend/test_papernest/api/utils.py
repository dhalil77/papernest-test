import pandas as pd
import logging
from pyproj import Transformer
from django.conf import settings
from pathlib import Path

logger = logging.getLogger('api')

def load_antenna_data():
    """Charge et transforme les données"""

    df = pd.read_csv( getattr(settings, 'COVERAGE_CSV_PATH', None), sep=',')

    # Convertir les coord Lambert93 -> GPS
    transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True)
    
    def convert_coords(row):
        try:
            return transformer.transform(row['x'], row['y'])
        except:
            return None, None
    
    coords = df.apply(convert_coords, axis=1, result_type='expand')
    df[['lon', 'lat']] = coords
    
    # Nettoyer les données
    df = df.dropna(subset=['lon', 'lat'])

    # Convertir les colonnes technologiques en booléens
    for tech in ['2G', '3G', '4G']:
        df[tech] = df[tech].astype(str).str.lower().isin(['true', '1', 'oui'])
    
    logger.info(f"Données chargées: {len(df)} antennes")

    return df
        
