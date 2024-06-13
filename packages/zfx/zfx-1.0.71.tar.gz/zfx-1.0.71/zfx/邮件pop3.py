import poplib


def 邮件pop3_登录(服务器地址, 用户名, 密码):
    """
    尝试连接到指定的POP3服务器并登录邮箱账户。

    参数:
    服务器地址 (str): POP3服务器的地址。
    用户名 (str): 登录邮箱的用户名。
    密码 (str): 登录邮箱的密码。

    返回值:
    如果登录成功，返回连接成功的POP3服务器对象；如果登录失败或出现异常，返回假(False)。
    """
    try:
        # 连接到POP3服务器
        邮件服务器 = poplib.POP3(服务器地址, 110)

        # 尝试登录邮箱
        响应用户 = 邮件服务器.user(用户名)
        响应密码 = 邮件服务器.pass_(密码)

        # 判断登录是否成功
        if 响应用户.startswith(b'+OK') and 响应密码.startswith(b'+OK'):
            return 邮件服务器  # 返回连接成功的POP3服务器对象
    except Exception:
        return False  # 如果连接失败或登录失败，直接返回 False


def 邮件pop3_获取邮件数量(服务器对象):
    """
    获取邮箱中的邮件数量。

    参数:
    邮件服务器 (poplib.POP3): 已经连接的POP3服务器对象。

    返回值:
    int: 邮件数量。如果出现异常，返回假(False)。

    异常:
    无
    """
    try:
        # 获取邮箱中的邮件数量
        num_messages, _ = 服务器对象.stat()
        return num_messages
    except Exception:
        return False


def 邮件pop3_获取邮箱占用空间(服务器对象):
    """
    获取邮箱的占用空间。

    参数:
    服务器对象 (poplib.POP3): 已经连接的POP3服务器对象。

    返回值:
    int: 邮箱占用空间（以字节为单位）。如果出现异常，返回假(False)。

    异常:
    无
    """
    try:
        # 获取邮箱的占用空间
        _, total_size = 服务器对象.stat()
        return total_size
    except Exception:
        return False


def 邮件pop3_获取邮件内容(服务器对象, 邮件索引):
    """
    获取指定索引的邮件内容。

    参数:
    服务器对象 (poplib.POP3): 已经连接的POP3服务器对象。
    邮件索引 (int): 要获取的邮件的索引。

    返回值:
    bytes: 邮件内容的字节串。如果出现异常或指定索引的邮件不存在，返回假(False)。
    """
    try:
        # 获取指定索引的邮件内容
        局_响应, 局_邮件列表, _ = 服务器对象.list()
        if 邮件索引 > len(局_邮件列表) or 邮件索引 <= 0:  # 索引从1开始，所以索引必然不可能小于或等于0，也不可能大于邮件的数量。
            return False  # 邮件不存在，返回 False

        局_响应, 局_邮件内容, _ = 服务器对象.retr(邮件索引)
        局_邮件内容字节串 = b'\n'.join(局_邮件内容)
        return 局_邮件内容字节串
    except Exception:
        return False


def 邮件pop3_删除邮件(服务器对象, 邮件索引):
    """
    删除指定索引的邮件。

    参数:
    服务器对象 (poplib.POP3): 已连接的POP3服务器对象。
    邮件索引 (int): 要删除的邮件的索引。

    返回值:
    bool: 如果成功删除邮件，则返回True；否则返回False。

    注意:
    删除邮件后，需要调用断开连接函数 `断开连接()` 才会生效。
    """
    try:
        服务器对象.dele(邮件索引)
        return True
    except Exception:
        return False


def 邮件pop3_断开连接(服务器对象):
    """
    断开与邮件服务器的连接。

    参数:
    服务器对象 (poplib.POP3): 已连接的POP3服务器对象。

    返回值:
    bool: 如果断开成功，则返回True；否则返回False。
    """
    try:
        服务器对象.quit()
        return True
    except Exception:
        return False