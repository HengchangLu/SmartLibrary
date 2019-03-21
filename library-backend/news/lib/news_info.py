import re
from django.forms import model_to_dict
from news.models import NoticeNews, SourceNews, LectureNews, ServiceSummaryNews
import requests
from bs4 import BeautifulSoup


class NewsInfo(object):
    news_url = 'http://www.lib.sdu.edu.cn/portal/tpl/home/'

    def __init__(self, current_tab, page_num):
        self.current_tab = current_tab
        self.page_num = page_num

    def update_news(self):
        target_model = [[LectureNews, SourceNews][self.current_tab == 2], NoticeNews][self.current_tab == 1]
        for page_num in range(1, self.page_num):
            res = requests.get(self.news_url + 'newslist?type={0}&p={1}'.format(self.current_tab, page_num))
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')

            news_list = [target_model(time=soup.select('.article li')[i].text.split()[0],
                                           title=''.join(item for item in soup.select('.article li')[i].text.split()[1:-1]),
                                           url=self.news_url + soup.select('.article li')[i].select('a')[0]['href'])
                          for i in range(len(soup.select('.article li')))
                          if not target_model.objects.filter(url=self.news_url + soup.select('.article li')[i].select('a')[0]['href']).exists()]
            target_model.objects.bulk_create(news_list)

    def get_news_list(self, news_page_num, callback_count):
        target_model = [[LectureNews, SourceNews][self.current_tab == 2], NoticeNews][self.current_tab == 1]
        news = target_model.objects.all()[(news_page_num - 1) * callback_count: (news_page_num - 1) * callback_count + callback_count]
        # if news.count() > news_page_num * callback_count:
        #     news = news[(news_page_num - 1) * callback_count: (news_page_num - 1) * callback_count + callback_count]
        # else:
        #     if news_page_num == 1:
        #         news = news
        #     else:
        #         news = news[(news_page_num - 1) *callback_count: news.count()]
        news_list = []
        for item in news:
            item = model_to_dict(item)
            news_list.append(item)

        return news_list

    def get_news_detail(self, news_id):
        target_model = [[LectureNews, SourceNews][self.current_tab == 2], NoticeNews][self.current_tab == 1]
        news_info = target_model.objects.filter(current_tab=self.current_tab, id=news_id)
        url = model_to_dict(news_info[0])['url']
        res = requests.get(url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        temp_content = soup.select('.article div[style="font-size:11pt;"] ')
        content = ' '.join(item for item in str(temp_content[0]).split())
        content = re.sub(r"<.?o:p>", "", content)
        content = re.sub(r"<.?xml:namespace prefix.*?>", "", content)
        try:
            attachment_content = str(soup.select('h3')[0])
            document_content = str(soup.select('.article a[href]')[0])
        except IndexError:
            return {
                    'result': True,
                    'url': url,
                    'content': content
            }
        else:
            return {
                    'result': True,
                    'url': url,
                    'content': content + ' ' + attachment_content + ' ' + document_content
            }

    @staticmethod
    def get_summary_service(url):
        # title = request.GET.get('title')
        # url = request.GET.get('url')
        # if url == '':
        #     search_article = ServiceSummaryNews.objects.get(title=title)
        #     url = search_article.url
        res = requests.get(url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.select('.article h2[align="center"]')[0].text
        time = soup.select('.article div[align="center"]')[0].text.split()[1]
        temp_content = soup.select('.article div[style="font-size:11pt;"] ')
        content = ' '.join(item for item in str(temp_content[0]).split())
        content = content.replace('font-family: 仿宋;', '').replace('FONT-FAMILY: 仿宋;', '')
        content = re.sub(r"<.?xml:namespace prefix.*?>", '', content)
        content = re.sub(r"<.?o:p>", "", content)

        response = {
            'result': True,
            'title': title,
            'time': time,
            'url': url,
            'content': content,
        }
        return response
