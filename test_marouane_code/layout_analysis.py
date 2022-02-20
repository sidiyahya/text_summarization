from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal

def layout_analysis(path):
    #Create resource manager
    rsrcmgr = PDFResourceManager()
    # Set parameters for analysis.
    laparams = LAParams()
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(path):
        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()
        text_elements = []
        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):
                text_elements.append(element.get_text())

        text_elements_ordered = order_pdfminer_text_page(text_elements)


def order_pdfminer_text_page(page_text):
    max_column_number = ""
    thresh = 0
    page_text_ordered =