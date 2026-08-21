import cv2

img = cv2.imread("phase1/test.png")

if img is not None:

    p1 = (100, 100)
    p2 = (240, 40)
    color = (225, 0, 0)  # Blue color in BGR
    thikness = 2

    cv2.line(img, p1, p2, color, thikness)

    cv2.imshow("Image with Line", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("Error: Image not found or unable to load.")