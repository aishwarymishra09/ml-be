job_status = {}

INPROGRESS = "INPROGRESS"
COMPLETED = "COMPLETED"
FAILED = "FAILED"

REGION = "eu-north-1"
ACCESS_KEY_ID = "AKIAYS2NTZNHNDGBP3PV"
SECRET_ACCESS_KEY = "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"
objs = {}
cwd_training = '/root/core/core-ml'

QUEUE_DATA_FILE = '/root/core/core-ml/queue-data.json'
MODEL_FILE = '/root/core/core-ml/logs/cat/{}/{}'
REMOTE_IMAGE_FILE = "https://rekogniz-training-data.s3.eu-north-1.amazonaws.com/infernce-rekogniz/{}/{}/sample_{}.png"
