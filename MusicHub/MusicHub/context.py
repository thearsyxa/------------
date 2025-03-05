from MusicHub_App.models import Artist

def test_context(request):
    ud = request.COOKIES.get("user_data", None)
    print("COOKIE_USER_DATA", ud)
    return {"user_data": Artist.objects.get(id=1)}