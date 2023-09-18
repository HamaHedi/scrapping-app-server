from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors
from script import scrape_coursesss

app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask app

@app.route("/scrape/", methods=["POST"])
def scrape_courses():
    data = request.get_json()
    url = data.get("url", "")
    page = data.get("page", 1)

    try:
        # Call your scraping function with the provided URL and page number
        output = scrape_coursesss(url, page)

        if output:
            return jsonify({"message": "Scraping completed successfully", "output": output})
        else:
            return jsonify({"message": "Scraping failed"}), 500

    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

