import base64

from elasticsearch import helpers, Elasticsearch
import PyPDF2
import json

def read_pdf(file_path):
    '''

    :param file_path:
    :return: return base64 encoded pdf
    '''
    pdf_reader = PyPDF2.PdfFileReader(file_path)

    # get document metadeta
    meta_data = pdf_reader.getDocumentInfo()

    # get number of pages
    num = pdf_reader.getNumPages()

    # create a dictionary object for page data
    all_pages = {}

    # put meta data into a dict key
    all_pages["meta"] = {}

    # Use 'iteritems()` instead of 'items()' for Python 2
    for meta, value in meta_data.items():
        print(meta, value)
        all_pages["meta"][meta] = value

    # iterate the page numbers
    for page in range(num):
        data = pdf_reader.getPage(page)
        # page_mode = read_pdf.getPageMode()

        # extract the page's text
        page_text = data.extractText()

        # put the text data into the dict
        all_pages[page] = page_text

    # create a JSON string from the dictionary
    json_data = json.dumps(all_pages)
    print("\nJSON:", json_data)

    bytes_string = bytes(json_data, 'utf-8')
    print("\nbytes_string:", bytes_string)

    encoded_pdf = base64.b64encode(bytes_string).decode('utf-8')
    # encoded_pdf = base64.b64encode(bytes_string)
    encoded_pdf = str(encoded_pdf)
    print("\nbase64:", encoded_pdf)

    # put the PDF data into a dictionary body to pass to the API request
    body_doc = {"data": encoded_pdf}

    return body_doc