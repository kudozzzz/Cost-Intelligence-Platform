import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Cost Intelligence Platform", layout="wide")

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

#Loading Dataset
cost = load_csv("data/cost_breakdown.csv")
routes = load_csv("data/routes_distance.csv")
fleet = load_csv("data/vehicle_fleet.csv")
delivery = load_csv("data/delivery_performance.csv")

#Preprocessing of Data
def lc(df):
    df.columns = [c.strip().lower() for c in df.columns]
    return df

cost = lc(cost)
routes = lc(routes)
fleet = lc(fleet)
delivery = lc(delivery)

#Cost Computation
possible_cost_cols = ["fuel_cost","labor_cost","vehicle_maintenance","insurance",
                      "packaging_cost","technology_platform_fee","other_overhead","other_overheads"]
existing_cost_cols = [c for c in possible_cost_cols if c in cost.columns]

if not existing_cost_cols:
    # fallback criteria 
    if "total_cost" not in cost.columns:
        st.error("No cost columns found in cost_breakdown.csv. Expected e.g. Fuel_Cost, Labor_Cost etc.")
        st.stop()


if "total_cost" not in cost.columns:
    cost["total_cost"] = cost[existing_cost_cols].sum(axis=1)

#Prepare delivery delay
if "delay_hours" not in delivery.columns:
    if "promised_time" in delivery.columns and "actual_time" in delivery.columns:
        def compute_delay(row):
            try:
                a = pd.to_datetime(row["actual_time"])
                p = pd.to_datetime(row["promised_time"])
                diff = (a - p).total_seconds() / 3600.0
                return diff
            except:
                return np.nan
        delivery["delay_hours"] = delivery.apply(compute_delay, axis=1)
    else:
        delivery["delay_hours"] = np.nan

#Merge datasets
for df, name in [(cost,"cost"), (routes,"routes"), (delivery,"delivery")]:
    if "order_id" not in df.columns:
        st.warning(f"{name}.csv does not have 'Order_ID' column (case-insensitive). Found columns: {list(df.columns)[:10]}")

# Merge cost + routes + delivery
df = cost.merge(routes, on="order_id", how="left")
df = df.merge(delivery, on="order_id", how="left")


if "vehicle_id" in df.columns and "vehicle_id" in fleet.columns:
    df = df.merge(fleet, on="vehicle_id", how="left")
else:
    pass

#Derived metrics
distance_cols = [c for c in df.columns if "distance" in c]
dist_col = distance_cols[0] if distance_cols else None

if dist_col is not None:
    df["cost_per_km"] = df["total_cost"] / (df[dist_col].replace({0:np.nan}))
else:
    df["cost_per_km"] = np.nan

# categorize delay: on-time vs delayed
df["delayed_flag"] = df["delay_hours"].apply(lambda x: "Delayed" if pd.notna(x) and x>0.5 else "On-time/Minor")

date_col = None
for c in df.columns:
    if "date" == c or c.endswith("_date") or c in ("date","delivery_date"):
        date_col = c
        break
if date_col:
    try:
        df[date_col] = pd.to_datetime(df[date_col])
    except:
        pass

# Front End with Streamlit
st.title("Cost Intelligence Platform — NexGen Logistics")
st.sidebar.header("Filters")
vehicle_types = []
if "vehicle_type" in df.columns:
    vehicle_types = sorted(df["vehicle_type"].dropna().unique().tolist())
selected_vehicle_types = st.sidebar.multiselect("Vehicle Type", vehicle_types, default=vehicle_types)

carrier_list = []
if "carrier" in df.columns:
    carrier_list = sorted(df["carrier"].dropna().unique().tolist())
selected_carriers = st.sidebar.multiselect("Carrier", carrier_list, default=carrier_list)

if selected_vehicle_types:
    if "vehicle_type" in df.columns:
        df = df[df["vehicle_type"].isin(selected_vehicle_types)]
if selected_carriers:
    if "carrier" in df.columns:
        df = df[df["carrier"].isin(selected_carriers)]

st.subheader("Key Metrics")
total_cost = df["total_cost"].sum()
avg_cost_per_km = df["cost_per_km"].mean(skipna=True)
avg_delay = df["delay_hours"].mean(skipna=True)

k1, k2, k3 = st.columns(3)
k1.metric("Total Operational Cost", f"₹{total_cost:,.0f}")
k2.metric("Avg Cost per Km", f"₹{avg_cost_per_km:.2f}" if not np.isnan(avg_cost_per_km) else "N/A")
k3.metric("Avg Delivery Delay (hrs)", f"{avg_delay:.2f}" if not np.isnan(avg_delay) else "N/A")

# Charts
st.markdown("### Visualizations")

# 1) Cost component breakdown 
if any(c in cost.columns for c in ["fuel_cost","labor_cost","vehicle_maintenance","insurance","packaging_cost"]):
    comp_cols = [c for c in cost.columns if c.endswith("_cost") or "maintenance" in c or "insurance" in c or "packaging" in c or "platform" in c]
    comp_sum = cost[comp_cols].sum().rename("value").reset_index()
    comp_sum.columns = ["component","value"]
    fig_comp = px.pie(comp_sum, values="value", names="component", title="Cost Components (Total)")
    st.plotly_chart(fig_comp, use_container_width=True)

# 2) Cost per route bar
if "route_id" in df.columns:
    agg_route = df.groupby("route_id", as_index=False)["total_cost"].sum().sort_values("total_cost", ascending=False).head(20)
    fig_route = px.bar(agg_route, x="route_id", y="total_cost", title="Top Routes by Total Cost")
    st.plotly_chart(fig_route, use_container_width=True)

# 3) Trend over time
if date_col and date_col in df.columns:
    trend = df.groupby(pd.Grouper(key=date_col, freq="D"))["total_cost"].sum().reset_index()
    fig_trend = px.line(trend, x=date_col, y="total_cost", title="Total Cost Trend")
    st.plotly_chart(fig_trend, use_container_width=True)

# 4) Delay vs Cost scatter
if "delay_hours" in df.columns:
    fig_scatter = px.scatter(df, x="delay_hours", y="total_cost", color="vehicle_type" if "vehicle_type" in df.columns else None,
                             title="Delay (hrs) vs Total Cost", hover_data=["order_id"])
    st.plotly_chart(fig_scatter, use_container_width=True)


# Show table and download
st.markdown("### Processed Data")
st.dataframe(df.head(200))

csv = df.to_csv(index=False)
st.download_button("Download processed CSV", csv, "cost_insights.csv")
