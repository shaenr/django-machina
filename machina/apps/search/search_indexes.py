# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
from django.db.models import get_model
from haystack import indexes

# Local application / specific library imports

Post = get_model('conversation', 'Post')


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name='search/post_text.txt')
    poster = indexes.CharField(model_attr='poster')

    forum = indexes.IntegerField(model_attr='topic__forum_id')
    forum_name = indexes.CharField()

    topic = indexes.IntegerField(model_attr='topic_id')
    topic_subject = indexes.CharField()

    created = indexes.DateTimeField(model_attr='created')
    updated = indexes.DateTimeField(model_attr='updated')

    def get_model(self):
        return Post

    def prepare_forum_name(self, obj):
        return obj.topic.forum.name

    def prepare_topic_subject(self, obj):
        return obj.topic.subject

    def read_queryset(self, using=None):
        return Post.objects.all().select_related('topic', 'poster')
