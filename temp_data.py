import os
import tempfile
from io import BytesIO

from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
import random
import string


def generate_random_string(length=8):
    """Generate a random string of fixed length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_random_number_string(length):
    """Generate a random string of digits of fixed length."""
    return ''.join(random.choices(string.digits, k=length))


def generate_unique_username(usernames):
    """Generate a unique username."""
    while True:
        username = generate_random_string()
        if username not in usernames:
            return username


def generate_unique_thaicitizenshipid(thai_citizenship_ids):
    """Generate a unique Thai citizenship ID."""
    while True:
        thaicitizenshipid = generate_random_number_string(13)

        try:
            checksum_thai_national_id(thaicitizenshipid)  # Validate the full 13-digit ID
            if thaicitizenshipid not in thai_citizenship_ids:
                return thaicitizenshipid
        except ValidationError:
            continue


def checksum_thai_national_id(value):
    """Validate the checksum of a Thai National ID."""
    if len(value) != 13 or not value.isdigit():
        raise ValidationError("Thai National ID must be exactly 13 digits.")

    # Calculate checksum
    weights = range(13, 1, -1)  # Weights from 13 down to 2
    checksum = sum(int(value[i]) * weights[i] for i in range(12)) % 11
    checksum = (11 - checksum) % 10  # Adjust checksum: if 10 -> 0, if 11 -> 1

    # Compare with the last digit
    if checksum != int(value[12]):
        raise ValidationError("Invalid Thai National ID checksum.")


def generate_secure_password():
    """
    Generate a secure password meeting Django's default requirements:
    - At least 8 characters long
    - Includes uppercase, lowercase, numbers, and special characters
    """
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    while True:
        password = ''.join(random.choices(chars, k=12))
        # Ensure the password has at least one of each type of character
        if (any(c.islower() for c in password) and
                any(c.isupper() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in "!@#$%^&*()-_=+" for c in password)):
            return password


def generate_email_from_username(username):
    """
    Generate an email address from the username.
    """
    return f"{username}@gmail.com"


def create_user(UserModel, image):
    """Create a user with a unique username and Thai citizenship ID."""
    username = generate_unique_username(UserModel)
    email = generate_email_from_username(username)
    password = generate_secure_password()
    phone_number = generate_random_number_string(10)
    thaicitizenshipid = generate_unique_thaicitizenshipid(UserModel)

    # Create the user
    user = UserModel.objects.create(
        username=username,
        password=password,
        email=email,
        phone_number=phone_number,
        thai_citizenship_id=thaicitizenshipid,
        thai_citizenship_id_image=image
    )
    return user


def create_temp_image_file():
    """
    Creates a temporary image file to simulate an upload for Selenium testing.
    Returns the file path of the created image.
    """
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)  # Prevent automatic deletion

    # Create an image using Pillow
    image = Image.new('RGB', (100, 100), color='blue')
    image.save(temp_file, format='PNG')

    # Return the file path
    temp_file.close()  # Close the file so it can be accessed by other processes
    return temp_file.name

def del_temp_image_file(filename):
    # if created image found, remove it
    if os.path.exists(filename):
        os.remove(filename)
