# Create your views here.
# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from websearch.models import Message
from websearch.models import Like
from websearch.models import Userprofile
import urllib2, sys
from pyquery import PyQuery as pq

def index(request):
    #return render(request, 'websearch/index.html')
    context = {}
    if request.user.is_authenticated():
        context['u'] = request.user
    return render_to_response('index.html', context, context_instance=RequestContext(request))

def like(request):
    context = {}
    #if request.user.is_authenticated():
    user = request.user
    context['u'] = user
    
    likes = user.userprofile.likes.all()
    context['likes'] = likes
    #print (msgs)
    return render_to_response("like_show.html", context, context_instance=RequestContext(request))



@csrf_exempt
def likeit(request):
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user)
        title = request.POST['title']
        img = request.POST['img']
        href = request.POST['href']
        try:
            like = Like.objects.get(href=href)
            like.title = title
            like.img = img
            like.save()    
            pro = Userprofile.objects.get(user=user)
            pro.likes.add(like)
            pro.save()
            return HttpResponse("Like Succeed.")
        except Exception:
            like = Like(title=title, img=img, href=href)
            like.save()
            pro = Userprofile.objects.get(user=user)
            pro.likes.add(like)
            pro.save()
            return HttpResponse("Like Succeed.")
    else:
        return HttpResponse("Please Login.")

@csrf_exempt
def unlikeit(request):
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user)
        href = request.POST['href']
        like = Like.objects.get(href=href)
        print like
        pro = Userprofile.objects.get(user=user)
        pro.likes.remove(like)
        pro.save()
        return HttpResponse("Unlike Succeed.")
    else:
        return HttpResponse("Please Login.")

def msg_show(request):
    context = {}
    #if request.user.is_authenticated():
    user = request.user
    context['u'] = user
    
    msgs = Message.objects.filter(to=str(user))
    context['msgs'] = msgs
    #print (msgs)
    return render_to_response("msg_show.html", context, context_instance=RequestContext(request))

def msg_add(request):
    context = {}
    #if request.user.is_authenticated():
    user = request.user
    context['u'] = user
    
    if request.method == 'POST':
        fr = str(user)
        to = request.POST['to']
        msg = request.POST['msg']
        message = Message(fr=fr, to=to, msg=msg)
        message.save()
        return HttpResponseRedirect(reverse('websearch:showmsg'))
    else:
        users = User.objects.all()
        context['users'] = users
        return render_to_response('msg_add.html',context, context_instance=RequestContext(request))

def contact(request):
    context = {}
    if request.user.is_authenticated():
        user = request.user
        context['u'] = user
    if request.method == 'POST':
        if request.user.is_authenticated():
            fr = str(user)
        else:
            fr = request.POST['fr']
        to = request.POST['to']
        msg = request.POST['msg']
        message = Message(fr=fr, to=to, msg=msg)
        message.save()
        return HttpResponseRedirect(reverse('websearch:index'))
    else:
        admins = User.objects.filter(is_staff=True)
        context['admins'] = admins
        return render_to_response('contact.html',context, context_instance=RequestContext(request))



def edit(request):
    context = {}
    user = request.user
    context['u'] = request.user
    if request.method == 'POST':
        password = request.POST['pw']
        face = request.POST['face']
        #print (face)
        #user = User.objects.get(username=request.user)
        if password.strip():
            user.set_password(password)    
            user.save()
        pro = Userprofile.objects.get(user=user)
        pro.face = face
        pro.save()
        return HttpResponseRedirect(reverse('websearch:index'))
    else:
        """
        try:
            user = User.objects.get(username=request.user)
        except Exception:
            raise Http404
            """
        context['face'] = user.userprofile.face[:user.userprofile.face.find('.')]
    #print (context['face'])
        return render_to_response('edit.html', context, context_instance=RequestContext(request))


@csrf_exempt
def checkuser(request):
    username = request.POST['username']
    try:
        user = User.objects.get(username=username)
        return HttpResponse("err")
    except Exception:
        return HttpResponse("ok")

@csrf_exempt
def checkemail(request):
    email = request.POST['email']
    try:
        user = User.objects.get(email=email)
        return HttpResponse("err")
    except Exception:
        return HttpResponse("ok")

def register(request):
    context = {}
    if request.method == 'POST':
        face = request.POST['face']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username, email, password)  
        if user is not None:
            pro = Userprofile(user=user, face=face)
            pro.save()
            user.save()
            usr = auth.authenticate(username=username, password=password)
            auth.login(request, usr)
            context['u'] = usr
            return HttpResponseRedirect(reverse('websearch:index'))
        else:  
            return render_to_response('register.html',{'msg': 'error'}, context_instance=RequestContext(request))
    else:
        return render_to_response('register.html', context_instance=RequestContext(request))



def login(request):
    if request.user.is_authenticated():
            auth.logout(request)
            return HttpResponseRedirect(reverse('websearch:index'))
    context = {}
    if request.method == 'POST':      
        username = request.POST['username']  
        password = request.POST['password'] 
        user = auth.authenticate(username=username, password=password)
        if user is not None:  
            auth.login(request, user)
            #context['u'] = user
            return HttpResponseRedirect(reverse('websearch:index')) 
        else:  
            return render_to_response('login.html', context_instance=RequestContext(request))
    else:
        return render_to_response('login.html', context_instance=RequestContext(request))



def search(request):  
    if('kw' in request.GET and request.GET['kw']):
        context = {}
        if request.user.is_authenticated():
            context['u'] = request.user
        if('pg' in request.GET):
            pg = request.GET['pg']
        else:
            pg = 1
        context['nextpg']= int(pg)+1
        context['pg']= int(pg)
        context['prepg']=int(pg)-1
        kw = request.GET['kw']
        kw_gbk = kw.encode('gbk')
        kw_url = urllib2.quote(kw_gbk)
        context['kw'] =kw
        
        Tdomain = "http://s.taobao.com/search?"
        Turl = Tdomain + "q="+ kw_url + "&" + "s=" + str((int(pg)-1)*40)
        
        Theaders = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
        Treq = urllib2.Request(Turl, headers=Theaders) 
        Tcontent = urllib2.urlopen(Treq).read()   # Taobao is GBK
        Tcontent_uni = Tcontent.decode('gbk')  # convert encode format 

        T = pq(Tcontent_uni)
        TDatas = T('.item-box')
        TLength = TDatas.length
        TList = []
        for i in range(0, TLength/4):
            Tfour = []
            for j in range(0, 4):
                TData = TDatas.eq(4*i+j)
                title = TData.find('h3.summary').text()
                price = TData.find('.price').text()

                TImg = TData.find('.pic-box')
                href = TImg.find('a').attr('href')
                img = TImg.find('img').attr('src')
                    
                tmp = {}
                tmp['href'] = href
                tmp['img'] = img
                tmp['title'] = title
                tmp['price'] = price
                Tfour.append(tmp)
            TList.append(Tfour)
        context['TDatas'] = TList
        #print float(TList[0]['price'][1:])


        Zdomain = "http://www.amazon.cn/s/ref=sr_st?"
        Zurl = Zdomain + "keywords=" + kw_url + "&" + "page=" + str(int(pg))

        Z = pq(url=Zurl)
        ZDatas = Z('.productImage + .productData')
        ZLength = ZDatas.length
        ZList = []
        for i in range(0, ZLength/4):
            Zfour = []
            for j in range(0, 4):
                ZData = ZDatas.eq(4*i+j)
                title = ZData.find('.productTitle').text()
                price = ZData.find('.newPrice').find('span').text()
                old_price = ZData.find('.newPrice').find('strike').text()

                ZImg = ZData.prevAll('.productImage').eq(0)
                href = ZImg.find('a').attr('href')
                img = ZImg.find('img').attr('src')
                
                tmp = {}
                tmp['href'] = href
                tmp['img'] = img
                tmp['title'] = title
                tmp['price'] = price
                Zfour.append(tmp)
            ZList.append(Zfour)
        context['ZDatas'] = ZList
        #print float(ZList[0]['price'][1:])
        
        return render_to_response('search.html', context)
    else:
        return HttpResponseRedirect(reverse('websearch:index'))
