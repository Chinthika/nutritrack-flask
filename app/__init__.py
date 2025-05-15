from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route("/health")
    def health():
        return {"status": "healthy"}, 200

    @app.route("/meals", methods=["GET"])
    def meals():
        return {"meals": [{"name": "Banana", "calories": 105}]}, 200

    return app
