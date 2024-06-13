# 示例用法
# 文件路径 = r"C:\Users\Administrator\Desktop\测试.txt"
# 新内容 = "这是新的内容，替换原来的内容。"
# 写入结果 = 写入文件内容(文件路径, 新内容)
# if 写入结果:
#     print("内容写入成功！")
# else:
#     print("内容写入失败！")

def 文本文件_写入文件内容(文件路径, 内容):
    """
    将指定内容写入指定文件路径的文本文件中，替换原本的内容。
    注意：文本编码格式需要为UTF-8
    参数:
    - 文件路径 (str): 要写入的文本文件的路径。
    - 内容 (str): 要写入文件的内容。

    返回:
    - 写入成功返回 True，写入失败返回 False。
    """
    try:
        with open(文件路径, 'w', encoding='utf-8') as file:
            file.write(str(内容))
        return True
    except Exception as e:
        print(f"写入文件 {文件路径} 时出现错误：{e}")
        return False
