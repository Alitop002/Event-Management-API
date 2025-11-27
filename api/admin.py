from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Event, Ticket, Booking, Category


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('phone', 'address', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Status', {'fields': ('status',)}),
    )
    list_display = ('username', 'email', 'status', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('email',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'update_at')
    list_display = ('title', 'user', 'category', 'start_time', 'end_time', 'created_at')
    search_fields = ('title', 'user__username', 'category__name')
    list_filter = ('category', 'start_time', 'end_time')
    ordering = ('-start_time',)
    fieldsets = (
        (None, {'fields': ('user', 'title', 'description', 'category')}),
        ('Timing', {'fields': ('start_time', 'end_time')}),
        ('Timestamps', {'fields': ('created_at', 'update_at')}),
    )

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'price', 'quantity', 'created_at', 'updated_at')
    search_fields = ('name', 'event__title')
    list_filter = ('event',)
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('event', 'name', 'price', 'quantity')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticket', 'quantity', 'booked_at')
    search_fields = ('user__username', 'ticket__name', 'ticket__event__title')
    list_filter = ('ticket__event', 'booked_at')
    ordering = ('-booked_at',)
    fieldsets = (
        (None, {'fields': ('user', 'ticket', 'quantity')}),
        ('Timestamps', {'fields': ('booked_at',)}),
    )