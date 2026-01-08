# from django.contrib import admin
# from .models import UserProfile, ContactMessage

# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'email', 'phone')
#     search_fields = ('name', 'email')
#     list_filter = ('name',)
#     ordering = ('id',)

# @admin.register(ContactMessage)
# class ContactMessageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'email', 'subject', 'is_read', 'created_at')
#     search_fields = ('name', 'email', 'subject')
#     list_filter = ('is_read', 'created_at')
#     ordering = ('-created_at',)
#     readonly_fields = ('created_at',)
    
#     # Mark messages as read/unread from admin
#     actions = ['mark_as_read', 'mark_as_unread']
    
#     def mark_as_read(self, request, queryset):
#         queryset.update(is_read=True)
#     mark_as_read.short_description = "Mark selected messages as read"
    
#     def mark_as_unread(self, request, queryset):
#         queryset.update(is_read=False)
#     mark_as_unread.short_description = "Mark selected messages as unread"


from django.contrib import admin
from .models import UserProfile, ContactMessage, Traveler


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'date_of_birth')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('date_of_birth',)
    ordering = ('id',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'email',
        'subject',
        'is_read',
        'created_at',
    )
    search_fields = ('name', 'email', 'subject')
    list_filter = ('is_read', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)

    mark_as_unread.short_description = "Mark selected messages as unread"


@admin.register(Traveler)
class TravelerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'destination',
        'email',
        'phone',
        'user',
        'created_at',
    )
    search_fields = ('name', 'email', 'destination', 'user__username')
    list_filter = ('destination', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
