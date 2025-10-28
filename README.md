# Cost Intelligence Platform — NexGen Logistics

**Author:** Aryan Sinha  
**Project:** OFI — Logistics Innovation Challenge  
**Tech:** Python, Streamlit, Pandas, Plotly

## Project Overview
Cost Intelligence Platform is an interactive dashboard built with Streamlit that provides NexGen Logistics engineers and managers clear visibility into operational costs. The app integrates cost breakdown, route distance, fleet, and delivery performance data to identify cost drivers, visualize trends, and highlight opportunities to reduce operational spend.

**Key goal:** Identify cost leakages (fuel, labor, maintenance, etc.) and provide actionable insights to reduce logistics costs by 15–20%.

---

## What the App Shows
- **KPI cards:** Total Operational Cost, Average Cost per Km, Average Delivery Delay (hrs).  
- **Visualizations (interactive):**
  - Pie chart: Cost composition by component (fuel, labor, maintenance, packaging, etc.).
  - Bar chart: Total cost by route (top cost routes).
  - Line chart: Total cost trend over time (daily aggregation if date data is available).
  - Scatter plot: Delay (hrs) vs Total Cost (shows correlation between delays & cost).
- **Filters:** Sidebar filters for Vehicle Type and Carrier to drill down by segment.  
- **Processed Data Table:** Shows merged dataset and allows CSV download of processed data.

---

## Datasets (place in `data/` folder)
Place the provided CSV files in `data/` with these exact names:
- `cost_breakdown.csv` — cost components by `Order_ID`
- `routes_distance.csv` — route metrics by `Order_ID` (distance_km, fuel_consumption_l, toll_charges_inr, route)
- `vehicle_fleet.csv` — vehicle meta data (vehicle_id, vehicle_type, fuel_efficiency)
- `delivery_performance.csv` — delivery columns (order_id, promised_time/actual_time or delivery_date, delay_hours, carrier, customer_rating)

> The app normalizes column names to lowercase and attempts to parse typical date column names (e.g., `date`, `delivery_date`, `promised_time`, `actual_time`).

---

## Requirements
Python 3.9+ recommended.

`requirements.txt` includes:
```
streamlit
pandas
plotly
numpy
```

(Install with `pip install -r requirements.txt`)

---

## Setup & Run (Windows / cross-platform)
1. (Optional, recommended) Create and activate a virtual environment:
```bash
python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install --upgrade pip
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure CSVs are in `data/` folder, filenames match exactly.

4. Run the Streamlit app:
```bash
python -m streamlit run app.py
```
Open the Local URL shown (usually `http://localhost:8501`).

---

## Quick Usage
- Use the left sidebar to filter by **Vehicle Type** and **Carrier**.  
- Top KPIs update instantly to reflect the active filters.  
- Hover on chart points for details, click legends to toggle series, and use the download button to export the processed CSV.

---

## Key Insights (example)
- Fuel and maintenance are the largest contributors to total operating cost.  
- Certain routes consistently appear in the top-5 costliest routes — prioritize route-review and consolidation.  
- Delayed deliveries tend to have higher cost; investigate causes for delayed shipments to reduce cost overruns.

*(Replace with your real numbers and insights after analysis.)*

---

## Project Structure
```
Cost_Intelligence_Platform/
│
├── app.py                   # Main Streamlit application
├── requirements.txt
├── README.md
├── Innovation_Brief.pdf     # 1-page summary 
└── data/
    ├── cost_breakdown.csv
    ├── routes_distance.csv
    ├── vehicle_fleet.csv
    └── delivery_performance.csv
```

---

## Future Improvements (optional / for bonus)
- Add a lightweight ML model to **predict cost per order** or **delay risk** (bonus evaluation points).  
- Add route optimization suggestions (OR-Tools) to recommend rerouting.  
- Display route maps using `pydeck` or Plotly mapbox for geospatial visualization.  
- Add alerting: notify when cost/km for a route exceeds a threshold.

---

## License & Contact
This project was prepared for the OFI Logistics Innovation Challenge. For questions or demo requests, contact **Aryan Sinha**.
