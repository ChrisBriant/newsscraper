from django.shortcuts import render
from .serializers import *
from newsadmin.models import *
from django.utils.timezone import make_aware
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import random
from datetime import datetime, timedelta


#Create a user profile
@api_view(['GET'])
def get_random_news_items(request):
    amount = int(request.query_params.get('amount'))

    if amount:
        #Limit to 10
        if amount > 10:
            amount = 10
    else:
        #Default is one item
        amount = 1

    date_now = datetime.now()
    start_of_day = make_aware(datetime.strptime(date_now.strftime('%Y-%m-%d'),'%Y-%m-%d') + timedelta(hours=5))
    print(start_of_day)
    #GET TODAY'S ITEMS
    items_today = NewsItem.objects.filter(date_added__gt=start_of_day)
    sample = random.sample(list(items_today),amount)
    serializer = NewsItemSerializer(sample,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)