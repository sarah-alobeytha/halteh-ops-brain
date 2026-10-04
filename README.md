# Halteh Flowers - Store Ops Brain (UI shell)

A Flask dashboard for the plants pilot: stock, demand forecast, reorder plan,
and customer segments. Every prediction is currently a placeholder — the
point of this shell is to have a working UI to click through and to give
each future agent a clear, single place to plug into.

## Run it

```bash
cd halteh-ops-brain
python -m venv venv
source venv/bin/activate      # venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000

## Structure

```
app.py                  Flask routes + page rendering
data/sample_stock.csv    Fake stock data — replace with real Halteh counts
models/forecast.py       Demand forecast — placeholder heuristic, swap for a trained model
models/reorder.py         Reorder logic — rule-based, tune once forecast is real
models/segmentation.py    Customer segments — fixed sample data, swap for real clustering
templates/               Jinja2 pages (overview, stock, forecast, reorder, customers)
static/css/style.css      Styling
```

## Where to plug in the real models

Every placeholder function is marked with `TODO: model` in its file.

- **`models/forecast.py` → `predict_demand(stock_df)`**
  Currently returns a random-but-stable estimate per plant/size. Once a few
  months of real sales are logged, replace the body of this function with
  a trained model call (e.g. an XGBoost model loaded from disk). Keep the
  same return shape — a list of dicts with `plant_type`, `size`,
  `current_stock`, `predicted_demand_7d`, `confidence` — and nothing else
  in the app needs to change.

- **`models/reorder.py` → `build_reorder_plan(stock_df, forecast)`**
  Rule-based: flags anything where stock won't cover the predicted 7-day
  demand plus a small buffer. Tune the `BUFFER` constant, or replace with
  a proper reorder-quantity model later.

- **`models/segmentation.py` → `get_customer_segments()`**
  Returns four fixed sample segments. Once customer purchase history
  exists, replace this with real clustering (e.g. k-means on recency /
  frequency / spend) and return the same shape.

## Swapping in real data

Replace `data/sample_stock.csv` with a real export using the same columns:
`date, plant_type, size, quantity, price_jod, notes`. As sales history
accumulates, add a second CSV/table for it and pass it into
`predict_demand()` alongside the stock data.

## API endpoints

`/api/forecast`, `/api/reorder`, `/api/customers` return the same data as
JSON — useful once you want to call this from a separate agent process
instead of just the built-in pages.
