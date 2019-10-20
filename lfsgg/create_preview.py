from PIL import ImageDraw, Image, ImageFont
import datetime
import math
import os

IMAGE_WIDTH = 560
IMAGE_HEIGHT = 300
DEFAULT_OFFSET = 10
CONTENT_OFFSET = 25
SCRIM_OFFSET = 50
LOGO_SIZE = 30
WHITE = (255, 255, 255)
filename = "scrim01.png"
TITLE_FONT = ImageFont.truetype("fonts/Helvetica.ttf", 24)
CONTENT_FONT = ImageFont.truetype("fonts/Helvetica.ttf", 18)
WATERMARK_FONT = ImageFont.truetype("fonts/Helvetica.ttf", 16)
# twitter text color => fill=(136, 153, 166)
image = Image.new(mode="RGB", size=(560, 300), color=(21, 32, 43))
draw = ImageDraw.Draw(image)


def create_scrim_text(scrim):
    return f"{scrim['date'].strftime('%-m/%d %-I%p').replace('PM', 'pm').replace('AM', 'am')} - {scrim['notes']}"


scrims = [
    {
        "date": datetime.datetime(day=21, month=10, year=2019, hour=20, minute=0),
        "notes": "2 maps"
    },
    {
        "date": datetime.datetime(day=22, month=10, year=2019, hour=21, minute=30),
        "notes": "warmup scrim"
    },
    {
        "date": datetime.datetime(day=23, month=10, year=2019, hour=20, minute=15),
        "notes": None
    }
]
logo = Image.open("hawk.jpg", 'r')
img_w, img_h = logo.size
print(img_w, img_h)
logo = logo.resize((LOGO_SIZE, LOGO_SIZE), Image.ANTIALIAS)
left_l = math.ceil(len(scrims) / 2)
right_l = math.floor(len(scrims) / 2)
print(left_l, right_l)
image.paste(logo, (DEFAULT_OFFSET, DEFAULT_OFFSET))

draw.text((DEFAULT_OFFSET * 2 + LOGO_SIZE, 15), "WLU Esports - LFS", fill=(255, 255, 255), font=TITLE_FONT)

SUBTITLE_OFFSET = DEFAULT_OFFSET * 2 + LOGO_SIZE
draw.text((CONTENT_OFFSET, SUBTITLE_OFFSET), "Available Scrims", fill=(255, 255, 255),
          font=CONTENT_FONT)

for i, scrim in enumerate(scrims[:left_l]):
    HEIGHT_OFFSET = SUBTITLE_OFFSET + (SCRIM_OFFSET * (i + 1))
    print(HEIGHT_OFFSET)
    draw.text((CONTENT_OFFSET, HEIGHT_OFFSET), create_scrim_text(scrim), fill=WHITE,
              font=CONTENT_FONT)

for j, scrim in enumerate(scrims[right_l:]):
    WIDTH_OFFSET = IMAGE_WIDTH / 2
    HEIGHT_OFFSET = SUBTITLE_OFFSET + (SCRIM_OFFSET * (j + 1))
    draw.text((WIDTH_OFFSET, HEIGHT_OFFSET), create_scrim_text(scrim), fill=WHITE, font=CONTENT_FONT)

text_length = (IMAGE_WIDTH - int(16 / 2) * len("lfs.gg"), IMAGE_HEIGHT - (16 + DEFAULT_OFFSET))
draw.text(text_length, "lfs.gg", fill=(255, 255, 255), font=WATERMARK_FONT)
image.save(filename)
