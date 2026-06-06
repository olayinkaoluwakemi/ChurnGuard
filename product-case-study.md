# ChurnGuard Product Case Study

## 1. Product Overview

ChurnGuard is a customer retention intelligence dashboard that predicts churn risk, explains why customers may leave, and helps teams prioritize outreach based on business impact.

It was designed for SaaS, enterprise platform, and customer success environments where retention is directly tied to revenue growth.

---

## 2. Problem Statement

Customer churn is expensive, but teams often lack a clear and explainable way to identify at-risk customers early.

Product and customer success teams may have data across support tickets, usage, billing, NPS, and feature adoption, but these signals are often scattered. ChurnGuard combines these signals into one decision-support product.

---

## 3. Target User Persona

### Persona: Customer Success Manager

**Goals**
- Identify high-risk customers early
- Prioritize outreach based on revenue impact
- Understand why customers may leave
- Improve retention outcomes

**Pain Points**
- Too many accounts to manually review
- Churn signals are spread across multiple systems
- Difficult to know which customer needs attention first
- Hard to explain churn risk to leadership

---

## 4. Product Goals

ChurnGuard aims to:

- Help teams act before customers churn
- Prioritize high-value customers at risk
- Explain churn drivers in plain language
- Connect product usage to retention outcomes
- Support better product and customer success decisions

---

## 5. MVP Features

### Churn Prediction
Uses machine learning to estimate churn probability for each customer.

### Risk Classification
Customers are classified as Low, Medium, or High risk.

### Revenue-at-Risk
Calculates expected revenue exposure based on churn probability and monthly recurring revenue.

### Explainable Drivers
Provides plain-English explanations such as low product usage, low feature adoption, poor NPS, or unresolved support issues.

### Retention Action Queue
Ranks customers by churn probability and revenue impact.

---

## 6. Success Metrics

| Metric | Why It Matters |
|---|---|
| Churn reduction | Core business outcome |
| Retention saves | Measures successful intervention |
| Time to identify high-risk accounts | Measures efficiency |
| Feature adoption lift | Measures product engagement |
| Revenue protected | Measures business impact |

---

## 7. Product Trade-Offs

### Model Accuracy vs. Explainability
A Random Forest model gives stronger predictive performance while still allowing practical risk explanations through product-defined drivers.

### Synthetic Data vs. Real Customer Data
Synthetic data allows public demonstration without exposing private customer records.

### Prediction vs. Action
The MVP focuses on prediction and prioritization. Future versions should recommend specific playbooks.

---

## 8. Roadmap

### V1: Retention Dashboard
- Churn prediction
- Risk levels
- Revenue-at-risk
- Action queue

### V2: Playbook Intelligence
- Recommended outreach actions
- Feature adoption nudges
- Customer health timelines

### V3: Workflow Integrations
- Salesforce CRM integration
- ServiceNow workflow trigger
- Slack or email alerts for high-risk accounts

---

## 9. Interview Story

I built ChurnGuard to solve a common product and business problem: identifying which customers are likely to churn and why.

The project demonstrates my ability to combine machine learning, product analytics, customer success strategy, and dashboard design into a practical decision-making tool. It also shows how I think beyond the model by focusing on user workflows, prioritization, business impact, and measurable outcomes.