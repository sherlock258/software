from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User,Article,Like,Attention,Comment
from django.core import serializers
from django.core.mail import send_mail
import random
import json
from bs4 import BeautifulSoup
from markdown import markdown
import datetime
import  os
from djangoProject import settings
from django.db.models import Q


def hello(request):
    return HttpResponse('欢迎使用Django！')


@csrf_exempt
def login(request):
    #用户登录
    response = {}
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        try:
            user = User.objects.get(email=email,password=password)
            response['msg'] = 'OK'
            response['user'] = [user.username, user.email, user.phone,user.id,user.avatarurl,user.description]
            return HttpResponse(json.dumps(response))
        except User.DoesNotExist:
            response['msg'] = 'NOTEXIST'
            return HttpResponse(json.dumps(response))

    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def register(request):
    #注册用户
    response = {}
    info = User()
    if request.method == 'POST':
        data = json.loads(request.body)
        info.username = data['username']
        info.password = data['password']
        info.email=data['email']
        info.phone=data['phone']
        try:
            user = User.objects.get(email=info.email)
            response['msg'] = 'EXIST'
            return HttpResponse(json.dumps(response))
        except User.DoesNotExist:
            response['msg'] = 'OK'
            info.save()
            return HttpResponse(json.dumps(response))

    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    
@csrf_exempt
def sendemail(request):
    #邮箱验证
    response={}
    code=''
    for i in range(6):
        num=random.randint(0,9)
        code+=str(num)
    info="您的验证码是:"+code[:]+"，请妥善保管，避免泄露！"
    if request.method=='POST':
        data = json.loads(request.body)
        email=data['email']
        try:
            user = User.objects.get(email=email)
            send_mail('邮箱验证', info, 'wangzhan0813@126.com',[email], fail_silently=False)
            response['code']=code
            response['msg']='OK'
            return HttpResponse(json.dumps(response))
        except User.DoesNotExist:
            response['msg'] = 'NOTEXIST'
            return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def userupdate(request):
    #更新用户信息
    response = {}
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        email = data['email']
        description=data['description']
        if password!='':
            User.objects.filter(email=email).update(password=password)
        if username!='':
            User.objects.filter(email=email).update(username=username)
        if description!='':
            User.objects.filter(email=email).update(description=description)
        user = User.objects.get(email=email)
        response['user']=[user.username,user.email,user.password,user.phone]
        response['msg']='OK'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def userarticle(request):
    #获取某个用户的文章，需要传入用户的id
    response = {}
    if request.method == 'GET':
        text = []
        author = []
        authorid=int(request.GET.get('authorid'))
        res=Article.objects.filter(author_id=authorid,status=1)
        user=User.objects.filter(id=authorid)
        for item in res:
            author.append(User.objects.get(id=item.author_id).username)
            html = markdown(item.content)
            str=''.join(BeautifulSoup(html).findAll(text=True))
            if len(str)>100:
               text.append(str[:100])
            else:text.append(str)
        response['list'] = json.loads(serializers.serialize("json", res))
        response['text'] = text
        response['author'] = author
        response['user']=json.loads(serializers.serialize("json", user))
        response['msg']='OK'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@csrf_exempt
def getarticle(request):
    #获取所有文章
    response = {}
    if request.method == 'GET':
        res = Article.objects.filter(status=1)
        response['msg'] = 'OK'
        text=[]
        author=[]
        for item in res:
            author.append(User.objects.get(id=item.author_id).username)
            html = markdown(item.content)
            str=''.join(BeautifulSoup(html).findAll(text=True))
            if len(str)>100:
               text.append(str[:100])
            else:text.append(str)
        response['list'] = json.loads(serializers.serialize("json", res))
        response['text']=text
        response['author']=author
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def selectkind(request):
    #获取某一类的所有文章，需传入参数kind
    response = {}
    if request.method == 'GET':
        text = []
        author = []
        kind = int(request.GET.get('kind'))
        res = Article.objects.filter(kind=kind,status=1)
        for item in res:
            author.append(User.objects.get(id=item.author_id).username)
            html = markdown(item.content)
            str=''.join(BeautifulSoup(html).findAll(text=True))
            if len(str)>100:
               text.append(str[:100])
            else:text.append(str)
        response['list'] = json.loads(serializers.serialize("json", res))
        response['text'] = text
        response['author'] = author
        response['msg'] = 'OK'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def articleid(request):
    #获取某个文章
    response = {}
    if request.method == 'GET':
        id = int(request.GET.get('id'))
        res = Article.objects.filter(id=id)
        html = markdown(res[0].content)
        text = ''.join(BeautifulSoup(html).findAll(text=True))
        author=User.objects.get(id=res[0].author_id).username
        avatar=User.objects.get(id=res[0].author_id).avatarurl
        time=res[0].time.strftime('%Y-%m-%d %H:%M:%S')[:]
        response['list'] = json.loads(serializers.serialize("json", res))
        response['author'] = author
        response['avatar'] = avatar
        response['time']=time
        response['text']=text
        response['msg'] = 'OK'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def publish(request):
    #发布文章
    response = {}
    if request.method == 'POST':
        data = json.loads(request.body)
        if data['id']==-1:
            article=Article()
            article.title = data['title']
            article.content = data['content']
            article.author_id=data['authorid']
            article.kind=data['kind']
            article.like=0
            article.html=data['html']
            article.status=1
            article.save()
            response['msg']='PUBLISH'
            return HttpResponse(json.dumps(response))
        else:
            id=data['id']
            title = data['title']
            content = data['content']
            html = data['html']
            kind = data['kind']
            time=datetime.datetime.now()
            response['msg'] = 'UPDATE'
            Article.objects.filter(id=id).update(title=title,content=content,html=html,kind=kind,time=time,status=1)
            return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def uploadpic(request):
    response = {}
    if request.method == 'POST':
        userid=request.POST.get('id')
        pic = request.FILES.get('pic')
        pic_name = userid+pic.name
        f = open(os.path.join(settings.MEDIA_ROOT, pic_name), 'wb')
        for i in pic.chunks():
            f.write(i)
        f.close()
        if userid!='':
            User.objects.filter(id=userid).update(avatarurl='http://127.0.0.1:8000' + '/media/'+pic_name)
        response['msg'] = 'OK'
        response['url']='/media/'+pic_name
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def select_in_like(request):
    #查看当前文章是否被点赞
    response={}
    if request.method=='POST':
        data=json.loads(request.body)
        userid=int(data['userid'])
        articleid=int(data['articleid'])
        res=Like.objects.filter(userid=userid,articleid=articleid)
        if len(res)>0:
            response['msg']='Liked'
        else:
            response['msg']='Unliked'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def select_all_like(request):
    #获取某个用户点赞的所有文章
    response = {}
    if request.method == 'GET':
        text = []
        author = []
        articles=[]
        userid=int((request.GET.get('userid')))
        res = Like.objects.filter(userid=userid)
        for item in res:
            article=Article.objects.get(id=item.articleid,status=1)
            print(article)
            articles.append(article)
            author_id=article.author_id
            author.append(User.objects.get(id=author_id).username)
            html = markdown(article.content)
            str=''.join(BeautifulSoup(html).findAll(text=True))
            if len(str)>100:
               text.append(str[:100])
            else:text.append(str)
        response['list'] = json.loads(serializers.serialize("json", articles))
        response['text'] = text
        response['author'] = author
        response['msg'] = 'OK'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def collect(request):
    response = {}
    if request.method == 'POST':
        data = json.loads(request.body)
        userid = int(data['userid'])
        articleid = int(data['articleid'])
        like=Like()
        like.userid=userid
        like.articleid=articleid
        like.save()
        article= Article.objects.get(id=articleid)
        Article.objects.filter(id=articleid).update(count=article.count+1)
        response['msg']='OK'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def uncollect(request):
    response = {}
    if request.method == 'POST':
        data = json.loads(request.body)
        userid = int(data['userid'])
        articleid = int(data['articleid'])
        Like.objects.filter(userid=userid,articleid=articleid).delete()
        article = Article.objects.get(id=articleid)
        print(article.count)
        Article.objects.filter(id=articleid).update(count=article.count - 1)
        response['msg'] = 'OK'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def select_in_attention(request):
    #查看当前文章是否被点赞
    response={}
    if request.method=='POST':
        data=json.loads(request.body)
        liking=int(data['liking'])
        liked=int(data['liked'])
        res=Attention.objects.filter(liking=liking,liked=liked)
        if len(res)>0:
            response['msg']='Attentioned'
        else:
            response['msg']='Notattention'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def attention(request):
    response = {}
    if request.method == 'POST':
        data = json.loads(request.body)
        liking = int(data['liking'])
        liked = int(data['liked'])
        attention=Attention()
        attention.liking=liking
        attention.liked=liked
        attention.save()
        response['msg']='OK'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def unattention(request):
    response = {}
    if request.method == 'POST':
        data = json.loads(request.body)
        liking = int(data['liking'])
        liked = int(data['liked'])
        Attention.objects.filter(liking=liking,liked=liked,).delete()
        response['msg']='OK'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def getattention(request):
    response = {}
    if request.method == 'GET':
        usering=[]
        usered=[]
        userid = int(request.GET.get('userid'))
        likings=Attention.objects.filter(liking=userid).distinct()
        likeds = Attention.objects.filter(liked=userid).distinct()
        for item in likings:
            user=User.objects.get(id=item.liked)
            if user not in usering:
                usering.append(user)
        for item in likeds:
            user = User.objects.get(id=item.liking)
            if user not in usered:
                usered.append(user)
        response['liking'] = json.loads(serializers.serialize("json", usering))
        response['liked'] = json.loads(serializers.serialize("json", usered))
        response['msg']='OK'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def article_del(request):
    response = {}
    if request.method == 'POST':
        data = json.loads(request.body)
        id = int(data['id'])
        Article.objects.filter(id=id).delete()
        Like.objects.filter(articleid=id).delete()
        response['msg'] = 'OK'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def getdraft(request):
    #获取某个用户的草稿，需要传入用户的id
    response = {}
    if request.method == 'GET':
        text = []
        author = []
        authorid=int(request.GET.get('id'))
        res=Article.objects.filter(author_id=authorid,status=2)
        for item in res:
            author.append(User.objects.get(id=item.author_id).username)
            html = markdown(item.content)
            str=''.join(BeautifulSoup(html).findAll(text=True))
            if len(str)>100:
               text.append(str[:100])
            else:text.append(str)
        response['list'] = json.loads(serializers.serialize("json", res))
        response['text'] = text
        response['author'] = author
        response['msg']='OK'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def draft_pub(request):
    #保存草稿
    response = {}
    if request.method == 'POST':
        data = json.loads(request.body)
        if data['id'] == -1:
            article = Article()
            article.title = data['title']
            article.content = data['content']
            article.author_id = data['authorid']
            article.kind = -1
            article.like = 0
            article.html = data['html']
            article.status = 2
            print(article)
            article.save()
            response['msg'] = 'newDraft'
            return HttpResponse(json.dumps(response))
        else:
            id = data['id']
            title = data['title']
            content = data['content']
            html = data['html']
            kind = -1
            time = datetime.datetime.now()
            response['msg'] = 'updateDraft'
            Article.objects.filter(id=id).update(title=title, content=content, html=html, kind=kind, time=time)
            return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def search(request):
    #搜索
    response = {}
    if request.method == 'GET':
        text = []
        author = []
        article=[]
        key = request.GET.get('key')
        if key == '':
            response['list'] = []
            response['text'] = text
            response['author'] = author
            response['msg'] = 'OK'
            return HttpResponse(json.dumps(response))
        res = Article.objects.filter(Q(title__icontains=key) | Q(content__icontains=key), status=1)
        for item in res:
            html = markdown(item.content)
            str = ''.join(BeautifulSoup(html).findAll(text=True))
            if str.count(key)!=0 or item.title.count(key)!=0:
                article.append(item)
                author.append(User.objects.get(id=item.author_id).username)
                if len(str) > 100:
                    text.append(str[:100])
                else:
                    text.append(str)
        response['list'] = json.loads(serializers.serialize("json", article))
        response['text'] = text
        response['author'] = author
        response['msg'] = 'OK'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def getcomment(request):
    response = {}
    author=[]
    time=[]
    if request.method == 'GET':
        articleid = request.GET.get('articleid')
        res = Comment.objects.filter(articleid=articleid)
        for item in res:
            time.append(item.time.strftime('%Y-%m-%d'))
            author.append(User.objects.get(id=item.userid))
        response['comment'] = json.loads(serializers.serialize("json", res))
        response['author']=json.loads(serializers.serialize("json", author))
        response['time']=time
        response['msg']='OK'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def addcomment(request):
    response = {}
    comment=Comment()
    if request.method == 'POST':
        data=json.loads(request.body)
        comment.userid=data['userid']
        comment.articleid=data['articleid']
        comment.status=data['status']
        comment.value=data['value']
        if data['status']==1:
            comment.towhich=data['towhich']
        comment.time=datetime.datetime.now()
        comment.save()
        response['msg']='OK'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def delcomment(request):
    response = {}
    if request.method == 'POST':
        data=json.loads(request.body)
        id=int(data['id'])
        Comment.objects.filter(id=id).delete()
        response['msg']='OK'
        return HttpResponse(json.dumps(response))
    else:
        response['msg'] = 'fail'
        return HttpResponse(json.dumps(response, ensure_ascii=False))
