from itertools import product
import fitz
import os
import shutil
from multiprocessing import pool, get_context

from PyPDF2 import PdfReader, PdfWriter

# enum
DPI: int = 220
TMP: str = ""
PDFFILEMARK: str = ""
CORE = 6
MULTIMETHOD: str = "spawn"


# print(TMP)
def setConfig(tmp: str, dpi: int, pdf_file_mark: str, core: int, method: str):
    global TMP, DPI, PDFFILEMARK, CORE, MULTIMETHOD
    TMP = tmp
    DPI = dpi
    PDFFILEMARK = pdf_file_mark
    CORE = core
    MULTIMETHOD = method


def _getTmpDir(src: str):
    """得到临时文件夹名字"""
    return TMP + "\\" + str(hash(src))


def __createTmpDir(src: str):
    """得到并创建临时文件夹"""
    try:
        os.mkdir(_getTmpDir(src))
    except FileExistsError:
        pass


def __delTmpDir(src: str):
    """删除临时文件夹"""
    try:
        # os.removedirs(__getTmpDir(src))
        shutil.rmtree(_getTmpDir(src))
        os.rmdir(_getTmpDir(src))
    except FileNotFoundError:
        pass


# 去除pdf的水印
def __remove_pdfwatermark(src: str):
    # 打开源pfd文件
    pdf_file = fitz.open(src)
    # page_no 设置为0
    page_no = 0

    # page在pdf文件中遍历
    __createTmpDir(src)
    for page in pdf_file:
        # 获取每一页对应的图片pix (pix对象类似于我们上面看到的img对象，可以读取、修改它的 RGB)
        # page.get_pixmap() 这个操作是不可逆的，即能够实现从 PDF 到图片的转换，但修改图片 RGB 后无法应用到 PDF 上，只能输出为图片
        page.draw_rect((0, 0, 600, 54), color=(1, 1, 1), fill=(1, 1, 1), width=0)
        page.draw_rect((0, 818, 600, 1000), color=(1, 1, 1), fill=(1, 1, 1), width=0)
        pix = page.get_pixmap(dpi=DPI)
        # 遍历图片中的宽和高，如果像素的rgb值总和大于510，就认为是水印，转换成255，255,255-->即白色
        for pos in product(range(pix.width), range(pix.height)):
            if sum(pix.pixel(pos[0], pos[1])) >= 510:
                pix.set_pixel(pos[0], pos[1], (255, 255, 255))
        # 保存去掉水印的截图
        pix.pil_save(f"{_getTmpDir(src)}/{page_no}.png", dpi=(30000, 30000))
        # 打印结果
        # print(f"第 {page_no} 页去除完成")
        page_no += 1


# 去除的pdf水印添加到pdf文件中
def __pictopdf(src: str, dst: str):
    # 水印截图所在的文件夹
    # pic_dir = input("请输入图片文件夹路径：")
    pic_dir = _getTmpDir(src)
    pdf = fitz.open()
    # 图片数字文件先转换成int类型进行排序
    img_files = sorted(os.listdir(pic_dir), key=lambda x: int(str(x).split(".")[0]))
    for img in img_files:
        # print(img)
        imgdoc = fitz.open(pic_dir + "/" + img)
        # 将打开后的图片转成单页pdf
        pdfbytes = imgdoc.convert_to_pdf()
        imgpdf = fitz.open("pdf", pdfbytes)
        # 将单页pdf插入到新的pdf文档中
        pdf.insert_pdf(imgpdf)
    pdf.ez_save(dst)
    pdf.close()
    __delTmpDir(src)


def _addWaterMark(pdf_file_in: str, pdf_file_out: str):
    """把水印添加到pdf中"""
    pdf_output = PdfWriter()
    input_stream = open(pdf_file_in, "rb")
    pdf_input = PdfReader(input_stream, strict=False)

    # 获取PDF文件的页数
    pageNum = len(pdf_input.pages)

    # 读入水印pdf文件
    pdf_watermark = PdfReader(open(PDFFILEMARK, "rb"), strict=False)
    # 给每一页打水印
    pdf_watermark.pages[0].scale_to(595, 842)
    for i in range(pageNum):
        page = pdf_input.pages[i]
        page.scale_to(595, 842)
        page.merge_page(pdf_watermark.pages[0], True)
        page.compress_content_streams()  # 压缩内容
        pdf_output.add_page(page)
    input_stream.close()
    with open(pdf_file_out, "wb") as fout:
        pdf_output.write(fout)


def __bypixfunc(src: str, dst: str, isAdd: bool = False):
    __remove_pdfwatermark(src)
    __pictopdf(src, dst)
    if isAdd is True:
        print("开始打水印")
        _addWaterMark(dst, dst)
    print(src, "处理完毕")


def err(i):
    print(i)


def delWatermarkByPix(
    files: list[tuple[str, str]], isAdd: bool = False, isDelSrc: bool = False
):
    """图像处理-删除水印功能
    ## params
    - files: 传入文件路径+转换目的路径列表，保证都是.pdf拓展名
    """
    mypool = pool.Pool(4, context=get_context(MULTIMETHOD))
    for src, dst in files:
        if os.path.exists(dst):
            os.remove(dst)

        # 加载PDF文件
        def delSrc(_):
            if isDelSrc and os.path.exists(src):
                os.remove(src)

        mypool.apply_async(
            __bypixfunc, (src, dst, isAdd), error_callback=err, callback=delSrc
        )

    mypool.close()
    mypool.join()
    print("全部文件已经去除水印\n")
    # os.system("pause")
