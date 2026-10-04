"""
Reorder recommendations.

Rule-based for now: compare predicted 7-day demand to current stock and
flag anything that will run out or come close. This is intentionally
simple (see the plan discussed for the pilot: rule-based first, model-based
once real sales data exists).

TODO: model
  - once forecast.py returns real predictions with proper confidence,
    tighten these thresholds or replace with an explicit reorder-quantity
    model rather than a fixed buffer.
"""

BUFFER = 1.2  # reorder if stock < predicted demand * BUFFER


def build_reorder_plan(stock_df, forecast):
    plan = []
    for f in forecast:
        stock_row = stock_df[
            (stock_df["plant_type"] == f["plant_type"]) & (stock_df["size"] == f["size"])
        ].iloc[0]

        current = f["current_stock"]
        predicted = f["predicted_demand_7d"]
        needed_buffer = predicted * BUFFER

        if current <= predicted:
            urgency = "urgent"
            action = f"Reorder now — stock likely to run out within 7 days."
        elif current < needed_buffer:
            urgency = "watch"
            action = f"Reorder soon — stock is tight against predicted demand."
        else:
            urgency = "ok"
            action = "No action needed."

        plan.append({
            "plant_type": f["plant_type"],
            "size": f["size"],
            "current_stock": current,
            "predicted_demand_7d": predicted,
            "price_jod": float(stock_row["price_jod"]),
            "urgency": urgency,
            "action": action,
        })

    # Surface the most urgent items first
    order = {"urgent": 0, "watch": 1, "ok": 2}
    plan.sort(key=lambda x: order[x["urgency"]])
    return plan
