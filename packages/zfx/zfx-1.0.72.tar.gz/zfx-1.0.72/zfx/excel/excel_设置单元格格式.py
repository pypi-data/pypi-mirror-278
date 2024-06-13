from openpyxl.styles import Font, Alignment


def excel_设置单元格格式(表格对象, 工作表名, 单元格, 对齐=None):
    """
    参数:
    - 表格对象: 要操作的表格对象
    - 工作表名: 要设置单元格格式的工作表名称
    - 单元格: 要设置格式的单元格坐标，例如 'A1'
    - 对齐: 对齐方式，可选值为 "左对齐"、"右对齐"、"居中对齐"

    返回值:
    - 如果成功设置单元格格式，则返回 True；如果设置失败，则返回 False
    """
    try:
        工作表 = 表格对象[工作表名]
        单元格对象 = 工作表[单元格]
        if 对齐:
            if 对齐 == "左对齐":
                单元格对象.alignment = Alignment(horizontal='left')
            elif 对齐 == "右对齐":
                单元格对象.alignment = Alignment(horizontal='right')
            elif 对齐 == "居中对齐":
                单元格对象.alignment = Alignment(horizontal='center')
        return True
    except Exception:
        return False