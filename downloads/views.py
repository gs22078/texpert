from django.http import HttpResponse
from django.shortcuts import render
import requests

repos = [
    {'owner': 'gshsTeXperT', 'repo': 'TeXperT-templates'},
    {'owner': 'gshstexsociety', 'repo': 'gshs-format'}
]


def index(request):
    context = {'repos': repos}
    return render(request, 'downloads/index.html', context)


def repo_page(request, owner, repo):
    if {'owner': owner, 'repo': repo} not in repos:
        return HttpResponse('404 Not Found')
    ref = requests.get(f'https://api.github.com/repos/{owner}/{repo}').json()['default_branch']
    template_api = f'https://api.github.com/repos/{owner}/{repo}/git/trees/{ref}'
    templates = requests.get(template_api).json()['tree']
    trees = [template for template in templates if template['type'] == 'tree' and not template['path'].startswith('.')]
    blobs = [template for template in templates if template['type'] == 'blob' and not template['path'].startswith('.')]
    context = {'trees': trees, 'blobs': blobs, 'owner': owner, 'repo': repo}
    return render(request, 'downloads/repo_page.html', context)
