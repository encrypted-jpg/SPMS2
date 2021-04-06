from django.contrib import admin

from .models import *

from apps.compPage.models import *
from apps.coursePage.models import *
from apps.partyPage.models import *
from apps.suggestionPortal.models import *
from apps.userPortal.models import *

admin.site.register(Member)
admin.site.register(NewUser)
admin.site.register(Committee)
admin.site.register(Coordinator)
admin.site.register(Manager)
admin.site.register(Competition)
admin.site.register(Game)
admin.site.register(Ticket)
admin.site.register(Course)
admin.site.register(Event)
admin.site.register(Feedback)
admin.site.register(Slot)
admin.site.register(Memberslot)
admin.site.register(Compslot)
admin.site.register(Gameslot)
admin.site.register(Courseslot)
admin.site.register(Eventslot)
admin.site.register(Membership_form)
admin.site.register(Message)
admin.site.register(EventBooking)
