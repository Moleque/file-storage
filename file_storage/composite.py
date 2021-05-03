"""Класс для композиции Storage"""
from .storage import Storage, FileData


class StorageComposite(Storage):
    """StorageComposite позволяет создавать композицию Storage"""
    def __init__(self) -> None:
        self._storages: [Storage] = []

    def add(self, storage: Storage) -> None:
        """add добавляет новый Storage"""
        self._storages.append(storage)

    def remove(self, storage: Storage) -> None:
        """remove удаляет существующий Storage"""
        self._storages.remove(storage)

    def files(self, path: str) -> [FileData]:
        """files возвращает список файлов из всех Storage"""
        files = []
        for storage in self._storages:
            files.append(storage.files(path))
        return files

    def upload(self, source: str, destination: str) -> bool:
        """
        upload загружает файл source во все Storage
        возвращает True если запись была произведена во все Storage
        """
        uploaded = True
        for storage in self._storages:
            if not storage.upload(source, destination):
                uploaded = False
        return uploaded

    def download(self, source: str, destination: str) -> bool:
        """
        download скачивает файл source из всех Storage
        возвращает True если файл был скачан хотя бы из одного Storage
        """
        downloaded = False
        for storage in self._storages:
            if storage.download(source, destination):
                downloaded = True
        return downloaded
