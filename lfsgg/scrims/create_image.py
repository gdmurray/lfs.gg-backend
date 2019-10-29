from django.conf import settings
from io import BytesIO
from lfsgg.constants import IMG
from lfsgg.utils import inc
from PIL import Image, ImageFont, ImageDraw
import requests
from django.apps import apps
from io import BytesIO
import boto


def create_image(schedule):
    filename = f"scrim-{schedule.id}.png"
    file = BytesIO()

    team = schedule.team
    # Start Image
    f_scrims = sorted([s for s in schedule.scrims.all()], key=lambda x: x.time)

    image = Image.new(mode="RGB", size=(IMG.IMAGE_WIDTH, IMG.IMAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    chunked_scrims = [f_scrims[i:i + IMG.CHUNK_SIZE] for i in range(0, len(f_scrims), IMG.CHUNK_SIZE)]

    # Keep Track of Drawing Cursor
    cursor = logo_cursor = (IMG.LOGO_OFFSET, IMG.LOGO_OFFSET)

    if team.logo:
        response = requests.get(team.logo.url)
        print(response)
        print(response.content)
        try:
            logo = Image.open(BytesIO(response.content))
        except OSError:
            print("???, ", response)
        else:
            # TODO:  AUTOMATICALLY RESIZE THE LOGO TO 50x50
            logo = logo.resize((IMG.LOGO_WIDTH, IMG.LOGO_HEIGHT), Image.ANTIALIAS)
            image.paste(logo, cursor)

            cursor = inc(cursor, x=(IMG.LOGO_WIDTH + IMG.TITLE_OFFSET))

    draw.text(cursor, f"{team.name} - LFS", fill=IMG.BLACK, font=IMG.TITLE_FONT)

    timezone_text = f"Timezone: {team.teamsettings.timezone}"

    timezone_cursor = (
        IMG.IMAGE_WIDTH - (int(IMG.SUBTITLE_FONT.size / 2) * len(timezone_text) + IMG.LOGO_OFFSET), IMG.LOGO_OFFSET)

    draw.text(timezone_cursor, timezone_text, fill=IMG.SECONDARY_COLOR, font=IMG.SUBTITLE_FONT)

    region_text = f"Region: {team.teamsettings.region}"

    region_cursor = inc(timezone_cursor, x=-(int(IMG.SUBTITLE_FONT.size / 2) * len(region_text) + IMG.TITLE_OFFSET))
    draw.text(region_cursor, region_text, fill=IMG.SECONDARY_COLOR, font=IMG.SUBTITLE_FONT)
    # set cursor to top of current scrim
    starting_cursor = inc(logo_cursor, 0, (IMG.LOGO_HEIGHT + IMG.LOGO_BOTTOM_OFFSET))

    updated_text = f"Last Updated: {schedule.thumbnail_updated.strftime('%m/%d     %-I:%M %p')}"
    updated_cursor = (
        IMG.IMAGE_WIDTH - (int(IMG.LAST_UPDATED_FONT.size / 2) * len(updated_text)),
        IMG.IMAGE_HEIGHT - IMG.LAST_UPDATED_BOTTOM_OFFSET)
    draw.text(updated_cursor, updated_text, fill=IMG.SECONDARY_COLOR, font=IMG.LAST_UPDATED_FONT)

    for panel, scrims in enumerate(chunked_scrims):
        # Increment X if # 2
        cursor = inc(starting_cursor,
                     x=((IMG.SCRIM_TIME_WIDTH + IMG.SCRIM_DATE_WIDTH + IMG.SCRIM_X_OFFSET) * panel))
        print("Panel Cursor, ", cursor)

        previous_notes = False
        for row, scrim in enumerate(scrims):
            # Increment Y
            # y_offset = IMG.SCRIM_Y_NOTES_OFFSET if previous_notes else IMG.SCRIM_Y_OFFSET

            inner_cursor = inc(cursor, y=((IMG.SCRIM_Y_OFFSET + IMG.SCRIM_DATE_HEIGHT) * row))
            notes_cursor = inc(inner_cursor, y=IMG.SCRIM_DATE_HEIGHT)
            # Draw Date Box
            draw.rectangle([inner_cursor, inc(inner_cursor, IMG.SCRIM_DATE_WIDTH, IMG.SCRIM_DATE_HEIGHT)],
                           fill=IMG.SCRIM_DATE_COLOR, outline=IMG.BLACK)

            draw.text(inc(inner_cursor, IMG.SCRIM_DATE_X_INNER, IMG.SCRIM_DATE_Y_INNER),
                      f"{scrim.get_time().strftime('%m/%d')}", fill=IMG.SCRIM_FONT_COLOR, font=IMG.SCRIM_FONT)

            # Set to next pointer
            inner_cursor = inc(inner_cursor, IMG.SCRIM_DATE_WIDTH)

            # Draw Time Box
            draw.rectangle([inner_cursor, inc(inner_cursor, IMG.SCRIM_TIME_WIDTH, IMG.SCRIM_TIME_HEIGHT)],
                           fill=IMG.BLACK)

            draw.text(inc(inner_cursor, IMG.SCRIM_TIME_X_INNER, IMG.SCRIM_TIME_Y_INNER),
                      f"{scrim.get_time().strftime('%-I:%M %p').lower()}", fill=IMG.SCRIM_FONT_COLOR,
                      font=IMG.SCRIM_FONT)

            if scrim.request_notes:
                draw.rectangle([notes_cursor, inc(notes_cursor, x=IMG.SCRIM_NOTES_WIDTH, y=IMG.SCRIM_NOTES_HEIGHT)],
                               fill=IMG.WHITE, outline=IMG.BLACK)
                draw.text(inc(notes_cursor, x=(IMG.SCRIM_NOTES_WIDTH - (
                        IMG.NOTES_FONT.getsize(scrim.request_notes)[0] + IMG.SCRIM_NOTES_PADDING))),
                          scrim.request_notes, fill=IMG.BLACK, font=IMG.NOTES_FONT)

            print("Inner Cursor, ", inner_cursor)

    image = image.resize((IMG.OG_IMAGE_WIDTH, IMG.OG_IMAGE_HEIGHT), Image.ANTIALIAS)
    image.save(file, format="PNG")
    file.seek(0)

    return file, filename
