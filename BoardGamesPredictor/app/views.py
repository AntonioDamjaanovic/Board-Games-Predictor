from django.shortcuts import render, redirect, get_object_or_404

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
