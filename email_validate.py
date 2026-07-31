email = input("Enter your email address: ")


if len(email) < 6:
    print("Email address is too short.")
elif "@" not in email or "." not in email:
    print("Invalid email address.")

else:
    print("Your email address is valid.")

