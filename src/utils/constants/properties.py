job_status = {}

INPROGRESS = "INPROGRESS"
COMPLETED = "COMPLETED"
FAILED = "FAILED"

REGION = "eu-north-1"
keys = {}
ACCESS_KEY_ID_encoded = "EPOHa\<RY`UPVcGP:]]W"
SECRET_ACCESS_KEY_encoded = "RRhxnzLo[y;v~LlTq>:u|MJ|pmKl5=lAoUyl"

ACCESS_KEY_ID = keys["ACCESS_KEY_ID"]
SECRET_ACCESS_KEY = keys["SECRET_ACCESS_KEY"]
objs = {}
cwd_training = '/root/core/core-ml'

QUEUE_DATA_FILE = '/root/core/core-ml/queue-data.json'
MODEL_FILE = '/root/core/core-ml/logs/cat/{}/{}'
REMOTE_IMAGE_FILE = "https://rekogniz-training-data.s3.ap-south-1.amazonaws.com/infernce-rekogniz/{}/{}/sample_{}.png"


GARMENT = "garment"
MODEL = "model"