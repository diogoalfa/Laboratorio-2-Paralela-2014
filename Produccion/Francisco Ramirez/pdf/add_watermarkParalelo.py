from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from StringIO import StringIO
from PIL import Image
import time
from mpi4py import MPI
starting_point=time.time()
comm = MPI.COMM_WORLD  # comunicador entre dos procesadores
rank = comm.rank     # id procesador actual
size = comm.size     # cantidad de procesadores a usar
WATERMARK_PATH = "inputs/agua3.png"
PDF_PATH = "inputs/pdfdoc.tex.pdf"
OUTPUT_FILE = "outputs/asd.pdf"

# Use PyPDF to merge the image-PDF into the template
infile = PdfFileReader(file(PDF_PATH, "rb"))
# print "infile: ",infile

num_pages = infile.getNumPages()
# print "num_pages: ", num_pages

# set up output file
output = PdfFileWriter()
watermark_image = Image.open(WATERMARK_PATH)
wm_width, wm_height = watermark_image.size
wm_width = float(wm_width)
# print wm_width
wm_height = float(wm_height)
# print wm_height

for i in xrange(num_pages):
    # get page data
    page = infile.getPage(i)
    # print "page: ",page
    imgTemp = StringIO()
    # print "imgTemp :",imgTemp
    imgDoc = canvas.Canvas(imgTemp)
    page_width, page_height = page.mediaBox.upperRight
    page_width = float(page_width)
    page_height = float(page_height)
    # print "width,height: ",page_width," ",page_height

    # get watermark image data
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

if rank == 0:
    #Save the result to a file
    output.write(file(OUTPUT_FILE, "w"))
    elapsed_time=time.time()-starting_point
    print ""
    print "Total Time [seconds]: " + str(elapsed_time)
