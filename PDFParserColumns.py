import os

from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTPage, LTChar, LTAnno, LAParams, LTTextBox, LTTextLine
from pdfminer.pdfpage import PDFPage

from pdfminer.high_level import extract_text

class PDFPageDetailedAggregator(PDFPageAggregator):
    def __init__(self, rsrcmgr, pageno=1, laparams=None):
        PDFPageAggregator.__init__(self, rsrcmgr, pageno=pageno, laparams=laparams)
        self.rows = []
        self.page_number = 0
    def receive_layout(self, ltpage):        
        def render(item, page_number):
            if isinstance(item, LTPage) or isinstance(item, LTTextBox):
                for child in item:
                    render(child, page_number)
            elif isinstance(item, LTTextLine):
                child_str = ''
                for child in item:
                    if isinstance(child, (LTChar, LTAnno)):
                        child_str += child.get_text()
                child_str = ' '.join(child_str.split()).strip()
                if child_str:
                    row = (page_number, item.bbox[0], item.bbox[1], item.bbox[2], item.bbox[3], child_str) # bbox == (x1, y1, x2, y2)
                    self.rows.append(row)
                for child in item:
                    render(child, page_number)
            return
        render(ltpage, self.page_number)
        self.page_number += 1
        self.rows = sorted(self.rows, key = lambda x: (x[0], -x[2]))
        self.result = ltpage
		
def writefile(path, a):
    with open(path, "w", encoding="utf-8") as output:
        for line in a:
            for block in line:
                output.write(block[5] + " ")
            output.write("\n")
            
#Ordeno bloques en lineas por Xinicio
def orderlines(a):
    #Ordeno bloques en lineas por Xinicio
    for linea in a:
        
        n = len(linea) 
      
        # Traverse through all array elements 
        for i in range(n-1): 
        # range(n) also work but outer loop will repeat one time more than needed. 
      
            # Last i elements are already in place 
            for j in range(0, n-i-1): 
      
                # traverse the array from 0 to n-i-1 
                # Swap if the element found is greater 
                # than the next element 
                if linea[j][1] > linea[j+1][1]  : 
                    linea[j], linea[j+1] = linea[j+1], linea[j] 
  
def block2line(a):
    Xdes = 0
    Ydes = 0.3

    YdesJump = 8

    out = []
    newline = []
    # Separo los blockes en lineas
    for i, block in enumerate(a):
        if i != 0:
        # Si el bloque tiene una altura distinta que el anterior corresponde a la siguiente linea
            Ydif = abs(block[4] - a[i-1][4])
            if Ydif > Ydes :
                # Por cada 9 de dif hago un salto de linea
                for _ in range(int(Ydif) // YdesJump):
                    out.append(newline)
                    newline = []
                
                newline.append(block);
            else:
                newline.append(block);
        else:
            newline.append(block);
    out.append(newline)
    newline = []  
    return out

def parseColumns(directory):
    ##obtengo ful paths
    files = sorted([os.path.join(directory, file) for file in os.listdir(directory)], key=os.path.getctime)
    print("Iniciando proceso")
    ##barras = []
    ##para cada archivo en carpeta
    for filename in files:
        if filename.endswith(".pdf"):
            print("Analizando archivo: " + filename)
            
            fp = open(filename, 'rb')
            parser = PDFParser(fp)
            doc = PDFDocument(parser)
            # doc.initialize() # leave empty for no password

            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageDetailedAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
                # receive the LTPage object for this page
                device.get_result()

            # Si esta en la mitad izquiera va a page1 sino a page2
            page1blocks = []
            page2blocks = []

            for i, block in enumerate(device.rows):
                if block[1] < 445:
                    page1blocks.append(block)
                else:
                    page2blocks.append(block)
                    
                    
            # Ordenar bloques en lineas
            # Desviacion Horizontal y vertical para salto de linea

            page1lines = block2line(page1blocks)
            page2lines = block2line(page2blocks)


            #Ordeno bloques en lineas por Xinicio
            orderlines(page1lines)
            orderlines(page2lines)

            # Escribir en salida
            page1txt = outfilename = filename + "-1.txt"
            page2txt = outfilename = filename + "-2.txt"

            writefile(page1txt, page1lines)
            writefile(page2txt, page2lines)

if __name__ == '__main__':
    directory = r'C:\Users\Agus\Desktop\Scripts\Python\pdf\split'
    parseColumns(directory)