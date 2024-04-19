import queue

from src.utils.helper.training_helper import launch_training


class TrainingExecution:
    def __init__(self):
        self.training_que = queue.Queue()

    def add_training_job(self, training_job):
        """This method adds a training job to the queue."""
        print(f"#### training job added in the queue with length {self.training_que.qsize()} #####")

        self.training_que.put(training_job)

    def get_training_job(self):
        """This method starts a training job."""
        print("#### training job function invoked #####")
        while True:
            if not self.training_que.empty():
                training_job = self.training_que.get()
                print(training_job)
                self._start_training_job(training_job)

    def _start_training_job(self, data):
        """This method starts a training job."""
        launch_training(data)

    def len_training_job(self):
        """This method returns the length of the queue."""
        print(self.training_que.qsize())
        return self.training_que.qsize()
