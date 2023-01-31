from .v1.health_check import router as health_check_router
from .v1.place import router as place_router
from .v1.user import router as user_router


v1_routes = [health_check_router, user_router, place_router]

# Add v2 endpoints here:
v2_routes = []

__all__ = ["v1_routes", "v2_routes"]
