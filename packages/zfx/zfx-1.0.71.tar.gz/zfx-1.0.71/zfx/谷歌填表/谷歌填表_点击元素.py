def 谷歌填表_点击元素(元素):
    """
    点击指定的网页元素。

    Args:
        元素: 要点击的元素对象。

    Returns:
        bool: 如果点击成功，则返回 True，否则返回 False。
    """
    try:
        元素.click()
        return True
    except Exception:
        return False