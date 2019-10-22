import pytz
from PIL import ImageFont

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class Region:
    NA = "NA"
    EU = "EU"
    LATAM = "LATAM"
    APAC = "APAC"
    CHOICES = (
        (NA, "NA"),
        (EU, "EU"),
        (LATAM, "LATAM"),
        (APAC, "APAC")
    )


class ManagementStatus:
    APPLIED = "APPLIED"  # Applied for management of team
    APPROVED = "APPROVED"  # Either staff or Owner approved
    DECLINED = "DECLINED"  # Either staff or Owner said no
    CREATED = "CREATED"  # User created the team -->
    CHOICES = (
        (APPLIED, "Applied"),
        (APPROVED, "Approved"),
        (DECLINED, "Declined"),
        (CREATED, "Created")
    )


class ManagementRole:
    OWNER = "OWNER"
    USER = "USER"
    CHOICES = (
        (OWNER, "Owner"),
        (USER, "User")
    )


REGION_AGGREGGATION = {
    "ANZ": "APAC",
    "South Korea": "APAC",
    "Japan": "APAC",
    "SEA": "APAC"
}


class IMG:
    MULTIPLIER = 5
    P = "fonts/Poppins"
    OG_IMAGE_WIDTH = 966
    OG_IMAGE_HEIGHT = 518
    IMAGE_WIDTH = OG_IMAGE_WIDTH * MULTIPLIER
    IMAGE_HEIGHT = OG_IMAGE_HEIGHT * MULTIPLIER

    CHUNK_SIZE = 5

    LOGO_OFFSET = 40 * MULTIPLIER
    LOGO_WIDTH = LOGO_HEIGHT = 50 * MULTIPLIER

    TITLE_OFFSET = 20 * MULTIPLIER

    TITLE_FONT = ImageFont.truetype(f"{P}/Poppins-SemiBold.ttf", 28 * MULTIPLIER)
    SUBTITLE_FONT = ImageFont.truetype(f"{P}/Poppins-Regular.ttf", 18 * MULTIPLIER)
    LAST_UPDATED_FONT = ImageFont.truetype(f"{P}/Poppins-Regular.ttf", 12 * MULTIPLIER)
    SCRIM_FONT = ImageFont.truetype(f"{P}/Poppins-SemiBold.ttf", 24 * MULTIPLIER)
    NOTES_FONT = ImageFont.truetype(f"{P}/Poppins-Regular.ttf", 14 * MULTIPLIER)

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    SECONDARY_COLOR = (164, 164, 164)
    SCRIM_DATE_COLOR = (175, 175, 175)
    SCRIM_FONT_COLOR = WHITE

    SCRIM_DATE_HEIGHT = 50 * MULTIPLIER
    SCRIM_DATE_WIDTH = 90 * MULTIPLIER

    SCRIM_TIME_WIDTH = 170 * MULTIPLIER
    SCRIM_TIME_HEIGHT = SCRIM_DATE_HEIGHT

    SCRIM_DATE_X_INNER = 13 * MULTIPLIER
    SCRIM_DATE_Y_INNER = 9 * MULTIPLIER

    SCRIM_TIME_X_INNER = 30 * MULTIPLIER
    SCRIM_TIME_Y_INNER = SCRIM_DATE_Y_INNER

    SCRIM_X_OFFSET = 50 * MULTIPLIER
    SCRIM_Y_OFFSET = 30 * MULTIPLIER
    # SCRIM_Y_NOTES_OFFSET = 35 * MULTIPLIER

    SCRIM_NOTES_HEIGHT = 20 * MULTIPLIER
    SCRIM_NOTES_WIDTH = SCRIM_DATE_WIDTH + SCRIM_TIME_WIDTH
    SCRIM_NOTES_PADDING = 3 * MULTIPLIER

    LOGO_BOTTOM_OFFSET = 15 * MULTIPLIER

    SCRIM_BOTTOM_OFFSET = 30 * MULTIPLIER

    LAST_UPDATED_BOTTOM_OFFSET = 50 * MULTIPLIER
