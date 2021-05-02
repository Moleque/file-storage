"""Пакет для работы с ftp-сервером"""
from ftplib import FTP, Error
from datetime import datetime

from .storage import Storage, FileData, EntryType


class FtpServer(Storage):
    """FtpServer класс взаимодействия с ftp-сервером"""
    def __init__(self, host: str, user: str, password: str) -> None:
        self._ftp = None
        self._host = host
        self._user = user
        self._password = password

    def _connect(self) -> bool:
        """_connect подключает к ftp-серверу"""
        self._ftp = FTP(self._host)
        try:
            if self._ftp.login(self._user, self._password) != "230 Login successful.":
                return False
            return True
        except Error:
            return False

    def _disconnect(self) -> None:
        """_disconnect отключает от ftp-сервера"""
        if self._ftp is not None:
            try:
                self._ftp.quit()
            except Error:
                self._ftp.close()
        self._ftp = None

    @staticmethod
    def _decode_file_data(data: str) -> dict:
        """_decode_file_data декодирует данные о файлах на ftp-сервере"""
        fields = data.split()
        return {
            "type": EntryType.FOLDER if fields[0] == "d" else EntryType.FILE,
            "size": int(fields[4]),
            "name": fields[-1],
            "time": datetime(   # время изменения
                year=datetime.now().year,
                month=datetime.strptime(fields[5], "%b").month,
                day=int(fields[6]),
                hour=int(fields[7].split(":")[0]),
                minute=int(fields[7].split(":")[-1]),
            ),
        }

    def files(self, path: str) -> []:
        """files получает информацию о файлах в директории path на ftp-сервера"""
        files = []
        if not self._connect():
            return files
        try:
            notes = []
            self._ftp.cwd(path)
            self._ftp.retrlines("LIST", notes.append)
            for note in notes:
                data = self._decode_file_data(note)
                files.append(FileData(data["name"], data["size"], data["type"], data["time"]))
            self._disconnect()
            return files
        except (FileNotFoundError, Error):
            self._disconnect()
            return files

    def upload(self, source: str, destination: str) -> bool:
        """upload загружает файл source на ftp-сервер"""
        if not self._connect():
            return False
        try:
            with open(source, "rb") as file:
                self._ftp.storbinary("STOR " + destination, file, 1024)
            self._disconnect()
            return True
        except (FileNotFoundError, Error):
            self._disconnect()
            return False

    def download(self, source: str, destination: str) -> bool:
        """download скачивает файл source с ftp-сервера"""
        if not self._connect():
            return False
        try:
            with open(destination, "wb") as file:
                self._ftp.retrbinary("RETR " + source, file.write, 1024)
            self._disconnect()
            return True
        except (FileNotFoundError, Error):
            self._disconnect()
            return False