from django.contrib import admin
#  Notice we ONLY import from .models here. No forms!
from .models import Category, Provider, ProviderBlockedDate ,ProviderWork,Booking

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'availability',
        'is_approved',
        'is_blocked',
        'is_featured',
        'is_bestworker'
    )

    list_filter = (
        'category',
        'availability',
        'is_approved',
        'is_blocked',
        'is_featured',
        'is_bestworker'
    )

    search_fields = ('name', 'phone', 'description')

    prepopulated_fields = {'slug': ('name',)}

    list_editable = (
        'price',
        'availability',
        'is_featured',
        'is_bestworker'
    )

    actions = ['approve_providers','block_providers', 'unblock_providers']
    def block_providers(self, request, queryset):
        queryset.update(is_blocked=True)

    def unblock_providers(self, request, queryset):
        queryset.update(is_blocked=False)

    def approve_providers(self, request, queryset):
        queryset.update(is_approved=True)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']



#  Register the core database Model
@admin.register(ProviderBlockedDate)
class ProviderBlockedDateAdmin(admin.ModelAdmin):
    list_display = ['provider', 'start_time', 'end_time','unavailable_time' ,'reason']

@admin.register(ProviderWork)
class ProviderWorkAdmin(admin.ModelAdmin):

    list_display = ('provider',
        'work_title',
        'customer_name',
        'completed_date',
    )

    list_filter = (
        'completed_date',
    )

    search_fields = (
        'provider__name',
        'work_title',
        'customer_name',
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "customer_name",
        "provider",
        "booking_date",
        "booking_time",
        "status",
    )

    list_filter = (
        "status",
        "booking_date",
    )

    search_fields = (
        "customer_name",
        "provider__name",
    )