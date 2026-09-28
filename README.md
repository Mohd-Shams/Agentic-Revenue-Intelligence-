# 🛒 NovCart
## AI-Powered Revenue Leakage & Root-Cause Intelligence Platform

> An end-to-end e-commerce analytics platform combining Python, SQL,
> Power BI and Agentic AI to identify performance deterioration,
> operational issues and modeled recovery opportunities.

---

## 1. 🎯 Business Problem

Our Q4 profit has declined significantly compared with Q3, but I want to understand more than just the headline decline. Can you identify where the profit leakage is occurring, determine which commercial and operational factors are contributing to the deterioration, and identify the areas where NovCart may have opportunities to recover value?” The analyst would then investigate the Q3-to-Q4 profitability change, examine factors such as discounts, product costs, shipping costs, returns, delivery performance, payment failures, and regional performance, and finally quantify modeled recovery opportunities under clearly defined assumptions. The purpose of the analysis is therefore to move from simply identifying that profit declined to understanding where the value is being lost, what factors require further investigation, and where potential recovery may exist.

NovCart experienced a significant deterioration in financial performance
from Q3 to Q4.

| Metric | Q3 | Q4 | Change |
|---|---:|---:|---:|
| Revenue | ₹3.86 Cr | ₹2.78 Cr | -28.03% |
| Profit | ₹94.23 L | ₹52.36 L | -44.44% |
| Profit Margin | 24.38% | 18.82% | -5.56 pp |

The central business question was:

> **Why did profitability deteriorate, where is NovCart leaking value,
> and which areas provide measurable recovery opportunities?**

The analysis focused on:

- Revenue and profit performance
- Regional profitability
- Delivery delays
- Product returns
- Return reasons
- Payment failures
- Discounting
- Marketing efficiency
- Profit leakage
- Modeled recovery opportunities

---

# 2. 🔎 Key Findings

- Revenue declined **28.03%** from Q3 to Q4.
- Profit declined **44.44%**, considerably faster than revenue.
- Profit margin decreased from **24.38% to 18.82%**.
- **East** experienced the largest absolute regional profit decline.
- Delivery delays emerged as an important operational signal associated
  with higher return rates.
- **Wireless Earbuds** showed a notable product-level return hotspot.
- **Quality issues** represented the largest return category.
- Payment failures represented another potential source of lost orders.
- Discounting represented the largest **modeled recovery opportunity**.
- Recovery opportunities are analytical scenarios and are **not guaranteed
  savings or audited losses**.

---

# 3. 📊 Power BI Dashboard

The Power BI dashboard tells the business story in three stages:

### Page 1 — Executive Performance

**Question:** What happened?

![Executive Performance](Power_Bi_Dashboard/Executive_Performance.png)

Revenue and profit performance deteriorated significantly in Q4,
with profit declining faster than revenue.

---

### Page 2 — Root Cause & Operations

**Question:** Where are the operational pressure points?

![Root Cause & Operations](Power_Bi_Dashboard/RootCause_&_Operations.png)

The analysis highlights delivery delays, returns, payment failures,
regional deterioration and product-level return hotspots.

---

### Page 3 — Q4 Leakage Analysis

**Question:** What does the deterioration mean financially?

![Q4 Leakage Analysis](Power_Bi_Dashboard/Q4Leakage_Analysis.png)

The final page connects operational issues with profitability
deterioration and modeled recovery opportunities.

---

# 4. 🤖 Agentic AI 
**[Launch NovCart AI Analyst](https://novcart-ai.streamlit.app/)**

NovCart includes an AI Business Analyst that allows users to ask
business questions using natural language.

### Example questions

```text
Why did profit decline from Q3 to Q4?

Which region had the biggest decline in profit?

Which region generated the most revenue?

Which products have high return rates?

Is delivery delay associated with returns?

What are the major return reasons?

How much modeled opportunity is associated with discounting?
