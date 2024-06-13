import os


def 目录_取运行目录():
    """
    获取当前运行目录的函数。

    返回:
        str: 当前运行目录的路径，如果获取失败则返回 None。

    使用示例:
        运行目录 = 目录_取运行目录()
        print(运行目录)
    """
    try:
        return os.getcwd()  # 尝试获取当前运行目录
    except Exception:
        return None