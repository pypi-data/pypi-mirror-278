def 谷歌填表_输入文本(元素, 文本):
    """
    在指定的网页元素中输入文本。

    Args:
        元素: 要输入文本的元素对象。
        文本: 要输入的文本内容。

    Returns:
        bool: 输入文本成功返回 True，失败返回 False。
    """
    try:
        元素.send_keys(文本)
        return True
    except Exception:
        return False