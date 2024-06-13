# # 示例用法
# 文件路径 = r"C:\Users\Administrator\Desktop\测试.txt"
# 文件内容 = 文本文件_读入全部内容(文件路径)
# if 文件内容:
#     print("文件内容:")
#     print(文件内容)

def 文本文件_读入全部内容(文件路径):
    """
    读取指定文件路径的文本文件内容。
    注意：文本编码格式需要为UTF-8
    参数:
    - 文件路径 (str): 要读取的文本文件的路径。

    返回:
    - 文件内容 (str): 文本文件的内容，失败将返回空
    """
    try:
        with open(文件路径, 'r', encoding='utf-8') as file:
            文件内容 = file.read()
        return 文件内容
    except FileNotFoundError:
        print(f"文件 {文件路径} 未找到！")
        return None
    except Exception as e:
        print(f"读取文件 {文件路径} 时出现错误：{e}")
        return None