from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from ice_breaker import ice_break_with

load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    # search_context = request.form["search_context"]
    # scenario_context = request.form["scenario_context"]
    search_context = "Uruguay desarrollo de software"
    scenario_context = "voy a entrevistarle para un trabajo de desarrollo de software"
    summary, profile_pic_url = ice_break_with(name, search_context, scenario_context)
    return jsonify(
        {
            "summary": summary.summary,
            "facts": summary.facts,
            "picture_url": profile_pic_url,
        }
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)