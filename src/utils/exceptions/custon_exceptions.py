class MlBaseApiError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, name, error_message):
        self.name = name
        self.error_message = error_message
        super().__init__(self.name, self.error_message)


class FileNotFound(MlBaseApiError):
    pass


class FileAlreadyExists(MlBaseApiError):
    pass


class AwsAccessDenied(MlBaseApiError):
    pass


class TrainingError(MlBaseApiError):
    pass


class TrainingNotFound(MlBaseApiError):
    pass


class InferenceError(MlBaseApiError):
    pass


class ServiceError(MlBaseApiError):
    pass
