"""
dashboard/app.py — Influencer Honesty Score Dashboard
Run: python dashboard/app.py
Then open: http://127.0.0.1:8050
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

COLORS = {
    'HIGH RISK':   '#E24B4A',
    'MEDIUM RISK': '#EF9F27',
    'LOW RISK':    '#639922',
}

app = dash.Dash(__name__)
app.title = "Influencer Honesty Score"

# ── Layout ─────────────────────────────────────────────────────
app.layout = html.Div(style={'fontFamily': 'Segoe UI, sans-serif', 'backgroundColor': '#f8f9fa', 'minHeight': '100vh', 'padding': '24px'}, children=[

    # Header
    html.Div(style={'textAlign': 'center', 'marginBottom': '32px'}, children=[
        html.H1("🔍 Influencer Honesty Score", style={'fontSize': '32px', 'fontWeight': '600', 'color': '#1a1a2e', 'margin': '0'}),
        html.P("Fitness Niche — India | Fake Engagement Detection", style={'color': '#666', 'marginTop': '6px'}),
    ]),

    # Summary cards
    html.Div(style={'display': 'flex', 'gap': '16px', 'marginBottom': '28px', 'flexWrap': 'wrap'}, children=[
        html.Div(style={'flex': '1', 'minWidth': '140px', 'background': '#fff', 'borderRadius': '12px', 'padding': '20px', 'textAlign': 'center', 'border': '1px solid #e0e0e0'}, children=[
            html.Div(str(len(df)), style={'fontSize': '28px', 'fontWeight': '600', 'color': '#1a1a2e'}),
            html.Div("Influencers Analyzed", style={'fontSize': '13px', 'color': '#888', 'marginTop': '4px'}),
        ]),
        html.Div(style={'flex': '1', 'minWidth': '140px', 'background': '#fff', 'borderRadius': '12px', 'padding': '20px', 'textAlign': 'center', 'border': '1px solid #e0e0e0'}, children=[
            html.Div(str((df['risk_label'] == 'HIGH RISK').sum()), style={'fontSize': '28px', 'fontWeight': '600', 'color': '#E24B4A'}),
            html.Div("High Risk Accounts", style={'fontSize': '13px', 'color': '#888', 'marginTop': '4px'}),
        ]),
        html.Div(style={'flex': '1', 'minWidth': '140px', 'background': '#fff', 'borderRadius': '12px', 'padding': '20px', 'textAlign': 'center', 'border': '1px solid #e0e0e0'}, children=[
            html.Div(str((df['risk_label'] == 'LOW RISK').sum()), style={'fontSize': '28px', 'fontWeight': '600', 'color': '#639922'}),
            html.Div("Authentic Accounts", style={'fontSize': '13px', 'color': '#888', 'marginTop': '4px'}),
        ]),
        html.Div(style={'flex': '1', 'minWidth': '140px', 'background': '#fff', 'borderRadius': '12px', 'padding': '20px', 'textAlign': 'center', 'border': '1px solid #e0e0e0'}, children=[
            html.Div(f"{df['fake_score'].mean():.1f}", style={'fontSize': '28px', 'fontWeight': '600', 'color': '#EF9F27'}),
            html.Div("Avg Fake Score / 100", style={'fontSize': '13px', 'color': '#888', 'marginTop': '4px'}),
        ]),
    ]),

    # Filter
    html.Div(style={'background': '#fff', 'borderRadius': '12px', 'padding': '20px', 'marginBottom': '24px', 'border': '1px solid #e0e0e0'}, children=[
        html.Label("Filter by Risk Level:", style={'fontWeight': '500', 'marginBottom': '8px', 'display': 'block'}),
        dcc.Dropdown(
            id='risk-filter',
            options=[{'label': 'All', 'value': 'All'}, {'label': 'High Risk', 'value': 'HIGH RISK'}, {'label': 'Medium Risk', 'value': 'MEDIUM RISK'}, {'label': 'Low Risk', 'value': 'LOW RISK'}],
            value='All',
            clearable=False,
            style={'width': '250px'}
        ),
    ]),

    # Charts row
    html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px', 'marginBottom': '24px'}, children=[
        html.Div(style={'background': '#fff', 'borderRadius': '12px', 'padding': '16px', 'border': '1px solid #e0e0e0'}, children=[
            dcc.Graph(id='bar-chart', style={'height': '380px'}),
        ]),
        html.Div(style={'background': '#fff', 'borderRadius': '12px', 'padding': '16px', 'border': '1px solid #e0e0e0'}, children=[
            dcc.Graph(id='scatter-chart', style={'height': '380px'}),
        ]),
    ]),

    # Pie chart + table
    html.Div(style={'display': 'grid', 'gridTemplateColumns': '340px 1fr', 'gap': '20px', 'marginBottom': '24px'}, children=[
        html.Div(style={'background': '#fff', 'borderRadius': '12px', 'padding': '16px', 'border': '1px solid #e0e0e0'}, children=[
            dcc.Graph(id='pie-chart', style={'height': '320px'}),
        ]),
        html.Div(style={'background': '#fff', 'borderRadius': '12px', 'padding': '20px', 'border': '1px solid #e0e0e0'}, children=[
            html.H3("Full Ranking Table", style={'margin': '0 0 14px', 'fontSize': '16px', 'fontWeight': '500'}),
            dash_table.DataTable(
                id='ranking-table',
                columns=[
                    {'name': 'Rank', 'id': 'rank'},
                    {'name': 'Username', 'id': 'username'},
                    {'name': 'Followers', 'id': 'followers'},
                    {'name': 'Engagement %', 'id': 'engagement_rate'},
                    {'name': 'Fake Score', 'id': 'fake_score'},
                    {'name': 'Risk', 'id': 'risk_label'},
                ],
                sort_action='native',
                filter_action='native',
                page_size=8,
                style_cell={'textAlign': 'left', 'padding': '8px 12px', 'fontSize': '13px', 'fontFamily': 'Segoe UI, sans-serif'},
                style_header={'fontWeight': '600', 'backgroundColor': '#f0f4ff', 'borderBottom': '2px solid #dde'},
                style_data_conditional=[
                    {'if': {'filter_query': '{risk_label} = "HIGH RISK"'}, 'color': '#E24B4A', 'fontWeight': '500'},
                    {'if': {'filter_query': '{risk_label} = "LOW RISK"'}, 'color': '#639922', 'fontWeight': '500'},
                ],
            ),
        ]),
    ]),

    html.Div("Built by Anu | Influencer Honesty Score Project | Python + Plotly Dash",
             style={'textAlign': 'center', 'color': '#aaa', 'fontSize': '12px', 'marginTop': '16px'}),
])


# ── Callbacks ──────────────────────────────────────────────────
@app.callback(
    Output('bar-chart', 'figure'),
    Output('scatter-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Output('ranking-table', 'data'),
    Input('risk-filter', 'value')
)
def update_all(risk_filter):
    filtered = df if risk_filter == 'All' else df[df['risk_label'] == risk_filter]
    top20 = filtered.nlargest(15, 'fake_score').sort_values('fake_score')

    # Bar chart
    bar = px.bar(
        top20, x='fake_score', y='username', orientation='h',
        color='risk_label',
        color_discrete_map=COLORS,
        title='Top 15 Most Suspicious Influencers',
        labels={'fake_score': 'Fake Score', 'username': ''},
    )
    bar.update_layout(margin=dict(l=10, r=10, t=40, b=10), showlegend=False, plot_bgcolor='white', paper_bgcolor='white')
    bar.update_xaxes(range=[0, 100])

    # Scatter chart
    scatter = px.scatter(
        filtered, x='followers', y='engagement_rate',
        color='risk_label',
        color_discrete_map=COLORS,
        hover_data=['username', 'fake_score'],
        title='Followers vs Engagement Rate',
        labels={'engagement_rate': 'Engagement Rate (%)', 'followers': 'Followers'},
        size='fake_score', size_max=20,
    )
    scatter.update_layout(margin=dict(l=10, r=10, t=40, b=10), plot_bgcolor='white', paper_bgcolor='white')

    # Pie chart
    risk_counts = filtered['risk_label'].value_counts().reset_index()
    risk_counts.columns = ['risk_label', 'count']
    pie = px.pie(
        risk_counts, names='risk_label', values='count',
        color='risk_label',
        color_discrete_map=COLORS,
        title='Risk Distribution',
        hole=0.4,
    )
    pie.update_layout(margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='white')

    table_data = filtered[['rank','username','followers','engagement_rate','fake_score','risk_label']].sort_values('rank').to_dict('records')

    return bar, scatter, pie, table_data


if __name__ == '__main__':
    print("\n Dashboard running at: http://127.0.0.1:8050\n")
    app.run(debug=True)
