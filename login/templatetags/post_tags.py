from django import template
from django.conf import settings
from login.models import Post, Answer, Question


register = template.Library()


def get_post(object, user):
    """
    Retrieves list of posts and renders
    The appropriate template to view it
    """
    post = Post.objects.get(id=object.id)
    upvotes = post.upvotes.all().count()
    return {
            "post": post,
            "user": user,
            'upvotes': upvotes}

register.inclusion_tag('post/post_view.html')(get_post)


def get_all_answers(object, user):
	answers = Answer.objects.filter(question = object)
	size = Answer.objects.filter(question = object).count()
	return {
            'answers':answers,
		'user': user,
		'size': size,}

register.inclusion_tag('post/all_answers.html')(get_all_answers)
	

def get_answer(object, user):
	# print(object)
	upvotes = object.upvotes.all().count()
	return {
            'answer': object,
		'upvotes': upvotes,
		'user': user,}

register.inclusion_tag('post/get_answer.html')(get_answer)

def all_things_question(object, user):
	answered = False
	myanswer = Answer.objects.all()[0] #for initialization
	if object.answers.filter(author=user):
		myanswer = object.answers.get(author=user)
		answered = True
	# print(myanswer.id)
	return {
            'quest': object,
		'user': user,
		'answered': answered,
		'myanswer': myanswer}

register.inclusion_tag('post/question.html')(all_things_question)


def question_feed(object, user):
	answered = False
	myanswer = Answer.objects.all()[0]
	if object.answers.filter(author=user):
		myanswer = object.answers.get(author=user)
		answered = True
	# print(myanswer.id)
	return {
            'quest': object,
		'user': user,
		'answered': answered,
		'myanswer': myanswer}

register.inclusion_tag('post/question_feed.html')(question_feed)


def get_user_popup(object, user):
    # print("our user "+user.username)
    return {
            "user": user,
            'objuser': object,}

register.inclusion_tag('post/mini_profile.html')(get_user_popup)


def get_user_tag(object, user):
    # print("our user "+user.username)
    return {
            "user": user,
            'objuser': object,}

register.inclusion_tag('post/profile_tag.html')(get_user_tag)



	

# def all_about_rubbish(object, user):
# 	return return {
#             'quest': object,
# 		'user': user,}

# register.inclusion_tag('post/question.html')(all_things_question)
# 	