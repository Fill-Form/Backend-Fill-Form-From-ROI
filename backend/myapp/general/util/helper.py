import base64 as stdlib_base64

import os
# import pytesseract
import easyocr
# import pdf2image

import json
# gen image from pdf
from pdf2image import convert_from_path

from general.model.schema import *

# for crop_image
from PIL import Image
import csv

import pprint
import glob
# algo 
# . decode base64 to pdf 
# . create object schema
# . convert base64 to pdf
# . convert pdf to image by page
# . crop image 
# . ocr image
# . gen CSV
# . delete image
# . delete pdf


# recevie [base64,...] output_file_path : file_output_name
path = './general/util/temp/'

def main_v1(schemas:list,array_base64:list):
    all_ocr_image = []
    # get header and roi
    header, rois = create_object(schemas)
    # creare pdf 
    i = 0
    for base64_string in array_base64:
        # decode base64 to pdf
        # format_string_name = 'pdf_' + str(i) + '.pdf'
        pdf_file = strip_prefix(base64_string)
        decode_base64_to_pdf(pdf_file,f'{path}pdf_{i}.pdf')
        # convert pdf to image by page
        files_image_name = create_page(f'{path}pdf_{i}.pdf')
        all_ocr_image.append(crop_image(files_image_name, rois))
        i+=1

    # ocr image
    all_result_ocr = ocr(all_ocr_image)
    # pprint.pprint(all_result_ocr)
    gen_csv(header,all_result_ocr)
    data_with_accuracy = get_accuracy(all_result_ocr)
    # pprint.pprint(data_with_accuracy)
    delete_file(path)
    return ['./general/util/temp/output.csv', data_with_accuracy]

def create_object(data):
    document = Document(data)
    header, rois = Document.get_roi(document)
    return header, rois

def strip_prefix(base64_string):
    prefix = 'data:application/pdf;base64,'
    if base64_string.startswith(prefix):
        base64_data = base64_string[len(prefix):]
        return bytes(base64_data, 'utf-8')
    return bytes(base64_string, 'utf-8') 

def decode_base64_to_pdf(base64_string, output_file_path):
    with open(output_file_path, 'wb') as pdf_file:
        pdf_file.write(stdlib_base64.b64decode(base64_string))
    
def create_page(file):
    images = convert_from_path(file)
    filename_without_extension, _ = os.path.splitext(file)
    filenames = []
    for i in range(len(images)):
        filename = f'{filename_without_extension}_page' + str(i) + '.jpg'
        images[i].save(filename, 'JPEG')
        filenames.append(filename)
    return filenames

def crop_image(files, rois):
    # crop image
    cropped_images = {}
    for file, page_rois in zip(files, rois.values()):
        image = Image.open(file)
        # page_number = int(os.path.splitext(file)[0].split('_')[-1]) + 1  # Extract page number from filename
        page_number = int(os.path.splitext(file)[0].split('_')[-1].replace('page', '')) + 1
        cropped_images[page_number] = []
        for roi in page_rois:
            x0,y0,x1,y1 = roi
            cropped_image = image.crop((x0, y0, x1, y1)) 
            cropped_images[page_number].append(cropped_image)

    cropped_image_names = []
    # save crop image
    for page_number, images in cropped_images.items():
        for i, image in enumerate(images):
            image_name = (f"{os.path.splitext(file)[0]}_page{page_number}_crop{i}.jpg")
            image.save(image_name)
            cropped_image_names.append(image_name)
    return cropped_image_names

def ocr(all_cropped_image_names):
    # v2
    all_result_ocr = []
    reader = easyocr.Reader(['th','en'])
    for cropped_image_name in all_cropped_image_names:
        result_ocr = []
        for img in cropped_image_name:
            result = reader.readtext(img)
            result_ocr.append(result)
        all_result_ocr.append(result_ocr)

    return all_result_ocr


def gen_csv(header,all_result_ocr):
    # bug v1
    # with open(f'{path}/output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # writer = csv.writer(csvfile)
        # writer.writerow(header)
        # for result_ocr in all_result_ocr:
        #     total_data = []
        #     max_length = max(len(data) for data in result_ocr)
        #     for i in range(max_length):
        #         sublist = []
        #         for data in result_ocr:
        #             item = data[i][1] if i < len(data) else "-"
        #             sublist.append(item)
        #         total_data.append(sublist)
        #     for row in total_data:
        #         writer.writerow(row)

    # finsih v2 
    with open(f'{path}/output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for result_ocr in all_result_ocr:
            total_data = []
            for sublist in result_ocr:
                if sublist:
                    text_data = []
                    for item in sublist:
                        text_data.append(item[1])
                    total_data.append(" ".join(text_data))
                else:
                    total_data.append("-")
            total_data = [total_data]
            for row in total_data:
                writer.writerow(row)

def get_accuracy(all_result_ocr):
    accuracy_data = {}
    for result_ocr in all_result_ocr:
        for sublist in result_ocr:
            for item in sublist:
                text = item[1]  # Get the recognized text from the tuple
                accuracy = item[2]  # Get the accuracy from the tuple
                if text in accuracy_data:
                    # If the text is already in the dictionary, append the accuracy to its list
                    accuracy_data[text].append(accuracy)
                else:
                    # If the text is not in the dictionary, create a new list for it
                    accuracy_data[text] = [accuracy]
    return accuracy_data

def delete_file(file_path):
    img_files = glob.glob(os.path.join(file_path, '*.jpg'))
    pdf_files = glob.glob(os.path.join(file_path, '*.pdf'))
    # csv_files = glob.glob(os.path.join(file_path, '*.csv'))
    # all_files = img_files + pdf_files + csv_files
    all_files = img_files + pdf_files 
    for file in all_files:
        os.remove(file)


