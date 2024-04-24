import os
import shutil
import subprocess
import sys
from typing import Dict, Any

from src.utils.constants.properties import cwd_training
from src.utils.helper.s3_helper import download_image_from_s3
from src.utils.logs.logger import logger


def download_images(s3_url, local_dir, class_dir, class_prompt):
    """download images from the cloud folder"""

    dir1 = download_image_from_s3(s3_url, local_dir)
    dir2 = make_class_images(dir1, class_dir, class_prompt)

    return dir1, dir2


def launch_training(train: Dict[str, Any]) -> None:
    """Launches the training process."""
    local_dir = os.getcwd() + f"/{train['id']}" + f"/{train['project_id']}/"
    class_dir = os.getcwd() + f"/{train['id']}" + f"/{train['project_id']}-cls/"
    #TODO: launch GPU instance to train the data

    instance_dir, class_dir = download_images(train['s3_url'], local_dir, class_dir, train['class_prompt'])
    logger.info('##### Launching training process #######')
    print(train)
    try:
        subprocess.call([sys.executable,
                         'diffusers_training_sdxl.py',
                         '--pretrained_model_name_or_path=stabilityai/stable-diffusion-xl-base-1.0',
                         f'--instance_data_dir={instance_dir}',
                         f'--class_data_dir={class_dir}',
                         f'--output_dir=./logs/cat/{train["id"]}/{train["project_id"]}',
                         '--with_prior_preservation',
                         '--real_prior',
                         '--prior_loss_weight=1.0',
                         f'--instance_prompt={train["instance_prompt"]}',
                         f'--class_prompt={train["class_prompt"]}',
                         f'--resolution={train["resolution"]}',
                         '--train_batch_size=1',
                         '--learning_rate=1e-5',
                         '--lr_warmup_steps=0',
                         '--max_train_steps=1000',
                         '--num_class_images=20',
                         '--scale_lr',
                         '--hflip',
                         f'--modifier_token={train["modifier_token"]}'],
                        cwd=cwd_training,
                        stdout=subprocess.PIPE)

    except Exception as e:
        logger.error(f"########## There are some error in launching training process, due to error:{e} #######")


def get_inference(inf: Dict[str, Any]):
    """will provide the inference results using the training unique ID """
    subprocess.call([sys.executable,
                     'diffusers_sample.py',
                     '--id={}'.format(inf['id']),
                     '--request_id={}'.format(inf['request_id']),
                     f'--delta_ckpt=/root/core/core-ml/logs/cat/{inf["id"]}/{inf["training_id"]}/delta.bin',
                     ' --ckpt=stabilityai/stable-diffusion-xl-base-1.0',
                     f'--prompt={inf["inference_schema"]["prompt"]}',
                     f'--negative_prompt={inf["inference_schema"]["negative_prompt"]}'
                     '--sdxl'],
                    cwd=cwd_training
                    )


def make_class_images(inctance_dir, class_dir, class_prompt):
    """makes the class images, from downloaded images from s3_url"""
    allowed_extensions = ('.png', '.jpg', '.jpeg')
    try:
        # Copy the entire directory and its contents recursively
        shutil.copytree(inctance_dir, class_dir)
        print("Directory copied successfully from", inctance_dir, "to", class_dir)
    except shutil.Error as e:
        # logger.info('Directory not copied. Error:', e)
        print(e)
    files = os.listdir(class_dir)
    with open(class_dir + '/images.txt', 'w') as f:
        for file in files:
            if file.endswith(allowed_extensions):
                f.write(class_dir+file + '\n')
    with open(class_dir + '/captions.txt', 'w') as f:
        for i in range(len(files)):
            f.write(class_prompt + '\n')

    return class_dir
