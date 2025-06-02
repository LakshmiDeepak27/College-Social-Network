from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

from .models import *


def get_notification_count(user):
    if user.is_authenticated:
        return Notification.objects.filter(recipient=user, is_read=False).count()
    return 0

def index(request):
    # Always ensure sample users exist (for demo/testing)
    sample_users = [
        {
            'username': 'john_doe',
            'first_name': 'John',
            'last_name': 'Doe',
            'content': 'Excited to share that I\'ve joined Google as a Senior Software Engineer! DSATM gave me the foundation I needed. #DSATMAlumni #TechCareer',
            'profile_pic': 'profile_pic/alumni1.jpg',
            'bio': 'Software Engineer @ Google | DSATM Alumni 2020'
        },
        {
            'username': 'sarah_smith',
            'first_name': 'Sarah',
            'last_name': 'Smith',
            'content': 'Just completed my Master\'s in Data Science from Stanford! Thank you DSATM for the amazing journey. #DSATMPride #DataScience',
            'profile_pic': 'profile_pic/alumni2.jpg',
            'bio': 'Data Scientist | Stanford Graduate | DSATM Alumni 2019'
        },
        {
            'username': 'mike_wilson',
            'first_name': 'Mike',
            'last_name': 'Wilson',
            'content': 'Started my own tech startup! The entrepreneurial spirit I developed at DSATM has been invaluable. #DSATMInnovation #StartupLife',
            'profile_pic': 'profile_pic/alumni3.jpg',
            'bio': 'Founder & CEO @ TechStart | DSATM Alumni 2018'
        },
        {
            'username': 'emma_chen',
            'first_name': 'Emma',
            'last_name': 'Chen',
            'content': 'Back on campus for the annual tech symposium! Great to see how DSATM has grown. #DSATMHomecoming #TechCommunity',
            'profile_pic': 'profile_pic/alumni4.jpg',
            'bio': 'Product Manager @ Microsoft | DSATM Alumni 2021'
        },
        {
            'username': 'alex_kumar',
            'first_name': 'Alex',
            'last_name': 'Kumar',
            'content': 'Just published my research paper on AI in healthcare! Thanks to my professors at DSATM for the guidance. #DSATMResearch #AIHealthcare',
            'profile_pic': 'profile_pic/alumni5.jpg',
            'bio': 'AI Researcher | PhD Candidate | DSATM Alumni 2020'
        }
    ]
    for user_data in sample_users:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'profile_pic': user_data['profile_pic'],
                'bio': user_data['bio'],
                'is_active': True
            }
        )
        if created:
            Post.objects.create(
                creater=user,
                content_text=user_data['content']
            )
            Post.objects.create(
                creater=user,
                content_text=f"Remembering my time at DSATM - the late night coding sessions, the hackathons, and the amazing friends I made. #DSATMMemories #CollegeLife"
            )
    all_posts = Post.objects.all().order_by('-date_created')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)
    suggestions = User.objects.exclude(username=request.user.username) if request.user.is_authenticated else User.objects.all()
    suggestions = suggestions.order_by('?')[:5]
    return render(request, "network/index.html", {
        "posts": posts,
        "suggestions": suggestions,
        "page": "all_posts",
        'profile': False,
        'unread_notifications_count': get_notification_count(request.user) if request.user.is_authenticated else 0
    })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("all_posts"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            email = request.POST.get("email")
            fname = request.POST.get("firstname")
            lname = request.POST.get("lastname")
            password = request.POST.get("password")
            confirmation = request.POST.get("confirmation")
            profile = request.FILES.get("profile")
            cover = request.FILES.get('cover')

            if not all([username, email, fname, lname, password, confirmation]):
                return render(request, "network/register.html", {
                    "message": "All fields are required."
                })

            # Ensure password matches confirmation
            if password != confirmation:
                return render(request, "network/register.html", {
                    "message": "Passwords must match."
                })

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.first_name = fname
                user.last_name = lname
                if profile is not None:
                    user.profile_pic = profile
                else:
                    user.profile_pic = "profile_pic/no_pic.png"
                if cover is not None:
                    user.cover = cover
                user.save()
                Follower.objects.create(user=user)
            except IntegrityError:
                return render(request, "network/register.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("all_posts"))
        except Exception as e:
            return render(request, "network/register.html", {
                "message": f"An error occurred: {str(e)}"
            })
    else:
        return render(request, "network/register.html")



def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'network/user_not_found.html', { 'username': username })
    all_posts = Post.objects.filter(creater=user).order_by('-date_created')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    followings = []
    suggestions = []
    follower = False
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]

        follower_obj, _ = Follower.objects.get_or_create(user=user)
        if request.user in follower_obj.followers.all():
            follower = True
    else:
        follower_obj, _ = Follower.objects.get_or_create(user=user)

    follower_count = follower_obj.followers.all().count()
    following_count = Follower.objects.filter(followers=user).count()
    return render(request, 'network/profile.html', {
        "username": user,
        "posts": posts,
        "posts_count": all_posts.count(),
        "suggestions": suggestions,
        "page": "profile",
        "is_follower": follower,
        "follower_count": follower_count,
        "following_count": following_count
    })

def following(request):
    if request.user.is_authenticated:
        # Get the list of user IDs the current user is following
        following_user_ids = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        # Get posts from those users
        all_posts = Post.objects.filter(creater__id__in=following_user_ids).order_by('-date_created')
        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        if page_number is None:
            page_number = 1
        posts = paginator.get_page(page_number)
        # Suggestions: show users you are not following and not yourself
        suggestions = User.objects.exclude(id__in=following_user_ids).exclude(username=request.user.username).order_by("?")[:6]
        return render(request, "network/index.html", {
            "posts": posts,
            "suggestions": suggestions,
            "page": "following"
        })
    else:
        return HttpResponseRedirect(reverse('login'))

def saved(request):
    if request.user.is_authenticated:
        all_posts = Post.objects.filter(savers=request.user).order_by('-date_created')

        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        if page_number == None:
            page_number = 1
        posts = paginator.get_page(page_number)

        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        return render(request, "network/index.html", {
            "posts": posts,
            "suggestions": suggestions,
            "page": "saved"
        })
    else:
        return HttpResponseRedirect(reverse('login'))
        

def create_post(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
        
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        pic = request.FILES.get('picture')
        
        if not text and not pic:
            return JsonResponse({
                'error': 'Post must contain either text or an image'
            }, status=400)
            
        try:
            post = Post.objects.create(
                creater=request.user,
                content_text=text,
                content_image=pic
            )
            return HttpResponseRedirect(reverse('all_posts'))
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)
    else:
        return HttpResponseRedirect(reverse('all_posts'))


@csrf_exempt
def edit_post(request, post_id):
    if request.method == 'POST':
        try:
            text = request.POST.get('text', '')
            pic = request.FILES.get('picture')
            img_chg = request.POST.get('img_change', 'false')
            post_id = request.POST.get('id')
            
            if not post_id:
                return JsonResponse({
                    "success": False,
                    "error": "Post ID is required"
                })
                
            post = Post.objects.get(id=post_id)
            if post.creater != request.user:
                return JsonResponse({
                    "success": False,
                    "error": "You don't have permission to edit this post"
                })
                
            try:
                post.content_text = text
                if img_chg != 'false' and pic is not None:
                    post.content_image = pic
                post.save()
                
                response_data = {
                    "success": True,
                    "text": post.content_text or False,
                    "picture": post.img_url() if post.content_image else False
                }
                return JsonResponse(response_data)
            except Exception as e:
                return JsonResponse({
                    "success": False,
                    "error": str(e)
                })
        except Post.DoesNotExist:
            return JsonResponse({
                "success": False,
                "error": "Post not found"
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            })
    else:
        return HttpResponse("Method must be 'POST'")

@csrf_exempt
def like_post(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        if request.user in post.likers.all():
            post.likers.remove(request.user)
            return JsonResponse({"message": "Post unliked", "likes": post.likers.count()})
        else:
            post.likers.add(request.user)
            # Send notification
            from notifications.utils import create_notification
            create_notification(
                recipient=post.creater,
                sender=request.user,
                notification_type='like',
                post=post
            )
            return JsonResponse({"message": "Post liked", "likes": post.likers.count()})
    else:
        return HttpResponse("Method must be 'POST'")

@csrf_exempt
def unlike_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            print(post)
            try:
                post.likers.remove(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def save_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            print(post)
            try:
                post.savers.add(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def unsave_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            print(post)
            try:
                post.savers.remove(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def follow(request, username):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        follow_obj, _ = Follower.objects.get_or_create(user=user)
        if request.user in follow_obj.followers.all():
            follow_obj.followers.remove(request.user)
            return JsonResponse({"message": "Unfollowed", "followers": follow_obj.followers.count()})
        else:
            follow_obj.followers.add(request.user)
            # Send notification
            from notifications.utils import create_notification
            create_notification(
                recipient=user,
                sender=request.user,
                notification_type='follow'
            )
            return JsonResponse({"message": "Followed", "followers": follow_obj.followers.count()})
    else:
        return HttpResponse("Method must be 'POST'")

@csrf_exempt
def unfollow(request, username):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            user = User.objects.get(username=username)
            print(f".....................User: {user}......................")
            print(f".....................Unfollower: {request.user}......................")
            try:
                follower = Follower.objects.get(user=user)
                follower.followers.remove(request.user)
                follower.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def comment(request, post_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.create(
            post=post,
            commenter=request.user,
            comment_content=data.get('comment')
        )
        post.comment_count += 1
        post.save()
        
        # Send notification
        from notifications.utils import create_notification
        create_notification(
            recipient=post.creater,
            sender=request.user,
            notification_type='comment',
            post=post,
            comment=comment
        )
        
        return JsonResponse(comment.serialize())
    else:
        return HttpResponse("Method must be 'POST'")

@csrf_exempt
def delete_post(request, post_id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(id=post_id)
            if request.user == post.creater:
                try:
                    delet = post.delete()
                    return HttpResponse(status=201)
                except Exception as e:
                    return HttpResponse(e)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))
