from itertools import product
import fitz
import os
import shutil
from multiprocessing import pool, get_context
from pigbe.plugins.WaterPrintFuncs.config import WaterPrintPlugCfg
from PyPDF2 import PdfReader, PdfWriter


def _getTmpDir(src: str):
    """得到临时文件夹名字"""
    return WaterPrintPlugCfg["tmp"] + "\\" + str(hash(src))


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
def __remove_pdfwatermark(src: str, dst: str, isdelsrc: bool = False):
    # 打开源pfd文件
    try:
        pdf_file = fitz.open(src)
    except BaseException:
        print("无法打开", src)
        return
    # page_no 设置为0
    page_no = 0

    # page在pdf文件中遍历
    __createTmpDir(src)
    isExistBig = False
    for page in pdf_file:
        # 删除页眉页脚水印
        text_instances = []

        # Search for the words and get their locations
        for word in WaterPrintPlugCfg["rowsToDelete"]:
            text_instances += page.search_for(word)

        # Cover each word location with a white rectangle
        for inst in text_instances:
            page.add_redact_annot(inst, fill=(1, 1, 1))

        page.apply_redactions()

        # 检测是否还存在水印(大的斜的)
        for word in WaterPrintPlugCfg["BigWaterMark"]:
            if len(page.search_for(word)) > 0:
                isExistBig = True
                # 获取每一页对应的图片pix (pix对象类似于我们上面看到的img对象，可以读取、修改它的 RGB)
                # page.get_pixmap() 这个操作是不可逆的，即能够实现从 PDF 到图片的转换，但修改图片 RGB 后无法应用到 PDF 上，只能输出为图片
                pix = page.get_pixmap(dpi=WaterPrintPlugCfg["dpi"])
                # 遍历图片中的宽和高，如果像素的rgb值总和大于510，就认为是水印，转换成255，255,255-->即白色
                for pos in product(range(pix.width), range(pix.height)):
                    if sum(pix.pixel(pos[0], pos[1])) >= 510:
                        pix.set_pixel(pos[0], pos[1], (255, 255, 255))
                # 保存去掉水印的截图
                pix.pil_save(f"{_getTmpDir(src)}/{page_no}.png", dpi=(30000, 30000))
                # 打印结果
                # print(f"第 {page_no} 页去除完成")
                page_no += 1
                break

    pdf_file.save(dst)
    pdf_file.close()
    if isdelsrc and os.path.exists(src):
        print("好想删", src)
        try:
            os.remove(src)
        except BaseException:
            print(src, "无法删除")
        # shutil.

    if isExistBig:
        try:
            pdf = fitz.open()
        except BaseException:
            print("无法打开", src)
            return
        pic_dir = _getTmpDir(src)
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


# # 去除的pdf水印添加到pdf文件中
# def __pictopdf(src: str, dst: str):
#     # 水印截图所在的文件夹
#     # pic_dir = input("请输入图片文件夹路径：")


def _addWaterMark(pdf_file_in: str, pdf_file_out: str, isdelsrc: bool = False):
    """把水印添加到pdf中"""
    try:
        input_stream = open(pdf_file_in, "rb")
    except BaseException:
        print("无法打开", pdf_file_in)
        return
    pdf_output = PdfWriter()
    pdf_input = PdfReader(input_stream, strict=False)

    # 获取PDF文件的页数
    pageNum = len(pdf_input.pages)

    # 读入水印pdf文件
    pdf_watermark = PdfReader(
        open(WaterPrintPlugCfg["WaterMarkTemplate"], "rb"), strict=False
    )
    # 给每一页打水印
    pdf_watermark.pages[0].scale_to(595, 842)
    for i in range(pageNum):
        page = pdf_input.pages[i]
        if page.get("/Rotate", 0) in [90, 270]:
            page.scale_to(842, 595)
            page.merge_page(pdf_watermark.pages[0], True)
        else:
            page.scale_to(595, 842)
            page.merge_page(pdf_watermark.pages[1], True)

        page.compress_content_streams()  # 压缩内容
        pdf_output.add_page(page)
    input_stream.close()

    if isdelsrc and os.path.exists(pdf_file_in):
        # print("好想删", src)
        try:
            os.remove(pdf_file_in)
        except BaseException:
            print(pdf_file_in, "无法删除")

    with open(pdf_file_out, "wb") as fout:
        pdf_output.write(fout)

        # shutil.


def __bypixfunc(src: str, dst: str, isAdd: bool = False, isdelsrc: bool = False):
    __remove_pdfwatermark(src, dst, isdelsrc=isdelsrc)
    # __pictopdf(src, dst)
    if isAdd is True:
        print("开始打水印")
        _addWaterMark(dst, dst, isdelsrc=isdelsrc)
    print(src, "处理完毕")


def err(i):
    print(i)


def delWatermarkByPix(
    files: list[tuple[str, str]], isAdd: bool = False, isdelsrc: bool = False
):
    """图像处理-删除水印功能
    ## params
    - files: 传入文件路径+转换目的路径列表，保证都是.pdf拓展名
    """
    mypool = pool.Pool(4, context=get_context(WaterPrintPlugCfg["MultiMethod"]))
    for src, dst in files:
        if os.path.exists(dst):
            os.remove(dst)

        mypool.apply_async(__bypixfunc, (src, dst, isAdd, isdelsrc), error_callback=err)

    mypool.close()
    mypool.join()
    print("全部文件已经完成处理\n")
    os.system("pause")
