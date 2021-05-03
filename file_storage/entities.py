from dataclasses import dataclass

class Type:
    DISK = "disk"
    FTP = "ftp"
    S3 = "s3"

@dataclass
class Key:
    url: str
    username: str
    password: str

@dataclass
class Resource:
    type: Type
    key: Key
    path: str