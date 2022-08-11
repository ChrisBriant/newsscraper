from rest_framework import serializers
from newsadmin.models import *

class NewsItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsItem
        fields = ('id','source','headline', 'link')
