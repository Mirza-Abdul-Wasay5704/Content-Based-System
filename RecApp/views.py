from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import json
import numpy as np

from .models import User_Profile, Item_Profile
from .utils import load_item_embeddings
from RecApp.vector_db.faiss_handler import FaissHandler


def home(request):
    return render(request, "home.html")


def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Account already exists.")
            return redirect("signup")

        user = User.objects.create_user(username=username, password=password)

        # Create user profile only if it doesn't exist yet
        User_Profile.objects.get_or_create(user=user)

        login(request, user)
        return redirect("survey")

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile = User_Profile.objects.get(user=user)
            if profile.survey_completed:
                return redirect("dashboard")
            else:
                return redirect("survey")
        else:
            messages.error(request, "Invalid credentials.")
            return redirect("login")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


@csrf_exempt
def survey_view(request):
    user_profile = User_Profile.objects.get(user=request.user)

    if request.method == "POST":
        selected_titles = request.POST.getlist("selected_items")
        if selected_titles:
            embeddings = []
            item_embeddings = load_item_embeddings()

            for title in selected_titles:
                if title in item_embeddings:
                    embeddings.append(item_embeddings[title])

            if embeddings:
                user_embedding = np.mean(embeddings, axis=0)
                user_profile.set_embedding(user_embedding)
                user_profile.survey_completed = True
                user_profile.save()
                return redirect("dashboard")

    # GET request: show items
    items_by_genre = {}
    all_items = Item_Profile.objects.all()
    genres = all_items.values_list("genre", flat=True).distinct()

    for genre in genres:
        items = Item_Profile.objects.filter(genre=genre).order_by("?")[:4]
        items_by_genre[genre] = items

    return render(request, "survey.html", {"items_by_genre": items_by_genre})


def dashboard_view(request):
    user_profile = User_Profile.objects.get(user=request.user)

    # Check if user has completed the survey
    if not user_profile.survey_completed:
        return redirect("survey")

    # Get the user embedding
    user_embedding = user_profile.get_embedding()

    # Get top 5 recommendations from FAISS
    faiss_handler = FaissHandler(
        "RecApp/vector_db/item_index.faiss", "RecApp/vector_db/titles.txt"
    )
    raw_recommendations = faiss_handler.get_top_k(user_embedding, k=5)

    # Format recommendations with full item details for the template
    formatted_recommendations = []
    for title, score in raw_recommendations:
        try:
            # Lookup the item details from the database
            item = Item_Profile.objects.get(title=title)

            # Format the score to 2 decimal places if it's a float
            if isinstance(score, float):
                score = round(score, 2)

            # Add to formatted recommendations
            formatted_recommendations.append(
                {"title": title, "score": score, "item": item}
            )
        except Item_Profile.DoesNotExist:
            # Handle case where item in FAISS doesn't exist in database
            continue

    return render(
        request, "dashboard.html", {"recommendations": formatted_recommendations}
    )


@require_POST
@login_required
def update_user_embedding(request):
    try:
        # Parse the JSON data from request body
        data = json.loads(request.body)
        clicked_item_title = data.get("item_title")

        if not clicked_item_title:
            return JsonResponse(
                {"status": "error", "message": "No item title provided"}, status=400
            )

        # Get user profile
        user_profile = User_Profile.objects.get(user=request.user)

        # Load item embeddings
        item_embeddings = load_item_embeddings()

        # Check if item exists in our embeddings
        if clicked_item_title not in item_embeddings:
            return JsonResponse(
                {"status": "error", "message": "Item not found"}, status=404
            )

        # Get current user embedding and clicked item embedding
        old_user_embedding = user_profile.get_embedding()
        clicked_item_embedding = item_embeddings[clicked_item_title]

        # Calculate new embedding using the formula
        # new_user_embedding = 0.7 * old_user_embedding + 0.3 * clicked_item_embedding
        new_user_embedding = 0.7 * old_user_embedding + 0.3 * clicked_item_embedding

        # Normalize the new user embedding
        new_user_embedding = new_user_embedding / np.linalg.norm(new_user_embedding)

        # Update user profile with new embedding
        user_profile.set_embedding(new_user_embedding)
        user_profile.save()

        return JsonResponse({"status": "success", "message": "User embedding updated"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
