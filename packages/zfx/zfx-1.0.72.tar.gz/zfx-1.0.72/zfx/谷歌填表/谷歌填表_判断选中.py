def 谷歌填表_判断选中(元素):
    """
    判断给定元素是否选中。

    Args:
        元素: 要进行选中状态检查的元素对象。

    Returns:
        bool: 如果元素选中，则返回 True；否则返回 False。
    """
    try:
        return 元素.is_selected()
    except Exception:
        return False