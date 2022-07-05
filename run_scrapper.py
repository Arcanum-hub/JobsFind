import asyncio
import time  # Time for complete func
from asyncio import tasks
import codecs
import os, sys
import datetime as dt
from django.conf import settings

from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"
import django
django.setup()

from scrap.HTMLParser import *
from scrap.models import Url, Vacancy, City, Language, Error
from django.contrib.auth import get_user_model

User = get_user_model()

parsers = (
    (hh, 'hh'),
    (jooble, 'jooble'),
    (indeed, 'indeed')
)

jobs, errors = [],[]

def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst

def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    print("print _settings")
    print(_settings)
    print("print qs")
    print(qs)
    urls = []
    
    for pair in _settings:
        if pair in  url_dct:
            print("print pair")
            print(pair)
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            url_data = url_dct.get(pair)
            if url_data:
                print("print url_data")
                print(url_data)
                tmp['url_data'] = url_dct.get(pair)
                urls.append(tmp)
            #tmp['url_data'] = url_dct[pair]
            #urls.append(tmp)
    return urls

async def main(value):
    
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)
    

settings = get_settings()
url_list = get_urls(settings)


start = time.time()


loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
            for data in url_list
            for func, key in parsers]
print("print tmp_tasks")            
print(tmp_tasks)

#for data in url_list:
#    for func, key in parsers:
#        url = data['url_data'][key]
#        j, e = func(url, city = data['city'], language= data['language'])
#        jobs += j
#        errors += e
if tmp_tasks:
    tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
    loop.run_until_complete(tasks)
    loop.close()

print(time.time()-start) # Time for complete func

for job in jobs:
    
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    qs = Error.objects.filter(timestamp = dt.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        er = Error(data=f'errors:{errors}').save()
#h = codecs.open('work2.txt','w', 'utf-8')
#h.write(str(jobs))
#h.close()

ten_days_ago = dt.date.today() - dt.timedelta(10)
Vacancy.objects.filter(timestamp__lte=ten_days_ago).delete()