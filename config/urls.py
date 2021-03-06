"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from recipes.forms import RecipeEditForm
from django.contrib import admin
from django.urls import path
from recipes import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="homepage"),
    path("recipes/<int:id>/", views.recipe_detail, name="recipe"),
    path('recipes/<int:id>/edit/', views.EditRecipeView.as_view()),
    # path('recipes/<int:id>/edit/', views.edit_recipe),
    path("author/<int:id>/", views.author_detail, name="author"),
    path("addauthor/", views.add_author, name="addauthor"),
    path("addrecipe/", views.add_recipe, name="addrecipe"),
    path('like/<int:id>/', views.like_recipe),
    path('unlike/<int:id>/', views.unlike_recipe),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
