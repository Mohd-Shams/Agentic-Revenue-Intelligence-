import warnings

warnings.filterwarnings(
    "ignore",
    message="Direct use of automatic function calling.*"
)

from google import genai
import pandas as pd
import json
import os

# ============================================================
# CONFIG
# ============================================================

MODEL = "gemini-flash-lite-latest"

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ============================================================
# 1. LOAD FILES
# ============================================================

CSV_FILE = "ecommerce_cleaned.csv"
JSON_FILE = "analysis_results.json"

df = pd.read_csv(CSV_FILE)

with open(JSON_FILE, "r", encoding="utf-8") as f:
    ANALYSIS_RESULTS = json.load(f)


# ============================================================
# 2. SEMANTIC LAYER
# ============================================================

SEMANTIC_LAYER = {

    "revenue": {
        "definition": "Total net revenue generated from orders.",
        "formula": "SUM(net_revenue)",
        "unit": "INR",
        "dimensions": [
            "month",
            "quarter",
            "region",
            "category",
            "product_name",
            "marketing_source",
            "campaign"
        ]
    },

    "profit": {
        "definition": "Total profit generated after applicable costs.",
        "formula": "SUM(profit)",
        "unit": "INR",
        "dimensions": [
            "month",
            "quarter",
            "region",
            "category",
            "product_name",
            "marketing_source",
            "campaign"
        ]
    },

    "profit_margin": {
        "definition": "Profit as a percentage of net revenue.",
        "formula": "SUM(profit) / SUM(net_revenue)",
        "unit": "percentage",
        "dimensions": [
            "month",
            "quarter",
            "region",
            "category",
            "product_name"
        ]
    },

    "orders": {
        "definition": "Number of unique orders.",
        "formula": "nunique(order_id)",
        "unit": "count",
        "dimensions": [
            "month",
            "quarter",
            "region",
            "category",
            "product_name"
        ]
    },

    "customers": {
        "definition": "Number of unique customers.",
        "formula": "nunique(customer_id)",
        "unit": "count",
        "dimensions": [
            "month",
            "quarter",
            "region",
            "category",
            "product_name"
        ]
    },

    "aov": {
        "definition": "Average order value.",
        "formula": "SUM(net_revenue) / nunique(order_id)",
        "unit": "INR",
        "dimensions": [
            "month",
            "quarter",
            "region",
            "category",
            "product_name"
        ]
    },

    "return_rate": {
        "definition": "Percentage of orders marked as returned.",
        "formula": "returned_orders / total_orders",
        "unit": "percentage",
        "dimensions": [
            "month",
            "quarter",
            "region",
            "category",
            "product_name",
            "return_reason"
        ]
    },

    "delivery_delay_rate": {
        "definition": "Percentage of orders experiencing delivery delay.",
        "formula": "delayed_orders / total_orders",
        "unit": "percentage",
        "dimensions": [
            "month",
            "quarter",
            "region",
            "category",
            "product_name"
        ]
    },

    "payment_failure_rate": {
        "definition": "Percentage of payments that failed.",
        "formula": "failed_payments / total_payments",
        "unit": "percentage",
        "dimensions": [
            "month",
            "quarter",
            "region",
            "payment_method"
        ]
    },

    "discount_rate": {
        "definition": "Discount amount relative to gross revenue.",
        "formula": "SUM(discount_amount) / SUM(gross_revenue)",
        "unit": "percentage",
        "dimensions": [
            "month",
            "quarter",
            "region",
            "category",
            "product_name"
        ]
    },

    "roas": {
        "definition": "Revenue attributed to advertising relative to advertising spend.",
        "formula": "attributed_revenue / ad_spend",
        "unit": "ratio",
        "dimensions": [
            "month",
            "quarter",
            "marketing_source",
            "campaign"
        ]
    }
}


# ============================================================
# 3. BUILD CSV CONTEXT
# ============================================================

def build_csv_context(df):

    context = {}

    # ========================================================
    # DATASET OVERVIEW
    # ========================================================

    context["dataset"] = {
        "rows": len(df),
        "columns": len(df.columns),
        "columns_list": list(df.columns)
    }

    # ========================================================
    # NUMERIC SUMMARY
    # ========================================================

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    numeric_summary = {}

    for col in numeric_columns:

        numeric_summary[col] = {
            "sum": float(df[col].sum()),
            "mean": float(df[col].mean()),
            "min": float(df[col].min()),
            "max": float(df[col].max())
        }

    context["numeric_summary"] = numeric_summary

    # ========================================================
    # CATEGORICAL SUMMARY
    # ========================================================

    categorical_columns = [
        "region",
        "category",
        "product_name",
        "marketing_source",
        "campaign",
        "payment_method",
        "return_reason",
        "quarter",
        "month"
    ]

    categorical_summary = {}

    for col in categorical_columns:

        if col not in df.columns:
            continue

        categorical_summary[col] = (
            df[col]
            .value_counts(dropna=False)
            .head(50)
            .to_dict()
        )

    context["categorical_summary"] = categorical_summary

    # ========================================================
    # BUSINESS AGGREGATIONS
    # ========================================================

    aggregations = {}

    # --------------------------------------------------------
    # Single-dimension aggregations
    # --------------------------------------------------------

    group_columns = [
        "region",
        "category",
        "product_name",
        "marketing_source",
        "campaign",
        "payment_method",
        "return_reason",
        "quarter",
        "month"
    ]

    for column in group_columns:

        if column not in df.columns:
            continue

        grouped = (
            df.groupby(column, dropna=False)
            .agg(
                revenue=("net_revenue", "sum"),
                profit=("profit", "sum"),
                orders=("order_id", "nunique")
            )
            .reset_index()
        )

        # Add profit margin
        grouped["profit_margin"] = (
            grouped["profit"] /
            grouped["revenue"]
        )

        aggregations[column] = grouped.to_dict(
            orient="records"
        )

    # ========================================================
    # Q4 + REGION
    # ========================================================

    if "quarter" in df.columns and "region" in df.columns:

        q4_region = df[
            df["quarter"].astype(str).str.upper() == "Q4"
        ]

        grouped = (
            q4_region
            .groupby("region", dropna=False)
            .agg(
                revenue=("net_revenue", "sum"),
                profit=("profit", "sum"),
                orders=("order_id", "nunique")
            )
            .reset_index()
        )

        grouped["profit_margin"] = (
            grouped["profit"] /
            grouped["revenue"]
        )

        # Sort by revenue
        grouped = grouped.sort_values(
            "revenue",
            ascending=False
        )

        aggregations["q4_by_region"] = (
            grouped.to_dict(orient="records")
        )

    # ========================================================
    # Q4 + CATEGORY
    # ========================================================

    if "quarter" in df.columns and "category" in df.columns:

        q4_category = df[
            df["quarter"].astype(str).str.upper() == "Q4"
        ]

        grouped = (
            q4_category
            .groupby("category", dropna=False)
            .agg(
                revenue=("net_revenue", "sum"),
                profit=("profit", "sum"),
                orders=("order_id", "nunique")
            )
            .reset_index()
        )

        grouped["profit_margin"] = (
            grouped["profit"] /
            grouped["revenue"]
        )

        grouped = grouped.sort_values(
            "revenue",
            ascending=False
        )

        aggregations["q4_by_category"] = (
            grouped.to_dict(orient="records")
        )

    # ========================================================
    # Q4 + PRODUCT
    # ========================================================

    if "quarter" in df.columns and "product_name" in df.columns:

        q4_product = df[
            df["quarter"].astype(str).str.upper() == "Q4"
        ]

        grouped = (
            q4_product
            .groupby("product_name", dropna=False)
            .agg(
                revenue=("net_revenue", "sum"),
                profit=("profit", "sum"),
                orders=("order_id", "nunique")
            )
            .reset_index()
        )

        grouped["profit_margin"] = (
            grouped["profit"] /
            grouped["revenue"]
        )

        grouped = grouped.sort_values(
            "revenue",
            ascending=False
        )

        aggregations["q4_by_product"] = (
            grouped.to_dict(orient="records")
        )

    # ========================================================
    # Q4 + MARKETING SOURCE
    # ========================================================

    if (
        "quarter" in df.columns
        and "marketing_source" in df.columns
    ):

        q4_marketing = df[
            df["quarter"].astype(str).str.upper() == "Q4"
        ]

        grouped = (
            q4_marketing
            .groupby("marketing_source", dropna=False)
            .agg(
                revenue=("net_revenue", "sum"),
                profit=("profit", "sum"),
                orders=("order_id", "nunique")
            )
            .reset_index()
        )

        grouped["profit_margin"] = (
            grouped["profit"] /
            grouped["revenue"]
        )

        grouped = grouped.sort_values(
            "revenue",
            ascending=False
        )

        aggregations["q4_by_marketing_source"] = (
            grouped.to_dict(orient="records")
        )

    # ========================================================
    # Q4 + PAYMENT METHOD
    # ========================================================

    if (
        "quarter" in df.columns
        and "payment_method" in df.columns
    ):

        q4_payment = df[
            df["quarter"].astype(str).str.upper() == "Q4"
        ]

        grouped = (
            q4_payment
            .groupby("payment_method", dropna=False)
            .agg(
                revenue=("net_revenue", "sum"),
                profit=("profit", "sum"),
                orders=("order_id", "nunique")
            )
            .reset_index()
        )

        grouped["profit_margin"] = (
            grouped["profit"] /
            grouped["revenue"]
        )

        aggregations["q4_by_payment_method"] = (
            grouped.to_dict(orient="records")
        )

    # ========================================================
    # MONTH + REGION
    # ========================================================

    if "month" in df.columns and "region" in df.columns:

        grouped = (
            df.groupby(
                ["month", "region"],
                dropna=False
            )
            .agg(
                revenue=("net_revenue", "sum"),
                profit=("profit", "sum"),
                orders=("order_id", "nunique")
            )
            .reset_index()
        )

        grouped["profit_margin"] = (
            grouped["profit"] /
            grouped["revenue"]
        )

        aggregations["month_by_region"] = (
            grouped.to_dict(orient="records")
        )

    # ========================================================
    # QUARTER + REGION
    # ========================================================

    if "quarter" in df.columns and "region" in df.columns:

        grouped = (
            df.groupby(
                ["quarter", "region"],
                dropna=False
            )
            .agg(
                revenue=("net_revenue", "sum"),
                profit=("profit", "sum"),
                orders=("order_id", "nunique")
            )
            .reset_index()
        )

        grouped["profit_margin"] = (
            grouped["profit"] /
            grouped["revenue"]
        )

        aggregations["quarter_by_region"] = (
            grouped.to_dict(orient="records")
        )

    # Q3 vs Q4 regional profit
    q3_q4_region = (
        df[df["quarter"].isin(["Q3", "Q4"])]
        .groupby(["quarter", "region"])
        .agg(
            revenue=("net_revenue", "sum"),
            profit=("profit", "sum")
        )
        .reset_index()
    )

    q3_q4_region["profit_margin"] = (
        q3_q4_region["profit"] /
        q3_q4_region["revenue"]
    )

    context["q3_q4_by_region"] = q3_q4_region.to_dict(orient="records")

        

    # ========================================================
    # FINAL CONTEXT
    # ========================================================

    context["business_aggregations"] = aggregations

    return context

CSV_CONTEXT = build_csv_context(df)

# ============================================================
# 4. COMBINE ALL BUSINESS KNOWLEDGE
# ============================================================

BUSINESS_CONTEXT = {

    "semantic_layer": SEMANTIC_LAYER,

    "validated_analysis": ANALYSIS_RESULTS,

    "csv_context": CSV_CONTEXT
}


BUSINESS_CONTEXT_JSON = json.dumps(
    BUSINESS_CONTEXT,
    indent=2,
    default=str
)


# ============================================================
# 5. SYSTEM INSTRUCTIONS
# ============================================================

SYSTEM_PROMPT = """

You are an AI Business Intelligence Analyst.

You answer questions about an e-commerce business using ONLY
the supplied business context.

The context contains three layers:

1. SEMANTIC LAYER
2. VALIDATED ANALYSIS
3. CSV DATA CONTEXT


============================================================
SEMANTIC LAYER
============================================================

The semantic layer defines the official meaning of business
metrics.

Always respect these definitions.

For example:

Revenue =
SUM(net_revenue)

Profit =
SUM(profit)

Profit margin =
SUM(profit) / SUM(net_revenue)

Orders =
nunique(order_id)

AOV =
SUM(net_revenue) / nunique(order_id)

Return rate =
returned_orders / total_orders

Delivery delay rate =
delayed_orders / total_orders

ROAS =
attributed_revenue / ad_spend


Do NOT invent alternative definitions.

If the user asks for a metric, use its semantic-layer definition.


============================================================
SOURCE PRIORITY
============================================================

Use information in this order:

1. Validated analysis results
2. Semantic layer definitions
3. CSV-derived business context
4. Derived calculations that can be safely calculated from
   the supplied context

Never invent missing numbers.


============================================================
FINANCIAL GOVERNANCE
============================================================

All financial values are in INR.

Always use ₹ for INR values.

Never use $.

Financial opportunity values are:

"modeled opportunity"

They are NOT:

- audited losses
- confirmed leakage
- realized savings
- guaranteed recovery


Do not present scenario estimates as actual financial losses.


============================================================
STATISTICAL GOVERNANCE
============================================================

Statistical association does NOT prove causality.

For example:

If delivery delay is statistically associated with returns,
say:

"Delivery delay and returns are statistically associated."

Do NOT say:

"Delivery delays caused the returns."


============================================================
BUSINESS QUESTIONS
============================================================

You can answer questions about:

- revenue
- profit
- profit margin
- orders
- customers
- AOV
- return rate
- delivery delays
- payment failures
- discounting
- ROAS
- regions
- categories
- products
- marketing
- campaigns
- return reasons
- Q3 vs Q4 performance
- root causes
- statistical evidence
- modeled financial opportunities
- management investigation areas


============================================================
ANSWERING "WHY" QUESTIONS
============================================================

For questions such as:

"Why did profit decline?"

Do not simply return one metric.

Build the answer using validated evidence.

Structure:

1. What changed
2. Important contributing signals
3. Supporting evidence
4. Financial implications
5. Governance/caveat


Do not claim that one factor caused the entire change unless
the supplied evidence explicitly establishes causality.


============================================================
ANSWER STYLE
============================================================

Be concise but analytical.

Use:

- bullet points
- percentages
- ₹ values
- comparisons
- tables when useful

Clearly distinguish:

FACT
VALIDATED EVIDENCE
MODELED OPPORTUNITY
INTERPRETATION
CAVEAT


If the supplied data does not support the question, say:

"Evidence is unavailable in the analyzed data to answer this question."

Do not use LaTeX formatting unless mathematical notation is genuinely required.
Write p-values as plain text, for example:
p-value = 3.39e-13

Do not make up an answer.


============================================================
BUSINESS CONTEXT
============================================================

"""


# ============================================================
# 6. GEMINI AGENT
# ============================================================

def ask_agent(question):

    prompt = (
        SYSTEM_PROMPT
        + "\n"
        + BUSINESS_CONTEXT_JSON
        + "\n\n"
        + "USER QUESTION:\n"
        + question
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text


# ============================================================
# 7. INTERACTIVE MODE
# ============================================================

print("=" * 60)
print("AI REVENUE INTELLIGENCE AGENT")
print("=" * 60)
print("Type 'exit' to stop.")
print()

# while True:

#     question = input("You: ").strip()

#     if question.lower() == "exit":
#         print("Agent stopped.")
#         break

#     if not question:
#         continue

#     try:

#         answer = ask_agent(question)

#         print("\nAgent:")
#         print(answer)
#         print()

#     except Exception as e:

#         print("\nError:", e)
#         print()