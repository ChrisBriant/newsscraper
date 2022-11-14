
from django.core.management.base import BaseCommand, CommandError
from urllib.request import Request, urlopen, HTTPError
from bs4 import BeautifulSoup
from newsadmin.models import NewsItem,StoredNewsItem
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

NEWS_SITES = [
    { 
        'site' : 'bbc',
        'url' : 'https://www.bbc.co.uk/news'
    },
    { 
        'site' : 'yahoo',
        'url' : 'https://uk.news.yahoo.com/'
    },
    { 
        'site' : 'gbnews',
        'url' : 'https://www.gbnews.uk'
    },
    { 
        'site' : 'metro',
        'url' : 'https://metro.co.uk/news/'
    },
    {
        'site' : 'channel4',
        'url' : 'https://www.channel4.com/news/'        
    },
]

collected_headlines = []
#Store top headline from each source
top_headlines = []

#Function to store the last appended item to the collected headlines
def store_top_headline():
    if len(collected_headlines) > 0:
        top_headlines.append(collected_headlines[-1])


def process_bbc(url,soup):
    base_url = url.split('/news')[0]
    results = soup.find_all(class_='gs-c-promo-heading')
    for result in results:
        href = result.attrs.get('href')
        title = result.find(class_='gs-c-promo-heading__title').decode_contents()
        if href:
            headline = {
                'site' : 'bbc',
            }
            headline['link'] = base_url + href
            headline['headline'] = title
            collected_headlines.append(headline)
    #Store top headline
    store_top_headline()

def process_yahoo(url,soup):
    results = soup.find_all(class_='js-content-viewer')
    print(results)

def process_gbnews(url,soup):
    results = soup.find_all(class_='headline')
    for result in results:
        parent_link = result.parent.attrs.get('href')
        if(parent_link):
            headline = {
                'site' : 'gbnews',
            }
            headline['link'] = url + parent_link
            headline['headline'] = result.decode_contents()
            #Check it is not the last entry which is not a headline
            if headline['headline'] != 'MORE GB NEWS':
                collected_headlines.append(headline)
    #Store top headline
    store_top_headline()

def process_metro(url,soup):
    results = soup.find_all(class_='metro__post__title')
    for result in results:
        news_link = result.findChild('a')
        headline = {
            'site' : 'metro',
        }
        headline['link'] = news_link.attrs.get('href')
        headline['headline'] = news_link.findChild('span').text
        collected_headlines.append(headline)
    #Store top headline
    store_top_headline()

def process_channel4(url,soup):
    results = soup.find_all(class_='content with-image')
    for result in results:
        if len(result) > 0:
            title = result.find(class_='description').decode_contents()
            link = result.find(class_='permalink')
            if link:
                headline = {
                    'site' : 'channel4',
                }
                headline['link'] = link.attrs.get('href')
                headline['headline'] = title
                collected_headlines.append(headline)
    #Store top headline
    store_top_headline()


def process_soup(site,soup):
    if site['site'] == 'bbc':
        process_bbc(site['url'],soup)
    if site['site'] == 'yahoo':
        #process_yahoo(site['url'],soup)
        pass
    if site['site'] == 'gbnews':
        process_gbnews(site['url'],soup)
    if site['site'] == 'metro':
        process_metro(site['url'],soup)
    if site['site'] == 'channel4':
        process_channel4(site['url'],soup)

def get_soup(request):
    source_code = None
    try:
        data = urlopen(request)
        data_bytes = data.read()
        source_code = data_bytes.decode('utf8')
        data.close()
    except HTTPError as e:
        print(e.fp.read())
        return None
    return BeautifulSoup(source_code, 'html.parser')

#Gets the old news items from the database and removes them to clean up DB
def purge_previous_news_items():
    date_now = datetime.now()
    start_of_day = make_aware(datetime.strptime(date_now.strftime('%Y-%m-%d'),'%Y-%m-%d') + timedelta(hours=5))
    print(start_of_day)
    #GET ALL PREVIOUS ITEMS
    items_before = NewsItem.objects.filter(date_added__lt=start_of_day)
    print(items_before)
    items_before.delete()

class Command(BaseCommand):
    help = 'Get news for today'

    # def add_arguments(self, parser):
    #     parser.add_argument('number', type=int)

    def handle(self, *args, **options):
        
        #For connecting
        hdr = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

        #MAIN

        purge_previous_news_items()

        for site in NEWS_SITES:
            req = Request(
                site['url'],
                data=None,
                headers = hdr
            )
            soup = get_soup(req)
            if soup:
                process_soup(site,soup)

        for headline in collected_headlines:
            NewsItem.objects.create(
                source = headline['site'],
                link = headline['link'],
                headline = headline['headline'],
            )

        #Add the top headlines to the perisisted headline table
        for headline in top_headlines:
            StoredNewsItem.objects.create(
                source = headline['site'],
                link = headline['link'],
                headline = headline['headline'],
            )

        self.stdout.write(self.style.SUCCESS('Collected Today\'s Headlines'))