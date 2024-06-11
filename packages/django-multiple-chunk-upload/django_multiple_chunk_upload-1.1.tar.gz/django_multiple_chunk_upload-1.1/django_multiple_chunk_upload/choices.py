from enum import Enum

from django.db.models import TextChoices


class StatusChunkUpload(TextChoices):
    STARTED = 'S', 'Started'
    COMPLETE = 'C', 'Complete'
    EXPIRE = 'E', 'Expire'


class HttpStatus(Enum):
    HTTP_SUCCESS_UPLOAD = 200
    HTTP_MAX_BYTES_EXCEEDED = 413
    HTTP_BAD_REQUEST = 400
    HTTP_UNPROCESSABLE_ENTITY = 422
    HTTP_REQUEST_TIMEOUT = 408
