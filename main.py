import threading
from datetime import datetime
from typing import Callable

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware

from src.controller.v1.cloth_swap import fashion
from src.training_scripts.executable import TrainingExecution
from fastapi.responses import JSONResponse
from src.controller.v1.training import train
from src.utils.constants.properties import objs, ACCESS_KEY_ID, SECRET_ACCESS_KEY, keys
from src.utils.exceptions.custon_exceptions import MlBaseApiError, FileNotFound, FileAlreadyExists, AwsAccessDenied, \
    TrainingError, TrainingNotFound, InferenceError, ServiceError
from src.utils.logs.logger import logger
from src.utils.misc.aws_key_helper import decode_aws_keys

app = FastAPI(title="Training APIs ", version="1.0.0")
# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
@app.get("/health")
async def health():
    return {"status": "OK"}

app.include_router(train, prefix="/v1", tags=["Training"])
app.include_router(fashion, prefix="/v1", tags=["Utility"])

def create_exception_handler(
    status_code: int, initial_detail: str
) -> Callable[[Request, MlBaseApiError], JSONResponse]:
    detail = {"message": initial_detail}  # Using a dictionary to hold the detail

    def exception_handler(_: Request, exc: MlBaseApiError) -> JSONResponse:
        if exc.error_message:
            detail["message"] = exc.error_message

        if exc.name:
            detail["message"] = f"{detail['message']} [{exc.name}]"

        logger.error(exc)
        return JSONResponse(
            status_code=status_code, content={"detail": detail["message"]}
        )

    return exception_handler



app.add_exception_handler(
    exc_class_or_status_code=FileNotFound,
    handler=create_exception_handler(
        status.HTTP_404_NOT_FOUND, "file not exist"),
    )

app.add_exception_handler(
    exc_class_or_status_code=FileAlreadyExists,
    handler=create_exception_handler(
        status.HTTP_403_FORBIDDEN, "file already exist"),
    )

app.add_exception_handler(
    exc_class_or_status_code=AwsAccessDenied,
    handler=create_exception_handler(
        status.HTTP_400_BAD_REQUEST, "aws connection denied"),
    )

app.add_exception_handler(
    exc_class_or_status_code=TrainingError,
    handler=create_exception_handler(
        status.HTTP_500_INTERNAL_SERVER_ERROR, "Training not ran properly"),
)

app.add_exception_handler(
    exc_class_or_status_code=TrainingNotFound,
    handler=create_exception_handler(
        status.HTTP_404_NOT_FOUND, "training not found"),
)

app.add_exception_handler(
    exc_class_or_status_code=InferenceError,
    handler=create_exception_handler(
        status.HTTP_400_BAD_REQUEST, "Inference not ran properly"),
)

app.add_exception_handler(
    exc_class_or_status_code=ServiceError,
    handler=create_exception_handler(
        status.HTTP_400_BAD_REQUEST, "service error"),
)


@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    # modify response adding custom headers
    execution_time = (datetime.utcnow() - start_time).microseconds
    print(execution_time)
    response.headers["x-execution-time"] = str(execution_time)
    return response


if __name__ == "__main__":
    try:
        import uvicorn

        keys["ACCESS_KEY_ID"], keys["SECRET_ACCESS_KEY"] = decode_aws_keys(ACCESS_KEY_ID, SECRET_ACCESS_KEY)
        objs['training_job'] = TrainingExecution()
        th_train = threading.Thread(target=objs['training_job'].get_training_job)
        th_cache = threading.Thread(target=objs['training_job'].save_queue_data)
        th_train.start()
        th_cache.start()
        uvicorn.run(app,host="0.0.0.0", port=8002,  timeout_keep_alive=240, timeout_graceful_shutdown=240)
    except Exception as e:
        print("###### EXCEPTION IN MAIN FILE IS {} ####### ".format(e))


