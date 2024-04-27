import json
from fastapi import BackgroundTasks, APIRouter
from starlette import status
from src.utils.constants.properties import objs, MODEL_FILE, job_status, REMOTE_IMAGE_FILE
from src.utils.data_class.data_class import TrainingData, InferenceData, InferenceSchema, InferenceCommonData
from src.utils.exceptions.custon_exceptions import FileNotFound
from src.utils.helper.custom_checks import check_model_existence, check_s3_file_exists
from src.utils.helper.s3_helper import create_s3_inference_file
from src.utils.helper.training_helper import get_inference, get_common_inference, launch_training
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
    # objs['training_job'].add_training_job(train_data)
    launch_training(train_data)
    return Response(status_code=status.HTTP_200_OK,
                    message="Training job triggered successfully",
                    data=training_time,
                    success=True).response()


@train.post("/concept-inference/")
def inference(inference: InferenceData):
    """This function is to handle the inference endpoint call"""
    inference_data = inference.json()
    inference_data = json.loads(inference_data)
    check_model_existence(MODEL_FILE.format(inference_data['id'], inference_data['training_id']))
    get_common_inference(inference_data)
    remote_files = create_s3_inference_file(inference_data)
    return Response(status_code=status.HTTP_200_OK,
                    message="inference invoked",
                    success=True,
                    data={"id": inference_data['id'],
                          "training_id": inference_data['training_id'],
                          "request_id": inference_data["request_id"],
                          "image_path": remote_files}).response()


@train.post("/inference/")
def common_inference(inference: InferenceCommonData):
    """This function is to handle the inference endpoint call"""
    inference_data = json.loads(inference.json())
    get_common_inference(inference_data)
    remote_files = create_s3_inference_file(inference_data)
    return Response(status_code=status.HTTP_200_OK,
                    message="inference invoked",
                    success=True,
                    data={"id": inference_data['id'],
                          "training_id": None,
                          "request_id": inference_data["request_id"],
                          "image_path": remote_files}).response()


@train.get("/wait-time")
async def wait_time():
    """This function is to calculate the wait time for training"""
    train_t = objs['training_job'].len_training_job()
    print(train_t)
    wait_time = train_t * 10
    return Response(status_code=status.HTTP_200_OK,
                    message="wait time",
                    success=True,
                    data=wait_time).response()


@train.get("/status/{training_id}")
async def status_call(training_id: str):
    """This function is to handle the inference endpoint call"""
    current_status = job_status[training_id]
    return Response(status_code=status.HTTP_200_OK,
                    message="status",
                    success=True,
                    data={"status": current_status,
                          "training_id": training_id}).response()
