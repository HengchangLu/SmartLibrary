from django.contrib import admin
from .models import NoticeNews, LectureNews, SourceNews, ServiceSummaryNews


admin.site.register(NoticeNews)
admin.site.register(LectureNews)
admin.site.register(SourceNews)
admin.site.register(ServiceSummaryNews)


class ServiceSummaryNewsAdmin(admin.ModelAdmin):
    list_display = ('title', )

    def save_model(self, request, obj, form, change):
        re = super(ServiceSummaryNews, self).save_model(request, obj, form, change)
