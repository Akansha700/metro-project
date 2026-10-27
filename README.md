# 🚇 DMRC Multi-File Metro Crowd Analytics & Live Weather AI Predictor

An enterprise-grade Delhi Metro (DMRC) passenger traffic analytics and AI crowd forecasting dashboard built with Streamlit. Featuring real-time **Delhi Weather API integration**, **meteorological shock modeling**, **road transit failure & modal shift analysis**, and **weather-responsive DMRC crowd control directives**.

---

## 🌟 Key New Features & Capabilities

### 1. 🌦️ Live Delhi Weather API & Crisis Simulator
- **Real-Time Delhi API Integration**: Fetches live temperature, precipitation (mm/hr), relative humidity, wind speed, and WMO weather codes directly from Open-Meteo API for Delhi NCR (`28.6139° N, 77.2090° E`).
- **Resilient Fallback Engine**: If running offline or behind restricted firewalls, the engine seamlessly switches to an internal Delhi meteorological simulator without disruption.
- **Delhi Crisis Scenarios**:
  - **⛈️ Monsoon Deluge / Severe Downpour**: Models the real-world **6 to 7.2 Lakh passenger journey surge** over daily averages (+28.5% network-wide, +48% at hubs) caused by severe arterial road waterlogging.
  - **🌧️ Moderate Monsoon Rain**: Continuous 12-20 mm/hr downpour triggering a 68% road disruption and +16.5% metro surge.
  - **🌦️ Passing Showers / Drizzle**: Localized slick roads prompting two-wheeler riders to take the metro (+6.5% surge).
  - **🔥 Scorching Summer Heatwave (44.5°C Loo)**: Thermal stress and 48°C+ heat index pushing passengers into air-conditioned DMRC trains (+14% surge).
  - **🌫️ Severe Winter Smog & AQI Crisis (GRAP-IV)**: CAQM private vehicle bans (BS-III petrol & BS-IV diesel) and DMRC's 60 extra daily train trips (+21.5% surge).
  - **❄️ Dense Winter Fog & Cold Wave**: Near-zero visibility on Ring Road & NH-48 driving office commuters to the metro (+10.5% surge).
  - **☀️ Pleasant / Clear Baseline Weather**: Standard timetable flow (0% delta).
  - **🛠️ Custom Weather Parameter Simulator**: Interactive sliders for rainfall intensity (0-60 mm/hr), temperature, and humidity.

---

### 2. 🔀 Modal Shift Breakdown & Road Transit Disruption
Academic and transit data shows that during severe Delhi downpours, surface transit suffers catastrophic delays (e.g. at Minto Bridge, Pul Prahladpur, ITO, Ashram, and Ring Road underpasses). Commuters shift to DMRC to benefit from its **99.95% operational punctuality**.

The dashboard automatically decomposes the origin of weather-surged passengers:
- **🛵 Two-Wheelers (Motorcycles / Scooters):** ~42% of shifted commuters (highest vulnerability to rain).
- **🛺 Auto-Rickshaws & E-Rickshaws:** ~26% of shifted commuters (stranded by flooded underpasses).
- **🚌 DTC & Cluster City Buses:** ~19% of shifted commuters (evading crawl speeds < 10 km/h).
- **🚕 App Cabs & Taxis (Ola / Uber):** ~13% of shifted commuters (avoiding extreme surge pricing & traffic jams).

---

### 3. 🏛️ Critical Interchange Hub Overcrowding Dynamics
Unlike terminus or local stations, major multi-line interchange hubs bear the brunt of sudden weather shocks as commuters complete cross-city journeys via rail:
- **Rajiv Chowk** (Yellow & Blue Lines) — *Central Business District & Heart of Network (1.48x sensitivity)*
- **Kashmere Gate** (Red, Yellow & Violet Lines) — *Triple Mega-Interchange & North Transit Terminal (1.52x sensitivity)*
- **Hauz Khas** (Yellow & Magenta Lines) — *South Delhi Arterial Junction & Airport Conduit (1.42x sensitivity)*
- **Central Secretariat** (Yellow & Violet Lines) — *Administrative & Government Ministries Hub (1.38x sensitivity)*
- **Anand Vihar** (Blue Line, Railway & ISBT) — *Inter-State Bus & Rail Gateway (1.36x sensitivity)*

---

### 4. 🔮 2026 AI Crowd Predictor & Dynamic Operational SOPs
- **Random Forest Machine Learning Engine**: Predicts hourly station footfall by hour, station encoding, day of week, and seasonality.
- **Dynamic Weather Coefficient**: Adjusts predictions dynamically based on ambient precipitation and temperature.
- **Operational Directives & Protocols**:
  - **Level 1 (Normal Operations < 900)**: 50/50 AFC gate split, 4.5-5.0 min train headway.
  - **Level 2 (Moderate Congestion 900 - 2,400)**: Convert reserve gates to Entry mode, 3.5 min headway.
  - **Level 3 (Heavy Weather Surge 2,400 - 4,200)**: All flexible gates to Entry, 2.5 min peak headway rakes injected, zigzag concourse queue barriers.
  - **Level 4 (Critical Overcrowding Alert > 4,200)**: **HOLD GATES** protocol initiated at Rajiv Chowk & Kashmere Gate, skip-stop empty rake injections from Yamuna Bank / Najafgarh depots.
- **Tactical Weather Directives**:
  - Monsoon: High-capacity de-watering sump pumps activated at subway gates 1 & 2; anti-skid rubber mats on glazed floors.
  - Heatwave: 100% chiller plant load; platform chilled drinking water stations.
  - Smog / GRAP-IV: 60 extra daily trips; 8-coach rake enforcement.

---

### 5. 📂 1-Click Built-in Sample Data Loader
- Includes real **September 2024 DMRC Entry and Exit datasets** covering 250+ metro stations.
- Click **"Load DMRC Official Sample Data"** on the dashboard to test all features instantly, or drag-and-drop custom multi-month CSV/Excel files.

---

## 📁 Repository Structure

```
STREAMLIT-METRO-DASHBOARD/
├── app.py                      # Main Streamlit dashboard application
├── weather_engine.py           # Live Delhi Open-Meteo API & behavioral transit shock engine
├── sample_data/                # Built-in DMRC official sample datasets
│   ├── sample_dmrc_entry.csv   # September 2024 stationwise hourly entry data
│   └── sample_dmrc_exit.csv    # September 2024 stationwise hourly exit data
├── requirements.txt            # Python dependencies
└── README.md                   # Comprehensive system documentation
```

---

## 🚀 Quickstart Guide

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/ananya623/STREAMLIT-METRO-DASHBOARD.git
cd STREAMLIT-METRO-DASHBOARD
pip install -r requirements.txt
```

### 2. Run the Dashboard
Launch the Streamlit app locally:
```bash
streamlit run app.py
```

### 3. Usage
1. Open the local URL displayed in the terminal (usually `http://localhost:8501`).
2. Click **"⚡ Load DMRC Official Sample Data"** to load the built-in September 2024 dataset, or upload your own files in Step 1.
3. In the sidebar, select between **Live Delhi Weather (Open-Meteo API)** or simulated scenarios (e.g. **Monsoon Deluge / Severe Downpour**).
4. Explore the 4 tabs:
   - **Tab 1:** Visual Analytics & Weather Dynamics (24-hour curves, hub overcrowding, modal shift breakdown).
   - **Tab 2:** 2026 AI Crowd Predictor & Weather Directives (station forecasts and SOPs).
   - **Tab 3:** Delhi Weather Crisis Stress-Test Matrix (cross-scenario comparison).
   - **Tab 4:** Raw Data Table with CSV export.

---

## 📊 Technical Reference & Data Sources
- **Live Weather API**: [Open-Meteo Weather Forecast API](https://open-meteo.com) (`latitude=28.6139`, `longitude=77.2090`).
- **Delhi Metro Data**: Delhi Metro Rail Corporation (DMRC) open data / hourly station-wise entry & exit records.
- **Monsoon Ridership Surges**: Empirical records from DMRC monsoon operations (logging +6 to 7 lakh journeys above daily baseline during severe waterlogging events).
