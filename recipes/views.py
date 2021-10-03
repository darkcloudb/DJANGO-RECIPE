from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, reverse, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from recipes.forms import AddAuthorForm, AddRecipeForm, LoginForm, RecipeEditForm
from recipes.models import Author, Recipe

# from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    template_name = "index.html"
    recipes = Recipe.objects.all()
    context = {"recipes": recipes}
    return render(request, template_name, context)


def recipe_detail(request, id):
    template_name = "recipe.html"
    recipe = Recipe.objects.get(id=id)
    context = {"recipe": recipe}
    return render(request, template_name, context)


def author_detail(request, id):
    template_name = "author.html"
    author = Author.objects.get(id=id)
    recipes = Recipe.objects.filter(author=author)
    context = {"author": author, "recipes": recipes}
    return render(request, template_name, context)


def add_author(request):
    if not request.user.is_staff:
        return HttpResponse("Access Denied - Need staff/admin permissions")
    if request.method == "POST":
        form = AddAuthorForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data.get("username"), password=data.get("password")
            )
            author = Author.objects.create(
                name=data.get("name"), bio=data.get("bio"), user=user
            )
            return HttpResponseRedirect(reverse("homepage"))

    else:
        form = AddAuthorForm()

    return render(request, "generic_form.html", {"form": form})


@login_required
def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            author = Recipe.objects.create(
                title=data.get("title"),
                author=data.get("author"),
                description=data.get("description"),
                time_required=data.get("time_required"),
                instructions=data.get("instructions"),
                created_by=request.user
            )
            return HttpResponseRedirect(reverse("homepage"))

    else:
        form = AddRecipeForm()

    return render(request, "generic_form.html", {"form": form})

# adding in EditRecipeView function view as per instructions
class EditRecipeView(LoginRequiredMixin, View):
    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        if request.user.is_staff or request.user == recipe.created_by:
            form = RecipeEditForm(initial={
                'title': recipe.title,
                'description': recipe.description,
                'time_required': recipe.time_required,
                'instructions': recipe.instructions
            })
            return render(request, 'generic_form.html', {'form': form})
        else:
            return HttpResponse("Access Denied - Need staff/admin permissions")

    def post(self, request, id):
        recipe = Recipe.objects.get(id=id)
        form = RecipeEditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            recipe.title = data['title']
            recipe.description = data['description']
            recipe.time_required = data['time_required']
            recipe.instructions = data['instructions']
            recipe.save()
            return HttpResponseRedirect(reverse('recipe', args=(id,)))

# adding in like and dislike functions
def like_recipe(request, id):
    self = request.user
    recipe = Recipe.objects.get(id=id)
    recipe.favorite.add(self)
    recipe.save()
    print('liked')
    return redirect(request.META.get("HTTP_REFERER"))

def unlike_recipe(request, id):
    self = request.user
    recipe = Recipe.objects.get(id=id)
    recipe.favorite.remove(self)
    recipe.save()
    print('disliked')
    return redirect(request.META.get("HTTP_REFERER"))


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data.get("username"), password=data.get("password")
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get("next", reverse("homepage"))
                )
    else:
        form = LoginForm()
    return render(request, "generic_form.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))
