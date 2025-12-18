# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.calculator import calculate_delivery_cost
from utils.geoutils import haversine_distance
import time

# Page config
st.set_page_config(
    page_title="Sasta Rapido 🚀",
    page_icon="📦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([0.15, 0.85])
with col1:
    st.image("https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/355/package_1f4e6.png", width=50)
with col2:
    st.title("Sasta Rapido 🚀")
    st.subheader("Fast • Affordable • Transparent")

st.markdown("💡 *Get instant delivery estimates — no hidden charges!*")

# Sidebar (optional settings)
with st.sidebar:
    st.header("⚙️ Settings")
    currency = st.selectbox("Currency", ["₹ INR", "$ USD", "₨ PKR", "₲ PYG"], index=0)
    lang = st.selectbox("Language", ["English", "Español", "हिन्दी"], disabled=True)
    st.info("💡 Pro tip: Shorter distance = lower cost!")

# Main form
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
    col1, col2, col3 = st.columns(3)
    with col1:
        base_fee = st.slider("Base Fee", 10, 100, 20, 5)
    with col2:
        per_km = st.slider("₹/km Rate", 5, 30, 10, 1)
    with col3:
        surge = st.slider("Surge Multiplier", 1.0, 2.5, 1.0, 0.1)
    
    discount = st.slider("Discount (%)", 0, 50, 0, 5)

st.markdown('</div>', unsafe_allow_html=True)

# Calculate
distance = haversine_distance(pickup_lat, pickup_lon, drop_lat, drop_lon)
cost_breakdown = calculate_delivery_cost(
    distance_km=distance,
    base_fee=base_fee,
    per_km_rate=per_km,
    surge_multiplier=surge,
    discount_percent=discount
)

# Simulate API latency for realism
with st.spinner("Calculating fastest route... 🚀"):
    time.sleep(0.5)

# Results section
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Estimate Summary")

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f'<div class="metric-card"><div class="metric-value">{distance:.2f} km</div><div class="metric-label">Distance</div></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="metric-card"><div class="metric-value">₨{cost_breakdown["base_fee"]}</div><div class="metric-label">Base</div></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="metric-card"><div class="metric-value">x{surge}</div><div class="metric-label">Surge</div></div>', unsafe_allow_html=True)
col4.markdown(f'<div class="metric-card"><div class="metric-value">-{discount}%</div><div class="metric-label">Discount</div></div>', unsafe_allow_html=True)

# Final total
st.markdown(f"""
<div style="text-align:center; margin: 1.5rem 0;">
    <h2 style="color:#2E7D32">✅ Total: 
        <span style="color:#FF6B35; font-size:2.2rem">₨{cost_breakdown['final_total']}</span>
    </h2>
    <p style="color:#666">Estimated delivery time: <b>{max(15, int(distance * 3))} mins</b></p>
</div>
""", unsafe_allow_html=True)

# Breakdown chart
fig = go.Figure(go.Waterfall(
    name="Cost",
    orientation="v",
    measure=["absolute", "relative", "relative", "relative", "total"],
    x=["Base Fee", "Distance", "Surge", "Discount", "Final Total"],
    textposition="outside",
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
    height=350
)

st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Export & Actions
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Export button
    df = pd.DataFrame([{
        "Distance (km)": distance,
        "Base Fee": cost_breakdown["base_fee"],
        "Distance Cost": cost_breakdown["distance_cost"],
        "Surge Amount": cost_breakdown["surge_amount"],
        "Discount": cost_breakdown["discount_amount"],
        "Total (₨)": cost_breakdown["final_total"]
    }])
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Estimate (CSV)",
        csv,
        "sasta_rapido_estimate.csv",
        "text/csv",
        key='download-csv',
        use_container_width=True
    )

# Footer
st.markdown("""
<footer>
    Built with ❤️ using Streamlit • <strong>Sasta Rapido</strong> — Delivery made simple.
</footer>
""", unsafe_allow_html=True)