import numpy as np
import cv2
import imutils
import base64
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def getNewImageName():
    listImages = os.listdir("readImages")
    formatedList = []
    for img in listImages:
        formatedList.append(int(img.replace(".jpg", "")))

    nextName = max(formatedList) + 1
    return 'readImages/' + str(nextName) + '.jpg'


def processImage(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayBilateral = cv2.bilateralFilter(gray, 11, 17, 17)
    cv2.imwrite(getNewImageName(), gray)
    cv2.imwrite(getNewImageName(), grayBilateral)
    return gray, grayBilateral


def findContours(image):
    edged = cv2.Canny(image, 170, 200)
    new, cnts, _ = cv2.findContours(
        edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imwrite(getNewImageName(), edged)
    return cnts


def findPlate(contours, image):
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:30]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(c)
            return image[y:y + h, x:x + w]


def processPlate(plate):
    thresh = cv2.threshold(
        plate, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    cv2.imwrite(getNewImageName(), invert)
    return invert


def readb64(base64_string):
    encoded_data = base64_string.split(',')[1]
    npArray = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(npArray, cv2.IMREAD_COLOR)
    return img


def carPlateString(base64Img):
    image = readb64(base64Img)
    grayImage, lessDetailsImage = processImage(image)
    contours = findContours(lessDetailsImage)
    croppedPlate = findPlate(contours, grayImage)
    processedPlate = processPlate(croppedPlate)
    plateText = pytesseract.image_to_string(processedPlate, config='--psm 11')

    if plateText:
        return plateText

    return "No plate"
