# Since these are used in the FastAPI example it might as well be async.
async def respond():
    return {"method": "get", "route": "/"}
