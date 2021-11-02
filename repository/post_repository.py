from models.models import Comment, Post, ChildComment


def read_post_list(page, tags):
    post_list = Post.objects(tags=tags).paginate(page=page, per_page=10)
    return post_list


def read_post_detail(id):
    post = Post.objects.get_or_404(id=id)
    return post



def create_post(title, content, date, current_user_id, tags):
    post = Post(title=title, content=content, create_date=date, user=current_user_id, hits=0)
    post.tags = tags
    post.save()
    id = post.id
    return id


def modify_post(id, title, content, modify_date, current_user_id):
    post = Post.objects.get_or_404(id=id)
    if post.user == current_user_id:
        post.update(title=title, content=content, modify_date=modify_date)
        return True
    return False


def delete_post(id, current_user_id):
    post = Post.objects.get_or_404(id=id)
    if post.user == current_user_id:
        post.delete()
        return True
    return False


def hit_post(id):
    post = Post.objects.get_or_404(id=id)
    post.update(hits=post.hits + 1)


def search_post(keyword, tags):
    post = Post.objects(title=keyword, tags=tags)
    return post


def create_child_comment_repository(create_comment_info):
    post = Post.objects.get_or_404(id=create_comment_info['post_id'])
    child_comment = ChildComment(content=create_comment_info['content'], create_date=create_comment_info['create_date'], user_id=create_comment_info['user_id'],\
                post_id=create_comment_info['post_id'])
    post.reply[create_comment_info['oid']]['reply'].append(child_comment)
    post.save()
    return True


def create_parent_comment_repository(create_comment_info):
    comment = Comment(content=create_comment_info['content'], create_date=create_comment_info['create_date'], user_id=create_comment_info['user_id'],\
                post_id=create_comment_info['post_id'])
    post = Post.objects.get_or_404(id=create_comment_info['post_id'])
    comment_id = str(comment.oid)
    post.reply[comment_id] = comment
    post.save()
    return comment_id

def search_comment_repository(delete_comment_info):
    comment = Comment.objects(user_id=delete_comment_info['user_id'],post_id=delete_comment_info['post_id'],\
                            id=delete_comment_info['comment_id'])
    comment_id = comment.id
    return comment_id

def delete_comment_repository(comment_id):
    comment_list = Comment.objects.get_or_404(parent_comment_id=comment_id)
    comment_list.delete()
    return True