from pathlib import Path
from fastapi import FastAPI
from routing import RouteBuilder

ROUTES_DIR = Path(__file__).parent / "routes"
app = FastAPI()

route_builder = RouteBuilder(routes_dir=ROUTES_DIR)

# Order matters
for route, handlers in sorted(
    route_builder.routes.items(), key=lambda x: x[0], reverse=False
):
    for method, fn in handlers.items():
        getattr(app, method)(route)(fn)
