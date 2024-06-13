import requests
import os
import shutil


def 网页协议_发送_GET请求(网址, 参数=None):
    """
    发送 GET 请求并返回服务器响应对象
    :param 网址: 请求的 URL
    :param 参数: 要发送的参数，字典形式，默认为 None
    :return: 服务器响应对象，如果请求失败则返回 None
    """
    try:
        响应 = requests.get(网址, params=参数)
        return 响应
    except Exception:
        return None


def 网页协议_发送_POST请求(网址, 数据):
    """
    发送 POST 请求并返回服务器响应
    :param 网址: 请求的 URL
    :param 数据: 要发送的数据，字典形式
    :return: 服务器响应的文本，如果请求失败则返回 None
    """
    try:
        响应 = requests.post(网址, data=数据)
        return 响应.text
    except Exception:
        return None


def 网页协议_获取_HTTP状态码(响应):
    """
    获取 HTTP 状态码
    :param 响应: 服务器响应对象
    :return: HTTP 状态码，如果响应为 None 则返回 None
    """
    if 响应 is not None:
        return 响应.status_code
    else:
        return None


def 网页协议_获取_响应文本(响应):
    """
    获取响应的文本内容
    :param 响应: 服务器响应对象
    :return: 响应的文本内容，如果响应为 None 则返回空字符串
    """
    if 响应 is not None:
        return 响应.text
    else:
        return ''


def 网页协议_获取_响应二进制内容(响应):
    """
    获取响应的二进制内容
    :param 响应: 服务器响应对象
    :return: 响应的二进制内容，如果响应为 None 则返回空字节串
    """
    if 响应 is not None:
        return 响应.content
    else:
        return b''


def 网页协议_获取_响应头(响应):
    """
    获取响应头的字典形式
    :param 响应: 服务器响应对象
    :return: 响应头的字典形式，如果响应为 None 则返回空字典
    """
    if 响应 is not None:
        return 响应.headers
    else:
        return {}


def 网页协议_获取_响应URL(响应):
    """
    获取响应的 URL
    :param 响应: 服务器响应对象
    :return: 响应的 URL，如果响应为 None 则返回空字符串
    """
    if 响应 is not None:
        return 响应.url
    else:
        return ''


def 网页协议_获取_响应编码(响应):
    """
    获取响应的编码格式
    :param 响应: 服务器响应对象
    :return: 响应的编码格式，如果响应为 None 则返回空字符串
    """
    if 响应 is not None:
        return 响应.encoding
    else:
        return ''


def 网页协议_获取_响应cookies(响应):
    """
    获取响应的 cookies
    :param 响应: 服务器响应对象
    :return: 响应的 cookies，如果响应为 None 则返回空字典
    """
    if 响应 is not None:
        return 响应.cookies
    else:
        return {}


def 网页协议_图片下载(图片链接, 保存目录, 图片名称):
    """
    下载图片并保存到指定目录和文件名。

    参数：
    图片链接 (str): 图片的URL链接。
    保存目录 (str): 保存图片的本地目录路径。
    图片名称 (str): 保存的图片文件名。

    返回值：
    bool: 下载成功返回True，下载失败返回False。

    # 示例使用
    图片链接 = "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"
    保存目录 = r"C:\tmp"
    图片名称 = 'downloaded_image.png'
    结果 = 网页协议_图片下载(图片链接, 保存目录, 图片名称)
    print(结果)
    """
    try:
        # 确保保存目录存在，如果不存在则创建
        if not os.path.exists(保存目录):
            os.makedirs(保存目录)

        # 构造完整的文件路径
        文件路径 = os.path.join(保存目录, 图片名称)

        # 发送GET请求获取图片
        response = requests.get(图片链接, stream=True)

        # 检查请求是否成功（状态码200表示成功）
        if response.status_code == 200:
            # 打开本地文件，准备写入
            with open(文件路径, 'wb') as file:
                # 使用shutil.copyfileobj将响应内容保存到文件
                shutil.copyfileobj(response.raw, file)
            return True
        else:
            return False
    except Exception:
        return False