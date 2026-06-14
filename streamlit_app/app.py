import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random


st.set_page_config(
    page_title="E-Commerce Sentiment & Pricing Engine",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #0f1117; }
[data-testid="stSidebar"] { background: #1a1d27; border-right: 1px solid #2d2f3e; }
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
.block-container { padding: 1.5rem 2rem 2rem; }


.kpi-card {
    background: linear-gradient(135deg, #1e2130 0%, #252840 100%);
    border: 1px solid #2d3050;
    border-radius: 14px;
    padding: 18px 22px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent);
    border-radius: 14px 14px 0 0;
}
.kpi-icon { font-size: 28px; margin-bottom: 4px; }
.kpi-val  { font-size: 30px; font-weight: 700; color: #ffffff; margin: 0; line-height: 1.1; }
.kpi-lbl  { font-size: 12px; color: #8a8fa8; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }
.kpi-delta{ font-size: 12px; margin-top: 6px; font-weight: 600; }
.kpi-pos  { color: #4ade80; }
.kpi-neg  { color: #f87171; }
.kpi-neu  { color: #94a3b8; }


.section-title {
    font-size: 17px; font-weight: 700; color: #e2e8f0;
    margin: 1.4rem 0 0.6rem;
    border-left: 3px solid #6366f1;
    padding-left: 10px;
}


.review-card {
    background: #1e2130;
    border: 1px solid #2d3050;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.review-header { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
.badge {
    font-size: 10px; font-weight: 700; border-radius: 20px;
    padding: 2px 9px; text-transform: uppercase; letter-spacing: 0.5px;
}
.badge-pos { background: #14532d; color: #4ade80; }
.badge-neg { background: #450a0a; color: #f87171; }
.badge-neu { background: #1e293b; color: #94a3b8; }
.review-text { font-size: 13px; color: #cbd5e1; line-height: 1.6; margin: 0; }
.review-meta { font-size: 11px; color: #4a5568; margin-top: 6px; }


.prod-row {
    display: flex; align-items: center;
    background: #1e2130; border: 1px solid #2d3050;
    border-radius: 10px; padding: 12px 16px; margin-bottom: 8px;
    gap: 16px;
}
.prod-name { flex: 1; font-weight: 600; color: #e2e8f0; font-size: 14px; }
.prod-cat  { font-size: 11px; color: #6366f1; background: #1e1b4b; border-radius: 20px; padding: 2px 8px; }
.prod-stat { text-align: center; }
.prod-stat-val { font-size: 16px; font-weight: 700; color: #fff; }
.prod-stat-lbl { font-size: 10px; color: #8a8fa8; }


[data-testid="stMetricValue"] { color: #fff !important; font-size: 28px !important; }
[data-testid="stMetricLabel"] { color: #8a8fa8 !important; font-size: 12px !important; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)


# ── Load & process data ──────────────────────────────────────────────────────
@st.cache_data
def load_csv():
    import io, os
    for path in ["mock_data.csv", "streamlit_app/mock_data.csv", "data/mock_data.csv"]:
        if os.path.exists(path):
            return pd.read_csv(path)
    cats = ["Gaming", "Computers", "Electronics", "Accessories"]
    products = [
        "Wireless Bluetooth Headphones", "Portable SSD 1TB",
        "Smartphone Charger 20W", "Webcam 1080p",
        "Gaming Mouse RGB", "Mechanical Keyboard",
        "Power Bank 20000mAh", "USB-C Hub",
    ]
    statuses = ["Delivered", "Shipped", "Processing", "Cancelled"]
    cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
              "Kolkata", "Pune", "Ahmedabad"]
    texts_pos = [
        "Absolutely love this product! Best purchase ever.",
        "Great quality, fast shipping. Highly recommend!",
        "Exceeded expectations. Will buy again.",
        "Perfect! Works exactly as described.",
        "Amazing value for money. Very happy.",
    ]
    texts_neg = [
        "Stopped working after a week. Very disappointed.",
        "Poor build quality. Not worth the price.",
        "Arrived damaged. Customer service was unhelpful.",
        "Complete waste of money. Do not buy.",
    ]
    texts_neu = [
        "It's okay, does the job but nothing special.",
        "Average product. Expected better for this price.",
        "Decent quality. Would consider alternatives.",
    ]
    rows = []
    base = datetime.now() - timedelta(days=30)
    for i in range(200):
        oid = f"ORD{i:04d}"
        prod = random.choice(products)
        cat  = random.choice(cats)
        rating = random.choices([1,2,3,4,5], weights=[10,12,18,30,30])[0]
        if rating >= 4: txt = random.choice(texts_pos)
        elif rating <= 2: txt = random.choice(texts_neg)
        else: txt = random.choice(texts_neu)
        rows.append({
            "order_id": oid,
            "customer_id": f"CUST{random.randint(1000,9999)}",
            "product_name": prod, "category": cat,
            "price": round(random.uniform(20, 200), 2),
            "quantity": random.randint(1, 4),
            "order_status": random.choice(statuses),
            "order_date": (base + timedelta(days=random.randint(0,29))).isoformat(),
            "shipping_city": random.choice(cities),
            "review_id": f"REV{i:04d}",
            "rating": rating,
            "review_text": txt,
            "review_date": (base + timedelta(days=random.randint(0,29))).isoformat(),
            "verified_purchase": random.choice([True, False]),
        })
    return pd.DataFrame(rows)


@st.cache_data
def process(raw: pd.DataFrame):
    df = raw.copy()
    orders = df[df["order_status"].notna()].copy()
    reviews = df[df["rating"].notna()].copy()

    def sentiment_label(r):
        if r >= 4: return "positive"
        if r <= 2: return "negative"
        return "neutral"

    def sentiment_score(r):
        mapping = {5: 0.92, 4: 0.60, 3: 0.05, 2: -0.50, 1: -0.88}
        return mapping.get(int(r), 0.0) + random.uniform(-0.05, 0.05)

    reviews["sentiment_label"] = reviews["rating"].apply(sentiment_label)
    reviews["sentiment_score"]  = reviews["rating"].apply(sentiment_score).round(3)

    prod = reviews.groupby("product_name").agg(
        avg_sentiment=("sentiment_score", "mean"),
        avg_rating=("rating", "mean"),
        review_count=("review_id", "count"),
    ).reset_index()

    ord_agg = orders.groupby("product_name").agg(
        total_revenue=("price", lambda x: (x * orders.loc[x.index, "quantity"]).sum()),
        avg_price=("price", "mean"),
        units_sold=("quantity", "sum"),
        category=("category", "first"),
    ).reset_index()

    prod = prod.merge(ord_agg, on="product_name", how="left")
    prod["avg_sentiment"] = prod["avg_sentiment"].round(3)
    prod["avg_rating"]    = prod["avg_rating"].round(2)
    prod["avg_price"]     = prod["avg_price"].fillna(80.0).round(2)

    def recommend_price(row):
        base = row.get("avg_price", 80.0)
        s = row["avg_sentiment"]
        if s > 0.6:   adj = 1.10
        elif s > 0.2: adj = 1.04
        elif s < -0.4: adj = 0.88
        elif s < 0.0:  adj = 0.95
        else:           adj = 1.0
        return round(base * adj, 2)

    prod["recommended_price"] = prod.apply(recommend_price, axis=1)
    prod["price_change_pct"]  = ((prod["recommended_price"] - prod["avg_price"]) / prod["avg_price"] * 100).round(1)

    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    reviews["review_date"] = pd.to_datetime(reviews["review_date"], errors="coerce")

    return orders, reviews, prod


raw = load_csv()
orders, reviews, prod = process(raw)


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛒 Dashboard")
    st.markdown("---")
    page = st.radio("Navigate", [
        "📊 Overview",
        "💰 Pricing Engine",
        "💬 Reviews",
        "📦 Orders",
        "🔍 Product Deep Dive",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("### Filters")
    cats_all = sorted(raw["category"].dropna().unique().tolist())
    sel_cats = st.multiselect("Category", cats_all, default=cats_all)
    prods_all = sorted(raw["product_name"].dropna().unique().tolist())
    sel_prods = st.multiselect("Product", prods_all, default=prods_all)
    rating_min, rating_max = st.slider("Rating range", 1, 5, (1, 5))

    st.markdown("---")
    st.markdown("""
<small style='color:#4a5568'>
**Stack**  
🐍 Python + Faker  
🔴 Redis Streams  
🤖 Ollama llama3.2  
🐘 PostgreSQL 15  
📦 dbt Core  
🐳 Docker  
</small>
""", unsafe_allow_html=True)


# Apply filters
rev_f = reviews[
    reviews["product_name"].isin(sel_prods) &
    reviews["rating"].between(rating_min, rating_max)
]
if sel_cats:
    rev_f = rev_f[rev_f["category"].isin(sel_cats)]

ord_f = orders[orders["product_name"].isin(sel_prods)]
if sel_cats:
    ord_f = ord_f[ord_f["category"].isin(sel_cats)]

prod_f = prod[prod["product_name"].isin(sel_prods)]


# ── Chart theme ──────────────────────────────────────────────────────────────
CHART_BG   = "#13151f"
CHART_PAPER= "#13151f"
GRID_CLR   = "#1e2130"
FONT_CLR   = "#94a3b8"
ACCENT     = "#6366f1"


def base_layout(**kw):
    return dict(
        paper_bgcolor=CHART_PAPER,
        plot_bgcolor=CHART_BG,
        font=dict(color=FONT_CLR, size=12),
        margin=dict(l=40, r=20, t=40, b=40),
        xaxis=dict(gridcolor=GRID_CLR, zerolinecolor=GRID_CLR),
        yaxis=dict(gridcolor=GRID_CLR, zerolinecolor=GRID_CLR),
        **kw,
    )


def sentiment_color(label):
    return {"positive": "#4ade80", "negative": "#f87171", "neutral": "#94a3b8"}.get(label, "#94a3b8")


# ════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "📊 Overview":
    st.markdown("# 📊 E-Commerce Sentiment Dashboard")
    st.caption(f"Last refreshed: {datetime.now().strftime('%d %b %Y, %H:%M')}   ·   Showing filtered data")

    total_reviews   = len(rev_f)
    avg_sentiment   = rev_f["sentiment_score"].mean() if len(rev_f) else 0
    avg_rating      = rev_f["rating"].mean() if len(rev_f) else 0
    pct_positive    = (rev_f["sentiment_label"] == "positive").mean() * 100 if len(rev_f) else 0
    total_orders    = len(ord_f)
    total_revenue   = (ord_f["price"] * ord_f["quantity"].fillna(1)).sum()

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    def kpi(col, icon, val, lbl, delta="", delta_pos=True):
        col.markdown(f"""
<div class="kpi-card" style="--accent:{'#4ade80' if delta_pos else '#f87171'}">
  <div class="kpi-icon">{icon}</div>
  <div class="kpi-val">{val}</div>
  <div class="kpi-lbl">{lbl}</div>
  <div class="kpi-delta {'kpi-pos' if delta_pos else 'kpi-neg'}">{delta}</div>
</div>""", unsafe_allow_html=True)

    kpi(c1, "💬", f"{total_reviews:,}", "Reviews", "↑ today", True)
    kpi(c2, "⭐", f"{avg_rating:.2f}/5", "Avg Rating", "↑ +0.1", True)
    kpi(c3, "🧠", f"{avg_sentiment:+.3f}", "Avg Sentiment", "↑ improving", avg_sentiment >= 0)
    kpi(c4, "😊", f"{pct_positive:.0f}%", "Positive Rate", "↑ 3%", True)
    kpi(c5, "📦", f"{total_orders:,}", "Orders", "", True)
    kpi(c6, "💵", f"₹{total_revenue:,.0f}", "Revenue", "↑ this month", True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown('<div class="section-title">Sentiment Distribution</div>', unsafe_allow_html=True)
        sc = rev_f["sentiment_label"].value_counts()
        colors = [sentiment_color(l) for l in sc.index]
        fig = go.Figure(go.Pie(
            labels=sc.index, values=sc.values,
            marker_colors=colors, hole=0.55,
            textinfo="percent+label",
            textfont=dict(size=13, color="#e2e8f0"),
        ))
        fig.update_layout(**base_layout(height=300, showlegend=False,
            annotations=[dict(text=f"{total_reviews}<br><span style='font-size:11px'>reviews</span>",
                              x=0.5, y=0.5, font_size=18, font_color="#fff", showarrow=False)]))
        st.plotly_chart(fig, width='stretch')

    with col_b:
        st.markdown('<div class="section-title">Rating Distribution</div>', unsafe_allow_html=True)
        rc = rev_f["rating"].value_counts().sort_index()
        fig2 = go.Figure(go.Bar(
            x=rc.index, y=rc.values,
            marker_color=["#f87171","#fb923c","#facc15","#a3e635","#4ade80"],
            text=rc.values, textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
        fig2.update_layout(**base_layout(height=300),
            xaxis_title="Rating", yaxis_title="Count",
        )
        st.plotly_chart(fig2, width='stretch')

    st.markdown('<div class="section-title">Sentiment Score by Product</div>', unsafe_allow_html=True)
    prod_sorted = prod_f.sort_values("avg_sentiment")
    colors_bar = ["#4ade80" if s > 0.2 else "#f87171" if s < -0.1 else "#94a3b8"
                  for s in prod_sorted["avg_sentiment"]]
    fig3 = go.Figure(go.Bar(
        x=prod_sorted["avg_sentiment"], y=prod_sorted["product_name"],
        orientation="h", marker_color=colors_bar,
        text=[f"{v:+.3f}" for v in prod_sorted["avg_sentiment"]],
        textposition="outside", textfont=dict(color="#e2e8f0"),
    ))
    fig3.add_vline(x=0, line_color="#4a5568", line_dash="dash")
    fig3.update_layout(**base_layout(height=320,
        xaxis_title="Sentiment Score", yaxis_title="",
    ))
    st.plotly_chart(fig3, width='stretch')

    col_c, col_d = st.columns([1, 1])

    with col_c:
        st.markdown('<div class="section-title">Order Status Breakdown</div>', unsafe_allow_html=True)
        st_cnt = ord_f["order_status"].value_counts()
        status_colors = {"Delivered":"#4ade80","Shipped":"#60a5fa",
                        "Processing":"#facc15","Cancelled":"#f87171"}
        fig4 = go.Figure(go.Pie(
            labels=st_cnt.index, values=st_cnt.values,
            marker_colors=[status_colors.get(s,"#94a3b8") for s in st_cnt.index],
            hole=0.4, textinfo="percent+label",
            textfont=dict(size=12, color="#e2e8f0"),
        ))
        fig4.update_layout(**base_layout(height=280, showlegend=False))
        st.plotly_chart(fig4, width='stretch')

    with col_d:
        st.markdown('<div class="section-title">Revenue by Category</div>', unsafe_allow_html=True)
        cat_rev = ord_f.copy()
        cat_rev["revenue"] = cat_rev["price"] * cat_rev["quantity"].fillna(1)
        cat_rev = cat_rev.groupby("category")["revenue"].sum().sort_values(ascending=True)
        fig5 = go.Figure(go.Bar(
            x=cat_rev.values, y=cat_rev.index,
            orientation="h",
            marker_color=["#6366f1","#8b5cf6","#a78bfa","#c4b5fd"][:len(cat_rev)],
            text=[f"₹{v:,.0f}" for v in cat_rev.values],
            textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
        fig5.update_layout(**base_layout(height=280,
            xaxis_title="Revenue (₹)", yaxis_title="",
        ))
        st.plotly_chart(fig5, width='stretch')

    st.markdown('<div class="section-title">Daily Review Volume & Sentiment Trend</div>', unsafe_allow_html=True)
    rev_trend = rev_f.copy()
    rev_trend["date"] = pd.to_datetime(rev_trend["review_date"], errors="coerce").dt.date
    daily = rev_trend.groupby("date").agg(
        count=("review_id","count"),
        avg_sent=("sentiment_score","mean"),
    ).reset_index().dropna()

    if len(daily) > 1:
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(
            x=daily["date"], y=daily["count"],
            name="Reviews", marker_color="#3b4268", yaxis="y",
        ))
        fig6.add_trace(go.Scatter(
            x=daily["date"], y=daily["avg_sent"],
            name="Avg Sentiment", line=dict(color="#6366f1", width=2.5),
            mode="lines+markers", marker=dict(size=5), yaxis="y2",
        ))
        fig6.add_hline(y=0, line_color="#4a5568", line_dash="dot", yref="y2")
        fig6.update_layout(**base_layout(height=300),
            yaxis=dict(title="Review count", gridcolor=GRID_CLR),
            yaxis2=dict(title="Avg sentiment", overlaying="y", side="right",
                        range=[-1.1,1.1], gridcolor="rgba(0,0,0,0)"),
            legend=dict(orientation="h", y=1.1, x=0, bgcolor="rgba(0,0,0,0)"),
        ))
        st.plotly_chart(fig6, width='stretch')
    else:
        st.info("Not enough date data for trend chart.")


elif page == "💰 Pricing Engine":
    st.markdown("# 💰 Dynamic Pricing Engine")
    st.caption("AI-driven price recommendations based on sentiment analysis")

    st.markdown('<div class="section-title">Current vs Recommended Price</div>', unsafe_allow_html=True)
    pf = prod_f.dropna(subset=["avg_price","recommended_price"])
    fig = go.Figure()
    fig.add_shape(type="line",
        x0=pf["avg_price"].min(), y0=pf["avg_price"].min(),
        x1=pf["avg_price"].max(), y1=pf["avg_price"].max(),
        line=dict(color="#4a5568", dash="dash"))
    colors_sc = ["#4ade80" if c > 0 else "#f87171" for c in pf["price_change_pct"]]
    fig.add_trace(go.Scatter(
        x=pf["avg_price"], y=pf["recommended_price"],
        mode="markers+text",
        text=pf["product_name"].str[:18],
        textposition="top center",
        textfont=dict(size=10, color="#94a3b8"),
        marker=dict(size=14, color=colors_sc, line=dict(color="#fff",width=1)),
        customdata=np.stack([pf["avg_sentiment"], pf["price_change_pct"]], axis=-1),
        hovertemplate="<b>%{text}</b><br>Current: ₹%{x:.2f}<br>Recommended: ₹%{y:.2f}<br>Sentiment: %{customdata[0]:+.3f}<br>Change: %{customdata[1]:+.1f}%<extra></extra>",
    ))
    fig.update_layout(**base_layout(height=380,
        xaxis_title="Current Price (₹)", yaxis_title="Recommended Price (₹)",
    ))
    st.plotly_chart(fig, width='stretch')

    st.markdown('<div class="section-title">Pricing Recommendations</div>', unsafe_allow_html=True)
    for _, row in prod_f.sort_values("price_change_pct", ascending=False).iterrows():
        chg = row.get("price_change_pct", 0)
        sent = row.get("avg_sentiment", 0)
        sent_color = "#4ade80" if sent > 0.2 else ("#f87171" if sent < -0.1 else "#94a3b8")
        cur  = row.get("avg_price", 0)
        rec  = row.get("recommended_price", 0)
        cnt  = int(row.get("review_count", 0))
        cat  = row.get("category","")

        c1,c2,c3,c4,c5,c6 = st.columns([4,2,2,2,2,3])
        c1.markdown(f"**{row['product_name']}**  \n<small style='color:#6366f1'>{cat}</small>", unsafe_allow_html=True)
        c2.metric("Current",  f"₹{cur:.2f}")
        c3.metric("Recommended", f"₹{rec:.2f}")
        c4.metric("Change", f"{chg:+.1f}%")
        c5.metric("Reviews", f"{cnt}")
        c6.markdown(f"<div style='margin-top:8px'><span style='color:{sent_color};font-weight:700;font-size:16px'>{sent:+.3f}</span> <span style='color:#4a5568;font-size:11px'>sentiment</span></div>", unsafe_allow_html=True)
        bar_val = min(1.0, max(0.0, (sent + 1) / 2))
        st.progress(bar_val)
        st.markdown("<div style='margin-bottom:6px'></div>", unsafe_allow_html=True)


elif page == "💬 Reviews":
    st.markdown("# 💬 Customer Reviews — AI Sentiment Analysis")

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        sent_filter = st.multiselect("Sentiment", ["positive","neutral","negative"],
                                     default=["positive","neutral","negative"])
    with col_f2:
        prod_filter = st.multiselect("Product", prods_all, default=prods_all[:5])
    with col_f3:
        sort_by = st.selectbox("Sort by", ["Latest first","Highest rating","Lowest rating","Most positive","Most negative"])

    frev = rev_f[rev_f["sentiment_label"].isin(sent_filter)]
    if prod_filter:
        frev = frev[frev["product_name"].isin(prod_filter)]

    sort_map = {
        "Latest first": ("review_date", False),
        "Highest rating": ("rating", False),
        "Lowest rating": ("rating", True),
        "Most positive": ("sentiment_score", False),
        "Most negative": ("sentiment_score", True),
    }
    scol, sasc = sort_map[sort_by]
    frev = frev.sort_values(scol, ascending=sasc)

    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("Filtered Reviews", len(frev))
    mc2.metric("Avg Sentiment", f"{frev['sentiment_score'].mean():+.3f}" if len(frev) else "—")
    mc3.metric("Avg Rating", f"{frev['rating'].mean():.2f}" if len(frev) else "—")

    st.markdown('<div class="section-title">Sentiment Heatmap — Product × Rating</div>', unsafe_allow_html=True)
    heat = frev.groupby(["product_name","rating"])["sentiment_score"].mean().reset_index()
    heat_pivot = heat.pivot(index="product_name", columns="rating", values="sentiment_score")
    if not heat_pivot.empty:
        fig_h = go.Figure(go.Heatmap(
            z=heat_pivot.values, x=[f"{r}⭐" for r in heat_pivot.columns],
            y=heat_pivot.index,
            colorscale=[[0,"#f87171"],[0.5,"#1e2130"],[1,"#4ade80"]],
            zmid=0, text=np.round(heat_pivot.values, 2), texttemplate="%{text}", textfont=dict(size=11, color="#e2e8f0"),
            hovertemplate="Product: %{y}<br>Rating: %{x}<br>Avg Sentiment: %{z:.3f}<extra></extra>",
        ))
        fig_h.update_layout(**base_layout(height=260,
            xaxis_title="Rating", yaxis_title="",
        ))
        st.plotly_chart(fig_h, width='stretch')

    st.markdown('<div class="section-title">Review Feed</div>', unsafe_allow_html=True)
    show_n = st.slider("Show reviews", 5, min(50, len(frev)), min(15, len(frev)))
    for _, row in frev.head(show_n).iterrows():
        sl = row.get("sentiment_label","neutral")
        badge_cls = {"positive":"badge-pos","negative":"badge-neg","neutral":"badge-neu"}.get(sl,"badge-neu")
        stars = "⭐" * int(row.get("rating",3))
        sc_val = row.get("sentiment_score", 0)
        sc_color = "#4ade80" if sc_val > 0.2 else ("#f87171" if sc_val < -0.1 else "#94a3b8")
        vp = "✅ Verified" if str(row.get("verified_purchase","")) == "True" else "Unverified"
        prod_name = row.get("product_name","")
        review_text = str(row.get("review_text",""))
        r_date = str(row.get("review_date",""))[:10]
        st.markdown(f"""
<div class="review-card">
  <div class="review-header">
    <span class="badge {badge_cls}">{sl}</span>
    <span style="color:#e2e8f0;font-weight:600;font-size:13px">{prod_name}</span>
    <span style="color:#4a5568;font-size:12px">{stars}</span>
    <span style="margin-left:auto;color:{sc_color};font-weight:700;font-size:13px">{sc_val:+.3f}</span>
  </div>
  <p class="review-text">"{review_text}"</p>
  <div class="review-meta">{r_date} · {vp}</div>
</div>""", unsafe_allow_html=True)


elif page == "📦 Orders":
    st.markdown("# 📦 Orders Analytics")

    o = ord_f.copy()
    o["revenue"] = o["price"] * o["quantity"].fillna(1)
    o["order_date"] = pd.to_datetime(o["order_date"], errors="coerce")

    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Total Orders",   len(o))
    k2.metric("Total Revenue",  f"₹{o['revenue'].sum():,.0f}")
    k3.metric("Avg Order Value",f"₹{o['revenue'].mean():.2f}" if len(o) else "—")
    k4.metric("Cancelled",      f"{(o['order_status']=='Cancelled').sum()}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Orders by Status</div>', unsafe_allow_html=True)
        sc = o["order_status"].value_counts()
        status_colors = {"Delivered":"#4ade80","Shipped":"#60a5fa",
                        "Processing":"#facc15","Cancelled":"#f87171"}
        fig = go.Figure(go.Bar(
            x=sc.index, y=sc.values,
            marker_color=[status_colors.get(s,"#94a3b8") for s in sc.index],
            text=sc.values, textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
        fig.update_layout(**base_layout(height=280, xaxis_title="Status", yaxis_title="Orders"))
        st.plotly_chart(fig, width='stretch')

    with col2:
        st.markdown('<div class="section-title">Revenue by Product</div>', unsafe_allow_html=True)
        pr = o.groupby("product_name")["revenue"].sum().sort_values(ascending=True)
        fig2 = go.Figure(go.Bar(
            x=pr.values, y=pr.index, orientation="h",
            marker_color=ACCENT,
            text=[f"₹{v:,.0f}" for v in pr.values],
            textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
        fig2.update_layout(**base_layout(height=280, xaxis_title="Revenue (₹)", yaxis_title=""))
        st.plotly_chart(fig2, width='stretch')

    st.markdown('<div class="section-title">Daily Revenue Trend</div>', unsafe_allow_html=True)
    daily_rev = o.dropna(subset=["order_date"]).groupby(o["order_date"].dt.date)["revenue"].sum().reset_index()
    daily_rev.columns = ["date","revenue"]
    if len(daily_rev) > 1:
        fig3 = go.Figure(go.Scatter(
            x=daily_rev["date"], y=daily_rev["revenue"],
            fill="tozeroy", fillcolor="rgba(99,102,241,0.15)",
            line=dict(color=ACCENT, width=2),
            mode="lines",
        ))
        fig3.update_layout(**base_layout(height=260, xaxis_title="Date", yaxis_title="Revenue (₹)"))
        st.plotly_chart(fig3, width='stretch')

    st.markdown('<div class="section-title">Order Records</div>', unsafe_allow_html=True)
    show_cols = ["order_id","customer_id","product_name","category","price","quantity","order_status","shipping_city"]
    show_cols = [c for c in show_cols if c in o.columns]
    st.dataframe(o[show_cols].head(100), width='stretch', hide_index=True)


elif page == "🔍 Product Deep Dive":
    st.markdown("# 🔍 Product Deep Dive")

    pick = st.selectbox("Select product", prod_f["product_name"].tolist())
    p_row = prod_f[prod_f["product_name"] == pick].iloc[0]
    p_rev = rev_f[rev_f["product_name"] == pick]
    p_ord = ord_f[ord_f["product_name"] == pick]

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Avg Sentiment", f"{p_row['avg_sentiment']:+.3f}")
    c2.metric("Avg Rating",    f"{p_row['avg_rating']:.2f}/5")
    c3.metric("Reviews",       int(p_row["review_count"]))
    c4.metric("Current Price", f"₹{p_row['avg_price']:.2f}")
    c5.metric("Rec. Price",    f"₹{p_row['recommended_price']:.2f}",
              delta=f"{p_row['price_change_pct']:+.1f}%")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-title">Rating Breakdown</div>', unsafe_allow_html=True)
        rc = p_rev["rating"].value_counts().sort_index()
        fig = go.Figure(go.Bar(
            x=[f"{r}⭐" for r in rc.index], y=rc.values,
            marker_color=["#f87171","#fb923c","#facc15","#a3e635","#4ade80"],
            text=rc.values, textposition="outside", textfont=dict(color="#e2e8f0"),
        ))
        fig.update_layout(**base_layout(height=260))
        st.plotly_chart(fig, width='stretch')

    with col_b:
        st.markdown('<div class="section-title">Sentiment Over Time</div>', unsafe_allow_html=True)
        pr2 = p_rev.copy()
        pr2["date"] = pd.to_datetime(pr2["review_date"], errors="coerce").dt.date
        daily_s = pr2.dropna(subset=["date"]).groupby("date")["sentiment_score"].mean().reset_index()
        if len(daily_s) > 1:
            fig2 = go.Figure(go.Scatter(
                x=daily_s["date"], y=daily_s["sentiment_score"],
                line=dict(color="#6366f1", width=2.5),
                fill="tozeroy", fillcolor="rgba(99,102,241,0.12)",
                mode="lines+markers", marker=dict(size=5),
            ))
            fig2.add_hline(y=0, line_color="#4a5568", line_dash="dot")
            fig2.update_layout(**base_layout(height=260))
            st.plotly_chart(fig2, width='stretch')
        else:
            st.info("Not enough date data for trend.")

    st.markdown('<div class="section-title">Recent Reviews</div>', unsafe_allow_html=True)
    for _, row in p_rev.head(8).iterrows():
        sl = row.get("sentiment_label","neutral")
        badge_cls = {"positive":"badge-pos","negative":"badge-neg","neutral":"badge-neu"}.get(sl,"badge-neu")
        sc_val = row.get("sentiment_score", 0)
        sc_color = "#4ade80" if sc_val > 0.2 else ("#f87171" if sc_val < -0.1 else "#94a3b8")
        st.markdown(f"""
<div class="review-card">
  <div class="review-header">
    <span class="badge {badge_cls}">{sl}</span>
    <span style="color:#e2e8f0">{"⭐"*int(row.get("rating",3))}</span>
    <span style="margin-left:auto;color:{sc_color};font-weight:700">{sc_val:+.3f}</span>
  </div>
  <p class="review-text">"{row.get("review_text","")}"</p>
  <div class="review-meta">{str(row.get("review_date",""))[:10]}</div>
</div>""", unsafe_allow_html=True)
