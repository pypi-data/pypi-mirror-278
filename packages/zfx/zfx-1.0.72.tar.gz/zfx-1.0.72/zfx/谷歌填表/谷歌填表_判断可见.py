def 谷歌填表_判断可见(元素):
    """
    判断给定元素是否可见。

    Args:
        元素: 要进行可见性检查的元素对象。

    Returns:
        bool: 如果元素可见，则返回 True；否则返回 False。
    """
    try:
        return 元素.is_displayed()
    except Exception:
        return False