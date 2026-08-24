import cv2

img = cv2.imread("phase1/test.png")

if img is not None:
    cv2.circle(img, (53,56), 44, (0, 255, 0), -1)  # Draw a filled green circle
    cv2.imshow("Image with Circle", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error: Image not found or unable to load.")