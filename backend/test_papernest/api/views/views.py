import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from drf_yasg import openapi
from ..utils import load_antenna_data
from ..services import GeocodingService, calculate_coverage

logger = logging.getLogger("démarrage de l'api")

antenna_data = None

def get_antenna_data():
    """Récupère les données d'antennes (chargement paresseux)"""
    global antenna_data
    if antenna_data is None:
        antenna_data = load_antenna_data()
    return antenna_data

class CoverageAPIView(APIView):
    
    @swagger_auto_schema(
        operation_description="Récupère la couverture réseau 2G/3G/4G par opérateur pour des adresses données",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            additional_properties=openapi.Schema(type=openapi.TYPE_STRING),
            example={
                "id1" : "157 boulevard Mac Donald 75019 Paris",
                "id4" : "5 avenue Anatole France 75007 Paris",
                "id5" : "1 Bd de Parc, 77700 Coupvray",
                "id6" : "Place d'Armes, 78000 Versailles",
                "id7" : "17 Rue René Cassin, 51430 Bezannes",
                "id8" : "78 Le Poujol, 30125 L'Estréchure"
            },
            description="Dictionnaire avec des IDs comme clés et des adresses comme valeurs"
        ),
        responses={
            200: openapi.Response(
                "Succès",
                examples={
                    "application/json": {
                        "id1": {
                            "Orange": {"2G": True, "3G": True, "4G": True},
                            "SFR": {"2G": True, "3G": True, "4G": True},
                            "Bouygues": {"2G": True, "3G": True, "4G": False}
                        },
                        "id2": {
                            "Orange": {"2G": True, "3G": True, "4G": False},
                            "SFR": {"2G": True, "3G": False, "4G": True}
                        }
                    }
                }
            ),
            400: "Erreur de validation",
            500: "Erreur serveur"
        },
        tags=['Coverage']
    )
    def post(self, request):
        """Traite les demandes de couverture"""
        try:
            # Validation des données
            data = request.data
            if not isinstance(data, dict) or not data:
                return Response(
                    {"error": "Format invalide. Attendu: {id: adresse}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            print(data)
            logger.info(f"Traitement de {len(data)} adresses")
            
            # Services
            geocoding = GeocodingService()
            antennas = get_antenna_data()
            
            result = {}
            
            for addr_id, address in data.items():
                try:
                    # Validation adresse

                    if not isinstance(address, str) or not address.strip():
                        result[addr_id] = {"error": "Adresse invalide"}
                        continue
                    
                    # Géocodage
                    coords = geocoding.get_coordinates(address)
                    if not coords:
                        result[addr_id] = {"error": "Adresse introuvable"}
                        continue
                    
                    lon, lat = coords
                    
                    # Calcul de couverture
                    coverage = calculate_coverage(lon, lat, antennas)
                    result[addr_id] = coverage
                    
                    logger.info(f"✅ {addr_id} traité avec succès")
                    
                except Exception as e:
                    logger.error(f"Erreur traitement {addr_id}: {e}")
                    result[addr_id] = {"error": f"Erreur: {str(e)}"}
            
            return Response(result)
            
        except Exception as e:
            logger.error(f"Erreur critique: {e}")
            return Response(
                {"error": "Erreur interne du serveur"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
