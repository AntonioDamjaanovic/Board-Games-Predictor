import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
import json
from .utils import predict_games

# Create your views here.
def home(request):
    context = {

    }
    return render(request, 'app/home.html', context)

def predict_view(request):
    mechanics_list = [
        "Hand Management", "Solo / Solitaire Game", "Variable Player Powers",
        "Dice Rolling", "Cooperative Game", "Income", "Set Collection",
        "Card Drafting", "Hexagon Grid", "Modular Board",
        "Area Majority / Influence", "Grid Movement", "Point to Point Movement",
        "Variable Set-up", "End Game Bonuses", "Campaign / Battle Card Driven",
        "Deck Bag and Pool Building", "Scenario / Mission / Campaign Game",
        "Simultaneous Action Selection", "Network and Route Building",
    ]

    domains_list = [
        "Strategy Games", "Abstract Games", "Family Games",
        "Party Games", "Thematic Games", "Wargames",
        "Children's Games", "Customizable Games",
    ]

    predicted_rating = None

    if request.method == "POST":
        try:
            # Try parsing JSON first
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                # Fall back to form data
                data = request.POST

            # Build game data
            game_data = {
                "Year Published": int(data.get("year_published", 0)),
                "Min Players": int(data.get("min_players", 1)),
                "Max Players": int(data.get("max_players", 1)),
                "Play Time": int(data.get("play_time", 0)),
                "Min Age": int(data.get("min_age", 0)),
                "Complexity Average": float(data.get("complexity_avg", 0)),
                "Owned Users": int(data.get("owned_users", 0)),
                "Users Rated": int(data.get("users_rated", 0)),
                "Mechanics": ",".join(data.getlist("mechanics") if hasattr(data, "getlist") else data.get("mechanics", [])),
                "Domains": ",".join(data.getlist("domains") if hasattr(data, "getlist") else data.get("domains", [])),
            }

            predicted_rating = predict_games(pd.DataFrame([game_data]))[0]

            # If JSON request, return JSON
            if request.headers.get("Content-Type") == "application/json":
                return JsonResponse({"prediction": predicted_rating})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    context = {
        "mechanics": mechanics_list,
        "domains": domains_list,
        "predicted_rating": predicted_rating,
    }

    return render(request, "app/predict.html", context)



