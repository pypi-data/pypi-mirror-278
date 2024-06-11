from typing import List, Type
from django.db import models
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from .choices import HttpStatus, StatusChunkUpload
from .exceptions import ChunkUploadError
from .models import ChunkUpload
from django.core.files.storage import default_storage
from django.utils.crypto import get_random_string
import os
from django.utils import timezone
import json
from django.conf import settings


class ModelClassValidator:
    def _is_django_model(self, model_class: Type[ChunkUpload]) -> bool:
        return issubclass(model_class, ChunkUpload)

    def _model_has_fields(
        self, fields: List[str], model_class: Type[ChunkUpload]
    ):
        model_fields = [field.name for field in model_class._meta.get_fields()]
        return all(field in model_fields for field in fields)


class UploadMixin(ModelClassValidator):
    MAX_BYTES = getattr(settings, 'MAX_BYTES', 1000000000)   # default = 1tb

    def _get_unique_file_name(
        self, original_name: str = 'chunk_uploads/tmp_file.mp4'
    ):
        """
        Generates a unique file name based on the original file name.

        Args:
            original_name: The original file name. Default is 'chunk_uploads/tmp_file.mp4'.

        Returns:
            str: A unique file name based on the original file name.
        """
        _, file_name = os.path.split(original_name)
        name, ext = os.path.splitext(file_name)
        unique_name = original_name

        if not default_storage.exists(unique_name):
            return f'{name}{ext}'

        while True:
            unique_name = f'{name}_{get_random_string(7)}{ext}'
            if not default_storage.exists(unique_name):
                break

        return unique_name

    def _create_default_model(
        self,
        file_fields: List[str],
        file_extensions: List[str],
        model_class: Type[ChunkUpload],
        upload_to: str,
    ):
        """
        Creates a default model instance with null file fields.

        Args:
            file_fields: List of file fields.
            file_extensions: List of file extensions corresponding to file_fields.
            model_class: The Django model class for the chunk upload.
            upload_to: The directory path where the files will be uploaded.

        Returns:
            ChunkUpload: The created default model instance.
        """
        null_files = {field: ContentFile(b'') for field in file_fields}
        for file, ext in zip(null_files.values(), file_extensions):
            print(file, ext)
            file.size = 0
            file.name = self._get_unique_file_name(
                os.path.join(upload_to, f'tmp_file.{ext}')
            ) 

        model = model_class(**null_files)
        model.save()
        return model

    def handle_chunk_upload(
        self,
        request: HttpRequest,
        file_fields: List[str],
        model_class: Type[ChunkUpload],
        upload_to: str,
    ):
        """
        Handles the upload of a chunk for a file.

        Args:
            request: The HTTP request object.
            file_fields: List of file fields to be uploaded as chunks.
            model_class: The Django model class for the chunk upload.
            upload_to: The directory path where the files will be uploaded.

        Returns:
            JsonResponse: JSON response containing the token_upload and file_hash.

        Raises:
            HttpResponse: If model_class is not a models.Model, if model_class does not have required fields,
                        if the chunk size exceeds MAX_BYTES, or if the upload token is missing or expired.
        """
        if not self._is_django_model(model_class):
            return HttpResponse(
                'model_class deve ser uma models.Model',
                status=HttpStatus.HTTP_BAD_REQUEST.value,
            )

        if not self._model_has_fields(file_fields, model_class):
            return HttpResponse(
                'model_class não possui os campos necessários',
                status=HttpStatus.HTTP_BAD_REQUEST.value,
            )

        files = {field: request.FILES.get(field) for field in file_fields}
        # chunk = request.FILES.get('file')
        token_upload = request.POST.get('token_upload')
        # file_name = request.POST.get('file_name')

        if any(
            [file.size > self.MAX_BYTES for file in files.values() if file]
        ):
            return HttpResponse(
                'O tamanho da chunk é maior que MAX BYTES',
                status=HttpStatus.HTTP_MAX_BYTES_EXCEEDED.value,
            )

        if not token_upload:
            file_extensions = json.loads(request.POST.get('file_extensions'))
            model = self._create_default_model(
                file_fields, file_extensions, model_class, upload_to
            )
            token_upload = model.token

        model = get_object_or_404(model_class, token=token_upload)

        if model.expired:
            return HttpResponse(
                'Tempo expirado', status=HttpStatus.HTTP_REQUEST_TIMEOUT.value
            )

        for field, file in files.items():
            if file:
                model.include_chunk(field, file, file.size)

        return JsonResponse(
            {'token_upload': model.token, 'file_hash': model.file_hash}
        )


class CompleteUploadMixin(ModelClassValidator):
    def handle_complete_upload(
        self,
        request: HttpRequest,
        non_file_fields: List[str],
        model_class: Type[ChunkUpload],
    ):
        """
        Handles the completion of a chunk upload process.

        Args:
            request: The HTTP request object.
            non_file_fields: List of non-file fields to be updated in the model.
            model_class: The Django model class for the chunk upload.

        Returns:
            JsonResponse: JSON response indicating the status of the chunk upload process.

        Raises:
            HttpResponse: If model_class is not a models.Model or if model_class does not have required fields.
        """

        if not self._is_django_model(model_class):
            return HttpResponse(
                'model_class deve ser uma models.Model',
                status=HttpStatus.HTTP_BAD_REQUEST.value,
            )

        if not self._model_has_fields(non_file_fields, model_class):
            return HttpResponse(
                'model_class não possui os campos necessários',
                status=HttpStatus.HTTP_BAD_REQUEST.value,
            )

        token_upload = request.POST.get('token_upload')
        total_size = request.POST.get('total_size')
        if not hasattr(model_class, 'token'):
            return HttpResponse(
                'A model_class nao possui o campo token.',
                status=HttpStatus.HTTP_UNPROCESSABLE_ENTITY.value,
            )

        model = get_object_or_404(model_class, token=token_upload)
        if model.size == int(total_size):
            model.status = StatusChunkUpload.COMPLETE
            model.user = request.user
            model.completed_on = timezone.now()
            # TODO: Realizar validação de integridade SHA256

            for field in non_file_fields:
                value = request.POST.get(field)
                setattr(model, field, value)

            model.save()
            return JsonResponse({'status': StatusChunkUpload.COMPLETE})
        return JsonResponse({'status': StatusChunkUpload.EXPIRE})
