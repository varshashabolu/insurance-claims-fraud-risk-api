from flask import Flask, jsonify, send_from_directory, render_template
from analysis import analysis
import os

app = Flask(__name__)

analysis.generate_plots()

@app.route("/")
def home():
    return render_template("index.html")  # Requires templates/index.html

# API routes...

@app.route("/api/average-claim")
def api_average_claim():
    return jsonify(analysis.average_claim_by_region())

@app.route("/api/fraud-count")
def api_fraud_count():
    return jsonify(analysis.fraud_count())

@app.route('/plots/<filename>')
def serve_plot(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'plots'), filename)

if __name__ == "__main__":
    app.run(debug=True)
