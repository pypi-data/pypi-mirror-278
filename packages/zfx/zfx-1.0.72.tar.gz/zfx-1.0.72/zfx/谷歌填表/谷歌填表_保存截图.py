def 谷歌填表_保存截图(参_driver, 文件名):
    """
    保存当前页面的截图。

    Args:
        参_driver: WebDriver 对象。
        文件名: 要保存的截图文件的名称。
    """
    参_driver.save_screenshot(文件名)