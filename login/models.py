from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.fields import (
    GenericForeignKey)
from django.contrib.contenttypes.models import ContentType
from draceditor.models import DraceditorField
#from markdownx.models import MarkdownxField

# Create your models here.
class Comment(models.Model):
	""" Represents an instance of Comment """
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	user = models.ForeignKey(User, related_name='commented')
	comment = models.CharField(max_length=512)
	likes_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
	timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
	def __str__(self):
		return str(self.likes_count)

	def get_class(self):
		return 'comment'


class Topic(models.Model):
	name = models.CharField(max_length = 30)
	def __str__(self):
		return str(self.name)

	def get_class(self):
		return 'topic'

class Like(models.Model):
	"""
	Represents an instance of a Like
	belonging to a Comment
	"""
	user = models.ForeignKey(User)
	comment = models.ForeignKey(Comment)

class Person(models.Model):
	username = models.OneToOneField(User , on_delete = models.CASCADE )
	display_pic= models.ImageField(blank=True)
	gen = (
		('m','Male'),
		 ('f','Female'),
		 ('o','Other'),
		 )
	gender = models.CharField(max_length=1, choices=gen)
	about_me = models.TextField(blank=True)
	cover_pic = models.ImageField(blank=True)
	follows = models.ManyToManyField('Person', related_name='followed_by')
	topic_follows = models.ManyToManyField('Topic', related_name = 'user_followers', blank = True)
	def __str__(self):
		return str(self.username)

	def get_absolute_url(self):
		return reverse('home:login', kwargs={'pk': self.pk})

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Person.objects.create(username = instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.person.save()


class Post(models.Model):
	author = models.ForeignKey(User, on_delete = models.CASCADE )
	title = models.CharField(max_length= 120)
	content = DraceditorField()
	#content = models.TextField()
	comments = GenericRelation(Comment)
	timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)
	upvotes = models.ManyToManyField('Person', related_name='upvoted_post')
	topic_follows = models.ManyToManyField('Topic', related_name = 'post_followers', blank = True)
	def __str__(self):
		return self.title

	def get_class(self):
		return 'post'


class Question(models.Model):
	author = models.ForeignKey(User, null=True, db_index=True, on_delete = models.CASCADE )
	question = models.TextField(max_length=300)
	details = models.TextField(max_length=1000, null=True, blank=True)
	comments = GenericRelation(Comment)
	timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)
	topic_follows = models.ManyToManyField('Topic', related_name = 'question_followers', blank = True)
	def __str__(self):
		return self.question

	def get_class(self):
		return 'question'

class Answer(models.Model):
	author = models.ForeignKey(User, on_delete = models.CASCADE, null=True, db_index=True)
	question = models.ForeignKey(Question, on_delete = models.CASCADE, related_name='answers')
	content = models.TextField()
	comments = GenericRelation(Comment)
	timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)
	upvotes = models.ManyToManyField('Person', related_name='upvoted_answer')
	def __str__(self):
		return self.author.username

	def display(self):
		return self.author.username

	def get_class(self):
		return 'answer'

class Item(models.Model):
	reported_by = models.ForeignKey(User, on_delete = models.CASCADE)
	name = models.CharField(max_length= 30)
	choice = (
		('L','Lost'),
		('F','Found')
		)
	lost = models.CharField(max_length=10, choices=choice)
	image = models.ImageField(blank=True, null=True)
	details = models.TextField(max_length= 1000, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)
	def __str__(self):
		return self.name

	def get_class(self):
		return 'item'
