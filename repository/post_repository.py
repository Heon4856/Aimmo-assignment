from models.models import Post


def read_post_detail(id):
    return Post.objects.get_or_404(id=id)


def create(title, content, date, current_user):
    post = Post(title=title, content=content, create_date=date, user=current_user).save()
    id = post.id
    return id


def modify(id, title, content, modify_date, current_user):
    post = Post.objects.get_or_404(id=id)
    post.update(title=title, content=content, modify_date=modify_date, user=current_user)


def delete(id, current_user):
    post = Post.objects.get_or_404(id=id)
    post.delete()
