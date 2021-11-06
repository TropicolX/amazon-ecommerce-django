from django.urls import path
from .views import Register, Login, BlacklistTokenView, ChangePassword

app_name = 'users'

urlpatterns = [
    path('register/', Register.as_view(), name="register_user"),
    path('login/', Login.as_view(), name="login_user"),
    path('logout/blacklist/', BlacklistTokenView.as_view(), name='blacklist'),
    path('change_password/', ChangePassword.as_view(), name='change_password'),
]
