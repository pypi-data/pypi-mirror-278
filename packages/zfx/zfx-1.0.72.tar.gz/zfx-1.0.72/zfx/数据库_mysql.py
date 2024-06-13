import mysql.connector


def 数据库_mysql_连接数据库(主机, 用户名, 密码, 数据库名):
    """
    连接到MySQL数据库并返回连接对象和游标对象。

    参数：
    - 主机：数据库主机名或IP地址。
    - 用户名：数据库用户名。
    - 密码：数据库密码。
    - 数据库名：要连接的数据库名。

    返回值：
    - 连接对象：表示与数据库的连接。如果连接失败，则返回 False。
    - 游标对象：用于执行查询和获取结果。如果连接失败，则返回 False。
    """
    try:
        # 连接到数据库
        连接对象 = mysql.connector.connect(
            host=主机,
            user=用户名,
            password=密码,
            database=数据库名
        )

        # 创建游标对象
        游标对象 = 连接对象.cursor()

        # 返回连接对象和游标对象
        return 连接对象, 游标对象
    except Exception:
        return False, False


def 数据库_mysql_查询记录(游标, 表名, 字段名, 排序方式="升序", 查询条件=""):
    """
    使用给定的游标对象执行查询，并返回符合条件的记录。

    参数：
    - 游标：数据库游标对象，用于执行查询。
    - 表名：要查询的表名。
    - 字段名：用于排序的字段名
    - 排序方式：可选，排序方式，默认为"升序"，可选值为"升序"或"降序"。
    - 查询条件：可选，查询条件，默认为空字符串。

    返回值：
    - 符合查询条件的记录，如果没有找到记录，则返回空列表。

    使用示例
    查询结果 = 数据库_mysql_查询记录(游标对象, "asida", "id", 排序方式="降序", 查询条件="id > 0")
    """
    try:
        # 构建查询语句
        查询语句 = f"SELECT * FROM {表名}"
        if 查询条件:
            查询语句 += f" WHERE {查询条件}"
        if 排序方式 == "升序":
            查询语句 += f" ORDER BY {字段名} ASC"
        elif 排序方式 == "降序":
            查询语句 += f" ORDER BY {字段名} DESC"

        # 执行查询
        游标.execute(查询语句)

        # 获取查询结果
        结果 = 游标.fetchall()

        return 结果
    except Exception:
        return False


def 数据库_mysql_增加记录(连接, 表名, 值字典):
    """
    向数据库表中插入新记录。

    参数：
    - 连接: 数据库连接对象。
    - 表名: 要插入新记录的表的名称，字符串类型。
    - 值字典: 插入的字段及其对应的值，字典类型。例如 {"username": "jack", "password": "jack@126.com"}。

    返回值：
    - 执行成功返回 True，失败返回 False。

    使用示例：
    值字典 = {"username": "jack", "password": "jack@126.com", "nua": 123}
    插入结果 = 数据库_mysql_增加记录(连接对象, "asida", 值字典)
    """
    try:
        # 构建插入语句
        列名 = ', '.join(值字典.keys())
        占位符 = ', '.join(['%s'] * len(值字典))
        插入语句 = f"INSERT INTO {表名} ({列名}) VALUES ({占位符})"

        # 执行插入操作
        游标 = 连接.cursor()
        游标.execute(插入语句, list(值字典.values()))

        # 提交事务
        连接.commit()

        # 关闭游标
        游标.close()

        return True
    except Exception:
        return False


def 数据库_mysql_删除记录(连接, 表名, 条件):
    """
    删除符合条件的记录。

    参数：
    - 连接: 数据库连接对象。
    - 表名：要进行删除操作的表的名称。
    - 条件：删除符合条件的记录的条件。如果为''(空字符串)，则删除所有记录。

    返回值：
    - 删除成功返回 True，失败返回 False。

    使用示例
    删除结果 = 数据库_mysql_删除记录(连接对象,  "asida", "username='jack'")
    删除结果 = 数据库_mysql_删除记录(连接对象,  "asida", "id > 5")
    """
    try:
        # 构建删除语句
        删除语句 = f"DELETE FROM {表名}"
        if 条件:
            删除语句 += f" WHERE {条件}"

        # 执行删除操作
        连接.cursor().execute(删除语句)

        # 提交事务
        连接.commit()

        return True
    except Exception:
        return False


def 数据库_mysql_更新记录(连接, 表名, 值字典, 条件字典=None):
    """
    更新指定字段的数据。

    参数：
    - 连接: 数据库连接对象。
    - 表名：要更新数据的表的名称。
    - 值字典：要更新的字段及其对应的值，字典类型。例如 {"字段1": "值1", "字段2": "值2", "字段3": 1234}。
    - 条件字典：查找符合条件的记录的条件，字典类型。例如 {"id": 1, "name": "Jack"}。如果为空字典或为 None，则更新所有记录。

    返回值：
    - 更新成功返回 True，失败返回 False。
    """
    try:
        # 构建更新语句
        赋值语句 = ', '.join([f"{字段}=%s" for 字段 in 值字典.keys()])
        更新语句 = f"UPDATE {表名} SET {赋值语句}"

        # 如果有条件，则添加条件到更新语句中
        if 条件字典:
            条件语句 = ' AND '.join([f"{字段}=%s" for 字段 in 条件字典.keys()])
            更新语句 += f" WHERE {条件语句}"

        # 提取值列表
        值列表 = list(值字典.values())
        if 条件字典:
            值列表.extend(list(条件字典.values()))

        # 执行更新操作
        连接.cursor().execute(更新语句, 值列表)

        # 提交事务
        连接.commit()

        return True
    except Exception:
        return False


def 数据库_mysql_关闭连接(连接对象, 游标对象=None):
    """
    关闭数据库连接和游标对象。

    参数：
    - 连接: 数据库连接对象。
    - 游标对象：可选，数据库游标对象。如果提供了游标对象，则同时关闭游标对象；如果未提供，则仅关闭连接对象。

    返回值：
    - 成功返回 True，失败返回 False
    """
    try:
        # 关闭游标对象（如果提供）
        if 游标对象:
            游标对象.close()

        # 关闭连接对象
        连接对象.close()
        return True
    except Exception:
        return False


def 数据库_mysql_查询表记录数(游标, 表名):
    """
    查询指定表的记录数量。

    参数：
    - 游标: 数据库游标对象。
    - 表名: 要查询记录数量的表名。

    返回值：
    - 返回指定表的记录数量，如果查询失败返回 None。
    """
    try:
        # 构建查询语句
        查询语句 = f"SELECT COUNT(*) FROM {表名}"

        # 执行查询操作
        游标.execute(查询语句)

        # 获取记录数量
        记录数 = 游标.fetchone()[0]

        return 记录数
    except Exception:
        return None