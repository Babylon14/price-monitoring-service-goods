from fastapi import FastAPI


app = FastAPI(
    title="Price Monitoring Service Goods API",
    description="FastAPI",
    version="0.1.0"
)

@app.post("/")
async def root():
    return {"message": "Hello World"}

