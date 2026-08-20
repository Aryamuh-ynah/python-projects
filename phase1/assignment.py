import cv2

image = input("Enter the path of the image: ")
image = cv2.imread(image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


if image is not None:
    print("Image loaded successfully.")
    cv2.imshow("Loaded Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("Failed to load the image.")

print("What would you like to do with the image? \n 1)Save the image \n 2)Convert to grayscale \n 3)Get image dimensions")

press = input("Enter your choice (1, 2, or 3): ")

match press:
    case "1":
        save = cv2.imwrite("phase1/output.png", image)
        if save:
            print("Image saved successfully.")
        else:
            print("Failed to save the image.")
    case "2":
        cv2.imshow("Grayscale Image", gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    case "3":
        h, w, c = image.shape
        print(f"Image dimensions: Height={h}, Width={w}, Channels={c}")

    