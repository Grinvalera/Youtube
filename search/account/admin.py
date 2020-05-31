from django.contrib import admin
from .models import Video, VideoInfo, Cart


class VideoInfoAdmin(admin.ModelAdmin):
    exclude = []

    class Meta:
        model = VideoInfo


class VideoInfoAdminInLines(admin.TabularInline):
    model = VideoInfo
    extra = 0


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    exclude = []
    inlines = [VideoInfoAdminInLines]


@admin.register(Cart)
class CartInfoAdmin(admin.ModelAdmin):
    exclude = []




