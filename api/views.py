from django.shortcuts import redirect


def redirect_view(request):
    response = redirect('api/v1/')
    return response
