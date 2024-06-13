# # 调用函数示例
#     行数 = 文本文件_取行数(r"C:\Users\Administrator\Desktop\测试.txt")
#     print("文本文件内的行数:", 行数)

def 文本文件_取指定文件文本行数(文件路径):
    """
    参数:
    文件路径: 要计算行数的文本文件路径。

    返回:
    整数，文本文件内的行数。失败返回 -1
    """
    try:
        with open(文件路径, 'r', encoding='utf-8') as file:
            行数 = sum(1 for _ in file)
        return 行数
    except Exception:
        return -1