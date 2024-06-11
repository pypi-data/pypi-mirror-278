from django.db import models
from secrets import token_urlsafe
from math import ceil
from .choices import StatusChunkUpload, HttpStatus
from hashlib import sha256
from django.core.files.base import ContentFile
from pathlib import Path
from django.core.files.storage import default_storage
from io import BytesIO
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

user = get_user_model()


def max_len_token_url_safe(nbytes):
    return ceil(((4 * nbytes) / 3) + 1)


LEN_TOKEN = 15


class ChunkUpload(models.Model):
    """
    Model representing a chunk upload process.

    Attributes:
        user: ForeignKey to the user who initiated the upload.
        token: Unique token for the upload process.
        size: Total size of the uploaded file.
        status: Current status of the upload process.
        file_hash: Hash of the uploaded file for integrity verification.
        completed_on: Date and time when the upload process was completed.
        created_at: Date and time when the upload process was initiated.

    Methods:
        save: Saves the instance and generates a token if not provided.
        include_chunk: Appends a chunk of bytes to the file field.
        expire_in: Property returning the expiration time of the upload process.
        expired: Property indicating if the upload process has expired.
    """

    user = models.ForeignKey(
        user, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    token = models.CharField(
        max_length=max_len_token_url_safe(LEN_TOKEN), unique=True
    )
    # file = models.FileField(upload_to='chunk_uploads')
    size = models.IntegerField(default=0)
    status = models.CharField(
        max_length=1,
        choices=StatusChunkUpload.choices,
        default=StatusChunkUpload.STARTED,
    )
    file_hash = models.CharField(max_length=64, null=True, blank=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = token_urlsafe(LEN_TOKEN)

        super(ChunkUpload, self).save(*args, **kwargs)

    def include_chunk(
        self,
        field_name: str,
        bytes: bytes,
        chunk_size: int = 0,
        last_chunk: bool = False,
    ):
        if not hasattr(self, field_name):
            raise ValueError(
                f'O campo {field_name} não existe na model {self.__class__.__name__}'
            )

        file = getattr(self, field_name)

        existing_content = BytesIO()
        with default_storage.open(file.name, 'rb') as existing_file:
            existing_content.write(existing_file.read())

        for chunk in bytes.chunks(chunk_size):
            existing_content.write(chunk)

        with default_storage.open(file.name, 'wb') as destination:
            destination.write(existing_content.getvalue())

        self.size += chunk_size

        if last_chunk:
            sha256_hash = (
                sha256()
            )   # SHA256 garante maior integridade, se preferir performance usar md5
            for chunk in file.chunks():
                sha256_hash = sha256.update(chunk)
            self.file_hash = sha256_hash.hexdigest()

        self.save()

    @property
    def expire_in(self):
        return self.created_at + timedelta(days=1)

    @property
    def expired(self):
        return self.expire_in <= timezone.now()

    class Meta:
        abstract = True
