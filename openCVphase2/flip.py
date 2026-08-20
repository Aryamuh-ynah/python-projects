import cv2


image = cv2.imread("phase1/test.png")

h, w, c = image.shape

print(f"Image dimensions: Height={h}, Width={w}, Channels={c}")

if image is not None:
    flipH = cv2.flip(image, 1)  # Flip the image horizontally
    flipV = cv2.flip(image, 0)  # Flip the image vertically
    flipB = cv2.flip(image, -1)  # Flip the image both horizontally and vertically

    cv2.imshow("Original Image", image)
    cv2.imshow("Flipped Horizontally", flipH)
    cv2.imshow("Flipped Vertically", flipV)
    cv2.imshow("Flipped Both", flipB)
    cv2.waitKey(0)
    cv2.destroyAllWindows()