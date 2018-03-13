from django.db.models import *
from django.db import models as models


class MainData(models.Model):
	created = models.DateTimeField(auto_now_add=True, editable=False)
	last_updated = models.DateTimeField(auto_now=True, editable=False)
	url = models.CharField(max_length=1000)
	title = models.CharField(max_length=250, blank=True, null=True)
	metadata = models.TextField(max_length=500, blank=True, null=True)
	meta_keywords = models.TextField(max_length=1000, blank=True, null=True)
	context = models.TextField(max_length=1000, blank=True, null=True)


	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return str(self.title)

	def get_absolute_url(self):
		return self.url