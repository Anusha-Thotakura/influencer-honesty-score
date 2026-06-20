"""
dashboard/app.py — Influencer Honesty Score Dashboard
Run: python dashboard/app.py
Then open: http://127.0.0.1:8050

v2 — Adds 5 navigable pages (Executive Overview, Rankings, Correlation
Analysis, Visual Analytics, Business Insights) on top of the original
single-page dashboard. All original functionality (risk filter, top-15 bar
chart, followers-vs-engagement scatter, risk pie chart, sortable/filterable
ranking table) is preserved — it now lives inside the "Rankings" tab.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
from dash import dcc, html, dash_table, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Load data ──────────────────────────────────────────────────
df = pd.read_csv('data/processed/influencers_scored.csv')

# Follower tier (presentation-only, same logic as analytics/utils.py)
bins = [-1, 50_000, 200_000, 1_000_000, float("inf")]
tier_labels = ["Nano (<50K)", "Micro (50K-200K)", "Macro (200K-1M)", "Mega (1M+)"]
df["follower_tier"] = pd.cut(df["followers"], bins=bins, labels=tier_labels)

HONESTY_COL = "fake_score"

COLORS = {
    'HIGH RISK':   '#E24B4A',
    'MEDIUM RISK': '#EF9F27',
    'LOW RISK':    '#639922',
}
RISK_ORDER = ['LOW RISK', 'MEDIUM RISK', 'HIGH RISK']

CORRELATION_METRICS = {
    "followers": "Followers",
    "following": "Following",
    "avg_likes": "Avg Likes",
    "avg_comments": "Avg Comments",
    "engagement_rate": "Engagement Rate",
    "lc_ratio": "Like-Comment Ratio",
    HONESTY_COL: "Honesty Risk Score",
}

CARD_STYLE = {'background': '#fff', 'borderRadius': '12px', 'padding': '16px', 'border': '1px solid #e0e0e0'}
PANEL_STYLE = {'background': '#fff', 'borderRadius': '12px', 'padding': '20px', 'border': '1px solid #e0e0e0'}

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Influencer Honesty Score"


# ─────────────────────────────────────────────────────────────────
# REUSABLE PIECES
# ─────────────────────────────────────────────────────────────────
def kpi_cards():
    return html.Div(style={'display': 'flex', 'gap': '16px', 'marginBottom': '28px', 'flexWrap': 'wrap'}, children=[
        html.Div(style={**CARD_STYLE, 'flex': '1', 'minWidth': '140px', 'textAlign': 'center'}, children=[
            html.Div(str(len(df)), style={'fontSize': '28px', 'fontWeight': '600', 'color': '#1a1a2e'}),
            html.Div("Influencers Analyzed", style={'fontSize': '13px', 'color': '#888', 'marginTop': '4px'}),
        ]),
        html.Div(style={**CARD_STYLE, 'flex': '1', 'minWidth': '140px', 'textAlign': 'center'}, children=[
            html.Div(str((df['risk_label'] == 'HIGH RISK').sum()), style={'fontSize': '28px', 'fontWeight': '600', 'color': '#E24B4A'}),
            html.Div("High Risk Accounts", style={'fontSize': '13px', 'color': '#888', 'marginTop': '4px'}),
        ]),
        html.Div(style={**CARD_STYLE, 'flex': '1', 'minWidth': '140px', 'textAlign': 'center'}, children=[
            html.Div(str((df['risk_label'] == 'LOW RISK').sum()), style={'fontSize': '28px', 'fontWeight': '600', 'color': '#639922'}),
            html.Div("Authentic Accounts", style={'fontSize': '13px', 'color': '#888', 'marginTop': '4px'}),
        ]),
        html.Div(style={**CARD_STYLE, 'flex': '1', 'minWidth': '140px', 'textAlign': 'center'}, children=[
            html.Div(f"{df['fake_score'].mean():.1f}", style={'fontSize': '28px', 'fontWeight': '600', 'color': '#EF9F27'}),
            html.Div("Avg Honesty Risk Score / 100", style={'fontSize': '13px', 'color': '#888', 'marginTop': '4px'}),
        ]),
    ])


def section_title(text):
    return html.H3(text, style={'margin': '0 0 14px', 'fontSize': '16px', 'fontWeight': '500'})


# ─────────────────────────────────────────────────────────────────
# TAB 1 — EXECUTIVE OVERVIEW
# ─────────────────────────────────────────────────────────────────
def executive_overview_tab():
    risk_counts = df['risk_label'].value_counts().reset_index()
    risk_counts.columns = ['risk_label', 'count']
    pie = px.pie(risk_counts, names='risk_label', values='count', color='risk_label',
                 color_discrete_map=COLORS, hole=0.45, title='Risk Distribution')
    pie.update_layout(margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white')

    tier_avg = df.groupby('follower_tier', observed=True)[HONESTY_COL].mean().reset_index()
    tier_chart = px.bar(tier_avg, x='follower_tier', y=HONESTY_COL,
                         title='Avg Honesty Risk Score by Follower Tier',
                         labels={'follower_tier': 'Follower Tier', HONESTY_COL: 'Avg Honesty Risk Score'},
                         color_discrete_sequence=['#8E44AD'])
    tier_chart.update_layout(margin=dict(l=10, r=10, t=40, b=10), plot_bgcolor='white', paper_bgcolor='white')

    most_suspicious = df.loc[df[HONESTY_COL].idxmax()]
    most_authentic = df.loc[df[HONESTY_COL].idxmin()]
    high_pct = (df['risk_label'] == 'HIGH RISK').mean() * 100

    findings = html.Div(style=PANEL_STYLE, children=[
        section_title("Key Findings"),
        html.Ul(style={'fontSize': '14px', 'lineHeight': '1.9', 'color': '#333', 'paddingLeft': '20px'}, children=[
            html.Li([html.B(f"{high_pct:.0f}% "), "of analyzed accounts are flagged HIGH RISK for fake engagement."]),
            html.Li([html.B(f"{most_suspicious['username']} "), f"is the most suspicious account (Score {most_suspicious[HONESTY_COL]:.1f})."]),
            html.Li([html.B(f"{most_authentic['username']} "), f"is the most authentic account (Score {most_authentic[HONESTY_COL]:.1f})."]),
            html.Li("Mega-tier (1M+ followers) accounts trend the most authentic; Nano-tier accounts trend the most suspicious."),
            html.Li("Engagement rate and Like-Comment Ratio are the two strongest drivers of the Honesty Risk Score — see the Correlation Analysis tab."),
        ]),
        html.P("Full narrative: reports/executive_summary.md", style={'fontSize': '12px', 'color': '#999', 'marginTop': '10px'}),
    ])

    return html.Div(children=[
        kpi_cards(),
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px', 'marginBottom': '20px'}, children=[
            html.Div(style=CARD_STYLE, children=[dcc.Graph(figure=pie, style={'height': '340px'})]),
            html.Div(style=CARD_STYLE, children=[dcc.Graph(figure=tier_chart, style={'height': '340px'})]),
        ]),
        findings,
    ])


# ─────────────────────────────────────────────────────────────────
# TAB 2 — RANKINGS  (original dashboard content, preserved)
# ─────────────────────────────────────────────────────────────────
def rankings_tab():
    return html.Div(children=[
        html.Div(style={**PANEL_STYLE, 'marginBottom': '24px'}, children=[
            html.Label("Filter by Risk Level:", style={'fontWeight': '500', 'marginBottom': '8px', 'display': 'block'}),
            dcc.Dropdown(
                id='risk-filter',
                options=[{'label': 'All', 'value': 'All'}, {'label': 'High Risk', 'value': 'HIGH RISK'},
                         {'label': 'Medium Risk', 'value': 'MEDIUM RISK'}, {'label': 'Low Risk', 'value': 'LOW RISK'}],
                value='All', clearable=False, style={'width': '250px'}
            ),
        ]),
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px', 'marginBottom': '24px'}, children=[
            html.Div(style=CARD_STYLE, children=[dcc.Graph(id='bar-chart', style={'height': '380px'})]),
            html.Div(style=CARD_STYLE, children=[dcc.Graph(id='scatter-chart', style={'height': '380px'})]),
        ]),
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '340px 1fr', 'gap': '20px', 'marginBottom': '24px'}, children=[
            html.Div(style=CARD_STYLE, children=[dcc.Graph(id='pie-chart', style={'height': '320px'})]),
            html.Div(style=PANEL_STYLE, children=[
                section_title("Full Ranking Table"),
                dash_table.DataTable(
                    id='ranking-table',
                    columns=[
                        {'name': 'Rank', 'id': 'rank'}, {'name': 'Username', 'id': 'username'},
                        {'name': 'Followers', 'id': 'followers'}, {'name': 'Engagement %', 'id': 'engagement_rate'},
                        {'name': 'Honesty Risk Score', 'id': 'fake_score'}, {'name': 'Risk', 'id': 'risk_label'},
                    ],
                    sort_action='native', filter_action='native', page_size=8,
                    style_cell={'textAlign': 'left', 'padding': '8px 12px', 'fontSize': '13px', 'fontFamily': 'Segoe UI, sans-serif'},
                    style_header={'fontWeight': '600', 'backgroundColor': '#f0f4ff', 'borderBottom': '2px solid #dde'},
                    style_data_conditional=[
                        {'if': {'filter_query': '{risk_label} = "HIGH RISK"'}, 'color': '#E24B4A', 'fontWeight': '500'},
                        {'if': {'filter_query': '{risk_label} = "LOW RISK"'}, 'color': '#639922', 'fontWeight': '500'},
                    ],
                ),
            ]),
        ]),
    ])


@app.callback(
    Output('bar-chart', 'figure'), Output('scatter-chart', 'figure'),
    Output('pie-chart', 'figure'), Output('ranking-table', 'data'),
    Input('risk-filter', 'value')
)
def update_rankings(risk_filter):
    filtered = df if risk_filter == 'All' else df[df['risk_label'] == risk_filter]
    top20 = filtered.nlargest(15, 'fake_score').sort_values('fake_score')

    bar = px.bar(top20, x='fake_score', y='username', orientation='h', color='risk_label',
                 color_discrete_map=COLORS, title='Top 15 Most Suspicious Influencers',
                 labels={'fake_score': 'Honesty Risk Score', 'username': ''})
    bar.update_layout(margin=dict(l=10, r=10, t=40, b=10), showlegend=False, plot_bgcolor='white', paper_bgcolor='white')
    bar.update_xaxes(range=[0, 100])

    scatter = px.scatter(filtered, x='followers', y='engagement_rate', color='risk_label',
                          color_discrete_map=COLORS, hover_data=['username', 'fake_score'],
                          title='Followers vs Engagement Rate',
                          labels={'engagement_rate': 'Engagement Rate (%)', 'followers': 'Followers'},
                          size='fake_score', size_max=20)
    scatter.update_layout(margin=dict(l=10, r=10, t=40, b=10), plot_bgcolor='white', paper_bgcolor='white')

    risk_counts = filtered['risk_label'].value_counts().reset_index()
    risk_counts.columns = ['risk_label', 'count']
    pie = px.pie(risk_counts, names='risk_label', values='count', color='risk_label',
                 color_discrete_map=COLORS, title='Risk Distribution', hole=0.4)
    pie.update_layout(margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white')

    table_data = filtered[['rank', 'username', 'followers', 'engagement_rate', 'fake_score', 'risk_label']] \
        .sort_values('rank').to_dict('records')

    return bar, scatter, pie, table_data


# ─────────────────────────────────────────────────────────────────
# TAB 3 — CORRELATION ANALYSIS
# ─────────────────────────────────────────────────────────────────
def correlation_analysis_tab():
    corr = df[list(CORRELATION_METRICS.keys())].corr().rename(
        index=CORRELATION_METRICS, columns=CORRELATION_METRICS)

    heatmap = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
                         title='Correlation Heatmap — Engagement & Honesty Metrics', aspect='auto')
    heatmap.update_layout(margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white')

    metric_options = [{'label': v, 'value': k} for k, v in CORRELATION_METRICS.items()]

    return html.Div(children=[
        html.Div(style=CARD_STYLE, children=[dcc.Graph(figure=heatmap, style={'height': '480px'})]),
        html.Div(style={**PANEL_STYLE, 'marginTop': '20px'}, children=[
            section_title("Explore a Relationship"),
            html.Div(style={'display': 'flex', 'gap': '16px', 'marginBottom': '12px', 'flexWrap': 'wrap'}, children=[
                html.Div(children=[
                    html.Label("X-axis metric", style={'fontSize': '13px', 'color': '#666'}),
                    dcc.Dropdown(id='corr-x', options=metric_options, value='followers', clearable=False, style={'width': '220px'}),
                ]),
                html.Div(children=[
                    html.Label("Y-axis metric", style={'fontSize': '13px', 'color': '#666'}),
                    dcc.Dropdown(id='corr-y', options=metric_options, value=HONESTY_COL, clearable=False, style={'width': '220px'}),
                ]),
            ]),
            dcc.Graph(id='corr-scatter', style={'height': '380px'}),
        ]),
    ])


@app.callback(
    Output('corr-scatter', 'figure'),
    Input('corr-x', 'value'), Input('corr-y', 'value')
)
def update_corr_scatter(x_col, y_col):
    r = df[x_col].corr(df[y_col])
    fig = px.scatter(df, x=x_col, y=y_col, color='risk_label', color_discrete_map=COLORS,
                      hover_data=['username'],
                      title=f"{CORRELATION_METRICS.get(x_col, x_col)} vs {CORRELATION_METRICS.get(y_col, y_col)}  (r = {r:+.2f})",
                      labels={x_col: CORRELATION_METRICS.get(x_col, x_col), y_col: CORRELATION_METRICS.get(y_col, y_col)})
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10), plot_bgcolor='white', paper_bgcolor='white')
    return fig


# ─────────────────────────────────────────────────────────────────
# TAB 4 — VISUAL ANALYTICS
# ─────────────────────────────────────────────────────────────────
def visual_analytics_tab():
    hist_followers = px.histogram(df, x='followers', nbins=10, title='Followers Distribution', color_discrete_sequence=['#3A7CA5'])
    hist_engagement = px.histogram(df, x='engagement_rate', nbins=10, title='Engagement Rate Distribution', color_discrete_sequence=['#E76F51'])
    hist_honesty = px.histogram(df, x=HONESTY_COL, nbins=10, title='Honesty Risk Score Distribution', color_discrete_sequence=['#8E44AD'])

    scatter_fe = px.scatter(df, x='followers', y='engagement_rate', color='risk_label', color_discrete_map=COLORS,
                             hover_data=['username'], title='Followers vs Engagement')
    scatter_lc = px.scatter(df, x='avg_likes', y='avg_comments', color='risk_label', color_discrete_map=COLORS,
                             hover_data=['username'], title='Likes vs Comments')

    box = px.box(df, x='risk_label', y=HONESTY_COL, color='risk_label', color_discrete_map=COLORS,
                  category_orders={'risk_label': RISK_ORDER}, points='all', title='Honesty Risk Score Spread by Risk Category')

    top10 = df.nsmallest(10, HONESTY_COL).sort_values(HONESTY_COL)
    bottom10 = df.nlargest(10, HONESTY_COL).sort_values(HONESTY_COL)
    top10_chart = px.bar(top10, x=HONESTY_COL, y='username', orientation='h', title='Top 10 Most Authentic',
                          color_discrete_sequence=['#2E8B57'])
    bottom10_chart = px.bar(bottom10, x=HONESTY_COL, y='username', orientation='h', title='Bottom 10 Most Suspicious',
                             color_discrete_sequence=['#C0392B'])

    tier_grouped = df.groupby('follower_tier', observed=True).agg(
        avg_honesty=(HONESTY_COL, 'mean'), avg_engagement=('engagement_rate', 'mean')).reset_index()
    category_chart = px.bar(tier_grouped, x='follower_tier', y=['avg_honesty', 'avg_engagement'], barmode='group',
                             title='Category Comparison — Follower Tier',
                             labels={'value': 'Average', 'follower_tier': 'Follower Tier', 'variable': 'Metric'})

    figs = [hist_followers, hist_engagement, hist_honesty, scatter_fe, scatter_lc, box, top10_chart, bottom10_chart, category_chart]
    for f in figs:
        f.update_layout(margin=dict(l=10, r=10, t=40, b=10), plot_bgcolor='white', paper_bgcolor='white')

    def cell(fig, height='340px'):
        return html.Div(style=CARD_STYLE, children=[dcc.Graph(figure=fig, style={'height': height})])

    return html.Div(children=[
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1fr', 'gap': '16px', 'marginBottom': '16px'}, children=[
            cell(hist_followers), cell(hist_engagement), cell(hist_honesty),
        ]),
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '16px', 'marginBottom': '16px'}, children=[
            cell(scatter_fe), cell(scatter_lc),
        ]),
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '16px', 'marginBottom': '16px'}, children=[
            cell(box), cell(category_chart),
        ]),
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '16px'}, children=[
            cell(top10_chart, height='400px'), cell(bottom10_chart, height='400px'),
        ]),
    ])


# ─────────────────────────────────────────────────────────────────
# TAB 5 — BUSINESS INSIGHTS
# ─────────────────────────────────────────────────────────────────
def insight_table(data, columns):
    return dash_table.DataTable(
        data=data, columns=[{'name': c[1], 'id': c[0]} for c in columns],
        style_cell={'textAlign': 'left', 'padding': '6px 10px', 'fontSize': '12px', 'fontFamily': 'Segoe UI, sans-serif'},
        style_header={'fontWeight': '600', 'backgroundColor': '#f0f4ff', 'borderBottom': '2px solid #dde'},
        style_data_conditional=[
            {'if': {'filter_query': '{risk_label} = "HIGH RISK"'}, 'color': '#E24B4A'},
            {'if': {'filter_query': '{risk_label} = "LOW RISK"'}, 'color': '#639922'},
        ] if any(c[0] == 'risk_label' for c in columns) else [],
        page_size=10,
    )


def business_insights_tab():
    cols = [('username', 'Username'), ('followers', 'Followers'), ('engagement_rate', 'Engagement %'),
            (HONESTY_COL, 'Honesty Risk Score'), ('risk_label', 'Risk')]

    top_authentic = df.nsmallest(10, HONESTY_COL).sort_values(HONESTY_COL)
    top_suspicious = df.nlargest(10, HONESTY_COL).sort_values(HONESTY_COL, ascending=False)

    median_followers = df['followers'].median()
    median_risk = df[HONESTY_COL].median()
    brand_deals = df[(df['followers'] >= median_followers) & (df[HONESTY_COL] <= median_risk)].sort_values(HONESTY_COL)

    top_engagement = df.nlargest(10, 'engagement_rate').sort_values('engagement_rate', ascending=False)
    low_risk = df[df['risk_label'] == 'LOW RISK'].sort_values(HONESTY_COL)
    high_risk = df[df['risk_label'] == 'HIGH RISK'].sort_values(HONESTY_COL, ascending=False)

    def block(title, subtitle, data):
        return html.Div(style={**PANEL_STYLE, 'marginBottom': '20px'}, children=[
            section_title(title),
            html.P(subtitle, style={'fontSize': '12px', 'color': '#888', 'marginTop': '-8px', 'marginBottom': '12px'}),
            insight_table(data.to_dict('records'), cols),
        ])

    return html.Div(children=[
        block("Top 10 Authentic Influencers", "Lowest Honesty Risk Score", top_authentic),
        block("Top 10 Suspicious Influencers", "Highest Honesty Risk Score", top_suspicious),
        block("Best Influencers for Brand Deals",
              f"Followers \u2265 median ({int(median_followers):,}) AND Honesty Risk Score \u2264 median ({median_risk:.1f})",
              brand_deals),
        block("Highest Engagement Accounts", "Cross-check the Risk column \u2014 very high ER is itself a red flag", top_engagement),
        block("Low Risk Accounts", f"{len(low_risk)} of {len(df)} accounts", low_risk),
        block("High Risk Accounts", f"{len(high_risk)} of {len(df)} accounts \u2014 recommend manual review before deals", high_risk),
    ])


# ─────────────────────────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────────────────────────
app.layout = html.Div(style={'fontFamily': 'Segoe UI, sans-serif', 'backgroundColor': '#f8f9fa', 'minHeight': '100vh', 'padding': '24px'}, children=[

    html.Div(style={'textAlign': 'center', 'marginBottom': '24px'}, children=[
        html.H1("🔍 Influencer Honesty Score", style={'fontSize': '32px', 'fontWeight': '600', 'color': '#1a1a2e', 'margin': '0'}),
        html.P("Fitness Niche — India | Fake Engagement Detection & Analytics", style={'color': '#666', 'marginTop': '6px'}),
    ]),

    dcc.Tabs(id='main-tabs', value='exec', children=[
        dcc.Tab(label='📈 Executive Overview', value='exec'),
        dcc.Tab(label='🏆 Rankings', value='rankings'),
        dcc.Tab(label='🔗 Correlation Analysis', value='correlation'),
        dcc.Tab(label='📊 Visual Analytics', value='visual'),
        dcc.Tab(label='💼 Business Insights', value='insights'),
    ], style={'marginBottom': '24px'}),

    html.Div(id='tab-content'),

    html.Div("Built by Anu | Influencer Honesty Score Project | Python + Pandas + Plotly Dash",
             style={'textAlign': 'center', 'color': '#aaa', 'fontSize': '12px', 'marginTop': '24px'}),
])


@app.callback(Output('tab-content', 'children'), Input('main-tabs', 'value'))
def render_tab(tab):
    if tab == 'exec':
        return executive_overview_tab()
    elif tab == 'rankings':
        return rankings_tab()
    elif tab == 'correlation':
        return correlation_analysis_tab()
    elif tab == 'visual':
        return visual_analytics_tab()
    elif tab == 'insights':
        return business_insights_tab()
    return html.Div("Unknown tab")


if __name__ == '__main__':
    print("\n Dashboard running at: http://127.0.0.1:8050\n")
    app.run(debug=True)
