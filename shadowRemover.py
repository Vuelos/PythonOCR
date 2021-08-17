import cv2
import numpy as np
import os

def identifytext(img_path,outdir):
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    # Read image from which text needs to be extracted
    img = cv2.imread(img_path)
    
    # Preprocessing the image starts
    
    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    
    # Specify structure shape and kernel size. 
    # Kernel size increases or decreases the area 
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect 
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 5))
    
    # Appplying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    
    # # Finding contours
    # contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    # # Creating a copy of image
    # im2 = img.copy()
    
    # # A text file is created and flushed
    # file = open("recognized.txt", "w+")
    # file.write("")
    # file.close()

    cleanname  = os.path.basename(img_path).split(".")[0]
    cv2.imwrite("%s\\txt_%s.png" % (outdir,cleanname), dilation)

def saltandpepperfix(img_path,outdir):
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    image = cv2.imread(img_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
    opening = 255 - cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    cleanname  = os.path.basename(img_path).split(".")[0]
    cv2.imwrite("%s\\sp_%s.png" % (outdir,cleanname), opening)

def spfix(img_path,outdir):
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        if cv2.contourArea(c) < 10:
            cv2.drawContours(thresh, [c], -1, (0,0,0), -1)

    result = 255 - thresh

    cleanname  = os.path.basename(img_path).split(".")[0]
    cv2.imwrite("%s\\sp2_%s.png" % (outdir,cleanname), result)

def shadowfix(img_path,outdir):
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
        
    # Load the input image as grayscale.
    img = cv2.imread(img_path, -1)

    rgb_planes = cv2.split(img)

    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        # Dilate the image, in order to get rid of the text. This step somewhat helps to preserve the bar code.
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        #Median blur the result with a decent sized kernel to further suppress any text.
        # This should get us a fairly good background image that contains all the shadows and/or discoloration.
        bg_img = cv2.medianBlur(dilated_img, 21)
        # Calculate the difference between the original and the background we just obtained. The bits that are identical will be black (close to 0 difference), the text will be white (large difference).
        # Since we want black on white, we invert the result.
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        # Normalize the image, so that we use the full dynamic range.
        norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)

    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)

    cleanname  = os.path.basename(img_path).split(".")[0]

    cv2.imwrite("%s\\o_%s.png" % (outdir,cleanname), result)
    cv2.imwrite("%s\\norm_%s.png" % (outdir,cleanname), result_norm)
    # cv2.imwrite('shadows_out.png', result)
    # cv2.imwrite('shadows_out_norm.png', result_norm)

if __name__ == '__main__':
    ##Setear directorio
    directory = r'C:\Workplace\imageExtract'
    outdir = r'C:\Workplace\shadowfix'

    ##Obtengo lista de archivos en directorio
    files = sorted([os.path.join(directory, file) for file in os.listdir(directory)], key=os.path.getctime)

    for filename in files:
        saltandpepperfix(filename,outdir)
