from .entities import Type, Key

from .storage import Storage
from .ftp import FtpServer
from .s3 import S3

def new_storage_by_type(storage_type: Type, key: Key) -> Storage:
	# if storage_type == Type.DISK:
	# 	return NewDisk()

    print(key)
	
    if storage_type == Type.FTP:
        return FtpServer(key.url, key.username, key.password)
    if storage_type == Type.S3:
        return S3(key.url, key.username, key.password)
        
    return None