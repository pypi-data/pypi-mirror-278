def 谷歌填表_判断可用(元素):
    """
    判断给定元素是否可用。

    Args:
        元素: 要进行可用性检查的元素对象。

    Returns:
        bool: 如果元素可用，则返回 True；否则返回 False。
    """
    try:
        return 元素.is_enabled()
    except Exception:
        return False