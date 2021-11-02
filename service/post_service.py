from repository import post_repository
from datetime import timedelta, datetime
import re


def read_post_list(page, tags):
    post_list = post_repository.read_post_list(page, tags)
    temp_post_list = []
    for post in post_list.items:
        temp_post_list.append(
            dict(_id=str(post.id), title=post.title, content=post.content, create_date=post.create_date, user=post.user,
                 modify_date=post.modify_date))
    return temp_post_list


def read_post_detail(id):
    post_data = post_repository.read_post_detail(id)
    return post_data.to_json()


def create_post(title, content, current_user_id, tags):
    date = datetime.now()
    return post_repository.create_post(title, content, date, current_user_id, tags)


def update_post(id, title, content, current_user_id):
    modify_date = datetime.now()
    return post_repository.modify_post(id, title, content, modify_date, current_user_id)


def count_hit_post(id, request):
    ''' 24시까지 유효한 쿠키를 만든다.'''
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.cookies.get('hitboard', '_')
    if f'{id}' not in cookie_value:
        post_repository.hit_post(id)
        cookie_value += f'{id}_'
    return cookie_value, max_age


def search_keyword(keyword, tags):
    regex = re.compile('.*' + keyword + '*')
    return post_repository.search_post(regex, tags)


def delete_post_if_user_authorized(id, current_user_id):
    return post_repository.delete_post(id, current_user_id)


def create_comment_service(comment_info):
    comment_info['create_date'] = datetime.now()
    if 'parent_comment_id' in comment_info:
        return post_repository.create_child_comment_repository(comment_info)
    return post_repository.create_parent_comment_repository(comment_info)


def delete_comment_service(delete_commnet_info):
    comment_id = post_repository.search_commnet_repository(delete_commnet_info)
    return post_repository.delete_comment_repository(comment_id)
    # if comment:
    #     comment_list = post_repository.search_child_comment_repository(comment.id)
    #     for child in comment_list:
    #         post_repository.delete_comment(child.id)