from uuid import UUID, uuid4


def get_uuid_str():
    """
    문자열 uuid 생성
    """
    uuid_v4 = uuid4()
    uuid_str = str(uuid_v4)
    return uuid_str


def str_to_uuid4(uuid_str: str):
    """
    문자열 -> uuid4 변환
    """
    try:
        return UUID(uuid_str, version=4)
    except ValueError:
        raise ValueError("Invalid UUID string")
