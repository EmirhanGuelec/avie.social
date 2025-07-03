import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm, ProfileForm
from meine_app.backend.registrierung_login.pruefung import check_login
from meine_app.backend.registrierung_login import registrierung as mod_registrierung
from meine_app.backend.registrierung_login import login as mod_login
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password


USER_JSON_PATH = os.path.join(
    settings.BASE_DIR,
    'meine_app',
    'backend',
    'registrierung_login',
    'users.json'
)

@login_required
def startseite(request):
    username = request.user.username
    
    posts = Post.objects.all().order_by('-created_at')
    post_form = PostForm()
    comment_form = CommentForm()
    liked_posts = list(
        Like.objects.filter(username=username, post__in=posts)
            .values_list('post_id', flat=True)
    )
    return render(request, "meine_app/index.html", {
        'posts': posts,
        'post_form': post_form,
        'comment_form': comment_form,
        'username': username,
        'liked_posts': liked_posts,
    })

@login_required
def create_post(request):
    username = request.user.username
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = username
            post.save()
            return redirect('startseite')
    else:
        form = PostForm()
    return render(request, "meine_app/posten.html", {
        'post_form': form,
        'username': username,
        
    })

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user.username
            comment.post = post
            comment.save()
    return redirect('startseite')

@login_required
def toggle_like_ajax(request):
    if request.method != "POST" or request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Nur AJAX-POST erlaubt"}, status=400)
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    user = request.user.username
    like, created = Like.objects.get_or_create(post=post, username=user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({"liked": liked, "count": post.likes.count()})

@login_required
def add_comment_ajax(request):
    if request.method != "POST" or request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Nur AJAX-POST erlaubt"}, status=400)
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    content = request.POST.get("content", "").strip()
    if not content:
        return JsonResponse({"error": "Kommentar darf nicht leer sein"}, status=400)
    author = request.user.username
    comment = Comment.objects.create(post=post, author=author, content=content)
    return JsonResponse({
        "author": author,
        "content": comment.content,
        "created_at": comment.created_at.strftime("%d.%m.%Y %H:%M")
    })
def register(request):
    return mod_registrierung.registrieren(request, USER_JSON_PATH)

def login_check(request):
    return mod_login.login_check(request, USER_JSON_PATH)

def saveUploadedFile(request):
    if request.method == "POST" and request.FILES.get("datei"):
        datei = request.FILES["datei"]
        FileSystemStorage("/var/www/static/dateien/").save(datei.name, datei)
    return render(request, "meine_app/template.html")

@login_required
def chat(request):
    username = request.user.username
    
    return render(request, "meine_app/chat.html")

@login_required
def freunde(request):
    username = request.user.username
    
    return render(request, "meine_app/freunde.html")


def impressum(request):
    username = request.user.username
    
    return render(request, "meine_app/impressum.html")

#def login(request):
    #return render(request, "meine_app/login.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('startseite')  
        else:
            messages.error(request, 'Benutzername oder Passwort ist falsch.')
    
    return render(request, 'meine_app/login.html')

@login_required
def posten(request):
    username = request.user.username
    
    form = PostForm()

    if request.method == "POST" and request.FILES.get("datei"):
        datei = request.FILES["datei"]
        FileSystemStorage("/var/www/static/dateien/").save(datei.name, datei)
       

    return render(request, "meine_app/posten.html", {
        "username": username,
        "post_form": form
    })


def registrierung(request):
    return render(request, "meine_app/registrierung.html")

@login_required
def suche(request):
    username = request.user.username
    
    query    = request.GET.get("q", "").strip()
    users    = []

    if query:
        try:
            with open(USER_JSON_PATH, 'r', encoding='utf-8') as f:
                all_users = json.load(f)
            for u in all_users:
                uname = u.get('username') or ''
                if query.lower() in uname.lower():
                    users.append(u)
        except FileNotFoundError:
            print(f"users.json nicht gefunden unter {USER_JSON_PATH}")
        except json.JSONDecodeError:
            print("users.json enthält ungültiges JSON")

    return render(request, "meine_app/suche.html", {
        'username': username,
        'users':    users,
        'query':    query,
    })

@login_required
def profilseite(request):
    
    current_user = request.user.username
    
    profile_user = request.GET.get("profil", current_user)

    # Beiträge des Profil-Users laden
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')

    # Profil-Daten aus users.json holen
    try:
        with open(USER_JSON_PATH, 'r', encoding='utf-8') as f:
            all_users = json.load(f)
        user_data = next((u for u in all_users if u.get('username') == profile_user), {})
    except Exception:
        user_data = {}

    avatar_url = user_data.get('avatar_url', '')
    bio        = user_data.get('bio', '')
    location   = user_data.get('location', '')

    return render(request, "meine_app/profilseite.html", {
        'username':     current_user,
        'profile_user': profile_user,
        'posts':        posts,
        'avatar_url':   avatar_url,
        'bio':          bio,
        'location':     location,
    })

@login_required
def edit_profile(request):
    username = request.user.username

    # JSON laden und aktuellen Nutzer finden
    with open(USER_JSON_PATH, 'r', encoding='utf-8') as f:
        all_users = json.load(f)
    user_data = next((u for u in all_users if u.get('username') == username), None)
    if user_data is None:
        return redirect (reverse('startseite'))

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            avatar_file = form.cleaned_data['avatar']
            if avatar_file:
                fs = FileSystemStorage(
                    location=os.path.join(settings.MEDIA_ROOT, 'profile_pics'),
                    base_url=settings.MEDIA_URL + 'profile_pics/'
                )
                fname = f"{username}_{avatar_file.name}"
                saved_name = fs.save(fname, avatar_file)
                user_data['avatar_url'] = fs.url(saved_name)
            user_data['bio']      = form.cleaned_data['bio']
            user_data['location'] = form.cleaned_data['location']

            with open(USER_JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump(all_users, f, indent=2, ensure_ascii=False)

            return redirect(reverse('profilseite'))
    else:
        form = ProfileForm(initial={
            'bio':      user_data.get('bio', ''),
            'location': user_data.get('location', '')
        })

    return render(request, "meine_app/edit_profile.html", {
        'form':       form,
        'avatar_url': user_data.get('avatar_url', ''),
        'username':   username,
    })


@login_required
def einstellungen(request):
    username = request.user.username
    
    return render(request, "meine_app/einstellungen.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def delete_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        if post.author == request.user.username:
            post.delete()
            messages.success(request, "Beitrag erfolgreich gelöscht.")
        else:
            messages.error(request, "Du kannst diesen Beitrag nicht löschen.")
    return redirect('profilseite')