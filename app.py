import sys
sys.path.append("C:\\Users\\Manvir\\Documents\\Dev\\AgentsOverview")
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from src.routers.health import router as health_router
from src.routers.book import router as book_router
import uvicorn

app = FastAPI()

app.include_router(health_router)
app.include_router(book_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)