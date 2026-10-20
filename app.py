from flask import Flask, jsonify, request, render_template
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from dotenv import load_dotenv

load_dotenv()

from flipkart.config import Config
from flipkart.data_ingestion import DataIngester
from flipkart.rag_chain import RAGChainBuilder

REQUEST_COUNTER = Counter("requests_total", "Total number of chat requests")


def create_app():
    Config.validate()
    app = Flask(__name__)

    vector_store = DataIngester().ingest(load_existing=True)
    rag_chain = RAGChainBuilder(vector_store).build_chain()

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/ask", methods=["POST"])
    def ask():
        REQUEST_COUNTER.inc()
        user_input = (request.form.get("msg") or "").strip()
        session_id = request.form.get("session_id", "default_session")
        if not user_input:
            return jsonify({"error": "Empty message"}), 400
        try:
            result = rag_chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}},
            )
        except Exception:
            app.logger.exception("RAG chain failed")
            return jsonify({"error": "Something went wrong, please try again."}), 500
        return jsonify({"answer": result["answer"]})

    @app.route("/metrics")
    def metrics():
        return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)