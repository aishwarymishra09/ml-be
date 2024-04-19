import json

from fastapi import FastAPI, BackgroundTasks, APIRouter
from starlette import status

from src.training_scripts.executable import TrainingExecution
from src.utils.constants.properties import objs
from src.utils.data_class.data_class import TrainingData, InferenceData
from src.utils.helper.training_helper import launch_training, get_inference
from src.utils.misc.custom_helper import Response

train = APIRouter()


@train.post("/train")
async def custom_train(train_data: TrainingData, background_tasks: BackgroundTasks):
    """This function is to handle the training apis call"""
    train_data = train_data.json()
    # background_tasks.add_task(launch_training, json.loads(train_data))

    objs['training_job'].add_training_job(json.loads(train_data))
    return Response(status_code=status.HTTP_200_OK,
                    message="Training job triggered successfully",
                    data=None,
                    success=True).response()


@train.get("/inference/{id}")
async def inference(inference: InferenceData, background_tasks: BackgroundTasks):
    """This function is to handle the inference endpoint call"""
    inference_data = inference.json()
    background_tasks.add_task(get_inference, json.loads(inference_data))
    return Response(status_code=status.HTTP_200_OK,
                    message="inference invoked",
                    success=True,
                    data=None).response()

@train.get("/wait-time")
async def wait_time(background_tasks: BackgroundTasks):
    """This function is to calculate the wait time for training"""
    train_t = objs['training_job'].len_training_job()
    print(train_t)
    wait_time = train_t*5 *60
    return Response(status_code=status.HTTP_200_OK,
                    message="wait time",
                    success=True,
                    data=wait_time).response()


@train.get("/status/{id}")
async def status_call():
    """This function is to handle the inference endpoint call"""
    pass
