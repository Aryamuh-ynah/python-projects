import qrcode as qr
from PIL import Image


img = qr.make("https://www.youtube.com/watch?v=FOGRHBp6lvM&list=PLjVLYmrlmjGfAUdLiF2bQ-0l8SwNZ1sBl")
img.save("qrcode.png")


#color qr code
q = qr.QRCode( version=1, error_correction=qr.constants.ERROR_CORRECT_H, 
box_size=10, border=4)

data = input("Enter the data or link to generate QR code: ")

q.add_data(data)
q.make(fit=True)
img = q.make_image(fill_color="red", back_color="black")
img.save("colored_qrcode.png")
