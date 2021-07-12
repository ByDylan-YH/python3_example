from io import StringIO
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
# 另外可以了解下: pdfplumber ,貌似更好用
# https://mp.weixin.qq.com/s/urqj9ba6ffBX_UwZCkVBYQ

# 读取url中的pdf
def read_pdf(pdf_path):
    sacList = []
    fp = open(pdf_path, 'rb')  # rb以二进制读模式打开本地pdf文件
    # 用文件对象来创建一个pdf文档分析器
    praser_pdf = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument(praser_pdf)
    # 连接分析器 与文档对象
    praser_pdf.set_document(doc)
    # doc.set_parser(praser_pdf)
    # 如果没有密码 就创建一个空的字符串
    # doc._initialize_password()
    # 检测文档是否提供txt转换,不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF参数分析器
        laparams = LAParams()
        # 创建聚合器
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF页面解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pageCount = 0
        # 循环遍历列表,每次处理一页的内容
        output = StringIO()
        for page in PDFPage.create_pages(doc):
            # 使用页面解释器来读取
            interpreter.process_page(page)
            # 使用聚合器获取内容
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure,
            # LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性,
            for x in layout:
                if hasattr(x, "get_text"):
                    content = x.get_text()
                    output.write(content)
            content = output.getvalue()
            print(content)


if __name__ == '__main__':
    read_pdf('E:\Downloads\W020171127655898615398.pdf')
