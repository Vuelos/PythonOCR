import os
import fitz

def imageExtract(filename,outdir):
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    doc = fitz.open(filename)
    page = doc.loadPage(0)  # number of page
    pix = page.getPixmap()

    cleanname  = os.path.basename(filename).split(".")[0]
    pix.writePNG("%s\\%s.png" % (outdir,cleanname))
        
if __name__ == '__main__':
    ##Setear directorio
    directory = r'C:\Workplace\splits'
    outdir = r'C:\Workplace\imageExtract'
    ##Obtengo lista de archivos en directorio
    files = sorted([os.path.join(directory, file) for file in os.listdir(directory)], key=os.path.getctime)

    for filename in files:
        imageExtract(filename,outdir)

