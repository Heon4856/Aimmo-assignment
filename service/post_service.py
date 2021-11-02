from repository import post_repository
from datetime import timedelta,datetime
import re

def read_post_list(page):
    post_list = post_repository.read_post_list(page)
    temp_post_list = []
    for post in post_list.items:
        temp_post_list.append(
            dict(_id=str(post.id), title=post.title, content=post.content, create_date=post.create_date, user=post.user,
                    modify_date=post.modify_date))
    return temp_post_list


def read_post_detail(id):
    post_data = post_repository.read_post_detail(id)
    return post_data.to_json()


def create_post(title, content, current_user_id):
    date = datetime.now()
    return post_repository.create(title, content, date, current_user_id)


def update_post(id, title, content, current_user_id):
    modify_date = datetime.now()
    return post_repository.modify(id, title, content, modify_date, current_user_id)


def count_hit_post(id, request, current_user):
    ''' 24시까지 유효한 쿠키를 만든다.'''
    expire_date, now = datetime.now(),datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0,second=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.cookies.get('hitboard', '_')
    if f'{current_user}' not in cookie_value:
        post_repository.hit(id)
        cookie_value += f'{current_user}_'
    return cookie_value, max_age


def search_keyword(keyword):
    regex = re.compile('.*' + keyword + '*')
    return post_repository.search(regex)


def delete_post_if_user_authorized(id, current_user_id):
    return post_repository.delete(id, current_user_id)
