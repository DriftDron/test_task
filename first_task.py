import pymupdf
import cv2
import os
import time

from pyzbar.pyzbar import decode


def convert_pdf_page_to_image(page, output_name):
    pix = page.get_pixmap()
    pix.save(output_name)


def read_barcode(image):
    barcodes = []
    img = cv2.imread(image)
    detected_barcodes = decode(img)
    for barcode in detected_barcodes:
        barcodes.append(barcode._asdict())
    return barcodes


def extract_info_from_pdf(path_to_pdf):
    with pymupdf.open(path_to_pdf) as file:
        text = ""
        for page_num in range(file.page_count):
            page = file.load_page(page_num)
            img_name = f'pdf_to_img_page_{page_num}.png'
            convert_pdf_page_to_image(page, img_name)
            barcode_info = read_barcode(img_name)
            text += page.get_text()

    lines = text.split('\n')
    size = os.path.getsize(path_to_pdf)
    creation_date = time.ctime(os.path.getctime(path_to_pdf))
    data = {'SIZE_BYTES': size,
            'FILE_CREATION_DATE': creation_date,
            'TITLE': lines[0]}

    for line in lines:
        if ':' in line:
            key, value = line.split(':')
            data[key.strip()] = value.strip()

    if 'NOTES:' in text:
        notes_index = lines.index('NOTES:')
        notes = " ".join(lines[notes_index + 1:])
        data['NOTES'] = notes.strip()

    for num, barcode in enumerate(barcode_info):
        data[f'barcode_{num}'] = barcode
    return data
