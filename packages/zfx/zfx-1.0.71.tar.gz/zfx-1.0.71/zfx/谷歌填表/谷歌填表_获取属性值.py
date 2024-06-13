def 谷歌填表_获取属性值(元素, 属性名):
    """
    获取元素的属性值。

    Args:
        元素: 要获取属性值的元素对象。
        属性名: 要获取的属性名称。

    Returns:
        str: 元素指定属性的值，如果属性不存在则返回 None。
    """
    try:
        return 元素.get_attribute(属性名)
    except Exception:
        return None