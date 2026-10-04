"""
Customer segmentation.

No real customer data is wired up yet, so this returns fixed sample
segments just to give the UI something to render. Once Halteh's customer
purchase history is available, replace this with real clustering
(e.g. k-means on recency/frequency/spend) fed by that data.

TODO: model
  - load real customer purchase history
  - cluster on recency, frequency, monetary value (RFM) or similar
  - return the same shape: a list of segment dicts
"""


def get_customer_segments():
    return [
        {
            "name": "VIP / high spend",
            "customer_count": 8,
            "description": "Frequent buyers, high average order value.",
            "suggested_action": "Early access to new plant arrivals, priority delivery slots.",
        },
        {
            "name": "Regulars",
            "customer_count": 21,
            "description": "Buy every 4-6 weeks, moderate spend.",
            "suggested_action": "Loyalty nudge — small discount on their usual plant type.",
        },
        {
            "name": "Event-driven",
            "customer_count": 14,
            "description": "Only purchase around occasions (weddings, holidays, gifting).",
            "suggested_action": "Targeted reminders ahead of known events (Valentine's, Mother's Day).",
        },
        {
            "name": "Lapsed",
            "customer_count": 17,
            "description": "No purchase in 60+ days, used to buy regularly.",
            "suggested_action": "Win-back message with a modest incentive.",
        },
    ]
