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
from .utils import load_item_embeddings, get_food_image
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

    items_by_genre = {}
    all_items = Item_Profile.objects.all()
    genres = all_items.values_list("genre", flat=True).distinct()

    for genre in genres:
        items = Item_Profile.objects.filter(genre=genre).order_by("?")[:4]
        items_by_genre[genre] = items

    return render(request, "survey.html", {"items_by_genre": items_by_genre})


def dashboard_view(request):
    user_profile = User_Profile.objects.get(user=request.user)

    if not user_profile.survey_completed:
        return redirect("survey")

    user_embedding = user_profile.get_embedding()

    faiss_handler = FaissHandler(
        "RecApp/vector_db/item_index.faiss", "RecApp/vector_db/titles.txt"
    )
    raw_recommendations = faiss_handler.get_top_k(user_embedding, k=5)

    formatted_recommendations = []
    for title, score in raw_recommendations:
        try:
            item = Item_Profile.objects.get(title=title)

            if isinstance(score, float):
                score = round(score, 2)

            image_url = get_food_image(title)

            formatted_recommendations.append(
                {
                    "title": title,
                    "score": score,
                    "item": item,
                    "image_url": image_url,
                }
            )
        except Item_Profile.DoesNotExist:
            continue

    return render(
        request, "dashboard.html", {"recommendations": formatted_recommendations}
    )


@login_required
def load_more_recommendations(request):
    try:
        offset = int(request.GET.get("offset", 0))

        count = int(request.GET.get("count", 5))

        user_profile = User_Profile.objects.get(user=request.user)
        user_embedding = user_profile.get_embedding()

        faiss_handler = FaissHandler(
            "RecApp/vector_db/item_index.faiss", "RecApp/vector_db/titles.txt"
        )
        raw_recommendations = faiss_handler.get_top_k(user_embedding, k=offset + count)

        raw_recommendations = raw_recommendations[offset : offset + count]

        formatted_recommendations = []
        for title, score in raw_recommendations:
            try:
                item = Item_Profile.objects.get(title=title)

                if isinstance(score, float):
                    score = round(score, 2)

                image_url = get_food_image(title)

                formatted_recommendations.append(
                    {
                        "title": title,
                        "score": score,
                        "ner": item.ner,
                        "directions": item.directions,
                        "image_url": image_url,
                    }
                )
            except Item_Profile.DoesNotExist:
                continue

        return JsonResponse(
            {"status": "success", "recommendations": formatted_recommendations}
        )

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@require_POST
@login_required
def update_user_embedding(request):
    try:
        data = json.loads(request.body)
        clicked_item_title = data.get("item_title")

        if not clicked_item_title:
            return JsonResponse(
                {"status": "error", "message": "No item title provided"}, status=400
            )

        user_profile = User_Profile.objects.get(user=request.user)

        item_embeddings = load_item_embeddings()

        if clicked_item_title not in item_embeddings:
            return JsonResponse(
                {"status": "error", "message": "Item not found"}, status=404
            )

        old_user_embedding = user_profile.get_embedding()
        clicked_item_embedding = item_embeddings[clicked_item_title]

        new_user_embedding = 0.7 * old_user_embedding + 0.3 * clicked_item_embedding

        new_user_embedding = new_user_embedding / np.linalg.norm(new_user_embedding)

        user_profile.set_embedding(new_user_embedding)
        user_profile.save()

        return JsonResponse({"status": "success", "message": "User embedding updated"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
