from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timesince import timesince
from django.utils import timezone
# Create your models here.


class Notifications(models.Model):
	""" Notification Fields """

	""" Type can be used to group different types of notifications together """
	Type = models.CharField(max_length=255, blank=True, null=True)

	recipient = models.ForeignKey(User, null=False, blank=False, related_name="notifications", on_delete=models.CASCADE)

	""" Generator of any type can create a notification. For instance it can be a user or any group or something else. """
	generator_ctype = models.ForeignKey(ContentType, related_name='genrated_notifications', blank=True, null=True, on_delete=models.CASCADE)
	generator_id = models.CharField(max_length=255, blank=True, null=True,)
	generator = GenericForeignKey('generator_ctype', 'generator_id')


	""" Action object can be of any type that's related to any certain notification """
	action_obj_ctype = models.ForeignKey(ContentType, related_name='action_notifications', blank=True, null=True, on_delete=models.CASCADE)
	action_obj_id = models.CharField(max_length=255, blank=True, null=True,)
	action_obj = GenericForeignKey('action_obj_ctype', 'action_obj_id')

	"""" Notification read or not """
	read = models.BooleanField(default=False, blank=False)

	""" Action verb is the activity that produced the notification 
		eg. <generator> commented on <action_obj>
			<description>
		where 'commented on' is an action verb """

	action_verb = models.CharField(max_length=255, default=" recieved a notification.")
	description = models.TextField(null=True, blank=True)

	""" Reference URL points to the web address the notification needs to redirect the recipient to """
	reference_url = models.URLField(max_length=255, blank=True, null=True)

	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):

		timedlta = timesince(self.timestamp, timezone.now())

		fields = {
			'recipient': self.recipient,
			'generator': self.generator,
			'action_obj': self.action_obj,
			'action_verb': self.action_verb,
			'timesince': timedlta,
		}

		if self.generator:
			if self.action_obj:
				return u'%(generator)s %(action_verb)s %(action_obj)s %(timesince)s ago' % fields
			return u'%(generator)s %(action_verb)s %(timesince)s ago' % fields

		return u'%(recipient)s %(action_verb)s %(timesince)s ago' % fields

	def __unicode__(self):
		return self.__str__(self)



		