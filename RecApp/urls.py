from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # default landing
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("survey/", views.survey_view, name="survey"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("api/update-embedding/", views.update_user_embedding, name="update_embedding"),
    path(
        "api/load-more/",
        views.load_more_recommendations,
        name="load_more_recommendations",
    ),
]
