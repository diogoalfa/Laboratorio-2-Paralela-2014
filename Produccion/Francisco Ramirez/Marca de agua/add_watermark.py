from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from StringIO import StringIO
from PIL import Image

WATERMARK_PATH = "inputs/watermark.png"
PDF_PATH = "inputs/pdfdoc.tex.pdf"
OUTPUT_FILE = "outputs/WMpdfdoc.tex.pdf"

# Use PyPDF to merge the image-PDF into the template
infile = PdfFileReader(file(PDF_PATH, "rb"))
num_pages = infile.getNumPages()
# set up output file
output = PdfFileWriter()
for i in xrange(num_pages):
    # get page data
    page = infile.getPage(i)
    imgTemp = StringIO()
    imgDoc = canvas.Canvas(imgTemp)
    page_width, page_height = page.mediaBox.upperRight
    page_width = float(page_width)
    page_height = float(page_height)
    # get watermark image data
    watermark_image = Image.open(WATERMARK_PATH)
    wm_width, wm_height = watermark_image.size
    wm_width = float(wm_width)
    wm_height = float(wm_height)
    xpos = 0.5*(page_width - wm_width)
    ypos = 0.5*(page_height - wm_height)
    # Draw image on Canvas and save PDF in buffer
    imgPath = WATERMARK_PATH
    imgDoc.drawImage(imgPath, xpos, ypos, wm_width, wm_height, mask='auto')
    #imgDoc.drawImage(imgPath, 399, 760, 160, 160)    ## at (399,760) with size 160x160
    imgDoc.save()
    # operate on page of PDF
    overlay = PdfFileReader(StringIO(imgTemp.getvalue())).getPage(0)
    page.mergePage(overlay)
    output.addPage(page)


#Save the result to a file
output.write(file(OUTPUT_FILE, "w"))
