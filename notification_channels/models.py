from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timesince import timesince
from django.utils import timezone

# Create your models here.


class Notification(models.Model):
	""" Notification Fields """

	""" Type can be used to group different types of notifications together """
	Type = models.CharField(max_length=255, blank=True, null=True)

	recipient = models.ForeignKey(User, null=False, blank=False, related_name="notifications", on_delete=models.CASCADE)

	""" Generator can be a number of people in order for multiple same notifications to be merged together """
	generator = models.ManyToManyField(User, related_name='activity_notifications', blank=True)

	""" target of any type can create a notification """
	target_ctype = models.ForeignKey(ContentType, related_name='related_notifications', blank=True, null=True, on_delete=models.CASCADE)
	target_id = models.CharField(max_length=255, blank=True, null=True,)
	target = GenericForeignKey('target_ctype', 'target_id') #change it to manytomany relation for merging similar notification

	""" Action object can be of any type that's related to any certain notification 
		for eg. a notification like '<generator> liked your post' has post as action object """
	action_obj_ctype = models.ForeignKey(ContentType, related_name='action_notifications', blank=True, null=True, on_delete=models.CASCADE)
	action_obj_id = models.CharField(max_length=255, blank=True, null=True,)
	action_obj = GenericForeignKey('action_obj_ctype', 'action_obj_id')

	"""" Notification read or not """
	read = models.BooleanField(default=False, blank=False)

	""" Action verb is the activity that produced the notification 
		eg. <generator> commented on <action_obj>
			<description>
		where 'commented on' is an action verb """

	action_verb = models.CharField(max_length=255, default="You recieved a notification.")
	description = models.TextField(null=True, blank=True)

	""" Reference URL points to the web address the notification needs to redirect the recipient to """
	reference_url = models.URLField(max_length=255, blank=True, null=True, default="#")

	timestamp = models.DateTimeField(auto_now=True)

	def __str__(self):

		timedlta = timesince(self.timestamp, timezone.now())
		count = self.generator.all().count()
		if count == 1:
			gen = self.generator.all()[0].username
		elif count == 2:
			gen = self.generator.all()[0].username + " and " + self.generator.all()[1].username
		elif count == 0:
			gen = ""
		else:
			gen = self.generator.all()[0].username + " , " + self.generator.all()[1].username + " and " + str(count-2) + " others"
		fields = {
			'recipient': self.recipient,
			'generator': gen,
			'action_obj': self.action_obj,
			'target': self.target,
			'action_verb': self.action_verb,
			'timesince': timedlta,
		}

		if self.generator:
			if self.action_obj:
				if self.target:
					return u'%(generator)s %(action_verb)s %(target)s %(action_obj)s %(timesince)s ago' % fields
				return u'%(generator)s %(action_verb)s %(action_obj)s %(timesince)s ago' % fields
			return u'%(generator)s %(action_verb)s %(timesince)s ago' % fields

		if self.action_obj:
			if self.target:
				return u'%(action_verb)s %(target)s %(action_obj)s %(timesince)s ago' % fields
			return u'%(action_verb)s %(action_obj)s %(timesince)s ago' % fields
		return u'%(action_verb)s %(timesince)s ago' % fields

	def __unicode__(self):
		return self.__str__(self)



		