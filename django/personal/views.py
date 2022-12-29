from django.shortcuts import render

def index(request):
    ''' return the homepage'''
    return render(request, "index.html")

def experience(request):
    ''' return the table of career path page'''
    return render(request, "experience.html")

def filler(request):
    ''' return the bonus page'''
    return render(request, "filler.html")

