def 谷歌填表_获取页面源代码(参_driver):
    """
    获取当前页面的源代码。

    Args:
        参_driver: WebDriver 对象。

    Returns:
        当前页面的源代码，如果失败则返回 None。
    """
    try:
        return 参_driver.page_source
    except Exception:
        return None