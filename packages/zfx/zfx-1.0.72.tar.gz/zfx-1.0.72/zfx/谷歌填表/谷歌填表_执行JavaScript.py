def 谷歌填表_执行JavaScript(参_driver, 脚本, *参数):
    """
    执行 JavaScript 脚本。

    Args:
        参_driver: WebDriver 对象。
        脚本: 要执行的 JavaScript 脚本。
        *参数: 传递给 JavaScript 脚本的参数。

    Returns:
        执行 JavaScript 脚本后的返回值。
    """
    return 参_driver.execute_script(脚本, *参数)