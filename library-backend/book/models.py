from django.db import models


class Book(models.Model):
    title = models.TextField(blank=True, null=True)
    subtitle = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    pub_date = models.CharField(max_length=255, blank=True, null=True)
    pages = models.CharField(max_length=255, blank=True, null=True)
    book_price = models.CharField(max_length=255, blank=True, null=True)
    book_img = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.TextField(blank=True, null=True)
    isbn = models.CharField(max_length=50, blank=True, null=True)
    zt_num = models.CharField(max_length=30)
    book_intro = models.TextField(blank=True, null=True)
    author_intro = models.TextField(blank=True, null=True)
    book_catalog = models.TextField(blank=True, null=True)
    book_url = models.CharField(max_length=500, blank=True, null=True)
    douban_res_msg = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=50, blank=True, null=True)
    db_score = models.FloatField(blank=True, null=True)
    emotion_1 = models.IntegerField(blank=True, null=True)
    emotion_2 = models.IntegerField(blank=True, null=True)
    emotion_3 = models.IntegerField(blank=True, null=True)
    emotion_4 = models.IntegerField(blank=True, null=True)
    emotion_5 = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "总图书信息"
        verbose_name_plural = verbose_name
        ordering = ['zt_num']

    def __str__(self):
        book_info = " - "
        seq = (self.title, self.author, self.zt_num, self.isbn)  # 字符串序列
        return book_info.join(seq)


class NewBook(models.Model):
    title = models.TextField(blank=True, null=True)
    subtitle = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    pub_date = models.CharField(max_length=255, blank=True, null=True)
    pages = models.CharField(max_length=255, blank=True, null=True)
    book_price = models.CharField(max_length=255, blank=True, null=True)
    book_img = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.TextField(blank=True, null=True)
    isbn = models.CharField(max_length=50, blank=True, null=True)
    zt_num = models.CharField(max_length=30)
    book_intro = models.TextField(blank=True, null=True)
    author_intro = models.TextField(blank=True, null=True)
    book_catalog = models.TextField(blank=True, null=True)
    book_url = models.CharField(max_length=500, blank=True, null=True)
    douban_res_msg = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=50, blank=True, null=True)
    db_score = models.FloatField(blank=True, null=True)
    emotion_1 = models.IntegerField(blank=True, null=True)
    emotion_2 = models.IntegerField(blank=True, null=True)
    emotion_3 = models.IntegerField(blank=True, null=True)
    emotion_4 = models.IntegerField(blank=True, null=True)
    emotion_5 = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "新书de 信息"
        verbose_name_plural = verbose_name
        ordering = ['zt_num']

    def __str__(self):
        book_info = " - "
        seq = (self.title, self.author, self.zt_num, self.isbn)  # 字符串序列
        return book_info.join(seq)


class RecommendBook(models.Model):
    title = models.TextField(blank=True, null=True)
    subtitle = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    pub_date = models.CharField(max_length=255, blank=True, null=True)
    pages = models.CharField(max_length=255, blank=True, null=True)
    book_price = models.CharField(max_length=255, blank=True, null=True)
    book_img = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.TextField(blank=True, null=True)
    isbn = models.CharField(max_length=50, blank=True, null=True)
    zt_num = models.CharField(max_length=30)
    book_intro = models.TextField(blank=True, null=True)
    author_intro = models.TextField(blank=True, null=True)
    book_catalog = models.TextField(blank=True, null=True)
    book_url = models.CharField(max_length=500, blank=True, null=True)
    douban_res_msg = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=50, blank=True, null=True)
    db_score = models.FloatField(blank=True, null=True)
    emotion_1 = models.IntegerField(blank=True, null=True)
    emotion_2 = models.IntegerField(blank=True, null=True)
    emotion_3 = models.IntegerField(blank=True, null=True)
    emotion_4 = models.IntegerField(blank=True, null=True)
    emotion_5 = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "推荐书籍信息"
        verbose_name_plural = verbose_name
        ordering = ['zt_num']

    def __str__(self):
        book_info = " - "
        seq = (self.title, self.author, self.zt_num, self.isbn)  # 字符串序列
        return book_info.join(seq)

