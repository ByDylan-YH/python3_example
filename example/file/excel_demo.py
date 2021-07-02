import xlrd
from xlutils.copy import copy

def edit_excel():
    # 打开 excel 文件
    readbook = xlrd.open_workbook("test_w67.xls")
    # 复制一份
    wb = copy(readbook)
    # 选取第一个表单
    sh1 = wb.get_sheet(0)
    # 在第四行新增写入数据
    sh1.write(3, 0, '王亮')
    sh1.write(3, 1, 59)
    # 选取第二个表单
    sh1 = wb.get_sheet(1)
    # 替换总成绩数据
    sh1.write(1, 0, 246.5)
    # 保存
    wb.save('test_w1.xls')

def read_excel():
    # 打开刚才我们写入的 test_w.xls 文件
    wb = xlrd.open_workbook("test_w67.xls")
    # 获取并打印 sheet 数量
    print("sheet 数量:", wb.nsheets)
    # 获取并打印 sheet 名称
    print("sheet 名称:", wb.sheet_names())
    # 根据 sheet 索引获取内容
    sh1 = wb.sheet_by_index(0)
    # 或者
    # 也可根据 sheet 名称获取内容
    # sh = wb.sheet_by_name('成绩')
    # 获取并打印该 sheet 行数和列数
    print(u"sheet %s 共 %d 行 %d 列" % (sh1.name, sh1.nrows, sh1.ncols))
    # 获取并打印某个单元格的值
    print("第一行第二列的值为:", sh1.cell_value(0, 1))
    # 获取整行或整列的值
    rows = sh1.row_values(0)  # 获取第一行内容
    cols = sh1.col_values(1)  # 获取第二列内容
    # 打印获取的行列值
    print("第一行的值为:", rows)
    print("第二列的值为:", cols)
    # 获取单元格内容的数据类型
    print("第二行第一列的值类型为:", sh1.cell(1, 0).ctype)
    # 遍历所有表单内容
    for sh in wb.sheets():
        for r in range(sh.nrows):
            # 输出指定行
            print(sh.row(r))

def write_excel():
    # 创建 xls 文件对象
    wb = xlwt.Workbook()
    # 新增两个表单页
    sh1 = wb.add_sheet('成绩')
    sh2 = wb.add_sheet('汇总')
    # 然后按照位置来添加数据,第一个参数是行，第二个参数是列
    # 写入第一个sheet
    sh1.write(0, 0, '姓名')
    sh1.write(0, 1, '成绩')
    sh1.write(1, 0, '张三')
    sh1.write(1, 1, 88)
    sh1.write(2, 0, '李四')
    sh1.write(2, 1, 99.5)
    # 写入第二个sheet
    sh2.write(0, 0, '总分')
    sh2.write(1, 0, 187.5)
    # 最后保存文件即可
    wb.save('C:\\Users\\BYDylan\\Desktop\\test_w67.xls')

if __name__ == '__main__':
    read_excel()