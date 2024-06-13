def 谷歌填表_切换窗口(参_driver, 窗口名称):
    """
    切换到指定名称的窗口。

    Args:
        参_driver: WebDriver 对象。
        窗口名称: 要切换到的窗口的名称。
    """
    参_driver.switch_to.window(窗口名称)