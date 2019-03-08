from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm
from rango.forms import UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index(request):
    # context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    # # return HttpResponse('Rango!')
    # return render(request, 'rango/index.html', context=context_dict)
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {"first": "shen", "second": "wei"}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    print("add_category")
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            cat = form.save(commit=True)
            print(cat, cat.slug)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    print(form)
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

# 注册
def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # 把UserForm中的数据存入数据库
            user = user_form.save()

            # 使用set_passwd 方法计算密码哈希值
            # 然后更新user对象
            user.set_password(user.password)
            user.save()

            # 处理UserProfile实例 因为要自行处理user属性，所以设定 commit=False
            # 延迟保存模型 以防止出现完整性问题
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print (user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # 根据上下文渲染模板
    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form':profile_form, 'registered':registered})

# 登录视图
def user_login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        # 返回一个User对象 
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user) 
                # 状态码 302 不是表示成功的200 reverse 函数找到index的url
                return HttpResponseRedirect(reverse('index'))
            else:
                # 账户未激活，禁止登录
                return HttpResponse("Your Rango account is disabled.")
        else:
            # 提供的账户或者密码有问题
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("账号或密码错误！")
    # 不是Http Post 请求， 显示登录表单
    else:
        return render(request, 'rango/login.html', {})

# 限制登录访问
def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse('You are logged in.')
    else:
        return HttpResponse("You are not logged in.")


# 使用装饰器限制访问 (类似于中间件的功能)
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


# 退出功能
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
