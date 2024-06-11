import os, cv2, pytesseract, glob, io
import numpy as np
from PIL import Image
from pytesseract import Output
from PyPDF2  import PdfWriter, PdfReader
from pdf2image import convert_from_path

def check_make_path(path):
  if os.path.exists(path):
    pass
  else:
    os.mkdir(path)
  return path

def get_pdf_text_bulk_pdf(pdf_folder_path, output_path, lang_code, draw_boxes=True):
  _ = check_make_path(output_path)
  out_path_bulk, imgs_path = [], []
  for pdf_path, dirs, files in os.walk(pdf_folder_path):
    for z, file in enumerate(files):
      if not file.lower().endswith('.pdf'):
              continue
      file_path = os.path.join(pdf_path, file)
      out_path = os.path.join(output_path, file)
      pages = convert_from_path(file_path, 500)
      with open(f'{out_path.replace(".pdf", ".txt")}', 'w') as the_file:  # write mode, coz one time
        for pageNum, imgBlob in enumerate(pages):
            text = pytesseract.image_to_string(imgBlob,lang=lang_code)
            if draw_boxes:
              imgs_path.append(draw_bounding_boxes(np.array(imgBlob), output_path, file_name.split('.')[-1], pageNum))
            the_file.write(text)
      out_path_bulk.append(out_path)
  return {'number_of_files': len(out_path_bulk), 'txt_file_path_bulk': out_path_bulk, 'bounding_img_path': imgs_path}

def get_pdf_text(file_pdf, output_path, lang_code, draw_boxes=True):
  imgs_path = []
  if not file_pdf.lower().endswith('.pdf'):
    raise ValueError('File is not a PDF')
  _ = check_make_path(output_path)
  file_name = os.path.basename(file_pdf)
  out_path = os.path.join(output_path, file_name)
  pages = convert_from_path(file_pdf, 500)
  txt_path = f'{out_path.replace(".pdf", ".txt")}'
  with open(txt_path, 'w') as the_file:  # write mode, coz one time
    for pageNum, imgBlob in enumerate(pages):
        text = pytesseract.image_to_string(imgBlob,lang=lang_code)
        if draw_boxes:
          imgs_path.append(draw_bounding_boxes(np.array(imgBlob), output_path, file_name.split('.')[-1], pageNum))
        the_file.write(text)
  return {'bounding_img_path': imgs_path, 'txt_file_path': txt_path}

def draw_bounding_boxes(img, output_path, file_name, pageNum):
  data = pytesseract.image_to_data(img, output_type=Output.DICT)
  n_boxes = len(data["text"])
  for i in range(n_boxes):
    if data["conf"][i] == -1:
        continue
    # Coordinates
    x, y = data["left"][i], data["top"][i]
    w, h = data["width"][i], data["height"][i]

    # Corners
    top_left = (x, y)
    bottom_right = (x + w, y + h)
    # Box params
    green = (0, 255, 0)
    thickness = 3  # pixels

    cv2.rectangle(img=img, pt1=top_left, pt2=bottom_right, color=green, thickness=thickness)
  _ = check_make_path(os.path.join(output_path, 'images_bounding'))
  file_out_folder = os.path.join('images_bounding', file_name+'_bounding_images')
  _ = check_make_path(os.path.join(output_path, file_out_folder))
  output_image_path = "{}/text_with_boxes_{}_{}.jpg".format(file_out_folder, file_name, pageNum)
  out_file = os.path.join(output_path, output_image_path)
  cv2.imwrite(out_file, img)
  return out_file

def scanned_pdf_to_text_searchable_pdf(file_pdf, output_folder_path_img, output_path, lang_code, image_converted_format="png", get_text=True, draw_boxes=False):
  _ = check_make_path(output_path)
  output_folder_path = os.path.join(output_path, output_folder_path_img)
  _ = check_make_path(output_folder_path)
  file_name = os.path.basename(file_pdf).split('.')[0]
  file_out_path = os.path.join(output_folder_path, file_name+'_images')
  _ = check_make_path(file_out_path)
  pages = convert_from_path(file_pdf, output_folder=file_out_path, fmt=image_converted_format)
  pdf_searchable_file = os.path.join(output_path, "searchable_pdf_{}.pdf".format(file_name))
  c = open(pdf_searchable_file, "w+b")
  c.close()
  f = open(pdf_searchable_file, "a+b")
  files = glob.glob(os.path.join(file_out_path, "*.{}".format(image_converted_format))) #os.listdir(file_out_path)
  files.sort()
  raw_pdf = [pytesseract.image_to_pdf_or_hocr(img_file) for img_file in files]
  pdf_writer = PdfWriter()
  for z, pg in enumerate(raw_pdf):
    pdf = PdfReader(io.BytesIO(pg))
    pdf_writer.add_page(pdf.pages[0])
  pdf_writer.write(f)
  f.close()
  text_file = None
  if get_text:
    text_file = get_pdf_text(file_pdf, output_path, lang_code, draw_boxes=draw_boxes)
  return {'file_name':file_name,'img_path': file_out_path, 'pdf_path': pdf_searchable_file, 'number_of_pages':len(raw_pdf), 'text_file': text_file}

def scanned_pdf_to_text_searchable_pdf_bulk(pdf_folder_path, output_folder_path_img, output_path, lang_code, image_converted_format, get_text=True, draw_boxes=False):
  list_files = []
  for pdf_path, dirs, files in os.walk(pdf_folder_path):
    for z, file in enumerate(files):
      if not file.lower().endswith('.pdf'):
              continue
      file_pdf = os.path.join(pdf_path, file)
      list_files.append(scanned_pdf_to_text_searchable_pdf(file_pdf, output_folder_path_img, output_path, lang_code, image_converted_format, get_text, draw_boxes))
  return {'number_files_converted': len(list_files), 'files_details': list_files}