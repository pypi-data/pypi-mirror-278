from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from wgsd_flow import module1_router
import json
 
app = FastAPI()
 
app.include_router(module1_router, prefix="/module1", tags=["module1"])
 
# Example endpoint to check the generated OpenAPI specification
@app.get("/openapi.json")
async def get_openapi_spec():
    return app.openapi()
 
# Function to generate and save OpenAPI spec for each router
def save_openapi_spec(router, filename):
    temp_app = FastAPI()
    temp_app.include_router(router)
    openapi_spec = get_openapi(
        title=temp_app.title,
        version=temp_app.version,
        openapi_version=temp_app.openapi_version,
        description=temp_app.description,
        routes=temp_app.routes,
    )
    with open(filename, "w") as f:
        json.dump(openapi_spec, f, indent=2)
 
if __name__ == "__main__":
    save_openapi_spec(module1_router, "module1_openapi.json")