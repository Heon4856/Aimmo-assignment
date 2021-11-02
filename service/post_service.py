from repository import post_repository
from datetime import datetime

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