from django.db import models

CASTE_CHOICES = (
		('open', 'Open'),
		('obc', 'OBC'),
		('sc', 'SC'),
		('st', 'ST')
	)

INCOME_CHOICES = (
		('0-100000', '0-100000'),
		('100001-250000', '100001-250000'),
		('250001-400000', '250001-400000'),
		('400001-600000', '400001-600000'),
		('600001 and above', '600001 and above')
	)

STREAM_CHOICES = (
		('10th', '10th'),
		('12th', '12th'),
		('be', 'Bachelor of Engineering (BE)'),
		('ba', 'Bachelor of Arts (BA)'),
		('mbbs', 'Bachelor of Medicine and Bachelor of Surgery (MBBS)'),
		('bba', 'Bachelor of Business Administration (BBA)'),
	)

TYPE_CHOICES = (
		('national', 'National'),
		('state', 'State')
	)

class Scholarship(models.Model):
	name = models.CharField(max_length=128, unique=True)
	url = models.CharField(max_length=200)
	type_of_scholorship = models.CharField(max_length=128, choices=TYPE_CHOICES)
	stream = models.CharField(max_length=256, choices=STREAM_CHOICES)
	income = models.CharField(max_length=256, choices=INCOME_CHOICES)
	caste = models.CharField(max_length=128, choices=CASTE_CHOICES)

	def __str__(self):
		return str(self.name) + ' for ' + str(self.stream)


