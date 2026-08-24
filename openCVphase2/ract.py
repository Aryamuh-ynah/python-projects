import cv2

img = cv2.imread("phase1/test.png")

if img is not None:

    p1 = (64, 50)
    p2 = (200, 100)

    color = (0, 255, 0)  # Green color in BGR
    thickness = 3

    cv2.rectangle(img, p1, p2, color, thickness)

    cv2.imshow("Image with Rectangle", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("Error: Image not found or unable to load.")