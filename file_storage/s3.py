"""Пакет для работы с S3 хранилищем"""
import boto3
from os.path import basename, dirname, split, join
from os import listdir

from botocore.client import Config

from .storage import Storage, FileData, EntryType


class S3(Storage):
    """S3 класс для работы с S3 хранилищем"""
    def __init__(
        self, url: str = "http://localhost:9000", key_id: str = "admin", secret_key: str = "admin"
    ) -> None:
        self._s3 = boto3.resource(
            "s3",
            endpoint_url=url,
            aws_access_key_id=key_id,
            aws_secret_access_key=secret_key,
            config=Config(signature_version="s3v4"),
        )

    def files(self, path: str) -> [FileData]:
        """files получает информацию о файлах в директории path в S3 хранилище"""
        files = []
        for file in self._s3.Bucket(path).objects.all():
            files.append(FileData(name=file.key, etype=EntryType.FILE))
        return files

    def upload(self, source: str, destination: str) -> bool:
        """upload загружает файл source в S3 хранилище"""
        filename = basename(source)
        try:
            bucket_name, path = destination.split("/", 1)
            bucket = self._s3.Bucket(bucket_name)
            if filename == "":
                for filename in listdir(source):
                    bucket.upload_file(join(source, filename), join(path, filename))
            else:
                if basename(destination) == "":
                    destination = join(destination, filename)
                bucket.upload_file(path, destination)
            return True
        except (FileNotFoundError, boto3.exceptions.botocore.exceptions.ClientError):
            return False

    def download(self, source: str, destination: str) -> bool:
        """download скачивает файл source из S3 хранилища"""
        filename = basename(source)
        try:
            bucket_name, path = source.split("/", 1)
            bucket = self._s3.Bucket(bucket_name)
            if filename == "":
                for s3_object in bucket.objects.filter(Prefix=path):
                    bucket.download_file(s3_object.key, join(destination, basename(s3_object.key)))
            else:
                if basename(destination) == "":
                    destination = join(destination, filename)
                bucket.download_file(path, destination)
            return True
        except (
            boto3.exceptions.botocore.exceptions.ClientError,
            boto3.exceptions.botocore.exceptions.ParamValidationError,
        ):
            return False