import psutil


def 进程_名取ID(进程名):
    """
    # 使用示例,成功返回进程ID  失败返回 0
    进程ID = 进程_名取ID("chrome.exe")
    """
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 进程名:
                return proc.info['pid']
        return 0  # 没有找到匹配的进程名
    except Exception as e:
        print(f"An error occurred while getting process ID: {e}")
        return 0