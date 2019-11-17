"""
查看pdf中的字段和值
"""
from pdf_write import *
from pdfrw import PdfReader

INPUT_PATH = '1022_entered.pdf'


def read_data(input_path):
    try:
        pdf_file = PdfReader(input_path)
    except ValueError:
        pdf_file = PdfReader(pdf_decryption(input_path))
    dict = {}

    for i in range(len(pdf_file.pages)):
        this_page = pdf_file.pages[i]
        if ANNOT_KEY in this_page.keys():
            annotations = this_page[ANNOT_KEY]
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if ANNOT_FIELD_KEY in annotation.keys():
                        key = annotation[ANNOT_FIELD_KEY][1:-1]
                    value = annotation[ANNOT_VAL_KEY]
                    if value:
                        dict[key] = annotation[ANNOT_VAL_KEY][1:-1]
                    else:
                        dict[key] = 'None'
    print(dict)


if __name__ == '__main__':
    read_data(INPUT_PATH)
