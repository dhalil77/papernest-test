import asyncio
import logging
from django.utils.decorators import sync_and_async_middleware

logger = logging.getLogger(__name__)

@sync_and_async_middleware
def async_coverage_middleware(get_response):
    """Middleware pour supporter les vues async dans Django"""
    
    async def async_middleware(request):
        # Pré-traitement async si nécessaire
        logger.debug(f"Traitement async de la requête: {request.path}")
        response = await get_response(request)
        # Post-traitement async si nécessaire
        return response
    
    def sync_middleware(request):
        # Version synchrone du middleware
        logger.debug(f"Traitement sync de la requête: {request.path}")
        response = get_response(request)
        return response
    
    # Retourner la version appropriée selon le type de vue
    if asyncio.iscoroutinefunction(get_response):
        return async_middleware
    else:
        return sync_middleware