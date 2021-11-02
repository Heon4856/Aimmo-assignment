from repository import post_repository
from datetime import timedelta,datetime


def read_post_detail(id):
    return post_repository.read_post_detail(id)


def create_post(title,content,current_user):
    date = datetime.now()
    return post_repository.create(title, content, date, current_user)


def update_post(id,title,content,current_user):
    modify_date= datetime.now()
    return post_repository.modify(id, title, content, modify_date, current_user)


def delete_post_if_user_authorized(id, current_user):
    return post_repository.delete(id, current_user)


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


