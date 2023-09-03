from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
import requests

def index(request):
    # Get GitHub Tree API
    # https://api.github.com/repos/gshsTeXperT/gshsTeXperT-Templates/git/trees/main
    template_api = "https://api.github.com/repos/gshsTeXperT/TeXperT-templates/git/trees/main"
    templates = requests.get(template_api).json()["tree"]
    # separate trees and blobs
    trees = [template for template in templates if template["type"] == "tree" and not template["path"].startswith(".")]
    blobs = [template for template in templates if template["type"] == "blob" and not template["path"].startswith(".")]
    return render(request, "downloads/index.html", {'trees': trees, 'blobs': blobs})
