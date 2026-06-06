import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Retail Sales BI Dashboard", layout="wide", page_icon="🛒")

st.markdown("""
<style>
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border-left: 4px solid #4361ee;
    }
    .metric-label { font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; }
    .metric-value { font-size: 26px; font-weight: 600; color: #1a1a2e; }
    .metric-sub { font-size: 12px; color: #aaa; margin-top: 2px; }
    .section-header { font-size: 14px; font-weight: 600; color: #444; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("retail_sales_dataset.csv")
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.month
    df["Month Name"] = df["Date"].dt.strftime("%b")
    df["Age Group"] = pd.cut(df["Age"], bins=[17, 25, 35, 45, 60, 100],
                              labels=["18-25", "26-35", "36-45", "46-60", "60+"])
    return df

df = load_data()

# ── Sidebar Filters ──────────────────────────────────────────────
with st.sidebar:
    st.title("🛒 Retail Sales BI")
    st.markdown("---")
    st.markdown("**Filters**")

    categories = ["All"] + sorted(df["Product Category"].unique().tolist())
    selected_cat = st.selectbox("Product Category", categories)

    genders = ["All"] + sorted(df["Gender"].unique().tolist())
    selected_gender = st.selectbox("Gender", genders)

    age_groups = ["All"] + ["18-25", "26-35", "36-45", "46-60", "60+"]
    selected_age = st.selectbox("Age Group", age_groups)

    month_range = st.slider("Month Range", 1, 12, (1, 12))
    st.markdown("---")
    st.caption("Data: 1,000 transactions · 2023")

# ── Apply Filters ────────────────────────────────────────────────
fdf = df.copy()
if selected_cat != "All":
    fdf = fdf[fdf["Product Category"] == selected_cat]
if selected_gender != "All":
    fdf = fdf[fdf["Gender"] == selected_gender]
if selected_age != "All":
    fdf = fdf[fdf["Age Group"] == selected_age]
fdf = fdf[(fdf["Month"] >= month_range[0]) & (fdf["Month"] <= month_range[1])]

# ── KPI Cards ────────────────────────────────────────────────────
st.markdown("## 📊 Sales Overview")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Revenue</div>
        <div class="metric-value">₹{fdf['Total Amount'].sum():,.0f}</div>
        <div class="metric-sub">{len(fdf)} transactions</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color:#f72585;">
        <div class="metric-label">Avg Order Value</div>
        <div class="metric-value">₹{fdf['Total Amount'].mean():,.0f}</div>
        <div class="metric-sub">Per transaction</div>
    </div>""", unsafe_allow_html=True)

with k3:
    top_cat = fdf.groupby("Product Category")["Total Amount"].sum().idxmax() if len(fdf) > 0 else "—"
    st.markdown(f"""
    <div class="metric-card" style="border-left-color:#4cc9f0;">
        <div class="metric-label">Top Category</div>
        <div class="metric-value">{top_cat}</div>
        <div class="metric-sub">By revenue</div>
    </div>""", unsafe_allow_html=True)

with k4:
    top_month = fdf.groupby("Month Name")["Total Amount"].sum().idxmax() if len(fdf) > 0 else "—"
    st.markdown(f"""
    <div class="metric-card" style="border-left-color:#7209b7;">
        <div class="metric-label">Peak Month</div>
        <div class="metric-value">{top_month}</div>
        <div class="metric-sub">Highest revenue</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Monthly Revenue + Category Breakdown ──────────────────
c1, c2 = st.columns([3, 2])

with c1:
    st.markdown('<div class="section-header">Monthly Revenue Trend</div>', unsafe_allow_html=True)
    month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    monthly = fdf.groupby("Month Name")["Total Amount"].sum().reindex(month_order).dropna().reset_index()
    monthly.columns = ["Month", "Revenue"]
    fig = px.bar(monthly, x="Month", y="Revenue",
                 color_discrete_sequence=["#4361ee"],
                 text=monthly["Revenue"].apply(lambda x: f"₹{x/1000:.0f}k"))
    fig.update_traces(textposition="outside", textfont_size=11)
    fig.update_layout(margin=dict(t=10,b=10,l=0,r=0), height=280,
                      plot_bgcolor="white", paper_bgcolor="white",
                      xaxis_title="", yaxis_title="Revenue (₹)",
                      yaxis=dict(showgrid=True, gridcolor="#f0f0f0"))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown('<div class="section-header">Revenue by Category</div>', unsafe_allow_html=True)
    cat_rev = fdf.groupby("Product Category")["Total Amount"].sum().reset_index()
    cat_rev.columns = ["Category", "Revenue"]
    fig2 = px.pie(cat_rev, names="Category", values="Revenue", hole=0.55,
                  color_discrete_sequence=["#4361ee","#f72585","#4cc9f0"])
    fig2.update_traces(textposition="outside", textinfo="label+percent")
    fig2.update_layout(margin=dict(t=10,b=10,l=0,r=0), height=280,
                       showlegend=False, paper_bgcolor="white")
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Age Group + Gender ────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="section-header">Revenue by Age Group</div>', unsafe_allow_html=True)
    age_rev = fdf.groupby("Age Group", observed=True)["Total Amount"].sum().reset_index()
    age_rev.columns = ["Age Group", "Revenue"]
    fig3 = px.bar(age_rev, x="Revenue", y="Age Group", orientation="h",
                  color_discrete_sequence=["#7209b7"],
                  text=age_rev["Revenue"].apply(lambda x: f"₹{x/1000:.0f}k"))
    fig3.update_traces(textposition="outside", textfont_size=11)
    fig3.update_layout(margin=dict(t=10,b=10,l=0,r=0), height=260,
                       plot_bgcolor="white", paper_bgcolor="white",
                       xaxis_title="Revenue (₹)", yaxis_title="",
                       xaxis=dict(showgrid=True, gridcolor="#f0f0f0"))
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.markdown('<div class="section-header">Revenue by Gender</div>', unsafe_allow_html=True)
    gen_rev = fdf.groupby("Gender")["Total Amount"].sum().reset_index()
    gen_rev.columns = ["Gender", "Revenue"]
    fig4 = px.bar(gen_rev, x="Gender", y="Revenue",
                  color="Gender",
                  color_discrete_map={"Male": "#4cc9f0", "Female": "#f72585"},
                  text=gen_rev["Revenue"].apply(lambda x: f"₹{x/1000:.0f}k"))
    fig4.update_traces(textposition="outside", textfont_size=12)
    fig4.update_layout(margin=dict(t=10,b=10,l=0,r=0), height=260,
                       plot_bgcolor="white", paper_bgcolor="white",
                       xaxis_title="", yaxis_title="Revenue (₹)",
                       showlegend=False,
                       yaxis=dict(showgrid=True, gridcolor="#f0f0f0"))
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3: Quantity by Category + Top Customers ──────────────────
c5, c6 = st.columns(2)

with c5:
    st.markdown('<div class="section-header">Quantity Sold by Category</div>', unsafe_allow_html=True)
    qty_cat = fdf.groupby("Product Category")["Quantity"].sum().reset_index()
    qty_cat.columns = ["Category", "Quantity"]
    fig5 = px.bar(qty_cat, x="Category", y="Quantity",
                  color_discrete_sequence=["#4cc9f0"],
                  text="Quantity")
    fig5.update_traces(textposition="outside")
    fig5.update_layout(margin=dict(t=10,b=10,l=0,r=0), height=260,
                       plot_bgcolor="white", paper_bgcolor="white",
                       xaxis_title="", yaxis_title="Units Sold",
                       yaxis=dict(showgrid=True, gridcolor="#f0f0f0"))
    st.plotly_chart(fig5, use_container_width=True)

with c6:
    st.markdown('<div class="section-header">Top 10 Customers by Spend</div>', unsafe_allow_html=True)
    top_cust = fdf.groupby("Customer ID")["Total Amount"].sum().nlargest(10).reset_index()
    top_cust.columns = ["Customer", "Total Spent"]
    top_cust["Total Spent"] = top_cust["Total Spent"].apply(lambda x: f"₹{x:,.0f}")
    st.dataframe(top_cust, use_container_width=True, hide_index=True, height=260)

# ── Raw Data Toggle ──────────────────────────────────────────────
st.markdown("---")
with st.expander("🔍 View Raw Data"):
    st.dataframe(fdf.drop(columns=["Month"]), use_container_width=True)
    st.caption(f"Showing {len(fdf)} records after filters")