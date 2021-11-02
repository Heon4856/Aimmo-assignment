from models.models import Post


def read_post_list(page):
    items_per_page = 10
    offset = (page - 1) * items_per_page
    post_list = Post.objects.skip(offset).limit(items_per_page)
    return post_list


def read_post_detail(id):
    return Post.objects.get_or_404(id=id)


def create(title, content, date, current_user_id):
    post = Post(title=title, content=content, create_date=date, user=current_user_id).save()
    id = post.id
    return id


def modify(id, title, content, modify_date, current_user_id):
    post = Post.objects.get_or_404(id=id)
    if post.user == current_user_id:
        post.update(title=title, content=content, modify_date=modify_date)
        return True
    return False


def delete(id, current_user_id):
    post = Post.objects.get_or_404(id=id)
    if post.user == current_user_id:
        post.delete()
        return True
    return False
