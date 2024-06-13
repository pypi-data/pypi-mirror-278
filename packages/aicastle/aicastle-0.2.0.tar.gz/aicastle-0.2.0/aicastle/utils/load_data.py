import os
import requests
from PIL import Image
import base64
from io import BytesIO

class ImageLoader:
    def __init__(self, image_path, image=None, original_format=None):
        self.image_path = image_path
        self.image = image if image else self.load_image()
        self.original_format = original_format if original_format else self.image.format
    
    def load_image(self):
        if os.path.isfile(self.image_path):
            image = Image.open(self.image_path)
        else:
            response = requests.get(self.image_path)
            image_data = BytesIO(response.content)
            image = Image.open(image_data)
        return image
    
    def get_base64(self, format='JPEG'):
        with BytesIO() as buffer:
            image = self.convert_image_format(self.image, format)
            image.save(buffer, format=format)
            img_str = base64.b64encode(buffer.getvalue())
        return img_str.decode('utf-8')
    
    def convert_image_format(self, image, format):
        if format == 'JPEG':
            return image.convert('RGB')
        elif format == 'GIF':
            return image.convert('P', palette=Image.ADAPTIVE)
        elif format == 'PNG':
            return image.convert('RGBA')
        return image
    
    def get_original_format(self):
        return self.original_format
    
    def resize(self, width, height):
        resized_image = self.image.resize((width, height))
        return ImageLoader(self.image_path, resized_image, self.original_format)
    
    def save_image(self, save_path, format=None):
        if format is None:
            format = self.original_format
        image = self.convert_image_format(self.image, format)
        with BytesIO() as buffer:
            image.save(buffer, format=format)
            with open(save_path, 'wb') as f:
                f.write(buffer.getvalue())
    
    def get_data_url(self, format='JPEG'):
        base64_image = self.get_base64(format)
        mime_type = f"image/{format.lower()}"
        return f"data:{mime_type};base64,{base64_image}"