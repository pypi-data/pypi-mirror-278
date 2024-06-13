def 谷歌填表_置浏览器大小和位置(参_driver, 宽度, 高度, x_位置, y_位置):
    """
    设置浏览器窗口的大小和位置。
    参数:
        驱动器: WebDriver 对象，表示浏览器驱动器。
        宽度: int，表示窗口宽度（像素）。
        高度: int，表示窗口高度（像素）。
        x_位置: int，表示窗口左上角的 x 坐标位置。
        y_位置: int，表示窗口左上角的 y 坐标位置。
    """
    参_driver.set_window_size(宽度, 高度)
    参_driver.set_window_position(x_位置, y_位置)