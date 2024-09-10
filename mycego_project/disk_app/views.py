import requests
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import PublicLinkForm
from typing import Dict, Any
from django.core.cache import cache

def list_files(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PublicLinkForm(request.POST)
        if form.is_valid():
            public_key = form.cleaned_data['public_key']
            file_type = form.cleaned_data['file_type']

            # Проверяем наличие кэша
            cached_files = cache.get(public_key)
            if cached_files:
                files_data = cached_files
            else:
                api_url = f"https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}"
                response = requests.get(api_url)

                if response.status_code == 200:
                    data: Dict[str, Any] = response.json()

                    if '_embedded' in data:
                        files_data = data['_embedded']['items']
                        cache.set(public_key, files_data, timeout=60*15)  # Кэшируем на 15 минут
                    else:
                        files_data = [data]  # Одиночный файл
                        cache.set(public_key, files_data, timeout=60*15)
                else:
                    return render(request, 'disk_app/error.html', {'error': response.text})

            # Фильтруем по типу файла
            if file_type == 'documents':
                files_data = [f for f in files_data if f['mime_type'].startswith('application')]
            elif file_type == 'images':
                files_data = [f for f in files_data if f['mime_type'].startswith('image')]

            return render(request, 'disk_app/files_list.html', {'files': files_data})
    else:
        form = PublicLinkForm()

    return render(request, 'disk_app/index.html', {'form': form})


