import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.training_scripts.executable import TrainingExecution
from src.utils.helper import aws_config
from src.controller.v1.training import train
from src.utils.constants.properties import objs

app = FastAPI(title="Training APIs ", version="1.0.0")
# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
@app.get("/")
async def root():
    return {"Hello": "World"}

app.include_router(train, prefix="/v1", tags=["Training"])


if __name__ == "__main__":
    try:
        import uvicorn
        objs['training_job'] = TrainingExecution()
        th = threading.Thread(target=objs['training_job'].get_training_job)
        th.start()
        uvicorn.run(app, port=8000)
    except Exception as e:
        print("###### EXCEPTION IN MAIN FILE IS {} ####### ".format(e))


