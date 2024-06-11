from .handle_scanned_pdf import get_pdf_text, get_pdf_text_bulk_pdf, draw_bounding_boxes, scanned_pdf_to_text_searchable_pdf, scanned_pdf_to_text_searchable_pdf_bulk
import numpy as np
import os, cv2

# Get text in Bulk from Multiple PDF files
pdf_folder_path = 'pdf_files'
output_path = 'output'
lang_code = 'ara'
draw_boxes = True
get_pdf_text_bulk_pdf(pdf_folder_path, output_path, lang_code, draw_boxes)

'''
{'number_of_files': 1,
 'txt_file_path_bulk': ['output/sample_.pdf'],
 'bounding_img_path': ['output/images_bounding/text_with_boxes_3ba4c1f1-775f-4e05-ab48-a40617087a57-1_0.jpg',
  'output/images_bounding/text_with_boxes_3ba4c1f1-775f-4e05-ab48-a40617087a57-1_1.jpg',
  'output/images_bounding/text_with_boxes_3ba4c1f1-775f-4e05-ab48-a40617087a57-1_2.jpg',
  'output/images_bounding/text_with_boxes_3ba4c1f1-775f-4e05-ab48-a40617087a57-1_3.jpg',
  'output/images_bounding/text_with_boxes_3ba4c1f1-775f-4e05-ab48-a40617087a57-1_4.jpg']}
'''

# Get text from single PDF file
pdf_path_ = 'sample_.pdf'
output_path = 'output'
lang_code = 'ara'
draw_boxes = True
get_pdf_text(pdf_path_, output_path, lang_code, draw_boxes)

'''
{'bounding_img_path': ['output/images_bounding/pdf_bounding_images/text_with_boxes_pdf_0.jpg',
  'output/images_bounding/pdf_bounding_images/text_with_boxes_pdf_1.jpg',
  'output/images_bounding/pdf_bounding_images/text_with_boxes_pdf_2.jpg',
  'output/images_bounding/pdf_bounding_images/text_with_boxes_pdf_3.jpg',
  'output/images_bounding/pdf_bounding_images/text_with_boxes_pdf_4.jpg'],
 'txt_file_path': 'output/sample_.txt'}
'''

# Get bounding boxes on text that can be extracted from PDF
img_path = 'output/img/sample__images/3ba4c1f1-775f-4e05-ab48-a40617087a57-1.png'
img = np.array(cv2.imread(img_path)) # Read image and convert to numpy array
output_path = 'output'
file_name = os.path.basename(img_path).split('.')[0]
pageNum = 0
draw_bounding_boxes(img, output_path, file_name, pageNum)

'''
output/images_bounding/3ba4c1f1-775f-4e05-ab48-a40617087a57-1_bounding_images/text_with_boxes_3ba4c1f1-775f-4e05-ab48-a40617087a57-1_0.jpg
'''

# Extract text, draw bounding boxes, and convert PDF file to text searchable PDF
file_pdf = 'sample_.pdf'
output_folder_path_img = 'img'
output_path = 'output'
lang_code = 'ara'
image_converted_format = 'png'
get_text=True
draw_boxes=False
scanned_pdf_to_text_searchable_pdf(file_pdf, output_folder_path_img, output_path, lang_code, image_converted_format, get_text, draw_boxes)

'''
{'file_name': 'sample_',
 'img_path': 'output/img/sample__images',
 'pdf_path': 'output/searchable_pdf_sample_.pdf',
 'number_of_pages': 5,
 'text_file': {'bounding_img_path': [],
  'txt_file_path': 'output/sample_.txt'}}
'''

# Extract text, draw bounding boxes, and convert PDF file to text searchable PDF in Bulk
pdf_folder_path = 'pdf_files'
output_folder_path_img = 'img'
output_path = 'output'
lang_code = 'ara'
image_converted_format = 'png'
get_text=True
draw_boxes=False
scanned_pdf_to_text_searchable_pdf_bulk(pdf_folder_path, output_folder_path_img, output_path, lang_code, image_converted_format, get_text, draw_boxes)

'''
{'number_files_converted': 1,
 'files_details': [{'file_name': 'sample_',
   'img_path': 'output/img/sample__images',
   'pdf_path': 'output/searchable_pdf_sample_.pdf',
   'number_of_pages': 5,
   'text_file': {'bounding_img_path': [],
    'txt_file_path': 'output/sample_.txt'}}]}
'''