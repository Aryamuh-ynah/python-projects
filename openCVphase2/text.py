import cv2

img = cv2.imread("phase1/test.png")

if img is not None:
    cv2.putText(img, "Humayra", (53, 56), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 25, 0), 2)
    cv2.imshow("Image with Text", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error: Image not found or unable to load.")