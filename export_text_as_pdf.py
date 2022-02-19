def export_text_as_pdf(algorithms_results):
    # Python program to convert
    # text file to pdf file

    from fpdf import FPDF

    # save FPDF() class into
    # a variable pdf
    #FPDF(orientation='P', unit='mm', format='A4')
    # save FPDF() class into
    # a variable pdf
    pdf = FPDF(orientation = 'P', unit = 'mm', format='A4')

    # Add a page
    pdf.add_page()
    '''pdf = FPDF()
    pdf.add_page()

    for title, result in algorithms_results:
        text2 = result.encode('latin-1', 'replace').decode('latin-1')
        pdf = add_algorithm_result(pdf, title, text2)'''
    for title, result in algorithms_results:
        text2 = result.encode('latin-1', 'replace').decode('latin-1')
        text = split_text_to_pdf(text2)
        #write_to_pdf(text2, "algorithms_results.pdf")
        pdf = save_to_pdf(pdf, title, text)

    # save the pdf with name .pdf
    pdf.output("algorithms_results.pdf")


def split_text_to_pdf(text):
    word_count = 9
    splitted_text = text.split()
    number_rep = int(len(splitted_text)/word_count)
    res = []
    start = 0
    for i in range(1, number_rep+1):
        end = word_count*i
        if(i==number_rep):
            if(end>len(splitted_text)):
                end = splitted_text

        tt = splitted_text[start:end]
        if(len(tt)>72):
            end = end-1
            tt = splitted_text[start:end]

        res.append(" ".join(tt))
        start = end
        if(len(splitted_text)>end and i==number_rep):
            res.append(" ".join(splitted_text[start:]))
    return res


def add_algorithm_result(pdf, title, result):
    # Add a page

    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size=12)

    # insert the texts in pdf
    pdf.cell(200, 10, txt=result)

    return pdf

def save_to_pdf(pdf, title, text):
    from fpdf import FPDF

    # set style and size of font
    # that you want in the pdf
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt=title, ln=1, align='L')

    #pdf.cell(40, 10, title)

    pdf.set_font("Arial", size=15)

    # insert the texts in pdf
    for x in text:
        pdf.cell(200, 10, txt=x, ln=1, align='L')

    pdf.ln(20)

    return pdf

def write_to_pdf(text, file_path):
    from PyPDF2 import PdfFileWriter, PdfFileReader
    import io
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(10, 100, text)
    can.save()


    # move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(file_path, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open("destination.pdf", "wb")
    output.write(outputStream)
    outputStream.close()