import os
import PDFSplitter
import shadowRemover
import PDFimageExtractor

if __name__ == '__main__':
    # Separar paginas de archivos--------------------------------
    # Setear directorios
    file = r'C:\Workplace\InputDecripted.pdf'
    outdir = r'C:\Workplace\splits'
    startpage = 117
    endpage = 119

    # Separar paginas deseadas
    PDFSplitter.split(file,outdir,startpage,endpage)
    # PDFSplitter.split(file,outdir)

    # Convertir paginas a imagenes------------------------------------
    # Setear directorio
    directory = r'C:\Workplace\splits'
    outdir = r'C:\Workplace\imageExtract'
    ##Obtengo lista de archivos en directorio
    files = sorted([os.path.join(directory, file) for file in os.listdir(directory)], key=os.path.getctime)

    for filename in files:
        PDFimageExtractor.imageExtract(filename,outdir)


    # # Corregir sombras en hojas------------------------------------
    # # Setear directorios
    directory = r'C:\Workplace\imageExtract'
    outdir = r'C:\Workplace\shadowfix'
    ##Obtengo lista de archivos en directorio
    files = sorted([os.path.join(directory, file) for file in os.listdir(directory)], key=os.path.getctime)
    
    for filename in files:
        shadowRemover.identifytext(filename,outdir)
        shadowRemover.shadowfix(filename,outdir)
        shadowRemover.saltandpepperfix(filename,outdir)
        shadowRemover.spfix(filename,outdir)
