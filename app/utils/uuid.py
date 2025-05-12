from uuid import uuid4


def get_uuid_str():
    """
    문자열 uuid 생성
    """
    uuid_v4 = uuid4()
    uuid_str = str(uuid_v4)
    return uuid_str
