import os
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw


class ImageMaker:

    def __init__(self):

        self.image = 'image.jpg'
        self.font_path = "Roboto-Medium.ttf"

    def weather_card(self, data):
        for postcard_description in data:
            colored_image = self.background_gradient(weather_description=data[postcard_description][2])
            open_cv_image = np.array(colored_image)
            open_cv_image = open_cv_image[:, :, ::-1].copy()
            font = ImageFont.truetype(self.font_path, 32)
            img_pil = Image.fromarray(open_cv_image)
            draw = ImageDraw.Draw(img_pil)
            draw.text((250, 40), str(data[postcard_description][0]), font=font, fill=(0, 0, 0))
            draw.text((270, 100), str(data[postcard_description][1]), font=font, fill=(255, 137, 0))
            draw.text((270, 135), str(data[postcard_description][2]), font=font, fill=(255, 137, 0))
            img = np.array(img_pil)
            w_sign = cv2.imread(self.weather_sign, cv2.IMREAD_UNCHANGED)
            scale_percent = 50
            width = int(w_sign.shape[1] * scale_percent / 100)
            height = int(w_sign.shape[0] * scale_percent / 100)
            size = (width, height)
            weather_sign = cv2.resize(w_sign, size)
            weather_sign = np.array(weather_sign)
            x = y = 50
            img[y:y + weather_sign.shape[0], x:x + weather_sign.shape[1]] = weather_sign

            out_path = r'weather_images'
            if not os.path.exists(out_path):
                os.makedirs(out_path)
                self.save_image(out_path=out_path, saved_image=img, filename=str(postcard_description))
            if os.path.exists(out_path):
                self.save_image(out_path=out_path, saved_image=img, filename=str(postcard_description))

    def save_image(self, out_path, saved_image, filename):
        cv2.imwrite(os.path.join(out_path, (filename + '.jpg')), saved_image)

    def background_gradient(self, weather_description):
        background_color = cv2.imread(self.image)
        i = 0
        k = 0
        for _ in range(50):
            if 'Ясно' in weather_description:
                background_color[:, 0 + i:70 + i] = (255, 255, 125 + k)
                self.weather_sign = 'weather_signs/sun.jpg'
            elif 'Дождь' in weather_description:
                background_color[:, 0 + i:70 + i] = (125 + k, 125 + k, 255)
                self.weather_sign = 'weather_signs/rain.jpg'
            elif 'Снег' in weather_description:
                background_color[:, 0 + i:70 + i] = (125 + k, 255, 255)
                self.weather_sign = 'weather_signs/snow.jpg'
            elif 'Малооблачно' or 'Облачно' or 'Пасмурно' in weather_description:
                background_color[:, 0 + i:70 + i] = (128 + k, 128 + k, 128 + k)
                self.weather_sign = 'weather_signs/cloud.jpg'
            i += 20
            k += 5

        return background_color
