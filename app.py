import io
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

import weather_engine

# --- APP CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="DMRC Metro Crowd Analytics & Live Weather AI Predictor",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for executive cards and sleek UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 1.2rem;
    }
    .weather-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 20px;
    }
    .metric-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🚇 DMRC Multi-File Metro Crowd Analytics & Live Weather AI Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Real-Time Delhi Weather API Integration • Severe Monsoon Surge Modeling (+6-7 Lakh Journeys) • Road Transit Disruption & Modal Shift • Critical Interchange Hub Overcrowding Protocols</div>', unsafe_allow_html=True)

# --- SIDEBAR: LIVE WEATHER INTEGRATION & SCENARIOS ---
st.sidebar.title("🌦️ Delhi Weather Engine")
st.sidebar.caption("Live Open-Meteo API & Transit Shock Simulator")

weather_mode = st.sidebar.selectbox(
    "Select Weather Environment:",
    [
        "🌐 Live Delhi Weather (Open-Meteo API)",
        "⛈️ Monsoon Deluge / Severe Downpour (+6-7L Journeys)",
        "🌧️ Moderate Monsoon Rain (Road Crawl)",
        "🌦️ Passing Showers / Light Drizzle",
        "🔥 Scorching Summer Heatwave (44.5°C Loo)",
        "🌫️ Severe Winter Smog & AQI Crisis (GRAP-IV)",
        "❄️ Dense Winter Fog & Cold Wave",
        "☀️ Pleasant / Clear Weather (Baseline)",
        "🛠️ Custom Weather Parameter Simulator",
    ],
    index=1,  # Default to Monsoon Deluge to demonstrate heavy crowd surge
    help="Toggle between real-time Delhi API weather or real-world simulated crisis scenarios."
)

# Fetch or resolve active weather configuration
if weather_mode == "🌐 Live Delhi Weather (Open-Meteo API)":
    with st.sidebar:
        with st.spinner("Fetching live Delhi weather..."):
            active_weather = weather_engine.fetch_live_delhi_weather()
elif weather_mode == "🛠️ Custom Weather Parameter Simulator":
    st.sidebar.markdown("#### Custom Meteorological Inputs")
    custom_rain = st.sidebar.slider("Rainfall Intensity (mm/hr)", 0.0, 60.0, 35.0, step=1.0)
    custom_temp = st.sidebar.slider("Ambient Temperature (°C)", 5.0, 48.0, 28.0, step=0.5)
    custom_humid = st.sidebar.slider("Relative Humidity (%)", 10, 100, 92)
    custom_wind = st.sidebar.slider("Wind Speed (km/h)", 0.0, 60.0, 25.0)

    surge_calc = weather_engine.calculate_weather_impact_from_metrics(
        precip_mm=custom_rain,
        temp_c=custom_temp,
        humidity=custom_humid,
        wind_kmh=custom_wind,
        wmo_code=65 if custom_rain >= 25 else (63 if custom_rain >= 8 else (53 if custom_rain > 0.5 else 0))
    )
    w_text, w_icon = weather_engine.decode_wmo_code(65 if custom_rain >= 25 else (63 if custom_rain >= 8 else 0))
    active_weather = {
        "is_live": False,
        "status_note": "🛠️ Custom Parameter Simulation",
        "temp_c": custom_temp,
        "apparent_temp_c": custom_temp + 2.5,
        "humidity": custom_humid,
        "precipitation_mm": custom_rain,
        "rain_mm": custom_rain,
        "wind_kmh": custom_wind,
        "wmo_code": 65 if custom_rain >= 25 else 0,
        "condition_text": f"{w_text} ({custom_rain} mm/hr)",
        "icon": w_icon,
        **surge_calc,
    }
else:
    # Lookup from preconfigured realistic scenarios
    matched_scenario = None
    for s_name, s_data in weather_engine.DELHI_SCENARIOS.items():
        if s_data["name"].lower() in weather_mode.lower() or s_name.lower() in weather_mode.lower():
            matched_scenario = s_data
            break
    if not matched_scenario:
        matched_scenario = weather_engine.DELHI_SCENARIOS["Monsoon Deluge / Severe Downpour"]

    active_weather = {
        "is_live": False,
        "status_note": "🏛️ Simulated Delhi Transit Scenario",
        **matched_scenario
    }

# Display Weather Summary in Sidebar
st.sidebar.markdown(f"""
---
**Active Weather:** {active_weather['icon']} **{active_weather['condition_text']}**
- 🌡️ **Temp:** {active_weather['temp_c']}°C (Feels {active_weather.get('apparent_temp_c', active_weather['temp_c'])}°C)
- 💧 **Precipitation:** {active_weather['precipitation_mm']} mm/hr
- 💨 **Humidity / Wind:** {active_weather['humidity']}% | {active_weather['wind_kmh']} km/h
- 🚦 **Road Disruption:** {active_weather['road_disruption_index']}%
- 📈 **Metro Surge:** **+{active_weather['base_surge_pct']}%**
""")

# --- TOP WEATHER IMPACT BANNER ---
w_c1, w_c2, w_c3, w_c4, w_c5 = st.columns([1.6, 1.2, 1.3, 1.3, 1.4])

with w_c1:
    st.markdown(f"""
    <div style='background: #1e293b; padding: 12px 16px; border-radius: 10px; border-left: 5px solid {active_weather["color"]};'>
        <div style='font-size: 0.8rem; color: #94a3b8;'>ACTIVE DELHI CONDITION</div>
        <div style='font-size: 1.15rem; font-weight: 700; color: #f8fafc;'>{active_weather['icon']} {active_weather['condition_text']}</div>
        <div style='font-size: 0.78rem; color: #cbd5e1;'>{active_weather.get("status_note", "")}</div>
    </div>
    """, unsafe_allow_html=True)

with w_c2:
    st.metric(
        label="Delhi Temperature",
        value=f"{active_weather['temp_c']} °C",
        delta=f"{active_weather['humidity']}% Humid | {active_weather['precipitation_mm']} mm/h rain",
        delta_color="off"
    )

with w_c3:
    st.metric(
        label="Network Passenger Uptick",
        value=f"+{active_weather['base_surge_pct']}%",
        delta=f"~{active_weather['daily_passengers_added'] / 100000:.1f} Lakh extra journeys" if active_weather['daily_passengers_added'] > 0 else "Baseline Flow",
        delta_color="inverse" if active_weather['base_surge_pct'] > 15 else "normal"
    )

with w_c4:
    st.metric(
        label="Road Disruption Index",
        value=f"{active_weather['road_disruption_index']} / 100",
        delta="Waterlogging & Crawl" if active_weather['road_disruption_index'] > 50 else "Normal Traffic",
        delta_color="inverse" if active_weather['road_disruption_index'] > 50 else "normal"
    )

with w_c5:
    st.markdown(f"""
    <div style='background: #1e293b; padding: 12px 16px; border-radius: 10px; border: 1px solid {active_weather["color"]}; text-align: center;'>
        <div style='font-size: 0.75rem; color: #94a3b8;'>DMRC STRAIN LEVEL</div>
        <div style='font-size: 0.95rem; font-weight: 800; color: {active_weather["color"]}; margin-top: 4px;'>{active_weather['alert_level']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- STEP 1: FILE INGESTION / SAMPLE DATA LOADER ---
with st.expander("📂 Step 1: Upload Multiple Entry & Exit Datasets (or Load Built-in DMRC Sample Data)", expanded=True):
    u_col1, u_col2 = st.columns([2.5, 1.2])
    with u_col1:
        uploaded_files = st.file_uploader(
            "Select and upload all your CSV / Excel files at once (e.g. entry CSVs, exit CSVs, multi-sheet Excel files):",
            type=["csv", "xlsx"],
            accept_multiple_files=True,
            help="You can drag & drop multiple files simultaneously from multiple months.",
        )
    with u_col2:
        st.markdown("**Or start immediately with sample data:**")
        load_sample = st.button("⚡ Load DMRC Official Sample Data (Sep 2024 Entry & Exit - 250+ Stations)", type="secondary", use_container_width=True)
        if "use_sample_data" not in st.session_state:
            st.session_state["use_sample_data"] = False
        if load_sample:
            st.session_state["use_sample_data"] = True

# --- DATA PROCESSING UTILITIES ---
def normalize(df):
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()
    return df.loc[:, ~df.columns.duplicated(keep="first")]

def prep_frame(df, val_name):
    df = normalize(df)
    hr_cols = [c for c in df.columns if c.upper().startswith("HR") and c.upper().replace("HR", "").isdigit()]
    if not hr_cols:
        return None
    id_cols = [c for c in df.columns if c not in hr_cols]
    melted = df.melt(id_vars=id_cols, value_vars=hr_cols, var_name="hour_col", value_name=val_name)
    melted["hour"] = melted["hour_col"].str.upper().str.replace("HR", "").astype(int)
    for c in list(melted.columns):
        lc = c.lower()
        if "station" in lc and "code" not in lc:
            melted = melted.rename(columns={c: "station name"})
        elif "business" in lc or "date" in lc:
            melted = melted.rename(columns={c: "businessday"})
    melted = normalize(melted)
    for col, default in {"entry": 0.0, "exit": 0.0, "businessday": "2024-09-01"}.items():
        if col not in melted.columns:
            melted[col] = default
    melted["entry"] = pd.to_numeric(melted["entry"], errors="coerce").fillna(0).astype(float)
    melted["exit"] = pd.to_numeric(melted["exit"], errors="coerce").fillna(0).astype(float)
    return melted[["station name", "hour", "businessday", "entry", "exit"]]

def parse_single_file(f_name, file_bytes):
    base_name = f_name.split("/")[-1].split("\\")[-1].lower()
    if "index.csv" in base_name or base_name.endswith("index"):
        return None
    try:
        if base_name.endswith(".csv"):
            is_exit = base_name.endswith("_exit.csv") or "exit" in base_name.split("-")[-1]
            return prep_frame(pd.read_csv(io.BytesIO(file_bytes), low_memory=False), "exit" if is_exit else "entry")
        sheets = []
        for sheet in pd.ExcelFile(io.BytesIO(file_bytes)).sheet_names:
            parsed = prep_frame(pd.read_excel(io.BytesIO(file_bytes), sheet_name=sheet), "exit" if "exit" in sheet.lower() or "exit" in base_name else "entry")
            if parsed is not None and not parsed.empty:
                sheets.append(parsed)
        return pd.concat(sheets, ignore_index=True) if sheets else None
    except Exception as err:
        st.error(f"Error parsing file `{f_name}`: {err}")
        return None

def process_multiple_files(files_list):
    parsed_dfs = []
    for f in files_list:
        try:
            file_bytes = f.getvalue() if hasattr(f, "getvalue") else f.read()
            if len(file_bytes) > 0:
                name = getattr(f, "name", "uploaded_file.csv")
                parsed = parse_single_file(name, file_bytes)
                if parsed is not None and len(parsed) > 0:
                    parsed_dfs.append(parsed)
        except Exception as err:
            st.error(f"Error reading file: {err}")
    if not parsed_dfs:
        return None, None

    combined = pd.concat(parsed_dfs, ignore_index=True)
    combined = normalize(combined)
    for col, default in {"station name": "Station A", "hour": 12, "entry": 0.0, "exit": 0.0, "businessday": "2024-09-01"}.items():
        if col not in combined.columns:
            combined[col] = default
    combined["entry"] = pd.to_numeric(combined["entry"], errors="coerce").fillna(0).astype(float)
    combined["exit"] = pd.to_numeric(combined["exit"], errors="coerce").fillna(0).astype(float)
    daily_grouped = combined.groupby(["station name", "hour", "businessday"])[["entry", "exit"]].sum().reset_index()
    daily_grouped["total_footfall"] = daily_grouped["entry"] + daily_grouped["exit"]
    total_cumulative_footfall = daily_grouped["total_footfall"].sum()
    avg_hourly = daily_grouped.groupby(["station name", "hour"])[["entry", "exit"]].mean().reset_index()
    avg_hourly["total_footfall"] = avg_hourly["entry"] + avg_hourly["exit"]
    avg_hourly["dow"] = 1
    avg_hourly["month_num"] = 8
    return avg_hourly, total_cumulative_footfall

# Determine input source: uploaded files or sample files
input_files = []
is_using_sample = False

if uploaded_files and len(uploaded_files) > 0:
    input_files = uploaded_files
    st.session_state["use_sample_data"] = False
elif st.session_state.get("use_sample_data", False):
    sample_dir = os.path.join(os.path.dirname(__file__), "sample_data")
    entry_path = os.path.join(sample_dir, "sample_dmrc_entry.csv")
    exit_path = os.path.join(sample_dir, "sample_dmrc_exit.csv")
    if os.path.exists(entry_path) and os.path.exists(exit_path):
        class LocalFile:
            def __init__(self, path, name):
                self.name = name
                with open(path, "rb") as f:
                    self.content = f.read()
            def getvalue(self):
                return self.content
        input_files = [LocalFile(entry_path, "sample_dmrc_entry.csv"), LocalFile(exit_path, "sample_dmrc_exit.csv")]
        is_using_sample = True

if not input_files:
    st.info("💡 **To get started:** Click **'Load DMRC Official Sample Data'** above to test the live dashboard instantly, or drag & drop your DMRC CSV/Excel files.")
    st.markdown("""
    #### Expected DMRC File Structure:
    - Files containing hourly passenger breakdown columns (`HR4`, `HR5`, ..., `HR23`, `HR0`).
    - Standard DMRC exports with station names and `businessday` / date records.
    - Drag & drop multiple entry and exit files simultaneously.
    """)
    st.stop()

# Load and process data
try:
    with st.spinner("Processing metro footfall datasets and training AI prediction model..."):
        df, grand_total_passengers = process_multiple_files(input_files)

    if df is None or len(df) == 0 or grand_total_passengers == 0:
        st.error("No valid footfall data found in the uploaded file(s). Please verify your files contain station names and hourly columns (HR4 to HR23).")
        st.stop()

    data_label = "built-in DMRC official sample dataset (Sep 2024)" if is_using_sample else f"{len(input_files)} uploaded file(s)"
    st.success(f"✅ Successfully loaded **{data_label}**! Cumulative Monitored Footfall: **{grand_total_passengers:,.0f} passengers** across **{df['station name'].nunique()} metro stations**.")

    df = df.loc[:, ~df.columns.duplicated(keep="first")].copy()

    # Train Random Forest crowd prediction model
    @st.cache_resource
    def train_model(data):
        df_clean = data.dropna(subset=["total_footfall", "hour", "station name"]).copy()
        le = LabelEncoder()
        df_clean["station_enc"] = le.fit_transform(df_clean["station name"].astype(str))
        rf = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
        rf.fit(df_clean[["hour", "station_enc", "dow", "month_num"]], df_clean["total_footfall"])
        return rf, le

    model, le_station = train_model(df)
except Exception as exc:
    st.error(f"Dashboard initialization failed: {exc}")
    st.stop()

# --- WEATHER ENRICHMENT ON AGGREGATE DATA ---
def enrich_df_with_weather(dataframe, weather_info):
    enriched = dataframe.copy()
    base_surge = weather_info.get("base_surge_pct", 0.0)

    # Calculate station-specific sensitivity multiplier
    station_mults = {}
    for st_name in enriched["station name"].unique():
        hub_info = weather_engine.get_station_interchange_info(st_name)
        station_mults[st_name] = hub_info["multiplier"]

    enriched["hub_multiplier"] = enriched["station name"].map(station_mults).fillna(1.0)
    enriched["weather_surge_pct"] = base_surge * enriched["hub_multiplier"]
    enriched["weather_footfall"] = enriched["total_footfall"] * (1 + enriched["weather_surge_pct"] / 100.0)
    enriched["footfall_delta"] = enriched["weather_footfall"] - enriched["total_footfall"]
    return enriched

df_weather = enrich_df_with_weather(df, active_weather)

# --- DASHBOARD TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visual Analytics & Weather Dynamics",
    "🔮 2026 AI Crowd Predictor & Weather Directives",
    "⚡ Delhi Weather Crisis Stress-Test Matrix",
    "📋 Raw Uploaded & Enriched Data Preview"
])

# --- TAB 1: VISUAL ANALYTICS & WEATHER DYNAMICS ---
with tab1:
    st.subheader("Transit Influx & Weather-Induced Modal Shift Analytics")

    total_baseline_daily = df["total_footfall"].sum()
    total_weather_daily = df_weather["weather_footfall"].sum()
    daily_delta_passengers = total_weather_daily - total_baseline_daily
    net_surge_pct = (daily_delta_passengers / total_baseline_daily * 100.0) if total_baseline_daily > 0 else 0.0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric(
            "Monitored Daily Footfall",
            f"{total_weather_daily:,.0f}",
            delta=f"Baseline: {total_baseline_daily:,.0f}/day",
            delta_color="off"
        )
    with k2:
        st.metric(
            "Weather-Driven Passenger Influx",
            f"+{daily_delta_passengers:,.0f}",
            delta=f"+{net_surge_pct:.1f}% System Surge",
            delta_color="inverse" if net_surge_pct > 10 else "normal"
        )
    with k3:
        rc_base = df[df["station name"].str.contains("Rajiv Chowk", case=False, na=False)]["total_footfall"].sum()
        if rc_base <= 0:
            rc_base = 65000.0
        rc_info = weather_engine.compute_station_crowd_impact(
            base_crowd=rc_base,
            station_name="Rajiv Chowk",
            weather_dict=active_weather
        )
        st.metric(
            "Rajiv Chowk Influx Strain",
            f"+{rc_info['effective_surge_pct']:.1f}%",
            delta=f"Est. Frisking Queue: {rc_info['queue_wait_mins']:.0f} mins",
            delta_color="inverse" if rc_info['queue_wait_mins'] > 10 else "normal"
        )
    with k4:
        st.metric(
            "Surface Transit Failure Index",
            f"{active_weather['road_disruption_index']}% Disrupted",
            delta="99.95% Metro Punctuality Shift",
            delta_color="inverse" if active_weather['road_disruption_index'] > 50 else "normal"
        )

    st.markdown("---")

    # Row 1: 24-Hour Curve (Baseline vs Weather Surge) & Critical Interchange Hub Overcrowding
    c1, c2 = st.columns([1.3, 1])

    with c1:
        st.markdown("#### 24-Hour System Footfall Curve: Baseline vs Weather Surge")
        hourly_base = df.groupby("hour")[["entry", "exit", "total_footfall"]].sum().reset_index()
        hourly_weather = df_weather.groupby("hour")["weather_footfall"].sum().reset_index()

        fig_24hr = go.Figure()
        fig_24hr.add_trace(go.Scatter(
            x=hourly_base["hour"], y=hourly_base["total_footfall"],
            mode="lines+markers", name="Baseline Normal Crowd",
            line=dict(color="#64748b", width=2.5, dash="dot"),
            marker=dict(size=6)
        ))
        fig_24hr.add_trace(go.Scatter(
            x=hourly_weather["hour"], y=hourly_weather["weather_footfall"],
            mode="lines+markers", name=f"Weather-Surged Footfall ({active_weather['icon']} {active_weather['condition_text']})",
            line=dict(color=active_weather["color"], width=4),
            marker=dict(size=8)
        ))
        fig_24hr.add_trace(go.Bar(
            x=hourly_base["hour"],
            y=hourly_weather["weather_footfall"] - hourly_base["total_footfall"],
            name="Added Weather Surge Delta",
            marker_color="rgba(239, 68, 68, 0.35)",
            yaxis="y"
        ))
        fig_24hr.update_layout(
            template="plotly_dark",
            title="Impact of Weather Shocks on Hourly Network Demand",
            xaxis=dict(title="Hour of Day (24-Hour Format)", dtick=1, range=[4, 23]),
            yaxis=dict(title="Total Hourly Passenger Trips"),
            legend=dict(orientation="h", y=1.14, x=0.0),
            margin=dict(l=20, r=20, t=40, b=20),
            height=400,
        )
        st.plotly_chart(fig_24hr, use_container_width=True)

    with c2:
        st.markdown("#### Critical Interchange Hub Overcrowding")
        hub_names_list = list(weather_engine.INTERCHANGE_HUBS.keys())
        hub_data = df_weather[df_weather["station name"].apply(
            lambda s: any(h.lower() in str(s).lower() for h in hub_names_list)
        )].groupby("station name")[["total_footfall", "weather_footfall", "footfall_delta"]].sum().reset_index()

        if len(hub_data) > 0:
            hub_data = hub_data.sort_values("weather_footfall", ascending=True).tail(8)
            fig_hubs = go.Figure()
            fig_hubs.add_trace(go.Bar(
                y=hub_data["station name"], x=hub_data["total_footfall"],
                name="Baseline Footfall", orientation="h", marker_color="#475569"
            ))
            fig_hubs.add_trace(go.Bar(
                y=hub_data["station name"], x=hub_data["footfall_delta"],
                name="Weather Influx Surge", orientation="h", marker_color=active_weather["color"]
            ))
            fig_hubs.update_layout(
                barmode="stack",
                template="plotly_dark",
                title="Interchange Hub Load Multiplication",
                xaxis=dict(title="Daily Passenger Volume"),
                yaxis=dict(title=""),
                legend=dict(orientation="h", y=1.14, x=0.0),
                margin=dict(l=20, r=20, t=40, b=20),
                height=400,
            )
            st.plotly_chart(fig_hubs, use_container_width=True)
        else:
            st.info("No known interchange hub names matched in the current file.")

    st.markdown("---")

    # Row 2: Road Transit Failure & Modal Shift Breakdown + Top 10 Busiest Stations
    c3, c4 = st.columns([1, 1.2])

    with c3:
        st.markdown("#### Road Transit Failure & Modal Shift Breakdown")
        st.caption("Academic & empirical breakdown of stranded road commuters shifting to DMRC:")

        total_shift_passengers = max(1000, int(daily_delta_passengers))
        modal_labels = [
            "Two-Wheelers (Bikes/Scooters)",
            "Auto-Rickshaws & E-Rickshaws",
            "DTC & Cluster City Buses",
            "App Cabs & Taxis (Ola/Uber Surge Avoidance)"
        ]
        modal_shares = [0.42, 0.26, 0.19, 0.13]
        modal_counts = [int(total_shift_passengers * s) for s in modal_shares]

        fig_donut = go.Figure(data=[go.Pie(
            labels=modal_labels,
            values=modal_counts,
            hole=0.5,
            marker_colors=["#3b82f6", "#eab308", "#ef4444", "#a855f7"],
            textinfo="label+percent",
            insidetextorientation="radial",
        )])
        fig_donut.update_layout(
            template="plotly_dark",
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20),
            height=360,
            annotations=[dict(
                text=f"<b>+{total_shift_passengers:,.0f}</b><br>Shifted<br>Riders",
                x=0.5, y=0.5, font_size=13, showarrow=False
            )]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with c4:
        st.markdown("#### Top 10 Busiest Stations Under Active Weather")
        top10_st = df_weather.groupby("station name")["weather_footfall"].sum().reset_index().sort_values("weather_footfall", ascending=True).tail(10)
        fig_top = px.bar(
            top10_st, x="weather_footfall", y="station name",
            orientation="h", color="weather_footfall",
            color_continuous_scale="Viridis", text_auto=".2s"
        )
        fig_top.update_layout(
            template="plotly_dark",
            coloraxis_showscale=False,
            xaxis=dict(title="Weather-Adjusted Daily Passenger Load"),
            yaxis=dict(title="Station Name"),
            margin=dict(l=20, r=20, t=20, b=20),
            height=360,
        )
        st.plotly_chart(fig_top, use_container_width=True)

    st.markdown("---")

    # Station-by-Station Deep Dive with Weather Impact Switch
    st.markdown("#### Station-by-Station Hourly Profile (With Weather Toggle)")
    all_st_names = sorted([str(s) for s in df["station name"].unique() if pd.notna(s)])
    default_st_idx = 0
    for prefer_st in ["Rajiv Chowk", "Kashmere Gate Metro", "Kashmere Gate", "Hauz Khas", "Central Secretariat"]:
        if prefer_st in all_st_names:
            default_st_idx = all_st_names.index(prefer_st)
            break

    s_col1, s_col2, s_col3 = st.columns([1.5, 1, 1])
    with s_col1:
        st_select = st.selectbox("Select Station:", all_st_names, index=default_st_idx)
    with s_col2:
        apply_weather_toggle = st.checkbox("Apply Weather Surge Overlay", value=True)
    with s_col3:
        chart_style = st.radio("Chart Type:", ["Grouped Bar Chart", "Dual Line Chart"], horizontal=True)

    st_df = df_weather[df_weather["station name"] == st_select].sort_values("hour")
    fig_st = go.Figure()

    if chart_style == "Grouped Bar Chart":
        fig_st.add_trace(go.Bar(x=st_df["hour"], y=st_df["entry"], name="Baseline Entry", marker_color="#2563eb"))
        fig_st.add_trace(go.Bar(x=st_df["hour"], y=st_df["exit"], name="Baseline Exit", marker_color="#dc2626"))
        if apply_weather_toggle:
            fig_st.add_trace(go.Bar(
                x=st_df["hour"],
                y=st_df["footfall_delta"],
                name=f"Weather Surge (+{active_weather['base_surge_pct']}%)",
                marker_color="#f59e0b"
            ))
        fig_st.update_layout(
            barmode="group",
            template="plotly_dark",
            title=f"Hourly Entry vs Exit vs Weather Surge — {st_select}",
            xaxis=dict(title="Hour of Day", dtick=1, range=[3.5, 23.5]),
            yaxis=dict(title="Hourly Passenger Trips"),
            legend=dict(orientation="h", y=1.12, x=0.1),
            margin=dict(l=20, r=20, t=40, b=20),
            height=380,
        )
    else:
        fig_st.add_trace(go.Scatter(x=st_df["hour"], y=st_df["entry"], mode="lines+markers", name="Baseline Entry", line=dict(color="#2563eb", width=3)))
        fig_st.add_trace(go.Scatter(x=st_df["hour"], y=st_df["exit"], mode="lines+markers", name="Baseline Exit", line=dict(color="#dc2626", width=3)))
        if apply_weather_toggle:
            fig_st.add_trace(go.Scatter(
                x=st_df["hour"], y=st_df["weather_footfall"],
                mode="lines+markers", name="Weather-Adjusted Total Load",
                line=dict(color="#f59e0b", width=4, dash="dash")
            ))
        fig_st.update_layout(
            template="plotly_dark",
            title=f"Hourly Profile & Weather Shock — {st_select}",
            xaxis=dict(title="Hour of Day", dtick=1, range=[4, 23]),
            yaxis=dict(title="Hourly Passenger Trips"),
            legend=dict(orientation="h", y=1.12, x=0.1),
            margin=dict(l=20, r=20, t=40, b=20),
            height=380,
        )
    st.plotly_chart(fig_st, use_container_width=True)

# --- TAB 2: 2026 AI CROWD PREDICTOR & WEATHER DIRECTIVES ---
with tab2:
    st.subheader("2026 Crowd Forecast & Weather-Adaptive DMRC Control Directives")
    st.caption("Machine Learning Random Forest model with live weather coefficient, modal shift, and station-specific sensitivity.")

    p1, p2, p3, p4 = st.columns([1.4, 1.2, 1, 1.4])
    with p1:
        pred_station = st.selectbox("Target Metro Station:", all_st_names, index=default_st_idx, key="p2_st")
    with p2:
        pred_date = st.date_input("Forecast Date (2026):", pd.to_datetime("2026-08-15"), key="p2_dt")
    with p3:
        pred_hour = st.slider("Target Hour:", 4, 23, 18, key="p2_hr")
    with p4:
        pred_weather_choice = st.selectbox(
            "Meteorological Condition:",
            ["Use Active Weather Mode"] + list(weather_engine.DELHI_SCENARIOS.keys()),
            index=0,
            key="p2_wc"
        )

    # Resolve target prediction weather
    if pred_weather_choice == "Use Active Weather Mode":
        target_weather = active_weather
    else:
        target_weather = weather_engine.DELHI_SCENARIOS[pred_weather_choice]

    if st.button("🔮 Predict Crowd & Generate Official Directives", type="primary", use_container_width=True):
        st_enc = le_station.transform([pred_station])[0] if pred_station in le_station.classes_ else 0
        dow = pred_date.weekday()
        month_num = pred_date.month

        # Baseline ML Random Forest prediction
        base_pred = model.predict([[pred_hour, st_enc, dow, month_num]])[0]
        base_pred = max(50.0, float(base_pred))

        # Weather impact computation
        impact = weather_engine.compute_station_crowd_impact(
            base_crowd=base_pred,
            station_name=pred_station,
            weather_dict=target_weather
        )

        st.markdown("---")

        # Results Summary
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.metric("Target Station & Time", f"{pred_station}", delta=f"{pred_date.strftime('%d %b %Y')} @ {pred_hour}:00 HRS")
        with r2:
            st.metric("Baseline ML Crowd", f"{impact['base_crowd']:,} Passengers", delta="Dry / Clear Conditions", delta_color="off")
        with r3:
            st.metric(
                "Weather-Induced Surge",
                f"+{impact['increment']:,} Passengers",
                delta=f"+{impact['effective_surge_pct']:.1f}% Influx ({target_weather['icon']})",
                delta_color="inverse" if impact['effective_surge_pct'] > 15 else "normal"
            )
        with r4:
            st.metric(
                "Predicted Total Crowd",
                f"{impact['final_crowd']:,} Passengers",
                delta=f"{impact['platform_density']} pass/m² (Density)",
                delta_color="inverse" if impact['platform_density'] > 3.0 else "normal"
            )

        # Operational metrics bar
        op1, op2, op3 = st.columns(3)
        with op1:
            st.info(f"🏛️ **Station Type:** {impact['hub_info']['role']} ({impact['hub_info']['lines']}) — Sensitivity Multiplier: **{impact['hub_info']['multiplier']}x**")
        with op2:
            st.warning(f"⏱️ **Estimated Security Frisking Queue Wait:** **{impact['queue_wait_mins']} minutes** delay per commuter.")
        with op3:
            st.error(f"🚨 **Operational Protocol:** **{impact['directives']['level_name']}**")

        # Modal Shift Influx Breakdown
        st.markdown("#### Commuter Shift Breakdown (Road Transit Failure Influx)")
        m_cols = st.columns(4)
        m_icons = {"Two-Wheelers (Bikes/Scooters)": "🛵", "Auto-Rickshaws & E-Rickshaws": "🛺", "DTC & Cluster City Buses": "🚌", "App Cabs & Taxis (Ola/Uber)": "🚕"}
        for idx, (m_mode, m_count) in enumerate(impact["modal_shift"].items()):
            with m_cols[idx]:
                st.metric(f"{m_icons.get(m_mode, '🚗')} {m_mode.split(' ')[0]}", f"+{m_count:,} riders", delta="Shifted from road")

        # DMRC Official Protocols and Directives
        st.markdown("---")
        st.subheader("Official DMRC Action Protocols & Emergency Directives")

        d = impact["directives"]
        getattr(st, d["level_kind"])(f"### {d['level_name']}")

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown(f"""
            #### 🎫 AFC Gate & Flow Control
            {d['afc_action']}

            #### 🚇 Train Frequency & Headway Injection
            {d['train_headway']}
            """)
        with col_d2:
            st.markdown(f"""
            #### 👮 CISF Security & Concourse Staffing
            {d['staffing']}

            #### 🌧️ Weather-Specific Tactical Directives
            """)
            for sop in d["weather_sops"]:
                st.markdown(sop)

# --- TAB 3: DELHI WEATHER CRISIS STRESS-TEST MATRIX (NEW) ---
with tab3:
    st.subheader("⚡ Delhi Meteorological Crisis Stress-Testing Matrix")
    st.caption("Simulate and compare how network traffic and interchange hubs respond across all Delhi weather extremes side-by-side.")

    stress_station = st.selectbox("Select Station to Stress-Test Across Scenarios:", all_st_names, index=default_st_idx, key="st_matrix")
    base_st_vol = df[df["station name"] == stress_station]["total_footfall"].sum()
    if base_st_vol <= 0:
        base_st_vol = 45000.0

    matrix_rows = []
    for sc_name, sc_data in weather_engine.DELHI_SCENARIOS.items():
        res = weather_engine.compute_station_crowd_impact(
            base_crowd=base_st_vol,
            station_name=stress_station,
            weather_dict=sc_data
        )
        matrix_rows.append({
            "Scenario": f"{sc_data['icon']} {sc_data['name']}",
            "Rainfall (mm/h)": sc_data["precipitation_mm"],
            "Temp (°C)": sc_data["temp_c"],
            "Road Disruption": f"{sc_data['road_disruption_index']}%",
            "Station Surge (%)": f"+{res['effective_surge_pct']:.1f}%",
            "Passenger Influx": f"+{res['increment']:,}",
            "Final Predicted Footfall": f"{res['final_crowd']:,}",
            "Platform Density (p/m²)": res["platform_density"],
            "Queue Wait (min)": res["queue_wait_mins"],
            "Protocol Level": res["directives"]["level_name"].split(":")[0],
        })

    matrix_df = pd.DataFrame(matrix_rows)
    st.dataframe(matrix_df, use_container_width=True)

    # Comparison bar chart
    fig_matrix = go.Figure()
    sc_names = [r["Scenario"] for r in matrix_rows]
    surges = [float(r["Station Surge (%)"].replace("+", "").replace("%", "")) for r in matrix_rows]
    colors = [weather_engine.DELHI_SCENARIOS[k]["color"] for k in weather_engine.DELHI_SCENARIOS.keys()]

    fig_matrix.add_trace(go.Bar(
        x=sc_names, y=surges,
        marker_color=colors,
        text=[f"+{s:.1f}%" for s in surges],
        textposition="auto"
    ))
    fig_matrix.update_layout(
        template="plotly_dark",
        title=f"Passenger Surge Sensitivity for {stress_station} Across Weather Extremes",
        xaxis=dict(title=""),
        yaxis=dict(title="Surge Percentage Influx (%)"),
        margin=dict(l=20, r=20, t=40, b=40),
        height=380,
    )
    st.plotly_chart(fig_matrix, use_container_width=True)

# --- TAB 4: RAW DATA & EXPORT ---
with tab4:
    st.subheader("Enriched DMRC Data Table")
    st.caption("Hourly entries, exits, total baseline footfalls, and weather-adjusted surge quantities.")

    show_cols = ["station name", "hour", "entry", "exit", "total_footfall", "hub_multiplier", "weather_surge_pct", "weather_footfall", "footfall_delta"]
    st.dataframe(df_weather[show_cols].head(200), use_container_width=True)

    # CSV Download Button
    csv_bytes = df_weather[show_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Weather-Enriched Footfall Dataset (CSV)",
        data=csv_bytes,
        file_name="dmrc_weather_enriched_analytics.csv",
        mime="text/csv",
    )
