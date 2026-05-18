from django.contrib import admin
from .models import Song

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'genre', 'payment_status', 
                   'approval_status', 'uploaded_at']
    list_filter = ['payment_status', 'approval_status', 'genre']
    search_fields = ['title', 'artist__stage_name']
    list_per_page = 20

    # Quick Action Buttons
    actions = ['approve_songs', 'reject_songs', 'mark_as_paid']

    def approve_songs(self, request, queryset):
        queryset.update(approval_status='approved')
        self.message_user(request, f"{queryset.count()} song(s) approved successfully!")
    approve_songs.short_description = "✅ Approve Selected Songs"

    def reject_songs(self, request, queryset):
        queryset.update(approval_status='rejected')
        self.message_user(request, f"{queryset.count()} song(s) rejected.")
    reject_songs.short_description = "❌ Reject Selected Songs"

    def mark_as_paid(self, request, queryset):
        queryset.update(payment_status='paid')
        self.message_user(request, f"{queryset.count()} song(s) marked as paid!")
    mark_as_paid.short_description = "💰 Mark as Paid"