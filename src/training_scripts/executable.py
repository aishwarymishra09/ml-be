import os
import pickle
import queue
import shutil
import time
from datetime import datetime, timedelta
from datetime import datetime
from pytz import timezone

from src.utils.constants.properties import QUEUE_DATA_FILE, job_status, INPROGRESS, COMPLETED
from src.utils.exceptions.custon_exceptions import ServiceError
from src.utils.helper.training_helper import launch_training
from src.utils.logs.logger import logger


class TrainingExecution:
    def __init__(self):
        try:
            with open(QUEUE_DATA_FILE, "rb") as f:
                l = pickle.load(f)
                q = queue.Queue()
                for i in l:
                    q.put(i)
                self.training_que = q
        except (FileNotFoundError, EOFError):

            self.training_que = queue.Queue()

    def add_training_job(self, training_job):
        """This method adds a training job to the queue."""
        logger.info(f"#### training job added in the queue with length {self.training_que.qsize()} #####")
        try:
            self.training_que.put(training_job)
        except Exception as e:
            raise ServiceError(name="queue failed", error_message="Queuing job failed : {}".format(e))

    def get_training_job(self):
        """This method starts a training job."""
        logger.info("#### training job function invoked #####")
        while True:
            if not self.training_que.empty():
                training_job = self.training_que.get()
                self._start_training_job(training_job)
                shutil.rmtree(os.getcwd() + f"/{training_job['id']}")
                logger.info("#### directory removed {} #####".format((os.getcwd() + f"/{training_job['id']}")))

    def _start_training_job(self, data):
        """This method starts a training job."""
        job_status[data["training_id"]] = INPROGRESS
        launch_training(data)
        job_status[data["training_id"]] = COMPLETED

    def len_training_job(self):
        """This method returns the length of the queue."""
        return self.training_que.qsize()

    def training_st_en_time(self):
        """This method starts a training job."""
        now = datetime.now(timezone("Asia/Kolkata")) + timedelta(minutes=self.len_training_job() * 1)
        now_plus_10 = now + timedelta(minutes=10)
        return {"start_time": now, "end_time": now_plus_10}

    def save_queue_data(self):
        # Serialize and save the queue contents
        while True:
            if not self.training_que.empty():
                with open(QUEUE_DATA_FILE, "wb") as f:
                    pickle.dump(list(self.training_que.queue), f)
            time.sleep(300)
