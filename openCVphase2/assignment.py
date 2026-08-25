import cv2

image = input("Enter the path of the image: ")
ima = cv2.imread(image)

if ima is not None:

    print("image loaded successfully.")
    print("What do you want to do with the image?")
    print("1. crop the image\n2. resize the image\n3. convert to grayscale\n4. draw on the image\n5. show the image")

    choice = input("Enter your choice (1, 2, 3, 4, or 5): ")

    match choice:
        case "1":
            x = int(input("Enter the x coordinate of the top-left corner: "))
            y = int(input("Enter the y coordinate of the top-left corner: "))
            w = int(input("Enter the width of the crop: "))
            h = int(input("Enter the height of the crop: "))
            cropped_image = ima[y:y+h, x:x+w]
            cv2.imshow("Cropped Image", cropped_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        case "2":
            new_width = int(input("Enter the new width: "))
            new_height = int(input("Enter the new height: "))
            resized_image = cv2.resize(ima, (new_width, new_height))
            cv2.imshow("Resized Image", resized_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()