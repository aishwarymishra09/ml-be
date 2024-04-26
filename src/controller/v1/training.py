import json
from fastapi import  BackgroundTasks, APIRouter
from starlette import status
from src.utils.constants.properties import objs, MODEL_FILE
from src.utils.data_class.data_class import TrainingData, InferenceData, InferenceSchema, InferenceCommonData
from src.utils.exceptions.custon_exceptions import FileNotFound
from src.utils.helper.custom_checks import check_model_existence, check_s3_file_exists
from src.utils.helper.training_helper import  get_inference, get_common_inference
from src.utils.misc.custom_helper import Response

train = APIRouter()


@train.post("/train")
async def custom_train(train_data: TrainingData):
    """This function is to handle the training apis call"""
    train_data = train_data.json()
    train_data = json.loads(train_data)
    if not check_s3_file_exists(train_data['s3_url']):
        raise FileNotFound(name=train_data['s3_url'], error_message="file does not exist in the file: ")
    training_time = objs['training_job'].training_st_en_time()
    objs['training_job'].add_training_job(train_data)
    return Response(status_code=status.HTTP_200_OK,
                    message="Training job triggered successfully",
                    data=training_time,
                    success=True).response()


@train.post("/concept-inference/")
async def inference(inference: InferenceData, background_tasks: BackgroundTasks):
    """This function is to handle the inference endpoint call"""
    inference_data = inference.json()
    inference_data = json.loads(inference_data)
    check_model_existence(MODEL_FILE.format(inference_data['id'], inference_data['training_id']))
    background_tasks.add_task(get_inference, inference_data)
    return Response(status_code=status.HTTP_200_OK,
                    message="inference invoked",
                    success=True,
                    data=None).response()


@train.post("/inference/")
async def common_inference(inference: InferenceCommonData, background_tasks: BackgroundTasks):
    """This function is to handle the inference endpoint call"""
    inference_data = inference.json()
    background_tasks.add_task(get_common_inference, json.loads(inference_data))
    return Response(status_code=status.HTTP_200_OK,
                    message="inference invoked",
                    success=True,
                    data=None).response()


@train.get("/wait-time")
async def wait_time():
    """This function is to calculate the wait time for training"""
    train_t = objs['training_job'].len_training_job()
    print(train_t)
    wait_time = train_t * 10 * 60
    return Response(status_code=status.HTTP_200_OK,
                    message="wait time",
                    success=True,
                    data=wait_time).response()


@train.get("/status/{id}")
async def status_call():
    """This function is to handle the inference endpoint call"""
    raise FileNotFound(name="sdfd", error_message="Status call not found")
