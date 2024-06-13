import math


def 算数_求正弦(角度):
    """
    计算给定角度的正弦值。

    参数:
    - 角度 (float): 要计算正弦值的角度，单位为度。

    # 示例用法
    angle = 45
    sin_value = 求正弦(angle)
    print(f"{angle}度的正弦值为: {sin_value}")

    返回:
    - 正弦值 (float): 给定角度的正弦值。
    """
    # 将角度转换为弧度
    弧度 = math.radians(角度)

    # 计算正弦值
    正弦值 = math.sin(弧度)

    return 正弦值



