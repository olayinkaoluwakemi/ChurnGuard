import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

st.set_page_config(
    page_title="ChurnGuard | Customer Retention Intelligence",
    page_icon="📉",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.hero {
    padding: 28px;
    border-radius: 18px;
    background: linear-gradient(135deg, #111827 0%, #1f2937 50%, #374151 100%);
    color: white;
    margin-bottom: 24px;
}
.hero h1 {
    font-size: 44px;
    margin-bottom: 6px;
}
.hero p {
    font-size: 17px;
    color: #e5e7eb;
}
.section-title {
    font-size: 23px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/customer_churn_data.csv")

def risk_label(probability):
    if probability >= 0.70:
        return "High"
    if probability >= 0.40:
        return "Medium"
    return "Low"

def explain_customer(row):
    reasons = []
    if row["active_days_last_30"] <= 7:
        reasons.append("low recent product usage")
    if row["feature_adoption_score"] < 0.35:
        reasons.append("low feature adoption")
    if row["nps_score"] <= 5:
        reasons.append("low NPS score")
    if row["support_tickets_last_30"] >= 5:
        reasons.append("high support volume")
    if row["avg_response_time_hours"] >= 12:
        reasons.append("slow support response time")
    if row["billing_issues_last_90"] >= 2:
        reasons.append("recent billing issues")
    if row["last_login_days_ago"] >= 30:
        reasons.append("long time since last login")
    if row["training_completed"] == 0:
        reasons.append("training not completed")

    if not reasons:
        return "No major churn drivers detected."
    return "Churn risk driven by " + ", ".join(reasons) + "."

data = load_data()

numeric_features = [
    "tenure_months",
    "monthly_recurring_revenue",
    "active_days_last_30",
    "support_tickets_last_30",
    "avg_response_time_hours",
    "feature_adoption_score",
    "nps_score",
    "billing_issues_last_90",
    "training_completed",
    "last_login_days_ago"
]
categorical_features = ["segment", "industry", "plan", "region"]

X = data[numeric_features + categorical_features]
y = data["churned"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numeric_features)
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=160, random_state=42, max_depth=8))
    ]
)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.25, stratify=y)
model.fit(X_train, y_train)

probabilities = model.predict_proba(X)[:, 1]
predictions = model.predict(X_test)
test_probs = model.predict_proba(X_test)[:, 1]

data["predicted_churn_probability"] = probabilities
data["risk_level"] = data["predicted_churn_probability"].apply(risk_label)
data["risk_explanation"] = data.apply(explain_customer, axis=1)
data["revenue_at_risk"] = data["monthly_recurring_revenue"] * data["predicted_churn_probability"]

auc = roc_auc_score(y_test, test_probs)
accuracy = accuracy_score(y_test, predictions)

st.markdown("""
<div class="hero">
    <h1>📉 ChurnGuard</h1>
    <p>Customer retention intelligence dashboard that predicts churn risk, explains why customers may leave, and helps product teams prioritize retention actions.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Dashboard Controls")
    st.caption("Filter retention risk by customer and business context.")

    segment = st.multiselect("Segment", sorted(data["segment"].unique()), default=sorted(data["segment"].unique()))
    plan = st.multiselect("Plan", sorted(data["plan"].unique()), default=sorted(data["plan"].unique()))
    industry = st.multiselect("Industry", sorted(data["industry"].unique()), default=sorted(data["industry"].unique()))
    risk = st.multiselect("Risk Level", ["High", "Medium", "Low"], default=["High", "Medium", "Low"])

    st.divider()
    st.caption("Portfolio Project")
    st.write("Built with Python, Streamlit, Scikit-learn, Plotly, and Pandas.")

filtered = data[
    data["segment"].isin(segment)
    & data["plan"].isin(plan)
    & data["industry"].isin(industry)
    & data["risk_level"].isin(risk)
]

st.markdown('<div class="section-title">Executive Retention Overview</div>', unsafe_allow_html=True)

total_customers = len(filtered)
high_risk_customers = int((filtered["risk_level"] == "High").sum())
avg_churn_risk = round(filtered["predicted_churn_probability"].mean() * 100, 1) if total_customers else 0
revenue_at_risk = round(filtered["revenue_at_risk"].sum(), 2)
avg_nps = round(filtered["nps_score"].mean(), 1) if total_customers else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Customers", f"{total_customers:,}")
c2.metric("High-Risk Customers", f"{high_risk_customers:,}")
c3.metric("Avg Churn Risk", f"{avg_churn_risk}%")
c4.metric("Revenue at Risk", f"${revenue_at_risk:,.0f}")
c5.metric("Avg NPS", f"{avg_nps}")

st.caption(f"Model performance on holdout data: ROC-AUC {auc:.2f}, Accuracy {accuracy:.2f}")

high_value_at_risk = filtered[(filtered["risk_level"] == "High") & (filtered["monthly_recurring_revenue"] >= filtered["monthly_recurring_revenue"].quantile(0.75))]
st.info(
    f"ChurnGuard found **{len(high_value_at_risk)} high-value customers at high churn risk**. "
    "Recommended action: prioritize outreach, onboarding support, and feature adoption interventions."
)

st.divider()

left, right = st.columns([1.2, 1])

with left:
    st.markdown('<div class="section-title">Churn Risk by Segment</div>', unsafe_allow_html=True)
    segment_risk = (
        filtered.groupby(["segment", "risk_level"])
        .size()
        .reset_index(name="customers")
    )
    fig = px.bar(
        segment_risk,
        x="segment",
        y="customers",
        color="risk_level",
        barmode="group",
        labels={"segment": "Segment", "customers": "Customers", "risk_level": "Risk Level"}
    )
    fig.update_layout(height=420, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown('<div class="section-title">Risk Distribution</div>', unsafe_allow_html=True)
    risk_counts = filtered["risk_level"].value_counts().reset_index()
    risk_counts.columns = ["risk_level", "count"]
    fig2 = px.pie(risk_counts, values="count", names="risk_level", hole=0.55)
    fig2.update_layout(height=420, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig2, use_container_width=True)

left2, right2 = st.columns([1.1, 1])

with left2:
    st.markdown('<div class="section-title">Revenue at Risk by Plan</div>', unsafe_allow_html=True)
    plan_revenue = (
        filtered.groupby("plan")["revenue_at_risk"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig3 = px.bar(
        plan_revenue,
        x="plan",
        y="revenue_at_risk",
        labels={"plan": "Plan", "revenue_at_risk": "Revenue at Risk"}
    )
    fig3.update_layout(height=420, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig3, use_container_width=True)

with right2:
    st.markdown('<div class="section-title">Usage vs Churn Probability</div>', unsafe_allow_html=True)
    fig4 = px.scatter(
        filtered,
        x="active_days_last_30",
        y="predicted_churn_probability",
        color="risk_level",
        size="monthly_recurring_revenue",
        hover_data=["customer_id", "segment", "plan", "nps_score"],
        labels={
            "active_days_last_30": "Active Days Last 30",
            "predicted_churn_probability": "Predicted Churn Probability",
            "risk_level": "Risk Level"
        }
    )
    fig4.update_layout(height=420, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

st.markdown('<div class="section-title">Retention Action Queue</div>', unsafe_allow_html=True)
st.caption("Prioritized customer list with explainable churn drivers and revenue impact.")

review = filtered.sort_values(["predicted_churn_probability", "revenue_at_risk"], ascending=[False, False])
review = review[[
    "customer_id",
    "segment",
    "industry",
    "plan",
    "monthly_recurring_revenue",
    "predicted_churn_probability",
    "risk_level",
    "active_days_last_30",
    "feature_adoption_score",
    "nps_score",
    "support_tickets_last_30",
    "revenue_at_risk",
    "risk_explanation"
]]

st.dataframe(review, use_container_width=True, hide_index=True)

st.divider()

st.markdown('<div class="section-title">Product Intelligence Layer</div>', unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)

with p1:
    st.subheader("User Problem")
    st.write(
        "Customer success and product teams often know churn is happening, but lack a clear way to prioritize which customers need intervention first."
    )

with p2:
    st.subheader("Product Solution")
    st.write(
        "ChurnGuard predicts churn probability, explains major risk drivers, and connects retention risk to revenue impact."
    )

with p3:
    st.subheader("Success Metrics")
    st.write(
        "Reduced churn, increased retention saves, improved outreach prioritization, higher feature adoption, and faster customer recovery."
    )

st.divider()

st.markdown('<div class="section-title">Why This Matters</div>', unsafe_allow_html=True)
st.write(
    "ChurnGuard helps teams move from reactive customer support to proactive retention strategy. "
    "It combines machine learning, product analytics, and business context so teams can act before customers leave."
)