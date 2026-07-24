import random

password = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%^&*()_+-=[]}{|;:',.<>?/`~qwertyuiopasdfghjklzxcvbnm"
length = int(input("Enter the length of password: "))

a = "".join(random.sample(password, length))
print("Your password is: ", a) 
