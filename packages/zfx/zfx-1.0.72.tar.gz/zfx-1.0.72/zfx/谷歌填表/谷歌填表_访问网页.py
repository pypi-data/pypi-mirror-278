def 谷歌填表_访问网页(参_driver, 网址):
    """
    使用提供的驱动程序访问指定的网址。

    Args:
        参_driver: WebDriver 对象，用于控制浏览器的行为。
        网址: 要访问的网址。

    Returns:
        bool: 访问成功返回 True，访问失败返回 False。
    """
    try:
        参_driver.get(网址)
        return True
    except Exception:
        return False