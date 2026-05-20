import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Bike Profit Predictor",
    page_icon="🚴",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main {
    background: linear-gradient(to right, #0f172a, #1e293b);
    color: white;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(90deg,#06b6d4,#3b82f6);
    color: white;
    border-radius: 12px;
    height: 3.2em;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    transform: scale(1.02);
}

.metric-card {
    background-color: #111827;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 0px 15px rgba(255,255,255,0.1);
}

.title {
    text-align: center;
    font-size: 90px !important;
    font-weight: 900;
    color: #38bdf8;
    line-height: 1.1;
    text-shadow: 0px 0px 25px #38bdf8;
    margin-top: -20px;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------

model = joblib.load("bike_sales_model.pkl")

# ---------------- HEADER ----------------

st.markdown(
    '<p class="title">🚴 AI Bike Sales Profit Predictor</p>',
    unsafe_allow_html=True
)



st.divider()

# ---------------- MAIN LAYOUT ----------------

left, right = st.columns(2)

# ---------------- CUSTOMER INPUTS ----------------

with left:

    st.subheader("📋 Customer Information")

    customer_age = st.slider(
        "Customer Age",
        10,
        100,
        25
    )

    customer_gender = st.radio(
        "Customer Gender",
        ["M", "F"],
        horizontal=True
    )

    country = st.selectbox(
        "🌍 Country",
        [
            "United States",
            "United Kingdom",
            "Germany",
            "France",
            "Canada",
            "Australia"
        ]
    )

    product_category = st.selectbox(
        "🛒 Product Category",
        [
            "Accessories",
            "Bikes",
            "Clothing"
        ]
    )

# ---------------- SALES INPUTS ----------------

with right:

    st.subheader("💰 Sales Information")

    order_quantity = st.number_input(
        "Order Quantity",
        min_value=1,
        value=1
    )

    unit_cost = st.number_input(
        "Unit Cost ($)",
        min_value=0.0,
        value=100.0
    )

    unit_price = st.number_input(
        "Unit Price ($)",
        min_value=0.0,
        value=150.0
    )

# ---------------- BUSINESS CALCULATIONS ----------------

revenue = order_quantity * unit_price
total_cost = order_quantity * unit_cost

# REAL BUSINESS PROFIT
actual_profit = revenue - total_cost

# ---------------- QUICK INSIGHTS ----------------

st.subheader("📊 Quick Business Insights")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Revenue", f"${revenue:,.2f}")

with c2:
    st.metric("Total Cost", f"${total_cost:,.2f}")

with c3:

    if actual_profit > 0:
        st.metric("Actual Profit", f"${actual_profit:,.2f}")

    elif actual_profit < 0:
        st.metric("Actual Loss", f"-${abs(actual_profit):,.2f}")

    else:
        st.metric("Break Even", "$0.00")

st.divider()

# ---------------- PREDICT BUTTON ----------------

if st.button("🚀 Predict Profit"):

    # ---------------- CREATE INPUT DATA ----------------

    input_data = pd.DataFrame({

        'Customer_Age': [customer_age],
        'Customer_Gender': [customer_gender],
        'Country': [country],
        'Product_Category': [product_category],
        'Order_Quantity': [order_quantity],
        'Unit_Cost': [unit_cost],
        'Unit_Price': [unit_price]

    })

    # ---------------- BUSINESS LOGIC FIRST ----------------

    # LOSS CASE
    if actual_profit < 0:

        predicted_profit = actual_profit

        prediction_type = "loss"

    # BREAK EVEN
    elif actual_profit == 0:

        predicted_profit = 0

        prediction_type = "break_even"

    # USE ML ONLY FOR VALID PROFITS
    else:

        prediction = model.predict(input_data)

        ml_prediction = float(prediction[0])

        # NEVER ALLOW ML TO EXCEED REAL PROFIT
        predicted_profit = min(ml_prediction, actual_profit)

        prediction_type = "profit"

    # ---------------- RESULT SECTION ----------------

    st.success("Prediction Completed Successfully ✅")

    result_col1, result_col2 = st.columns([2, 1])

    # ---------------- MAIN RESULT CARD ----------------

    with result_col1:

        # LOSS
        if prediction_type == "loss":

            st.markdown(f"""
            <div class="metric-card">
                <h1>📉 Business Loss</h1>
                <h1 style="color:#ef4444;">
                    -${abs(predicted_profit):,.2f}
                </h1>
            </div>
            """, unsafe_allow_html=True)

        # BREAK EVEN
        elif prediction_type == "break_even":

            st.markdown("""
            <div class="metric-card">
                <h1>⚖️ Break Even</h1>
                <h1 style="color:#facc15;">
                    $0.00
                </h1>
            </div>
            """, unsafe_allow_html=True)

        # PROFIT
        else:

            st.markdown(f"""
            <div class="metric-card">
                <h1>💵 Predicted Profit</h1>
                <h1 style="color:#22c55e;">
                    ${predicted_profit:,.2f}
                </h1>
            </div>
            """, unsafe_allow_html=True)

    # ---------------- SIDE STATUS ----------------

    with result_col2:

        if prediction_type == "loss":

            st.error("⚠️ Loss Detected")

        elif prediction_type == "break_even":

            st.warning("⚖️ No Profit No Loss")

        elif predicted_profit > 5000:

            st.success("🔥 Extremely High Profit")

        elif predicted_profit > 1000:

            st.info("📈 High Profit Opportunity")

        else:

            st.warning("💡 Moderate Profit")

    # ---------------- PROFIT EFFICIENCY ----------------

    st.subheader("📊 Profit Efficiency Analysis")

    if revenue > 0:
        efficiency = (actual_profit / revenue) * 100
    else:
        efficiency = 0

    progress_value = min(max(int(abs(efficiency)), 0), 100)

    st.progress(progress_value)

    # NEGATIVE
    if efficiency < 0:

        st.error(f"Loss Efficiency: {efficiency:.2f}%")

    # BREAK EVEN
    elif efficiency == 0:

        st.warning("Efficiency: 0% (Break Even)")

    # POSITIVE
    else:

        st.success(f"Profit Efficiency: {efficiency:.2f}%")

    # ---------------- SMART AI RECOMMENDATION ----------------

    st.subheader("🤖 Smart AI Recommendation")

    # LOSS CASE
    if prediction_type == "loss":

        st.error("""
        ⚠️ Heavy Business Loss Detected

        Recommendations:
        - Increase selling price
        - Reduce supplier costs
        - Avoid selling below cost price
        - Reduce operational expenses
        """)

    # BREAK EVEN
    elif prediction_type == "break_even":

        st.warning("""
        ⚖️ Break-Even Situation

        Recommendations:
        - Slightly increase selling price
        - Reduce manufacturing cost
        - Add premium features for higher value
        """)

    # ACCESSORIES
    elif product_category == "Accessories":

        st.success("""
        🧤 Accessories Category Analysis

        Recommendations:
        - Bundle accessories with bikes
        - Promote combo offers
        - Increase digital marketing
        """)

    # BIKES
    elif product_category == "Bikes":

        st.info("""
        🚴 Bikes Category Analysis

        Recommendations:
        - Focus on premium customers
        - Launch seasonal offers
        - Provide EMI/financing options
        """)

    # CLOTHING
    elif product_category == "Clothing":

        st.info("""
        👕 Clothing Category Analysis

        Recommendations:
        - Launch seasonal collections
        - Collaborate with influencers
        - Promote sports fashion trends
        """)

    # BULK ORDERS
    elif order_quantity > 10:

        st.success("""
        📦 Bulk Order Opportunity

        Recommendations:
        - Negotiate supplier discounts
        - Expand warehouse inventory
        - Use wholesale pricing
        """)

    # HIGH PROFIT
    elif efficiency > 40:

        st.success("""
        🔥 Excellent Profitability

        Recommendations:
        - Scale marketing campaigns
        - Expand to new countries
        - Increase inventory stock
        """)

    # DEFAULT
    else:

        st.info("""
        📊 Stable Business Performance

        Recommendations:
        - Continue monitoring sales trends
        - Improve customer retention
        - Optimize operational efficiency
        """)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🚴 Bike Dashboard")

    st.write("### Product Categories")

    st.info("""
    🚲 Bikes → High-value bicycles
    
    🧤 Accessories → Helmets, gloves, lights
    
    👕 Clothing → Jerseys, jackets
    """)

    st.divider()

    st.write("### 🌍 Supported Countries")

    st.write("""
    🇺🇸 United States  
    🇬🇧 United Kingdom  
    🇩🇪 Germany  
    🇫🇷 France  
    🇨🇦 Canada  
    🇦🇺 Australia  
    """)

    st.divider()

    st.write("### ⏰ Current Time")

    st.write(datetime.now().strftime("%d %B %Y"))
    st.write(datetime.now().strftime("%I:%M:%S %p"))

    st.divider()

    st.success("AI + Real Business Logic Enabled")

# ---------------- FOOTER ----------------

st.divider()

st.caption("© 2026 AI Bike Sales Prediction System")
