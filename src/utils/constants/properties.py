job_status = {}

INPROGRESS = "INPROGRESS"
COMPLETED = "COMPLETED"
FAILED = "FAILED"

REGION = "eu-north-1"
ACCESS_KEY_ID = "AKIAYS2NTZNHMYCK4VUN"
SECRET_ACCESS_KEY = "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"
objs = {}
cwd_training = '/root/core/core-ml'

QUEUE_DATA_FILE = '/root/core/core-ml/queue-data.json'
MODEL_FILE = '/root/core/core-ml/logs/cat/{}/{}'
REMOTE_IMAGE_FILE = "https://rekogniz-training-data.s3.ap-south-1.amazonaws.com/infernce-rekogniz/{}/{}/sample_{}.png"
