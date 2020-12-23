from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.core.mail import send_mail
from django.conf import settings as config
from django.template.loader import render_to_string

from django.views.decorators.csrf import csrf_exempt


from .models import Profile
from news.models import Article
from django.http import JsonResponse
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            email = user_form.cleaned_data.get('email')
            messages.success(request, f'Account created for {username}! Log in below')
            template = render_to_string('users/email_template.html', {'username': username})
            send_mail(
                'Welcome',
                template,
                config.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('login')
    else:
        user_form = UserRegisterForm()
    return render(request, 'users/register.html', { 
        'user_form': user_form,
        })


@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def settings(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        prof_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            messages.success(request, f'Account updated!')
            return redirect('profile')
    
    else:
        user_form = UserUpdateForm(instance=request.user)
        prof_form = ProfileUpdateForm(instance=request.user.profile)

    
    context = {
        'user_form': user_form,
        'prof_form': prof_form
    }

    return render(request, 'users/settings.html', context)

@csrf_exempt
@ login_required
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('articleid'))
        article = get_object_or_404(Article, id=id)
        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user)
            article.like_count -= 1
            result = article.like_count
            article.save()
        else:
            article.likes.add(request.user)
            article.like_count += 1
            result = article.like_count
            article.save()

        return JsonResponse({'result': result, })
