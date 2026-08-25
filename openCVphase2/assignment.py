import cv2

image = input("Enter the path of the image: ")
ima = cv2.imread(image)
red = (0, 0, 255)
green = (0, 255, 0)
pink = (255, 0, 255)
blue = (255, 0, 0)
yellow = (0, 250, 250)

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

        case "3":
            gray_img = cv2.cvtColor(ima, cv2.COLOR_BAYER_BG2BGR)
            cv2.imshow("Grayscale Image", gray_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        case "4":
            print("what do you want to draw on the image?\n 1. Line\n2. Rectangle\n3. Circle\n4. Text")
            draw_choice = input("Enter your choice (1, 2, 3, or 4): ")
            color_choice = input("Choose a color (red, green, pink, blue, yellow): ").lower()
            match draw_choice:
                case "1":
                    x1 = int(input("Enter the x coordinate of the starting point: "))
                    y1 = int(input("Enter the y coordinate of the starting point: "))
                    x2 = int(input("Enter the x coordinate of the ending point: "))
                    y2 = int(input("Enter the y coordinate of the ending point: "))
                    cv2.line(ima, (x1, y1), (x2, y2), eval(color_choice), 2)
                    cv2.imshow("Image with Line", ima)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                case "2":
                    x1 = int(input("Enter the x coordinate of the top-left corner: "))
                    y1 = int(input("Enter the y coordinate of the top-left corner: "))
                    x2 = int(input("Enter the x coordinate of the bottom-right corner: "))
                    y2 = int(input("Enter the y coordinate of the bottom-right corner: "))
                    cv2.rectangle(ima, (x1, y1), (x2, y2), eval(color_choice), 2)
                    cv2.imshow("Image with Rectangle", ima)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                case "3":
                    x = int(input("Enter the x coordinate of the center: "))
                    y = int(input("Enter the y coordinate of the center: "))
                    radius = int(input("Enter the radius of the circle: "))
                    thickness = int(input("Enter the thickness of the circle (use -1 for filled): "))
                    cv2.circle(ima, (x, y), radius, eval(color_choice), thickness)
                    cv2.imshow("Image with Circle", ima)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                case "4":
                    text = input("Enter the text to draw: ")
                    x = int(input("Enter the x coordinate of the bottom-left corner of the text: "))
                    y = int(input("Enter the y coordinate of the bottom-left corner of the text: "))
                    font_scale = float(input("Enter the font scale (e.g., 1.0): "))
                    thickness = int(input("Enter the thickness of the text: "))
                    cv2.putText(ima, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, eval(color_choice), thickness)
                    cv2.imshow("Image with Text", ima)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
        case "5":
            cv2.imshow("Loaded Image", ima)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    print("Do you want to save the image? (yes/no): ")
    save_choice = input().lower()
    if save_choice == "yes":
        cv2.imwrite("output_image.jpg", ima)
        print("Image saved as output_image.jpg")

else:
    print("Failed to load the image.")