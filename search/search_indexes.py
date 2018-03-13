import datetime
from haystack import indexes
from .models import MainData


class MainSearchIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	url = indexes.CharField(model_attr='url', null=True)
	title = indexes.EdgeNgramField(model_attr='title', null=True)
	metadata = indexes.EdgeNgramField(model_attr='metadata', null=True)
	meta_keywords = indexes.CharField(model_attr='meta_keywords', null=True)
	context = indexes.EdgeNgramField(model_attr='context', null=True)
	suggestions = indexes.FacetCharField()

	def get_model(self):
		return MainData

	def index_queryset(self, using=None):
		return MainData.objects.filter(created__lte=datetime.datetime.now())

	def prepare(self, obj):
		prepared_data = super(MainSearchIndex, self).prepare(obj)
		prepared_data['suggestions'] = prepared_data['text']
		return prepared_data