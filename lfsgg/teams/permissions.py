from .models import TeamManagement
from lfsgg.constants import ManagementRole, ManagementStatus


def user_belongs_to_team(user, team):
    try:
        management = TeamManagement.objects.get(user=user, team=team,
                                                status=ManagementStatus.APPROVED,
                                                role__in=[ManagementRole.OWNER,
                                                          ManagementRole.USER,
                                                          ManagementRole.PLAYER])
    except TeamManagement.DoesNotExist:
        return False
    else:
        return True


