from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal

def layout_analysis(path, as_object=False, as_list=False):
    ### 1.a) convert text from pdf (using pdfminer)
    #Create resource manager
    rsrcmgr = PDFResourceManager()
    # Set parameters for analysis.
    laparams = LAParams()
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages_content = []
    pages_content_as_lines = []
    for page in PDFPage.get_pages(path):
        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()
        text_elements = []
        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):
                text_elements.append(element)

        ### 1.b) text reconstruction
        text_elements_ordered = order_pdfminer_text_page(text_elements, as_object=as_object)
        if(not as_list and not as_object):
            pages_content.append("".join(text_elements_ordered))
        else:
            pages_content_as_lines.append(text_elements_ordered)

    return "".join(pages_content) if(not as_list and not as_object) else pages_content_as_lines



def order_pdfminer_text_page(page_text_elements, as_object=False):
    max_column_number = ""
    x_thresh = 50
    page_text_ordered = 0
    xs = []
    found = False
    for i in range(len(page_text_elements)):
        element = page_text_elements[i]
        l_x = element.x0
        l_y = element.y0
        found = False
        if(len(xs)!=0):
            for column_xs_i in range(len(xs)):
                 column_xs = xs[column_xs_i]
                 for x_existant_i in range(len(column_xs)):
                     x_existant = column_xs[x_existant_i]
                     if(abs(x_existant[0]-l_x)<x_thresh):
                         xs[column_xs_i]+=[[l_x, l_y, i]]
                         found=True
                         break
                 if(found):
                     break

            if(not found):
                xs += [[[l_x, l_y, i]]]

        else:
            xs += [[[l_x, l_y, i]]]


    columns_to_sort = [xs[i][0] + [i] for i in range(len(xs))]
    columns_sorted = sorted(columns_to_sort, key=lambda x: x[:][0], reverse=False)
    elements_sorted_by_column = [xs[i[3]] for i in columns_sorted]
    #sort by Y
    text = []
    for column in elements_sorted_by_column:
        for element in column:
            text.append(page_text_elements[element[2]].get_text() if(not as_object) else page_text_elements[element[2]])

    return text

'''
    #xs_sorted = sorted(xs, key=lambda x: x[:][0], reverse=True)
    ys_sorted = sorted(xs, key=lambda y: y[:][1], reverse=True)
        columns_to_sort = [ys_sorted[i][0]+[i] for i in range(len(ys_sorted))]
            all_sorted = [ys_sorted[i[2]] for i in columns_sorted]


'''