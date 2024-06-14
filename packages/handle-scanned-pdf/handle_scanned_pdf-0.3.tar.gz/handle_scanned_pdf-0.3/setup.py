from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

project_urls = {
    "Source Code": "https://github.com/sxaxmz/handle_scanned_pdf"  # Replace with your actual project URL
}

# entry_points={'console_scripts':["get_text_single", "get_text_bulk", "get_searchable_single", "get_searchable_bulk"]}
setup(name='handle_scanned_pdf', 
      version='0.3', 
      packages=find_packages(),
      install_requires=['pytesseract >= 0.3.10', 'pdf2image >= 1.17.0', 'PyPDF2 >= 3.0.1', 'opencv-python'],
      long_description=description,
      long_description_content_type='text/markdown',
      project_urls=project_urls)