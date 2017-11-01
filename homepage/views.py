from django.shortcuts import render

# Create your views here.

def index(req):
    class Item:
        def __init__(self, link, content):
            self.link = link
            self.content = content

    items = [
        Item('/accounts/login/', 'Login'),
        Item('/accounts/signup/', 'Signup'),
        Item('/store/', 'Guest'),
    ]
    return render(req, 'homepage/index.html', {'items': items})
