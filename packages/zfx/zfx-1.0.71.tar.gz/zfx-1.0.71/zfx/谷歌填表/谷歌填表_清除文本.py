def 谷歌填表_清除文本(元素):
    """
    清除元素中的文本。

    Args:
        元素: 要清除文本的元素对象。

    Returns:
        bool: 清除文本成功返回 True，失败返回 False。
    """
    try:
        元素.clear()
        return True
    except Exception:
        return False