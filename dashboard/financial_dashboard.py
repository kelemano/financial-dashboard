import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Financial Dashboard | kelemano",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# THEME CONFIGURATION - PREMIUM DARK
# =============================================================================

COLORS = {
    'bg_primary': '#0E1117',
    'bg_secondary': '#262730',
    'bg_tertiary': '#1E1E2E',
    'text_primary': '#FAFAFA',
    'text_secondary': '#B4B7C9',
    'text_muted': '#6B7280',
    'accent_blue': '#3B82F6',
    'accent_blue_light': '#60A5FA',
    'accent_blue_dark': '#2563EB',
    'success': '#10B981',
    'success_light': '#34D399',
    'success_dark': '#059669',
    'warning': '#F59E0B',
    'warning_light': '#FBBF24',
    'danger': '#EF4444',
    'danger_light': '#F87171',
    'danger_dark': '#DC2626',
    'border': 'rgba(75, 85, 99, 0.3)',
    'border_light': 'rgba(75, 85, 99, 0.2)',
    'hover': 'rgba(59, 130, 246, 0.08)',
    'grid': 'rgba(75, 85, 99, 0.2)',
    'chart_bg': 'rgba(38, 39, 48, 0.5)',
}

# =============================================================================
# CUSTOM CSS
# =============================================================================

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    * {{ box-sizing: border-box; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }}
    .main {{ background-color: {COLORS['bg_primary']}; padding: 1rem 2rem; }}
    [data-testid="stSidebar"] {{ background-color: {COLORS['bg_secondary']}; border-right: 1px solid {COLORS['border']}; padding: 2rem 1rem; }}
    h1 {{ color: {COLORS['text_primary']}; font-weight: 800; font-size: 2.5rem !important; margin-bottom: 0.5rem; }}
    .subtitle {{ color: {COLORS['text_secondary']}; font-size: 1rem; margin-bottom: 1.5rem; }}
    .metric-card {{ background: linear-gradient(135deg, rgba(38,39,48,0.88) 0%, rgba(30,30,46,0.95) 100%); border: 1px solid {COLORS['border']}; border-radius: 16px; padding: 20px; transition: transform 0.28s cubic-bezier(.4,0,.2,1), box-shadow 0.28s; position: relative; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; min-height: 220px; height: 220px; max-height: 220px; }}
    @media (min-width: 1600px) {{ .metric-card {{ min-height: 240px; height: 240px; max-height: 240px; padding: 24px; }} }}
    .metric-top {{ display:flex; align-items:center; gap:14px; }}
    .metric-icon-box {{ width:56px; height:56px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:1.6rem; font-weight:700; color:white; font-family:'JetBrains Mono', monospace; transition: transform 0.28s ease, box-shadow 0.28s ease; flex:0 0 auto; }}
    .metric-body {{ margin-top:10px; flex:1 1 auto; display:flex; flex-direction:column; justify-content:flex-start; }}
    .metric-label {{ color: {COLORS['text_secondary']}; font-size:0.78rem; font-weight:600; text-transform:uppercase; letter-spacing:0.1em; }}
    .metric-value {{ color:{COLORS['text_primary']}; font-size:2.15rem; font-weight:800; font-family:'JetBrains Mono', monospace; line-height:1; margin-top:10px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
    .metric-footer {{ margin-top:12px; display:flex; align-items:center; gap:10px; justify-content:flex-start; flex:0 0 auto; }}
    .metric-delta {{ color:{COLORS['text_muted']}; font-size:0.95rem; font-weight:600; display:flex; align-items:center; gap:8px; }}
    .metric-delta.positive {{ color:{COLORS['success']}; }} .metric-delta.negative {{ color:{COLORS['danger']}; }} .metric-delta.neutral {{ color:{COLORS['warning']}; }}
    .metric-card:hover {{ transform: translateY(-6px); box-shadow: 0 16px 32px rgba(0,0,0,0.45); }}
    .metric-card:hover .metric-icon-box {{ transform: scale(1.12) rotate(5deg); box-shadow: 0 6px 18px rgba(59,130,246,0.28); }}
    .metric-card::before {{ display:none; }}
    .section-header {{ display:flex; align-items:center; gap:12px; margin-top:3.5rem; margin-bottom:1.5rem; padding-bottom:0.5rem; border-bottom:1px solid {COLORS['border']}; }}
    .section-dot {{ width:10px; height:10px; border-radius:50%; background: linear-gradient(180deg, {COLORS['accent_blue']} 0%, {COLORS['success']} 100%); box-shadow: 0 4px 10px rgba(59,130,246,0.12); flex:0 0 auto; }}
    .section-header h2 {{ margin:0; font-size:1.5rem; font-weight:700; color:{COLORS['text_primary']}; }}
    .chart-container {{ background-color:{COLORS['bg_secondary']}; border:1px solid {COLORS['border']}; border-radius:12px; padding:14px; }}
    .dataframe thead tr th {{ background-color:{COLORS['bg_tertiary']} !important; color:{COLORS['text_primary']} !important; }}
    @media (max-width:900px) {{ .metric-card {{ height:auto; min-height:180px; }} .metric-icon-box {{ width:48px; height:48px; }} .metric-value {{ font-size:1.75rem; }} }}
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA LOADING
# =============================================================================

@st.cache_data(show_spinner=False)
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processed_dir = os.path.join(base_dir, 'data', 'processed_data')
    transactions = pd.read_csv(os.path.join(processed_dir, 'transactions_processed.csv'))
    budget = pd.read_csv(os.path.join(processed_dir, 'budget_analysis.csv'))
    invoices = pd.read_csv(os.path.join(processed_dir, 'invoices_summary.csv'))
    transactions['Date'] = pd.to_datetime(transactions['Date'])
    transactions['Month'] = pd.to_datetime(transactions['Month'])
    budget['Month'] = pd.to_datetime(budget['Month'])
    invoices['Date'] = pd.to_datetime(invoices['Date'])
    return transactions, budget, invoices

# =============================================================================
# HELPERS
# =============================================================================

def format_currency(value):
    if pd.isna(value):
        return "€0"
    if value >= 1_000_000:
        return f"€{value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"€{value/1_000:.1f}K"
    else:
        return f"€{value:,.0f}"

def format_percentage(value):
    try:
        return f"{value:.2f}%"
    except:
        return str(value)

def get_trend_indicator(value, threshold=0):
    if value > threshold:
        return "↗", "positive"
    elif value < threshold:
        return "↘", "negative"
    else:
        return "→", "neutral"

# =============================================================================
# LOAD DATA
# =============================================================================

try:
    with st.spinner('Loading financial data...'):
        transactions_df, budget_df, invoices_df = load_data()
except FileNotFoundError:
    st.error("⚠Processed data files not found! Please run data_processing.py first.")
    st.stop()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.markdown("### Dashboard Controls")
    st.markdown("---")
    min_date = transactions_df['Date'].min().date()
    max_date = transactions_df['Date'].max().date()
    date_range = st.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    st.markdown("---")
    departments = ['All Departments'] + sorted(transactions_df['Department'].unique().tolist())
    selected_department = st.selectbox("Department", departments)
    st.markdown("---")
    categories = ['All Categories'] + sorted(transactions_df['Category'].unique().tolist())
    selected_category = st.selectbox("Category", categories)
    st.markdown("---")
    st.metric("Total Transactions", f"{len(transactions_df):,}")
    st.metric("Total Value", format_currency(transactions_df['Revenue'].sum()))

# =============================================================================
# FILTERS APPLY
# =============================================================================

filtered_df = transactions_df.copy()
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    filtered_df = filtered_df[(filtered_df['Date'].dt.date >= date_range[0]) & (filtered_df['Date'].dt.date <= date_range[1])]
if selected_department != 'All Departments':
    filtered_df = filtered_df[filtered_df['Department'] == selected_department]
if selected_category != 'All Categories':
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

# =============================================================================
# HEADER
# =============================================================================

st.markdown("# Financial Analytics Dashboard")
st.markdown(f"<p class='subtitle'>Comprehensive financial performance overview • Period: {date_range[0].strftime('%B %d, %Y')} - {date_range[1].strftime('%B %d, %Y')}</p>", unsafe_allow_html=True)

# =============================================================================
# KPI ROW
# =============================================================================

st.markdown("<div class='section-header'><div class='section-dot'></div><h2>Key Performance Indicators</h2></div>", unsafe_allow_html=True)

total_revenue = filtered_df['Revenue'].sum()
total_cost = filtered_df['Cost'].sum()
total_profit = filtered_df['Profit'].sum()
avg_margin = filtered_df['Margin_%'].mean()

revenue_change = 12.5
profit_change = 8.3
cost_change = 5.2
margin_change = 2.1

col1, col2, col3, col4 = st.columns(4)

def render_metric(col, letter, letter_bg, label, value, delta_html):
    col.markdown(f"""
        <div class="metric-card">
            <div class="metric-top">
                <div class="metric-icon-box" style="background: {letter_bg};">{letter}</div>
                <div style="flex:1 1 auto;"></div>
            </div>
            <div class="metric-body">
                <span class="metric-label">{label}</span>
                <span class="metric-value">{value}</span>
            </div>
            <div class="metric-footer">
                {delta_html}
            </div>
        </div>
    """, unsafe_allow_html=True)

render_metric(col1, "R", f"linear-gradient(135deg, {COLORS['accent_blue']}, {COLORS['accent_blue_light']})",
              "Total Revenue", format_currency(total_revenue),
              f"<div class='metric-delta positive'><span style='font-size:1.2rem;'>↗</span> {revenue_change:.1f}% vs prev period</div>")

render_metric(col2, "P", f"linear-gradient(135deg, {COLORS['success']}, {COLORS['success_dark']})",
              "Total Profit", format_currency(total_profit),
              f"<div class='metric-delta positive'><span style='font-size:1.2rem;'>↗</span> {profit_change:.1f}% vs prev period</div>")

render_metric(col3, "C", f"linear-gradient(135deg, {COLORS['danger']}, {COLORS['danger_dark']})",
              "Total Cost", format_currency(total_cost),
              f"<div class='metric-delta neutral'>{format_percentage(total_cost/total_revenue*100)} of revenue</div>")

margin_status = "positive" if avg_margin >= 70 else "negative"
render_metric(col4, "M", f"linear-gradient(135deg, {COLORS['warning']}, {COLORS['warning_light']})",
              "Average Margin", format_percentage(avg_margin),
              f"<div class='metric-delta {margin_status}'>Target: 70% <span style='font-size:1.2rem;'>↗</span></div>")

# =============================================================================
# Trends chart
# =============================================================================

st.markdown("<div class='section-header'><div class='section-dot'></div><h2>Revenue & Profit Trends</h2></div>", unsafe_allow_html=True)

monthly_data = filtered_df.groupby(filtered_df['Date'].dt.to_period('M')).agg({'Revenue':'sum','Cost':'sum','Profit':'sum'}).reset_index()
monthly_data['Date'] = monthly_data['Date'].astype(str)

fig_trends = go.Figure()
fig_trends.add_trace(go.Scatter(x=monthly_data['Date'], y=monthly_data['Revenue'], name='Revenue',
                                line=dict(color=COLORS['accent_blue'], width=3), mode='lines+markers',
                                marker=dict(size=6, line=dict(width=2, color=COLORS['bg_primary'])),
                                hovertemplate='<b>Revenue</b><br>%{y:,.0f}<extra></extra>'))
fig_trends.add_trace(go.Scatter(x=monthly_data['Date'], y=monthly_data['Profit'], name='Profit',
                                line=dict(color=COLORS['success'], width=3), mode='lines+markers',
                                marker=dict(size=6, line=dict(width=2, color=COLORS['bg_primary'])),
                                hovertemplate='<b>Profit</b><br>%{y:,.0f}<extra></extra>'))
fig_trends.add_trace(go.Scatter(x=monthly_data['Date'], y=monthly_data['Cost'], name='Cost',
                                line=dict(color=COLORS['danger'], width=3), mode='lines+markers',
                                marker=dict(size=6, line=dict(width=2, color=COLORS['bg_primary'])),
                                hovertemplate='<b>Cost</b><br>%{y:,.0f}<extra></extra>'))

fig_trends.update_layout(height=450, paper_bgcolor=COLORS['chart_bg'], plot_bgcolor=COLORS['chart_bg'],
                         font=dict(family='Inter', size=12, color=COLORS['text_primary']),
                         xaxis=dict(title="", gridcolor=COLORS['grid'], showgrid=True, zeroline=False, color=COLORS['text_primary']),
                         yaxis=dict(title="", gridcolor=COLORS['grid'], showgrid=True, zeroline=False, color=COLORS['text_primary'], tickformat=',.0f'),
                         hovermode='x unified', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                         margin=dict(l=60, r=40, t=60, b=60))
st.plotly_chart(fig_trends, use_container_width=True)

# =============================================================================
# Departments charts
# =============================================================================

st.markdown("<div class='section-header'><div class='section-dot'></div><h2>Department Performance</h2></div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    dept_revenue = filtered_df.groupby('Department')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False)
    fig_dept_revenue = go.Figure(data=[go.Bar(x=dept_revenue['Department'], y=dept_revenue['Revenue'],
                                              marker=dict(color=COLORS['accent_blue'], line=dict(color=COLORS['accent_blue_dark'], width=1)),
                                              text=dept_revenue['Revenue'].apply(lambda x: format_currency(x)),
                                              textposition='outside',
                                              hovertemplate='<b>%{x}</b><br>Revenue: %{y:,.0f}<extra></extra>')])
    fig_dept_revenue.update_layout(title=dict(text="Revenue by Department", font=dict(size=16, color=COLORS['text_primary'])),
                                   height=380, paper_bgcolor=COLORS['chart_bg'], plot_bgcolor=COLORS['chart_bg'],
                                   xaxis=dict(gridcolor=COLORS['grid'], color=COLORS['text_primary']), yaxis=dict(gridcolor=COLORS['grid'], color=COLORS['text_primary']), margin=dict(l=60, r=20, t=60, b=60))
    st.plotly_chart(fig_dept_revenue, use_container_width=True)

with col2:
    dept_margin = filtered_df.groupby('Department')['Margin_%'].mean().reset_index().sort_values('Margin_%', ascending=False)
    colors_margin = [COLORS['success'] if m >= 70 else COLORS['warning'] if m >= 60 else COLORS['danger'] for m in dept_margin['Margin_%']]
    fig_dept_margin = go.Figure(data=[go.Bar(x=dept_margin['Department'], y=dept_margin['Margin_%'],
                                             marker=dict(color=colors_margin, line=dict(color=COLORS['bg_primary'], width=1.5)),
                                             text=dept_margin['Margin_%'].apply(lambda x: f"{x:.1f}%"),
                                             textposition='outside',
                                             hovertemplate='<b>%{x}</b><br>Margin: %{y:.2f}%<extra></extra>')])
    fig_dept_margin.add_hline(y=70, line_dash="dash", line_color=COLORS['text_muted'], line_width=2)
    fig_dept_margin.update_layout(title=dict(text="Average Margin by Department", font=dict(size=16, color=COLORS['text_primary'])),
                                  height=380, paper_bgcolor=COLORS['chart_bg'], plot_bgcolor=COLORS['chart_bg'],
                                  margin=dict(l=60, r=20, t=60, b=60))
    st.plotly_chart(fig_dept_margin, use_container_width=True)

# =============================================================================
# Category breakdown
# =============================================================================

st.markdown("<div class='section-header'><div class='section-dot'></div><h2>Category Breakdown</h2></div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    category_revenue = filtered_df.groupby('Category')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False)
    colors_cat = [COLORS['accent_blue'], COLORS['success'], COLORS['warning'], COLORS['danger'], COLORS['accent_blue_light'], COLORS['success_light']]
    fig_cat_donut = go.Figure(data=[go.Pie(labels=category_revenue['Category'], values=category_revenue['Revenue'], hole=0.5,
                                           marker=dict(colors=colors_cat[:len(category_revenue)], line=dict(color=COLORS['bg_primary'], width=2)),
                                           textfont=dict(size=12, family='Inter', color=COLORS['text_primary']),
                                           hovertemplate='<b>%{label}</b><br>Revenue: %{value:,.0f}<br>Share: %{percent}<extra></extra>')])
    fig_cat_donut.add_annotation(text=f"<b>{format_currency(category_revenue['Revenue'].sum())}</b><br><span style='font-size:12px'>Total</span>", x=0.5, y=0.5, showarrow=False, font=dict(size=18, family='JetBrains Mono', color=COLORS['text_primary']))
    fig_cat_donut.update_layout(height=380, paper_bgcolor=COLORS['chart_bg'], plot_bgcolor=COLORS['chart_bg'], margin=dict(l=20, r=120, t=60, b=20))
    st.plotly_chart(fig_cat_donut, use_container_width=True)

with col2:
    category_profit = filtered_df.groupby('Category')['Profit'].sum().reset_index().sort_values('Profit', ascending=True)
    max_profit = max(category_profit['Profit'].max(), 1)
    colors_profit = [f'rgba({int(16 + (239-16)*(1-p/max_profit))}, {int(185 + (68-185)*(1-p/max_profit))}, {int(129 + (68-129)*(1-p/max_profit))}, 0.8)' for p in category_profit['Profit']]
    fig_cat_profit = go.Figure(data=[go.Bar(y=category_profit['Category'], x=category_profit['Profit'], orientation='h', marker=dict(color=colors_profit, line=dict(color=COLORS['bg_primary'], width=1.5)), text=category_profit['Profit'].apply(lambda x: format_currency(x)), textposition='outside', hovertemplate='<b>%{y}</b><br>Profit: %{x:,.0f}<extra></extra>')])
    fig_cat_profit.update_layout(height=380, paper_bgcolor=COLORS['chart_bg'], plot_bgcolor=COLORS['chart_bg'], margin=dict(l=120, r=80, t=60, b=40))
    st.plotly_chart(fig_cat_profit, use_container_width=True)

# =============================================================================
# Budget performance
# =============================================================================

st.markdown("<div class='section-header'><div class='section-dot'></div><h2>Budget Performance Analysis</h2></div>", unsafe_allow_html=True)

dept_achievement = budget_df.groupby('Department')['Revenue_Achievement_%'].mean().reset_index().sort_values('Revenue_Achievement_%', ascending=False)
colors_achievement = [COLORS['success'] if a >= 100 else COLORS['warning'] if a >= 90 else COLORS['danger'] for a in dept_achievement['Revenue_Achievement_%']]

# Compute x-axis max (achievement %)
x_max_val = max(dept_achievement['Revenue_Achievement_%'].max() * 1.05, 130)
x_axis_max = int(round(x_max_val + 5))

fig_budget = go.Figure()

fig_budget.add_trace(go.Bar(
    y=dept_achievement['Department'],
    x=dept_achievement['Revenue_Achievement_%'],
    orientation='h',
    marker=dict(color=colors_achievement, line=dict(color=COLORS['bg_primary'], width=1.5)),
    text=dept_achievement['Revenue_Achievement_%'].apply(lambda x: f'{x:.1f}%'),
    textposition='outside',
    textfont=dict(size=12, family='JetBrains Mono', color=COLORS['text_primary']),
    hovertemplate='<b>%{y}</b><br>%{x:.2f}%<extra></extra>'
))

# Zone shading across the X axis (vertical bands)
fig_budget.add_shape(type="rect", xref="x", x0=100, x1=x_axis_max, yref="paper", y0=0, y1=1,
                     fillcolor="rgba(16,185,129,0.06)", line_width=0, layer="below")
fig_budget.add_shape(type="rect", xref="x", x0=90, x1=100, yref="paper", y0=0, y1=1,
                     fillcolor="rgba(245,158,11,0.06)", line_width=0, layer="below")
fig_budget.add_shape(type="rect", xref="x", x0=0, x1=90, yref="paper", y0=0, y1=1,
                     fillcolor="rgba(239,68,68,0.03)", line_width=0, layer="below")

# Guideline lines
fig_budget.add_hline(y=0, line_dash="solid", line_color="rgba(0,0,0,0)", line_width=0)  # noop to keep layout consistent
fig_budget.add_vline(x=100, line_dash="solid", line_color="rgba(200,200,200,0.6)", line_width=2)
fig_budget.add_vline(x=90,  line_dash="dot",   line_color=COLORS['warning'], line_width=1.5)

# Compact annotations on right (inside plot area)
fig_budget.add_annotation(x=0.995, y=1.02, xref="paper", yref="paper",
                          text="Target: 100%", showarrow=False,
                          xanchor="right", yanchor="bottom",
                          font=dict(size=11, color="rgba(200,200,200,0.95)"),
                          bgcolor="rgba(0,0,0,0.45)", borderpad=6)

fig_budget.add_annotation(x=0.995, y=0.98, xref="paper", yref="paper",
                          text="Warning: 90%", showarrow=False,
                          xanchor="right", yanchor="bottom",
                          font=dict(size=11, color=COLORS['warning']),
                          bgcolor="rgba(0,0,0,0.45)", borderpad=6)

# Layout and margins
fig_budget.update_layout(
    title=dict(text="Revenue Achievement by Department (%)", font=dict(size=18, weight=700, color=COLORS['text_primary'])),
    height=420,
    paper_bgcolor=COLORS['chart_bg'],
    plot_bgcolor=COLORS['chart_bg'],
    font=dict(family='Inter', color=COLORS['text_primary']),
    xaxis=dict(gridcolor=COLORS['grid'], color=COLORS['text_primary'], title="Achievement (%)", range=[0, max(x_axis_max, 110)]),
    yaxis=dict(gridcolor=COLORS['grid'], color=COLORS['text_primary']),
    showlegend=False,
    margin=dict(l=60, r=160, t=60, b=60),
    hoverlabel=dict(bgcolor=COLORS['bg_secondary'], font_size=12)
)

# Optional: annotate outlier (Research) so the high value is highlighted
if 'Research' in dept_achievement['Department'].values:
    research_val = float(dept_achievement.loc[dept_achievement['Department'] == 'Research', 'Revenue_Achievement_%'].values[0])
    fig_budget.add_annotation(
        x=research_val,
        y='Research',
        xref="x",
        yref="y",
        text=f"Research {research_val:.1f}%",
        showarrow=True,
        arrowhead=3,
        ax=-40,
        ay=0,
        font=dict(size=11, color=COLORS['text_primary'], family='JetBrains Mono'),
        bgcolor=COLORS['accent_blue'],
        bordercolor=COLORS['accent_blue'],
        opacity=0.95
    )

st.plotly_chart(fig_budget, use_container_width=True)

# =============================================================================
# Invoice & Transactions
# =============================================================================

st.markdown("<div class='section-header'><div class='section-dot'></div><h2>Invoice & Payment Analysis</h2></div>", unsafe_allow_html=True)
paid_invoices = invoices_df[invoices_df['Status']=='Paid']
pending_invoices = invoices_df[invoices_df['Status']=='Pending']

col1, col2, col3, col4 = st.columns(4)
render_metric(col1, "#", f"linear-gradient(135deg, {COLORS['accent_blue']}, {COLORS['accent_blue_dark']})", "Total Invoices", f"{len(invoices_df)}", f"<div class='metric-delta positive'>{len(paid_invoices)} paid ({len(paid_invoices)/len(invoices_df)*100:.1f}%)</div>")
render_metric(col2, "€", f"linear-gradient(135deg, {COLORS['success']}, {COLORS['success_dark']})", "Total Amount", format_currency(invoices_df['Amount'].sum()), f"<div class='metric-delta positive'>{format_currency(paid_invoices['Amount'].sum())} received</div>")
avg_payment_days = paid_invoices['Days_to_Payment'].mean() if len(paid_invoices)>0 else 0
payment_trend = "positive" if avg_payment_days <= 30 else "negative"
render_metric(col3, "T", f"linear-gradient(135deg, {COLORS['warning']}, {COLORS['warning_light']})", "Avg Payment Time", f"{avg_payment_days:.0f} days", f"<div class='metric-delta {payment_trend}'>Target: ≤30 days</div>")
outstanding = pending_invoices['Amount'].sum()
render_metric(col4, "!", f"linear-gradient(135deg, {COLORS['danger']}, {COLORS['danger_dark']})", "Outstanding", format_currency(outstanding), f"<div class='metric-delta neutral'>{len(pending_invoices)} pending</div>")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<div class='section-header'><div class='section-dot'></div><h2>Transaction Details</h2></div>", unsafe_allow_html=True)
display_df = filtered_df[['Date','Department','Category','Revenue','Cost','Profit','Margin_%','Client_Type']].head(50).copy()
display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
display_df['Revenue'] = display_df['Revenue'].apply(lambda x: f"€{x:,.2f}")
display_df['Cost'] = display_df['Cost'].apply(lambda x: f"€{x:,.2f}")
display_df['Profit'] = display_df['Profit'].apply(lambda x: f"€{x:,.2f}")
display_df['Margin_%'] = display_df['Margin_%'].apply(lambda x: f"{x:.2f}%")
st.dataframe(display_df, use_container_width=True, height=450, hide_index=True)

csv = filtered_df.to_csv(index=False).encode('utf-8')
col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.download_button(label="Download Full Dataset (CSV)", data=csv, file_name=f'financial_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv', mime='text/csv', use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"<div class='footer'><p class='footer-title'>Financial Analytics Dashboard </p><p class='footer-subtitle'>Created by Olha Keleman | November 2025</p></div>", unsafe_allow_html=True)