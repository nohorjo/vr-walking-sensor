from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

disp = adafruit_ssd1306.SSD1306_I2C(128, 64, busio.I2C(SCL, SDA))
font = ImageFont.load_default()

image = Image.new("1", (disp.width, disp.height))
draw = ImageDraw.Draw(image)

def clear():
    disp.fill(0)
    disp.show()

def show():
    disp.image(image)
    disp.show()

# 21x7 grid
def text(string, line):
    if line >= 7 or line < 0:
        raise Exception('Invalid line number: %d'%(line))
    #  if len(string) > 21:
        #  raise Exception('String too long')
    y = line * 9
    draw.rectangle((0, y, 128, y + 9), outline=0, fill=0)
    draw.text((0, y), string, font=font, fill=255)
