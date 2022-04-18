from django.http import HttpResponse


def email_success(request):
    res = "Your email is verified!"
    return HttpResponse("<p>%s</p>" % res)
