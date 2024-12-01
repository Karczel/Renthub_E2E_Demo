from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


def create_temp_image_file():
    """
    Creates a temporary image file to simulate an upload for testing.
    Returns a SimpleUploadedFile object that can be assigned to an ImageField.
    """
    # Create an image using Pillow
    temp_file = BytesIO()
    image = Image.new('RGB', (100, 100), color='blue')
    image.save(temp_file, format='PNG')
    temp_file.seek(0)  # Rewind the BytesIO object to the start

    # Wrap the BytesIO content in a SimpleUploadedFile, simulating a real file upload
    return SimpleUploadedFile('temp_image.png', temp_file.read(), content_type='image/png')
