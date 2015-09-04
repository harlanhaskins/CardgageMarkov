from flask import Flask, jsonify, request, Response, json, make_response, render_template, abort
from flask_cors import CORS
import argparse
from homestarkov import Homestarkov

app = Flask(__name__)
cors = CORS(app)

base = "/api"

# _characters = {
#     "cardgage": Homestarkov("cardgage", "Senor Cardgage",
#         "Dump Tell No Mandy!"),
#     "homsar": Homestarkov("homsar", "Homsar", "Legitimate Business!"),
#     "hackernews": Homestarkov("hackernews", "Hacker News", "Presented by Y-Combinator"),
#     "guyfieri": Homestarkov("guyfieri", "Guy Fieri", "Take me to Flavortown")
# }

max_quotes = 100

@app.route('/', methods=["GET"])
def list():
    return render_template('list.html', characters=Homestarkov.select())

@app.route('/<path>', methods=["GET"])
def character_page(path):
    character_query = Homestarkov.select().where(Homestarkov.path == path)
    if not character_query.exists():
        abort(404)
    return render_template('quote.html', character=character_query.first())


@app.route(base + "/characters", methods=["GET"])
def characters():
    character_list = [c.json_object() for c in Homestarkov.select()]
    return jsonify(characters=character_list)

@app.route(base + "/quotes/<path>", methods=["GET"])
def quote(path):
    character_query = Homestarkov.select().where(Homestarkov.path == path)

    if not character_query.exists():
        abort(404)

    markov = character_query.first()

    count_string = request.args.get("count", "1")
    count = int(count_string) if count_string.isdigit() else 1
    count = max(1, min(count, max_quotes))
    quotes = []
    for i in range(count):
        quotes.append(markov.new_string())

    return jsonify(quotes=quotes)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="Runs flask in debug mode.",
                          action="store_true")
    args = parser.parse_args()
    app.run(host="0.0.0.0", port=5585, debug=args.test)
