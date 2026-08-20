import cv2


image = cv2.imread("phase1/test.png")

if image is not None:
    cropped = image[50:200, 100:300]  # Crop the region of interest [startY:endY, startX:endX]

    cv2.imshow("Original Image", image)
    cv2.imshow("Cropped Image", cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Image not loaded successfully.")