from pdfrw import PdfReader
import pdfrw
from data import *
import pypdftk

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'
AcroForm_KEY = '/AcroForm'

APPLICANT_LAST_NAME_KEY = 'name fam'
APPLICANT_GIVEN_NAMES_KEY = 'name giv'


def pdf_file_write(form_path, applicant_data):
    """
    根据传入的表格文件路径以及数据，尝试将匹配的数据写入到表格文件中并保存
    :param form_path: 表格文件
    :param applicant_data: 要填写的数据
    :return: None
    """
    if "decrypted" not in form_path:
        try:
            decrypted_file_path = pdf_decryption(form_path)
            pdf_template = PdfReader(decrypted_file_path)
        except Exception as err:
            print(err)
            return
    else:
        pdf_template = PdfReader(form_path)

    if pdf_template:
        data = {}
        if applicant_data and len(applicant_data) != 0:
            for key in applicant_data.keys():
                if applicant_data[key] and applicant_data[key] != '':  # 过滤掉数据中值为0的情况
                    data[key] = applicant_data[key]

        # 解决写入值后在 adobe中不显示，在浏览器预览中可以显示值的问题，但是在adobe中打开，大部分显示不全
        # 使用浏览器打开可以显示，存在的问题：日期、checkbox、大段文本展示效果较差
        # https://github.com/pmaupin/pdfrw/issues/84
        pdf_template.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))

        for i in range(len(pdf_template.pages)):
            this_page = pdf_template.pages[i]
            if ANNOT_KEY in this_page.keys():
                annotations = this_page[ANNOT_KEY]
                for annotation in annotations:
                    if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                        if ANNOT_FIELD_KEY in annotation.keys():
                            key = annotation[ANNOT_FIELD_KEY][1:-1]
                            if key in data.keys() and data[key] != 'None':
                                annotation.update(pdfrw.PdfDict(AP=''))  # 解决在浏览器预览中不显示的问题
                                annotation.update(
                                    pdfrw.PdfDict(V='{}'.format(data[key]))
                                )
        # flatten the pdf  https://stackoverflow.com/questions/14454387/pdfbox-how-to-flatten-a-pdf-form
        # 不起作用
        # pdf_template.Root.AcroForm.update(pdfrw.PdfDict(Ff=1))

        dst_name = get_out_pdf_file_name(form_path, applicant_data)
        pdfrw.PdfWriter().write(dst_name, pdf_template)

        # https://github.com/mikehaertl/php-pdftk/issues/62 尚未解决
        pypdftk.fill_form("1022_Zhang_Lingyun.pdf",
                          out_file='out.pdf',
                          flatten=True)


def get_out_pdf_file_name(form_path, applicant_data):
    """
    根据表格路径以及申请人姓名来设置输出文件的名称
    :return "C:\\timit\\1022_Lingyun_Zhang.pdf"
    """
    file_name = form_path[:form_path.rindex('.')] + "_{}_{}.pdf".format(applicant_data[APPLICANT_LAST_NAME_KEY],
                                                                        applicant_data[APPLICANT_GIVEN_NAMES_KEY])
    return file_name


def pdf_decryption(input_file_path):
    out_name = input_file_path[:input_file_path.rindex('.')] + '_decrypted.pdf'
    command = "qpdf --decrypt {} {}".format(input_file_path, out_name)
    import os
    if os.system(command) == 0:
        return out_name
    else:
        raise Exception("解密失败")


if __name__ == '__main__':
    pdf_file_write("1022.pdf", data_2)
