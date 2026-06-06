# ChurnGuard: Customer Retention Intelligence Dashboard

ChurnGuard is a product analytics and machine learning dashboard that predicts customer churn, explains why customers may leave, and helps product and customer success teams prioritize retention actions.

This project was designed as a portfolio project for Product Management, Product Analytics, Data Science, Technical Program Management, and SaaS-focused internship applications.

---

## Problem

Many companies know churn is a major business problem, but teams often struggle to answer:

- Which customers are most likely to leave?
- Why are they at risk?
- Which customers should we prioritize first?
- How much revenue is at risk?

Without a clear decision system, product and customer success teams may respond too late or spend time on the wrong accounts.

---

## Solution

ChurnGuard predicts customer churn risk and provides a dashboard for decision-making.

It helps teams:

- Identify high-risk customers
- Understand churn drivers
- Prioritize customer outreach
- Connect churn risk to revenue impact
- Monitor retention patterns by segment, plan, and industry

---

## Target Users

### Primary User
Customer Success Manager or Product Manager responsible for retention.

### Secondary Users
Revenue operations teams, growth teams, executives, product analysts, and account managers.

---

## Core Features

- Churn prediction using machine learning
- Risk levels: Low, Medium, High
- Explainable churn drivers
- Revenue-at-risk calculation
- Customer action queue
- Interactive filters by segment, plan, industry, and risk level
- Executive retention metrics

---

## Tech Stack

- Python
- Streamlit
- Pandas
- Scikit-learn
- Plotly
- Synthetic SaaS/customer success dataset

---

## How to Run

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/ChurnGuard.git
cd ChurnGuard
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

---

## Product Metrics

Success can be measured by:

- Reduction in customer churn
- Increase in retention saves
- Decrease in time to identify high-risk customers
- Increase in feature adoption among at-risk customers
- Revenue saved through proactive intervention

---

## Product Roadmap

### Version 1
- Build churn prediction dashboard
- Add explainable risk drivers
- Add revenue-at-risk metrics

### Version 2
- Add recommended next-best actions
- Add customer health score timeline
- Add retention playbook suggestions

### Version 3
- Integrate CRM data
- Add Salesforce/ServiceNow workflow triggers
- Add automated alerts for high-value customers

---

## Why This Project Matters

ChurnGuard shows how product thinking, machine learning, customer analytics, and business strategy can be combined to solve a real company problem: preventing customer loss before it happens.