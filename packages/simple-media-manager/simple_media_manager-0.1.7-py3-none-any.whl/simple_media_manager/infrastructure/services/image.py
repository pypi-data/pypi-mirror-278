import io
import os

from PIL import Image as PillowImage
from io import BytesIO
from django.core.files import File
from django.core.files.uploadedfile import TemporaryUploadedFile


class ImageProcessingService:

    @classmethod
    def resize_image(cls, image_file: TemporaryUploadedFile, resize_percent: int) -> File:
        image = PillowImage.open(image_file)
        image_io = BytesIO()
        new_size = (
            int(image.width - image.width * (resize_percent / 100)),
            int(image.height - image.height * (resize_percent / 100))
        )
        resized_image = image.resize(new_size, resample=4)
        resized_image.save(image_io, format=image.format, quality=60, optimize=True)
        django_image = File(image_io, name=image_file.name)
        return django_image
