from django.contrib import admin
from .models import User, Category, Outfit, Booking, LateFee

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone', 'is_staff']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_per_day', 'size', 'stock']
    list_filter = ['category', 'size']
    search_fields = ['name', 'description']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'outfit', 'start_date', 'end_date', 'status', 'total_price']
    list_filter = ['status', 'start_date']
    search_fields = ['user__username', 'outfit__name']
    actions = ['mark_as_confirmed', 'mark_as_returned']

    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='Confirmed')
    mark_as_confirmed.short_description = "Mark selected bookings as Confirmed"

    def mark_as_returned(self, request, queryset):
        queryset.update(status='Returned')
    mark_as_returned.short_description = "Mark selected bookings as Returned"

@admin.register(LateFee)
class LateFeeAdmin(admin.ModelAdmin):
    list_display = ['booking', 'days_late', 'fee_amount', 'paid']
    list_filter = ['paid']
