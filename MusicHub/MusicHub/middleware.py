from django.utils.timezone import now


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response=get_response
    
    
    def __call__(self, request):
        print(f"[{now()}] Incoming request: {request.method} {request.path}")
        if not request.COOKIES.get('user_data'):
            print("Cookie 'user_data' отсутствует. Оно будет установлено после обработки запроса.")
        response = self.get_response(request)

        if not request.COOKIES.get('user_data'):
            response.set_cookie(
                "user_data", 
                "Custom value set by middleware",
                max_age=3600,  
                httponly=True, 
                secure=False,  
                samesite="Lax"  
            )
            print("Cookie 'user_data' установлено.")
        print(f"[{now()}] Response status code: {response.status_code}")
        return response