import numpy as np
import cv2 as cv
import os, sys

from multiprocessing import Pool, Queue

def init_pool(d_b):
    global detection_buffer
    detection_buffer = d_b

def crop_to_object(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

    cnts = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x,y,w,h = cv.boundingRect(c)
        if w > (img.shape[1]/8) or h > (img.shape[0]/8):
            #print("(x,y,w,h): " + str((x,y,w,h)))
            break

    print("Cropping to "+str(w)+" x "+str(h))
    img = img[y-50:y+h+50, x-50:x+w+50]
    return img

def grabCutSeperation(img):
    mask = np.zeros(img.shape[:2],np.uint8)    
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    rect = (1,1,img.shape[1],img.shape[0])
    cv.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = img*mask2[:,:,np.newaxis]
    return img

def floodFill(img, thresh):
    th, im_th = cv.threshold(img, thresh, 255, cv.THRESH_BINARY_INV);

    im_floodfill = im_th.copy()

    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    cv.floodFill(im_floodfill, mask, (0,0), 255)

    im_floodfill_inv = cv.bitwise_not(im_floodfill)

    im_out = img | im_floodfill_inv
   
    return im_out

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 Cropper.py <path to folder with jpg/png> [(-f) || (-g)}")
        sys.exit(1)

    print("Start Batch Background Removal")
    outDir = sys.argv[1]+ "processed"
    if(not os.path.isdir(outDir)):
        os.mkdir(outDir)

    for filename in os.listdir(sys.argv[1]):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".JPG") or filename.endswith(".PNG") or filename.endswith(".tiff") or filename.endswith(".tif"):
            print("Processing: " + filename)
            print("read image")
            img = cv.imread(sys.argv[1] + "/" + filename)

            img = crop_to_object(img)

            if len(sys.argv) > 2 and sys.argv[2] == "-g":
                img = grabCutSeperation(img)
            elif len(sys.argv) > 2 and sys.argv[2] == "-f":
                img = floodFill(img, 208)
                

            print("write image")
            cv.imwrite(outDir + "/" + filename, img)
            print("Done: " + filename)
        
        
        
        
        
        
#        img = cv2.imread(sys.argv[1] + "/" + filename)
#        # First Convert to Grayscale
#        myimage_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    
#        ret,baseline = cv2.threshold(myimage_grey,127,255,cv2.THRESH_TRUNC)
#    
#        ret,background = cv2.threshold(baseline,126,255,cv2.THRESH_BINARY)
#    
#        ret,foreground = cv2.threshold(baseline,126,255,cv2.THRESH_BINARY_INV)
#    
#        foreground = cv2.bitwise_and(img,img, mask=foreground)  # Update foreground with bitwise_and to extract real foreground
#    
#        # Convert black and white back into 3 channel greyscale
#        background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)
#        # Combine the background and foreground to obtain our final image
#        finalimage = background+foreground
#
#        print("write image")
#        cv2.imwrite(outDir + "/" + filename, finalimage)
#        print("Done: " + filename)
           
        
        
        
        
        
        
