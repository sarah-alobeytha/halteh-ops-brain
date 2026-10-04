"""
Demand forecasting.

Right now this is a simple heuristic so the UI has real numbers to show
before any historical sales data exists. Once a few months of real sales
are logged, replace predict_demand() with a trained model (e.g. XGBoost)
that takes the same stock dataframe (plus a sales-history dataframe) and
returns the same shape of output, so nothing else in the app needs to change.

TODO: model
  - swap the heuristic below for a trained regressor
  - add a sales-history CSV/DB as an input alongside `stock`
  - fold in seasonality signals (upcoming events, holidays) as features
"""

import random

# Known demand-boosting events for a flower/plant shop. Used only to nudge
# the placeholder numbers — a real model would encode this properly.
SEASONAL_BOOST = 1.0  # e.g. bump this to 1.4 in the weeks around Valentine's/Mother's Day


def predict_demand(stock_df):
    """
    Returns a list of dicts, one per stock row, each with a predicted
    demand for the next 7 days.

    Placeholder logic: assume weekly demand is roughly 20-45% of current
    stock, adjusted by a seasonal multiplier. This is deliberately naive —
    it exists so every other part of the app (reorder, dashboard) has
    something real to consume while actual sales data is collected.
    """
    random.seed(42)  # stable fake numbers between runs, easy to spot as placeholder
    results = []
    for _, row in stock_df.iterrows():
        base_rate = random.uniform(0.20, 0.45)
        predicted = round(row["quantity"] * base_rate * SEASONAL_BOOST, 1)
        results.append({
            "plant_type": row["plant_type"],
            "size": row["size"],
            "current_stock": int(row["quantity"]),
            "predicted_demand_7d": predicted,
            "confidence": "low (placeholder model, no sales history yet)",
        })
    return results
