# 유틸리티 관련 함수 정의
import math


def divide_with_ceil(divide_num: int, divide_by: int) -> int:
    if not divide_by or divide_by == 0:
        return 1
    return math.ceil(divide_num / divide_by)
