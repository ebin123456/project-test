from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

import pandas as pd

def index(request):
    data = pd.read_csv("ipl/df/matches.csv")
    seasons = data['season'].unique().tolist()
    context = {
        "seasons":seasons
    }
    return render(request, "index.html", context)


def stats(request):
    season = request.GET.get('season',"")
    if not season.isdigit() or len(season) != 4:
        return JsonResponse({"message":"invalied season"}, status=422)
    season = int(season)
    data = pd.read_csv(settings.DF_DIR+"/matches.csv")
    df = pd.read_csv(settings.DF_DIR+"/deliveries.csv")
    data = data[data['season'] == season]
    if len(data.index) == 0:
        return JsonResponse({"message":"data not available"}, status=422)
    out = {}
    out["toss_winner"] = data.groupby('toss_winner')["id"].count().sort_values(ascending=False).head(1).to_dict()
    out["winner"] = data.groupby('winner')["id"].count().sort_values(ascending=False).head(4).to_dict()
    winner = [*out["winner"]][0]
    out["mom"] = data.groupby('player_of_match')["id"].count().sort_values(ascending=False).head(1).to_dict()
    out["winner_venue"] = data[(data["winner"] == winner)].groupby('venue')["id"].count().sort_values(ascending=False).head(1).to_dict()
    out["toss_and_bat"] = data.groupby('toss_decision')[["id"]].count().apply(lambda x: x["bat"]/(x["bat"] + x["field"])).to_list()[0]
    out["win_by_wickets"] = data[(data["win_by_wickets"]== data["win_by_wickets"].max())]["winner"].to_list()[0]
    out["toss_and_win"] = data[(data["winner"]== data["toss_winner"])]["id"].count()
    out["toss_and_win"] = int(out["toss_and_win"])
    out["most_catch"] = data.merge(df[df["dismissal_kind"]=="caught"],left_on="id", right_on="match_id",how="left").groupby(["fielder"])[["fielder"]].count().head(1).to_dict()["fielder"]
    return JsonResponse({"data":out})