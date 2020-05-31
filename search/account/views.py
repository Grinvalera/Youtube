import requests

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.conf import settings
from django.views.generic.edit import FormView, View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from isodate import parse_duration

from .models import Video, VideoInfo, User, Cart


def youtube(request):
    return render(request, 'account/youtube.html', {'section': youtube})


def search(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        quest = Video(search=request.POST['search'])

        if Video.objects.filter(search=quest).exists():
            videos = VideoInfo.objects.filter(search__search=quest)
            return render(request, 'account/search.html', locals())

        else:
            search_params = {
                'part': 'snippet',
                'q': request.POST['search'],
                'key': settings.API_KEY_YOUTUBE,
                'maxResults': 9,
                'type': 'video'
            }

            g = Video(search=request.POST['search'])
            g.save()

            r = requests.get(search_url, params=search_params)

            results = r.json()['items']

            video_ids = []
            for result in results:
                video_ids.append(result['id']['videoId'])

            if request.POST['submit'] == 'lucky':
                return redirect(f'https://www.youtube.com/watch?v={video_ids[0]}')

            video_params = {
                'key': settings.API_KEY_YOUTUBE,
                'part': 'snippet,contentDetails',
                'id': ','.join(video_ids),
                'maxResults': 9
            }

            r = requests.get(video_url, params=video_params)

            results = r.json()['items']

            for result in results:
                video_data = {
                    'search': request.POST['search'],
                    'title': result['snippet']['title'],
                    'id': result['id'],
                    'url': f'https://www.youtube.com/watch?v={result["id"]}',
                    'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                    'thumbnail': result['snippet']['thumbnails']['high']['url']
                }

                video = VideoInfo(search=g,
                                  title=result['snippet']['title'],
                                  ide=result['id'],
                                  url=f'https://www.youtube.com/watch?v={result["id"]}',
                                  duration=int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                                  thumbnail=result['snippet']['thumbnails']['high']['url'],
                                  )

                video.save()

                videos.append(video_data)

        video_id = Video.objects.first()

        context_object_name = {
            'videos': videos,
            'id': video_id,
        }
        return render(request, 'account/search.html', context_object_name)


def cart(request, pk):
    user = User.objects.get(username=request.user)
    video = VideoInfo.objects.get(id=pk)

    favorites = Cart(user=user,
                     title=video.title,
                     ide=video.ide,
                     url=video.url,
                     duration=video.duration,
                     thumbnail=video.thumbnail,
                     )

    favorites.save()
    return HttpResponseRedirect("/youtube/favorite")


def favorite(request):
    user = User.objects.get(username=request.user)
    video = Cart.objects.all().filter(user=user)
    return render(request, 'account/cart.html', locals())


class RegisterFormView(FormView):
    form_class = UserCreationForm

    success_url = "/youtube/login/"
    template_name = "registration/registration.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm

    template_name = "registration/login.html"
    success_url = "/youtube/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/youtube/")
