import cv2
import numpy as np

def process_image(img_path):
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

    cv2.imwrite('shadows_out.png', result)
    cv2.imwrite('shadows_out_norm.png', result_norm)