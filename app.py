"""
Halteh Flowers - Store Ops Brain
Flask UI shell. Sample/heuristic data is used everywhere a real model
will eventually plug in. Search for "TODO: model" to find every spot
that should be swapped for a trained model or a live data source.
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import os

from models.forecast import predict_demand
from models.reorder import build_reorder_plan
from models.segmentation import get_customer_segments

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
STOCK_PATH = os.path.join(DATA_DIR, "sample_stock.csv")


def load_stock():
    return pd.read_csv(STOCK_PATH)


@app.route("/")
def overview():
    stock = load_stock()
    forecast = predict_demand(stock)
    reorder = build_reorder_plan(stock, forecast)

    total_units = int(stock["quantity"].sum())
    total_value = float((stock["quantity"] * stock["price_jod"]).sum())
    urgent_reorders = sum(1 for r in reorder if r["urgency"] == "urgent")

    return render_template(
        "overview.html",
        active="overview",
        total_units=total_units,
        total_value=round(total_value, 2),
        urgent_reorders=urgent_reorders,
        item_count=len(stock),
        top_reorders=reorder[:4],
    )


@app.route("/stock")
def stock_page():
    stock = load_stock()
    rows = stock.to_dict(orient="records")
    return render_template("stock.html", active="stock", rows=rows)


@app.route("/forecast")
def forecast_page():
    stock = load_stock()
    forecast = predict_demand(stock)
    return render_template("forecast.html", active="forecast", forecast=forecast)


@app.route("/reorder")
def reorder_page():
    stock = load_stock()
    forecast = predict_demand(stock)
    plan = build_reorder_plan(stock, forecast)
    return render_template("reorder.html", active="reorder", plan=plan)


@app.route("/customers")
def customers_page():
    segments = get_customer_segments()
    return render_template("customers.html", active="customers", segments=segments)


# --- JSON endpoints, for whenever the UI is wired to a live model service ---

@app.route("/api/forecast")
def api_forecast():
    stock = load_stock()
    return jsonify(predict_demand(stock))


@app.route("/api/reorder")
def api_reorder():
    stock = load_stock()
    forecast = predict_demand(stock)
    return jsonify(build_reorder_plan(stock, forecast))


@app.route("/api/customers")
def api_customers():
    return jsonify(get_customer_segments())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)