import cv2
image = cv2.imread("phase1/qrcode.png")

if image is not None:
    cv2.imshow("Showing Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Image not loaded successfully.")

