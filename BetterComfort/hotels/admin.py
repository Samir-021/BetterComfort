from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import *
from django.contrib.admin import ModelAdmin, register

# Change the admin site header and title
admin.site.site_header = _("BetterComfort Administration")
admin.site.site_title = _("BetterComfort Admin Portal")
admin.site.index_title = _("Welcome to BetterComfort Admin")

admin.site.register(HotelRestro)
admin.site.register(FavoriteHotel)
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'rating', 'review_text', 'created_at')  # Fields to display in the list view
    search_fields = ('user__username', 'hotel__name', 'review_text')  # Fields to enable search
    list_filter = ('rating', 'created_at')  # Filters for the list view
    ordering = ('-created_at',)  # Default ordering

admin.site.register(Booking)