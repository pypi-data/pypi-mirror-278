def 谷歌填表_切换框架(参_driver, 框架引用):
    """
    切换到指定的框架。

    Args:
        参_driver: WebDriver 对象。
        框架引用: 要切换到的框架的引用，可以是名称、索引或 WebElement 对象。
    """
    参_driver.switch_to.frame(框架引用)