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
- Q4 revenue declined by 28.03% compared with Q3, falling from approximately ₹3.86 Cr to ₹2.78 Cr.

- Q4 profit declined by 44.44%, from ₹94.23L to ₹52.36L — a much sharper deterioration than revenue.

- Profit margin dropped from 24.38% to 18.82%, a decline of 5.56 percentage points, indicating significant margin pressure.

- Returns were a major operational concern, with an overall return rate of approximately 11.41%.
  
- Delivery delays were strongly associated with returns: delayed orders had a return rate of 26.61%, compared with 10.48% for non-delayed orders.

- The statistical analysis supported this relationship, with χ² = 52.97 and p = 3.39 × 10⁻¹³. This indicates association, not proof of causation.

- Quality issues were the largest return reason, accounting for approximately 32.33% of the return-value breakdown, followed by late delivery and damaged products.

- Wireless Earbuds showed the highest product return rate, at approximately 14.41%, making it an important product-level area for investigation.

- Regional profitability deteriorated from Q3 to Q4, with every region in the reported comparison showing lower Q4 profit.

- The combined analysis identified discounting, marketing efficiency, returns, delivery and shipping as areas for modeled recovery opportunities. These are scenario-based opportunities, not guaranteed savings, and require further validation.

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


- Business-question interface — Managers can ask questions about NovCart’s revenue, profit, returns, delivery, discounts, marketing and other KPIs in natural language.

- Uses existing analysis — The agent builds on the validated Python/SQL analysis instead of independently recreating the entire analysis for every question.

- Semantic layer — It defines standard meanings for metrics such as Revenue, Profit, Profit Margin, Orders, AOV, Return Rate, Delivery Delay Rate and ROAS.

- Metric mapping — Different phrases such as “sales,” “revenue,” or “earnings” can be mapped to the appropriate governed metric.

- Evidence-based answers — The agent uses prepared findings/evidence such as Q3–Q4 comparisons, regional changes, operational hotspots and modeled opportunities.

- Statistical awareness — It understands that an association between delivery delays and returns does not automatically prove causation.

- Business reasoning — Instead of only returning numbers, it explains what the number means for the business and connects related findings.

- Recovery analysis — It can explain the modeled opportunities around discounting, marketing efficiency, returns, delivery and shipping.

- LLM + application layer — The LLM is used to convert the governed metrics and evidence into a natural-language business response, while the application controls the context supplied to it.

- Overall purpose — The agent turns Python + SQL + Power BI findings into a conversational business analyst, allowing management to explore the project findings without manually navigating every analysis.

NovCart includes an AI Business Analyst that allows users to ask
business questions using natural language.

### Example questions

```text
Why did profit decline from Q3 to Q4?

Which region had the biggest decline in profit?

Which region generated the most revenue?

Which products have high return rates?
```

# Recommendations Linked to Key Findings
| Key finding                                                                                                                | Recommendation                                                         | Business action                                                                                                                                          |
| -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Profit fell 44.44%** from **₹94.23L in Q3 to ₹52.36L in Q4**, while revenue fell only **28.03%**.                        | **Prioritize margin protection.**                                      | Track profit margin alongside revenue instead of focusing only on sales growth; Q3 margin was **24.38% vs 18.82% in Q4**.                                |
| **Delayed orders had a 26.61% return rate vs 10.48% for non-delayed orders** — a **16.13 pp gap**.                         | **Reduce delivery delays.**                                            | Investigate delayed orders by region, product and fulfillment partner, and measure whether lower delays reduce returns.                                  |
| **Quality issues were ~32.33% of return value**, the largest return category in the dashboard analysis.                    | **Attack product-quality returns first.**                              | Investigate high-return SKUs, quality complaints and supplier/fulfillment issues; prioritize products such as **Wireless Earbuds (14.41% return rate)**. |
| **East profit fell from ₹22.71L to ₹11.43L**, a decline of about **₹11.28L**; North also fell from **₹26.15L to ₹14.95L**. | **Prioritize regional diagnosis.**                                     | Break down East and North by product, delivery, returns, discounts and shipping to identify the specific drivers behind the profit decline.              |
| **Modeled recovery opportunity ≈ ₹36.3L**, with discounting representing the largest modeled opportunity.                  | **Test discount optimization rather than blindly reducing discounts.** | Segment discounts by product/customer and run controlled tests to determine whether lower discounting improves profit without damaging conversion.       |
| **Overall return rate was 11.41%** and payment failure rate was **2.33%**.                                                 | **Create operational monitoring.**                                     | Track return rate and payment failures by month, region, product and payment method to identify recurring leakage.                                       |
| The analysis identified **marketing efficiency** as another recovery area.                                                 | **Improve ROAS efficiency.**                                           | Compare current ROAS with the historical baseline and test reallocating spend from weaker-performing campaigns/segments.                                 |
| **Shipping cost** was included as a smaller modeled recovery driver.                                                       | **Investigate high shipping-cost segments.**                           | Examine shipping cost as a percentage of revenue by region/product and target unusually expensive combinations.                                          |


# NovCart — Project Summary

NovCart is an end-to-end E-commerce Performance & Leakage Analytics platform designed to answer:

Why did profitability deteriorate, where is the business leaking value, and what areas should management investigate for recovery?

What the project does

Python → EDA, statistical analysis, root-cause investigation and modeled recovery scenarios.

SQL → Repeatable business analysis using CTEs, window functions, ranking, customer analysis and Q3–Q4 comparisons.

Power BI → Three-page management story:
Executive Performance → Root Cause & Operations → Q4 Leakage Analysis

Modeled Opportunity → Estimates potential recovery from discounting, marketing efficiency, returns, delivery and shipping using historical baselines.

AI Agent → Combines an LLM + Semantic Layer + Evidence Layer + Streamlit to let managers ask business questions in natural language and receive grounded answers.

Final business story

Performance declined → root causes were investigated → operational hotspots were identified → potential recovery areas were modeled → findings were converted into an interactive dashboard → AI was added as a conversational decision-support layer.

The key analytical discipline is that observed findings, statistical associations and modeled opportunities are kept separate, so the project does not present assumptions as confirmed financial losses.



