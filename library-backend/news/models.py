from django.db import models


class NoticeNews(models.Model):
    time = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    # is_save = models.BooleanField(default=False)
    current_tab = models.IntegerField(default=1)

    class Meta:
        verbose_name = "图书馆公告消息"
        verbose_name_plural = verbose_name
        ordering = ['-time', 'title']

    def __str__(self):
        book_info = "  "
        seq = (self.time, self.title, self.url)
        return book_info.join(seq)


class SourceNews(models.Model):
    time = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    # is_save = models.BooleanField(default=False)
    current_tab = models.IntegerField(default=2)

    class Meta:
        verbose_name = "图书馆资源动态"
        verbose_name_plural = verbose_name
        ordering = ['-time', 'title']

    def __str__(self):
        book_info = "  "
        seq = (self.time, self.title, self.url)
        return book_info.join(seq)


class LectureNews(models.Model):
    time = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    # is_save = models.BooleanField(default=False)
    current_tab = models.IntegerField(default=3)

    class Meta:
        verbose_name = "图书馆讲座信息"
        verbose_name_plural = verbose_name
        ordering = ['-time', 'title']

    def __str__(self):
        book_info = "  "
        seq = (self.time, self.title, self.url)
        return book_info.join(seq)


class ServiceSummaryNews(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)

    class Meta:
        verbose_name = "服务 交流 图书馆概况 信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        service_summary_news = "  "
        seq = (self.title, self.url)
        return service_summary_news.join(seq)
