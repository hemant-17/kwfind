from django.db.models.fields import related
from django.shortcuts import render,redirect
from django.http import HttpResponse , JsonResponse
import json
from django.core import serializers
import time
import requests
from bs4 import BeautifulSoup
from .forms import *
from collections import Counter
# Create your views here.


def index(request):
    return render(request,"index.html")


def appsearcher(request):
    return render(request,'appsearch.html')


def keyfinder(request):
    urlform=UrlForm()
    recm_url=[]
    related_url=[]
    if request.method=='POST':
        url=request.POST['url']
        print(url)
        ##Keyword extraction
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        metas = soup.find_all('meta')
        desc=[ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'Description' ]
        keywords=[ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'Keywords']

        ##preprocessing of keywords
        for i in keywords:
            keywords=i.split(',')
        j=[]
        for x in keywords:
            j.append(x.strip())
        existing_keywords=Keyword.objects.all()
        existing_list=[]
        for g in existing_keywords:
            existing_list.append(g.keyword)

        ##checking if they already exists in db
        set2 = set(existing_list)
        final_keywords = [o for o in j if o not in existing_list]

        ##saving in db if not duplicate
        for i in final_keywords:
            keyword_obj=Keyword(keyword=i)
            keyword_obj.save()

        #checking if url already exists
        existing_url=Url.objects.all()
        url_list=[]
        for i in existing_url:
            url_list.append(i.url)

        if url in url_list:
            print("Already exists")
        else:
            url_obj=Url(url=url)
            url_obj.save()
            print("Url added to db")
            ##add mapping
            url_id=Url.objects.get(url=url)
            for i in j:
                kobj=Keyword.objects.get(keyword=i)
                mapping_obj=Mapping_of_url(keyword=kobj,url_id=url_id)
                mapping_obj.save()
            print("Mapping done")
        ## recommendation
        for i in j:
            rec_url=Mapping_of_url.objects.filter(keyword=i).values_list('url_id',flat=True)
            print(rec_url)
            related_urlid=[]
            for x in rec_url:
                related_urlid.append(x)
        x=Counter(related_urlid)
        related_urlid=list(set(related_urlid))
        print(related_urlid)
        print(x)
        recm_url_id=[]
        for i in x.items():
            print(i)
            if i[1] > 3:
                recm_url_id.append(i[0])
        print(recm_url_id)
        for i in related_urlid:
            x=Url.objects.get(id=i)
            related_url.append(x.url)
        for i in recm_url_id:
            x=Url.objects.get(id=i)
            recm_url.append(x.url)
        for i in related_url:
            if i in recm_url:
                related_url.remove(i)

    return render(request,'keyfinder.html',{'form':urlform,'related_url':related_url,'recom_url':recm_url})

def getinfo(request):
    if request.method=='POST':
        packagename=request.POST['packagename']
        print(packagename)
        req=requests.get("https://play.google.com/store/apps/details?id={}&hl=en_IN".format(packagename))
        if req.status_code == 200:
                print('Package exists..loading')
                soup=BeautifulSoup(req.content,"html.parser")

                # res=soup.title
                # print("Title of the page--",res.get_text())

                app_name = soup.find('h1', class_="AHFaub")
                print("App name--",app_name.get_text())
                app_name=app_name.get_text()

                developer_name=soup.find('a', class_="hrTbp R8zArc")
                print("Developer name--",developer_name.get_text())
                developer_name = developer_name.get_text()
                print(type(developer_name))

                description=soup.find('div', attrs={'jsname':"sngebd"})
                print("Description--"+description.get_text()[:200]+"..")

                description=description.get_text()[:200]+".."
                print(type(description))

                #installs: <span class="htlgb">
                desc=soup.find_all('div',class_="hAyfc")
                for i in desc:
                        if i.find("div",class_="BgcNfc").text=='Installs':
                                # children = desc.findChildren("div" , class_="IQ1z0d",recursive=False)
                                x=i.find_next('span',class_="htlgb")
                                print(x.get_text())
                                desc=x.get_text()
                                print(type(desc))

                # ratings: <div class="BHMmbe">
                ratings =soup.find('div', attrs={'class':"BHMmbe"})
                print("Ratings--",ratings.get_text())
                ratings=ratings.get_text()
                print(type(ratings))

        #         # # no of peoples: <span class="EymY4b">
                no_of_ratings=soup.find('span',attrs={'class':'EymY4b'})
                print("Rating count people",no_of_ratings.get_text())
                no_of_ratings=no_of_ratings.get_text()

                link = soup.find(itemprop="image")
                print(link["src"])
                img_link=link["src"]
                print(type(img_link))
                return JsonResponse({"app_name":app_name, "developer_name":developer_name, "description":description,"installs":desc,"ratings":ratings,"peps_rate":no_of_ratings,"imgsrc":img_link}, status=200)
        else:
                print('Wrong package Name, Please Check')
                response = JsonResponse({"error": "Wrong package Name, Please Check"})
                response.status_code = 403 # To announce that the user isn't allowed to publish
                return response


def apple_info(request):
    if request.method=='POST':
        app_name=request.POST['appname']
        app_id=request.POST['appid']
        print(app_name,app_id)
        req=requests.get("https://apps.apple.com/in/app/{appname}/id{appid}".format(appname=app_name,appid=app_id))
        if req.status_code == 200:
                print('Package exists..loading')
                soup=BeautifulSoup(req.content,"html.parser")

                # res=soup.title
                # print("Title of the page--",res.get_text())

                app_name = soup.find('h1', class_="product-header__title app-header__title").text
                span = soup.find('span', attrs={"class":"badge badge--product-title"}).text
                final_text = app_name[:len(app_name)-len(span)-1]
                print("App name--",final_text.strip())
                app_name=final_text.strip()

                devl = soup.find('dd', attrs={"class":"information-list__item__definition"}).text
                developer_name = devl.strip()
                print(type(developer_name))


                #installs: <span class="htlgb">
                desc=soup.find('div',class_="section__description")
                children = desc.findChildren("div" , class_="l-row",recursive=False)
                for child in children:
                    print("Description: "+child.get_text().strip()[:200]+"..")
                    description=child.get_text().strip()[:200]+".."
                    print(type(desc))

                # ratings: <div class="BHMmbe">
                rt = soup.find('span', attrs={"class":"we-customer-ratings__averages__display"}).text
                print("Ratings--",rt.strip())
                ratings=rt.strip()
                print(type(ratings))

        #         # # no of peoples: <span class="EymY4b">
                nori = soup.find('div', attrs={"class":"we-customer-ratings__count small-hide medium-show"}).text
                print("Rating count people",nori.strip())
                no_of_ratings=nori.strip()

                tags=soup.findAll('source')
                img_icon=tags[0]['srcset'].split(',')
                print(img_icon[0][:-2])
                img_link=img_icon[0][:-2]
                return JsonResponse({"app_name":app_name, "developer_name":developer_name, "description":description,"ratings":ratings,"peps_rate":no_of_ratings,"imgsrc":img_link}, status=200)
        else:
                print('Wrong package Name, Please Check')
                response = JsonResponse({"error": "Wrong package Name, Please Check"})
                response.status_code = 403 # To announce that the user isn't allowed to publish
                return response