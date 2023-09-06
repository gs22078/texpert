from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import os
from datetime import datetime
import zipfile

repos = [
    {'owner': 'gshsTeXperT', 'repo': 'TeXperT-templates'},
    {'owner': 'gshstexsociety', 'repo': 'gshs-format'}
]


def github_api_requests(url, public=True):
    key = 'PUBLIC' if public else 'PRIVATE'
    github_token = os.environ[f'GITHUB_TOKEN_{key}']
    headers = {'Authorization': f'token {github_token}'}
    return requests.get(url, headers=headers)


def index(request):
    tmp = []
    for repo in repos:
        req = github_api_requests(f'https://api.github.com/repos/{repo["owner"]}/{repo["repo"]}').json()
        avatar = req['owner']['avatar_url']
        description = req['description']
        last_mod = datetime.strptime(req['pushed_at'], '%Y-%m-%dT%H:%M:%SZ')
        last_mod = last_mod.strftime('%Y-%m-%d')
        tmp.append({'owner': repo['owner'], 'repo': repo['repo'], 'avatar': avatar, 'description': description,
                    'last_mod': last_mod})
    context = {'repos': tmp}
    return render(request, 'downloads/index.html', context)


def repo_page(request, owner, repo):
    if {'owner': owner, 'repo': repo} not in repos:
        return HttpResponse('404 Not Found')
    ref = github_api_requests(f'https://api.github.com/repos/{owner}/{repo}').json()['default_branch']
    template_api = f'https://api.github.com/repos/{owner}/{repo}/git/trees/{ref}'
    templates = github_api_requests(template_api).json()['tree']
    trees = [template for template in templates if template['type'] == 'tree' and not template['path'].startswith('.')]
    blobs = [template for template in templates if template['type'] == 'blob' and not template['path'].startswith('.')]
    context = {'trees': trees, 'blobs': blobs, 'owner': owner, 'repo': repo, 'ref': ref}
    return render(request, 'downloads/repo_page.html', context)


try:
    tmp = os.environ['HOME']
except KeyError:
    tmp = os.environ['TMP']


def download(request, owner, repo, ref, path, get_font=False):
    global fonts
    if {'owner': owner, 'repo': repo} not in repos:
        pass
    dir_api = f'https://api.github.com/repos/{owner}/{repo}/git/trees/{ref}:{path}?recursive=1'
    dir_tree = github_api_requests(dir_api).json()['tree']
    blobs = [blob for blob in dir_tree if blob['type'] == 'blob']
    zip_file = zipfile.ZipFile(f'{tmp}/{path}.zip', 'w')
    for blob in blobs:
        if blob['path'] == 'fonts.json':
            fonts = requests.get(f'https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}/fonts.json').json()
            continue
        content_raw = f'https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}/{blob["path"]}'
        content = requests.get(content_raw).content
        zip_file.writestr(blob['path'], content)
    if get_font:
        for lang in fonts:
            for font in fonts[lang]:
                font_raw = f'https://raw.githubusercontent.com/gs22078/TeX-fonts/main/{lang}/{font}'
                font_content = github_api_requests(font_raw, public=False).content
                zip_file.writestr(f'fonts/{font}', font_content)
    zip_file.close()
    return


def download_repo(request, owner, repo, ref, path):
    if {'owner': owner, 'repo': repo} not in repos:
        pass
    download(request, owner, repo, ref, path, get_font=True)
    response = HttpResponse(open(f'{tmp}/{path}.zip', 'rb'), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={path}.zip'
    os.remove(f'{tmp}/{path}.zip')
    return response


def download_file(request, owner, repo, ref, path):
    if {'owner': owner, 'repo': repo} not in repos:
        pass
    content_raw = f'https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}'
    content = requests.get(content_raw).content
    response = HttpResponse(content, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={path}'
    return response


def open_in_overleaf(request, owner, repo, ref, path):
    if {'owner': owner, 'repo': repo} not in repos:
        pass
    download(request, owner, repo, ref, path, get_font=True)
    url = f'https://www.overleaf.com/docs?snip_uri=https://texpert.azurewebsites.net/downloads/{owner}/{repo}/o/{ref}/{path}.zip'
    return redirect(url)


def open_in_overleaf_zip(request, owner, repo, ref, path):
    if {'owner': owner, 'repo': repo} not in repos:
        pass
    tmp = os.environ['HOME']
    response = HttpResponse(open(f'{tmp}/{path}.zip', 'rb'), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={path}.zip'
    os.remove(f'{tmp}/{path}.zip')
    return response
