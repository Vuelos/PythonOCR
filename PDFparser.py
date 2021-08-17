import os
from pdfminer.high_level import extract_text

def parse(directory):
    ##obtengo ful paths
    files = sorted([os.path.join(directory, file) for file in os.listdir(directory)], key=os.path.getctime)
    ##patron a buscar
    ##pattern = r'[0-9]{58}'
    text = ""
    print("Iniciando proceso")
    ##barras = []
    ##para cada archivo en carpeta
    for filename in files:
        if filename.endswith(".pdf"):

            print("Analizando archivo: " + filename)

            ##extraer texto
            text = extract_text(filename)
            print("Texto extraido")
            
            outfilename = filename + ".txt"
            with open(outfilename, "w", encoding="utf-8") as output:
                output.write(text)
            #encontrar matcheos de regex
            ##matchs = re.findall(pattern, text)
            ##print("Regular Expression")
            ##print(matchs)

            #agregar a la salida
            ##barras.extend(matchs)
        else:
            continue

def parse(files):
    ##patron a buscar
    ##pattern = r'[0-9]{58}'
    text = ""
    print("Iniciando proceso")
    ##barras = []
    ##para cada archivo en carpeta
    for filename in files:
        if filename.endswith(".pdf"):

            print("Analizando archivo: " + filename)

            ##extraer texto
            text = extract_text(filename)
            print("Texto extraido")
            
            outfilename = filename + ".txt"
            with open(outfilename, "w", encoding="utf-8") as output:
                output.write(text)
            #encontrar matcheos de regex
            ##matchs = re.findall(pattern, text)
            ##print("Regular Expression")
            ##print(matchs)

            #agregar a la salida
            ##barras.extend(matchs)
        else:
            continue    

if __name__ == '__main__':
    directory = r'C:\Workplace\splits'
    parse(directory)
