import json
from fastapi import APIRouter, Header
from starlette import status
from src.utils.data_class.utility_data_class import Fashion, AddBg, BgCustom
from src.utils.helper.custom_checks import decode_verification_key_sync
from src.utils.helper.utility_helper import model_cloth_swap, custom_bg
from src.utils.misc.custom_helper import Response

fashion = APIRouter()

@fashion.post("/cloth")
def swap_fashion(fashion:Fashion, verification_key: str = Header(default=...)):
    """This is used to handle the swa cloth functionality"""
    decode_verification_key_sync(encoded=verification_key)
    fashion_data = fashion.json()
    fashion_data = json.loads(fashion_data)
    remote_files = model_cloth_swap(fashion_data['id'], fashion_data['prompt'], fashion_data['model_path'],
                                    fashion_data['s3_path'])

    return Response(status_code=status.HTTP_200_OK,
                    message="cloth swapped",
                    success=True,
                    data={"id": fashion_data['id'],
                          "image_path": remote_files}).response()


@fashion.post("/background")
def swap_background(bg:AddBg, verification_key: str = Header(default=...)):
    pass

@fashion.post("/custom_background")
def swap_background(bg: BgCustom, verification_key: str = Header(default=...)):
    decode_verification_key_sync(encoded=verification_key)
    bg_data = bg.json()
    bg_data = json.loads(bg_data)
    remote_files = custom_bg(bg_data['id'], bg_data['s3_path'], bg_data['prompt'], bg_data['bg_prompt'])

    return Response(status_code=status.HTTP_200_OK,
                    message="background_generated",
                    success=True,
                    data={"id": bg_data['id'],
                          "image_path": [remote_files]}).response()




fashion.post("/pose")
def pose_change():
    pass


