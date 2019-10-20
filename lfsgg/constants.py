import pytz

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
