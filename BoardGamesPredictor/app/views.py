from django.shortcuts import render, redirect, get_object_or_404
import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

AZURE_ENDPOINT = "https://ruap-projekt-predictor.polandcentral.inference.ml.azure.com/score"
AZURE_API_KEY = "BJJkzVqzxnJ7Ss9edWweF5HhF7abOHAUK0rlTi2n94MG6gdmgcOtJQQJ99CBAAAAAAAAAAAAINFRAZMLN7ui"


# Create your views here.
def home(request):
    context = {

    }
    return render(request, 'app/home.html', context)

def predict_view(request):
    mechanics = [
        "Hand Management",
        "Solo / Solitaire Game",
        "Variable Player Powers",
        "Dice Rolling",
        "Cooperative Game",
        "Income",
        "Set Collection",
        "Card Drafting",
        "Hexagon Grid",
        "Modular Board",
        "Area Majority / Influence",
        "Grid Movement",
        "Point to Point Movement",
        "Variable Set-up",
        "End Game Bonuses",
        "Campaign / Battle Card Driven",
        "Deck Bag and Pool Building",
        "Scenario / Mission / Campaign Game",
        "Simultaneous Action Selection",
        "Network and Route Building",
    ]

    domains = [
        "Strategy Games",
        "Abstract Games",
        "Family Games",
        "Party Games",
        "Thematic Games",
        "Wargames",
        "Children's Games",
        "Customizable Games",
    ]

    context = {
        "mechanics": mechanics,
        "domains": domains,
    }

    return render(request, "app/predict.html", context)

@csrf_exempt
def predict_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AZURE_API_KEY}",
    }

    response = requests.post(
        AZURE_ENDPOINT,
        headers=headers,
        json=payload,
        timeout=15,
    )

    result = response.json()
    prediction = float(result[0])

    return JsonResponse({"prediction": prediction})
