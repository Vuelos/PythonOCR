import os
import os.path
from PyPDF2 import PdfFileWriter, PdfFileReader

def split(filename,outdir):
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    if filename.endswith(".pdf"):
        inputpdf = PdfFileReader(open(filename, "rb"))

        for i in range(inputpdf.numPages):
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(i))
            with open("%s\page%s.pdf" % (outdir,i), "wb") as outputStream:
                output.write(outputStream)

def split(filename,outdir,startpage,endpage):
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    if filename.endswith(".pdf"):
        inputpdf = PdfFileReader(open(filename, "rb"))

        for i in range(startpage,endpage):
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(i))
            with open("%s\page%s.pdf" % (outdir,i), "wb") as outputStream:
                output.write(outputStream)

if __name__ == '__main__':
    ##Setear directorio
    directory = r'C:\Workplace'
    outdir = r'C:\Workplace\splits'

    ##Obtengo lista de archivos en directorio
    files = sorted([os.path.join(directory, file) for file in os.listdir(directory)], key=os.path.getctime)

    for filename in files:
        split(filename,outdir)
