from bs4 import BeautifulSoup
from flask import Flask, render_template
import requests

app = Flask(__name__)
url = "https://totalsportek.online"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

matches = []

for league_div in soup.find_all("div", class_="my-1"):
    league_name = league_div.find("span").text.strip()

    for match_div in league_div.find_next_sibling("div", class_="div-main-box rounded-lg overflow-hidden").find_all("div", class_="div-child-box bg-dark-gray bg-white py-2 position-relative"):
        link = match_div.parent["href"]

        team1 = match_div.find("div", class_="col-5 text-right").find("span").text.strip()
        team2 = match_div.find("div", class_="col-5 text-left").find("span").text.strip()
        time = match_div.find("div", class_="col-2 text-center").find("span").text.strip()

        match_name = f"{team1} vs {team2}"

        match = {
            "match_name": match_name,
            "time": time,
            "match_url": link,
            "stream_links": [],
            "league_name": league_name
        }
        matches.append(match)


for match in matches:
    match_url = match["match_url"]
    match_response = requests.get(match_url)
    match_soup = BeautifulSoup(match_response.content, "html.parser")

    stream_divs = match_soup.find_all("input")
    for stream_div in stream_divs:
      stream_link = stream_div["value"]
      match["stream_links"].append(stream_link)
    
    match["league"] = match.pop("league_name")


@app.route("/")
def index():
    return render_template("idex.html", matches=matches)

@app.route("/match/<match_name>")
def show_match(match_name):
    match = [m for m in matches if m["match_name"] == match_name][0]
    return render_template("match.html", match=match)

if __name__ == "__main__":
    app.run(debug=True)
