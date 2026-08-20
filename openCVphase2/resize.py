import cv2


image = cv2.imread("phase1/test.png")

h, w, c = image.shape

print(f"Image dimensions: Height={h}, Width={w}, Channels={c}")

if image is not None:
    resize = cv2.resize(image, (300, 300)) #w/2 , h/2 can be used to resize the image to half of its original size
    cv2.imshow("Image", image)
    cv2.imshow("Resized Image", resize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()