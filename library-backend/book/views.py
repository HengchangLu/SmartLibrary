import json
from django.forms import model_to_dict
from django.http import HttpResponse
from .models import Book, NewBook, RecommendBook
from django.db.models import Q
from lib.base.exceptions import RequestParamError
from .lib.book_info import BookBorrowed, BookInfo
from lib.base.base_lib import api_response


def book_info(request):
    """
    :param request:
                search_content：用户输入的关键词
                search_ISBN：用户输入的ISBN码
    :return:
    """
    response_list = []
    search_content = request.GET.get('searchContent', '')
    search_ISBN = request.GET.get('ISBN', '')
    if search_ISBN == '':
        info = Book.objects.filter(name__icontains=search_content)
    else:
        info = Book.objects.filter(ISBN=search_ISBN)

    for item in info:
        info = model_to_dict(item)
        response_list.append(info)
    response = {
        'result': True,
        'list': response_list
    }
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@api_response
def borrowed_book(request):
    """
    获取该用户的借书列表
    :param request:
                    account：校园卡账号
                    password：校园卡查询密码
    :return:
    """
    try:
        account = request.GET['account']
        password = request.GET['password']
    except Exception as e:
        raise RequestParamError(str(e))
    else:
        user = BookBorrowed(account, password)
        return user.get_borrowed_book()


@api_response
def renew_book(request):
    """
    续借 暂时需重新登录学校图书馆 我的图书馆 mylib
    :param request:
                    account：校园卡账号
                    password：校园卡查询密码
                    bar_code:
                    check:
    :return:
                {
                    'result': Boolean
                    'renew_msg':
                }
    """
    try:
        account = request.GET['account']
        password = request.GET['password']
        bar_code = request.GET['code']
        check = request.GET['check']
    except Exception as e:
        raise RequestParamError(str(e))
    else:
        user = BookBorrowed(account, password)
        return user.renew_book(bar_code, check)


@api_response
def get_book_list(request):
    """
        model： NewBook、RecommendBook
    :param request:
                    current_type:
                    book_page_num: 页数
                    callback_count: 每一页书本的数量
    :return:
                {
                    'result': Boolean
                    'list':
                }
    """
    try:
        current_type = int(request.GET['currentType'])
        book_page_num = int(request.GET['bookPageNum'])
        callback_count = int(request.GET['callbackCount'])
        target_model = [RecommendBook, NewBook][current_type == 1]
    except Exception as e:
        raise RequestParamError(str(e))
    else:
        books = target_model.objects.all().order_by('-book_img')[(book_page_num - 1) * callback_count: (book_page_num - 1) * callback_count + callback_count]
        book_list = []
        for book in books:
            info = model_to_dict(book)
            content = {'title': info['title'], 'author': info['author'], 'zt_num': info['zt_num'],
                       'publisher': info['publisher'], 'db_score': info['db_score'], 'isbn': info['isbn'],
                       'book_img': info['book_img'],
                       }
            book_list.append(content)

        return {
            'result': True,
            'list': book_list,
        }


@api_response
def book_detail(request):
    """
    注意：
        有部分书籍因为过旧的原因，所以没有isbn码的存在 只有书名
        但必须考虑书名 有可能重复
        可以考虑两个索引值同时搜索
    :param request:
                    current_type: 哪个表（Book，NewBook）
                    isbn：书籍isbn码
                    title: 书名
    :return:
                {
                    'result':
                    'content': 书的详细内容
                }
    """
    current_type = int(request.GET['currentType'])
    isbn = request.GET.get('isbn', '')
    title = request.GET.get('title', '')
    target_model = [RecommendBook, NewBook][current_type == 1]
    info = target_model.objects.get(isbn__icontains=isbn, title__icontains=title)
    content = model_to_dict(info)

    return {
        'result': True,
        'content': content,
    }


@api_response
def search_book(request):
    """

    :param request:
                    current_type: 哪个表（Book，NewBook）
                    search_content: 搜索内容：有可能是title(书名) 或者isbn码
    :return:
              {
                'result':
                'list':
             }
    """
    try:
        current_type = int(request.GET['currentType'])
        search_content = request.GET.get('searchContent')
        target_model = [Book, NewBook][current_type == 1]
    except Exception as e:
        raise RequestParamError(str(e))
    else:
        search_content = search_content.replace('-', '')
        books = target_model.objects.filter(Q(title__icontains=search_content) | Q(isbn__icontains=search_content))
        book_list = []
        for book in books:
            info = model_to_dict(book)
            content = {
                'title': info['title'], 'author': info['author'], 'zt_num': info['zt_num'],
                'publisher': info['publisher'], 'db_score': info['db_score'], 'isbn': info['isbn'],
                'book_img': info['book_img']
                }
            book_list.append(content)

        return {
            'result': True,
            'list': book_list,
        }

