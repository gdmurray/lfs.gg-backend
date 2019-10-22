from django.core.management.base import BaseCommand

from lfsgg.scrims.models import Scrim, Schedule
from lfsgg.scrims.create_image import create_image


class Command(BaseCommand):
    help = 'Help Text'

    def handle(self, *args, **options):
        # sched_id = "a6162acc-f467-11e9-b2b9-469ea25f7e20"
        sched_id = "2385b356-f3c3-11e9-b2b9-469ea25f7e20"

        schedule = Schedule.objects.get(id=sched_id)
        file, filename = create_image(schedule)
        with open('newgen.png', 'wb') as f:
            f.write(file.read())
