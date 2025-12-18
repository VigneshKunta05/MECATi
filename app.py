# app.py — Sasta Rapido: Delivery Cost Estimator (Single File)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math
import time

# ───────────────────────────────
# 🔧 UTILITY FUNCTIONS (inlined)
# ───────────────────────────────

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate great circle distance in km."""
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_delivery_cost(
    distance_km,
    base_fee=20,
    per_km_rate=10,
    surge_multiplier=1.0,
    discount_percent=0,
    min_total=30
):
    distance_cost = distance_km * per_km_rate
    subtotal = base_fee + distance_cost
    surcharged = subtotal * surge_multiplier
    discounted = surcharged * (1 - discount_percent / 100)
    total = max(discounted, min_total)
    
    return {
        "base_fee": base_fee,
        "distance_cost": round(distance_cost, 2),
        "subtotal": round(subtotal, 2),
        "surge_multiplier": surge_multiplier,
        "surge_amount": round(surcharged - subtotal, 2),
        "discount_percent": discount_percent,
        "discount_amount": round(surcharged - discounted, 2),
        "final_total": round(total, 2)
    }

# ───────────────────────────────
# 🎨 EMBEDDED CSS (no external file)
# ───────────────────────────────
CUSTOM_CSS = """
<style>
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
}
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 1.5rem;
    transition: transform 0.2s;
}
.card:hover {
    transform: translateY(-3px);
}
.metric-card {
    text-align: center;
    padding: 1rem;
    border-radius: 12px;
    background: #f8f9fa;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #FF6B35;
}
.metric-label {
    font-size: 0.9rem;
    color: #6c757d;
}
footer {
    font-size: 0.8rem;
    text-align: center;
    margin-top: 2rem;
    color: #6c757d;
}
</style>
"""

# ───────────────────────────────
# 🚀 STREAMLIT APP
# ───────────────────────────────

st.set_page_config(
    page_title="Sasta Rapido 🚀",
    page_icon="📦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Header
col1, col2 = st.columns([0.15, 0.85])
with col1:
    st.image("https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/355/package_1f4e6.png", width=50)
with col2:
    st.title("Sasta Rapido 🚀")
    st.subheader("Fast • Affordable • Transparent")

st.markdown("💡 *Get instant delivery estimates — no hidden charges!*")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    currency = st.selectbox("Currency", ["₹ INR", "$ USD", "₨ PKR", "₲ PYG"], index=0)
    st.info("💡 Shorter distance = lower cost!")

# Input form
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📍 Enter Delivery Details")

col1, col2 = st.columns(2)

with col1:
    st.write("**Pickup Location**")
    pickup_lat = st.number_input("Latitude", value=19.0760, format="%.4f", help="e.g., 19.0760 for Mumbai")
    pickup_lon = st.number_input("Longitude", value=72.8777, format="%.4f", help="e.g., 72.8777 for Mumbai")

with col2:
    st.write("**Drop-off Location**")
    drop_lat = st.number_input("Drop Latitude", value=19.1136, format="%.4f", help="e.g., 19.1136 (Andheri)")
    drop_lon = st.number_input("Drop Longitude", value=72.8697, format="%.4f", help="e.g., 72.8697 (Andheri)")

# Advanced options
with st.expander("⚙️ Advanced Pricing (optional)"):
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        base_fee = st.slider("Base Fee", 10, 100, 20, 5)
    with col_b:
        per_km = st.slider("₹/km Rate", 5, 30, 10, 1)
    with col_c:
        surge = st.slider("Surge Multiplier", 1.0, 2.5, 1.0, 0.1)
    discount = st.slider("Discount (%)", 0, 50, 0, 5)

st.markdown('</div>', unsafe_allow_html=True)

# Compute
distance = haversine_distance(pickup_lat, pickup_lon, drop_lat, drop_lon)
cost_breakdown = calculate_delivery_cost(
    distance_km=distance,
    base_fee=base_fee,
    per_km_rate=per_km,
    surge_multiplier=surge,
    discount_percent=discount
)

with st.spinner("Calculating fastest route... 🚀"):
    time.sleep(0.4)

# Results
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Estimate Summary")

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f'<div class="metric-card"><div class="metric-value">{distance:.2f} km</div><div class="metric-label">Distance</div></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="metric-card"><div class="metric-value">₨{cost_breakdown["base_fee"]}</div><div class="metric-label">Base</div></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="metric-card"><div class="metric-value">x{surge}</div><div class="metric-label">Surge</div></div>', unsafe_allow_html=True)
col4.markdown(f'<div class="metric-card"><div class="metric-value">-{discount}%</div><div class="metric-label">Discount</div></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center; margin: 1.5rem 0;">
    <h2 style="color:#2E7D32">✅ Total: 
        <span style="color:#FF6B35; font-size:2.2rem">₨{cost_breakdown['final_total']}</span>
    </h2>
    <p style="color:#666">Estimated delivery time: <b>{max(15, int(distance * 3))} mins</b></p>
</div>
""", unsafe_allow_html=True)

# Waterfall chart
fig = go.Figure(go.Waterfall(
    orientation="v",
    measure=["absolute", "relative", "relative", "relative", "total"],
    x=["Base Fee", "Distance", "Surge", "Discount", "Final Total"],
    text=[
        f"₨{cost_breakdown['base_fee']}",
        f"₨{cost_breakdown['distance_cost']}",
        f"+₨{cost_breakdown['surge_amount']}",
        f"-₨{cost_breakdown['discount_amount']}",
        f"₨{cost_breakdown['final_total']}"
    ],
    y=[
        cost_breakdown["base_fee"],
        cost_breakdown["distance_cost"],
        cost_breakdown["surge_amount"],
        -cost_breakdown["discount_amount"],
        cost_breakdown["final_total"]
    ],
    connector={"line": {"color": "rgb(63, 63, 63)"}},
    decreasing={"marker": {"color": "#E53935"}},
    increasing={"marker": {"color": "#1E88E5"}},
    totals={"marker": {"color": "#43A047"}}
))

fig.update_layout(
    title="💰 Cost Breakdown",
    showlegend=False,
    height=350,
    margin=dict(t=40, b=40)
)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Export button
df = pd.DataFrame([{
    "Distance (km)": distance,
    "Base Fee (₨)": cost_breakdown["base_fee"],
    "Distance Cost (₨)": cost_breakdown["distance_cost"],
    "Surge Amount (₨)": cost_breakdown["surge_amount"],
    "Discount (₨)": cost_breakdown["discount_amount"],
    "Total (₨)": cost_breakdown["final_total"],
    "Surge Multiplier": surge,
    "Discount (%)": discount
}])

csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    "📥 Download Estimate (CSV)",
    csv,
    "sasta_rapido_estimate.csv",
    "text/csv",
    use_container_width=True
)

# Footer
st.markdown("""
<footer>
    Built with ❤️ using Streamlit • <strong>Sasta Rapido</strong> — Delivery made simple.
</footer>
""", unsafe_allow_html=True)