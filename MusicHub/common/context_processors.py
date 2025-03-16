def is_authenticated(request):
    return {'is_auth' : request.user.is_authenticated}