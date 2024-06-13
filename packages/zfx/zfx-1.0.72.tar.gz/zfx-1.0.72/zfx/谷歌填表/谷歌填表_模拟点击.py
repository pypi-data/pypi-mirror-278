def 谷歌填表_模拟点击(driver, 元素对象):
    """
    模拟点击元素对象。

    参数:
    - driver: WebDriver 对象，用于执行 JavaScript 脚本。
    - 元素对象: 要模拟点击的 WebElement 对象。
    """
    driver.execute_script("arguments[0].click();", 元素对象)