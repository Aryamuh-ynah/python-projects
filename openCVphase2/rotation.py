import cv2


image = cv2.imread("phase1/test.png")

h, w, c = image.shape

print(f"Image dimensions: Height={h}, Width={w}, Channels={c}")

if image is not None:
    (h, w) = image.shape[:2]

    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, 45, 1.0)  # Rotate by 45 degrees
    rotated = cv2.warpAffine(image, M, (w, h))

    cv2.imshow("Original Image", image)
    cv2.imshow("Rotated Image", rotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Image not loaded successfully.")