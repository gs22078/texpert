from django.http import HttpResponse
from django.shortcuts import render
import requests
import os

repos = [
    {'owner': 'gshsTeXperT', 'repo': 'TeXperT-templates'},
    {'owner': 'gshstexsociety', 'repo': 'gshs-format'}
]


def github_api_requests(url):
    github_token = os.environ['GITHUB_TOKEN']
    headers = {'Authorization': f'token {github_token}'}
    return requests.get(url, headers=headers)


def index(request):
    tmp = []
    for repo in repos:
        req = github_api_requests(f'https://api.github.com/repos/{repo["owner"]}/{repo["repo"]}').json()
        avatar = req['owner']['avatar_url']
        description = req['description']
        tmp.append({'owner': repo['owner'], 'repo': repo['repo'], 'avatar': avatar, 'description': description})
    context = {'repos': tmp}
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
