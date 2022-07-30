from re import X
from tkinter import Y
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import json


Q1 = pd.read_excel('Q1_2022_CLAIMS.xlsx')
fig1 = px.bar(
    Q1, #dataframe
    x=Q1.groupby("INSURER")["CPR Q1 2022"].agg(sum), #y
    y=Q1["INSURER"].unique(),#x
    labels={"x": "Claims Payment Ratio", "y": "INSURER"}, #define lable
    color=Q1.groupby("INSURER")["CPR Q1 2022"].agg(sum),
    color_continuous_scale=px.colors.sequential.RdBu,#color
    text=Q1.groupby("INSURER")["CPR Q1 2022"].agg(sum),#text
    title="Claims Payment Ratio (CPR)", #title
    orientation="h"  #horizonal bar chart
)
fig1.update_layout(
    xaxis_tickangle=30,#angle of the tick on x-axis
    title=dict(x=0.5), #set the title in center
    xaxis_tickfont=dict(size=9), #set the font for x-axis
    yaxis_tickfont=dict(size=9), #set the font for y-axis
    margin=dict(l=20, r=20, t=50, b=20), #set the margin
    paper_bgcolor="LightSteelblue", #set the background color for chart
) 
fig2 = px.scatter(
    Q1, #dataframe
    x="DECLINED", #x
    y="PAID", #y
    size="PAID", #bubble size
    color="PAID",#bubble color
    color_continuous_scale=px.colors.sequential.Plotly3, #color theme
    title="PAID vs DECLINED CLAIMS", #chart title
)
fig2.update_layout(
    xaxis_tickangle=30,#angle of the tick on x-axis
    title=dict(x=0.5), #set the title in center
    xaxis_tickfont=dict(size=9), #set the font for x-axis
    yaxis_tickfont=dict(size=9), #set the font for y-axis
    margin=dict(l=20, r=20, t=50, b=20), #set the margin
    paper_bgcolor="LightSteelblue", #set the background color for chart
) 

liability_claims = pd.read_excel('Q1_2022_CLAIMS.xlsx', sheet_name='liability_claims')
non_liability_claims = pd.read_excel('Q1_2022_CLAIMS.xlsx', sheet_name='non_liability_claims')
long_term_claims = pd.read_excel('Q1_2022_CLAIMS.xlsx', sheet_name='long_term_claims')


trace1 = go.Bar(    #setup the chart for liability claims
    x=liability_claims["INSURER"].unique(), #y for liability claims in Q4 2021
    y=liability_claims.groupby("INSURER")["CPR Q1 2022"].agg(sum),#x for claims payment ration in Q4 2021
    marker_color=px.colors.qualitative.Dark24[0],  #color
    text=liability_claims.groupby("INSURER")["CPR Q1 2022"].agg(sum), #label/text
    textposition="outside", #text position
    name="claims payment ratio (CPR) of Liability Claims", #legend name
)
trace2 = go.Bar(   #setup the chart for non liability claims
    x=non_liability_claims["INSURER"].unique(),
    y=non_liability_claims.groupby("INSURER")["CPR Q4 2021"].agg(sum),
    text=non_liability_claims.groupby("INSURER")["CPR Q1 2022"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[1],
    textposition="outside",
    name="claims payment ratio (CPR) of Non liability Claims",
)
trace3 = go.Bar(   #setup the chart for long term claims
    x=long_term_claims["INSURER"].unique(),
    y=long_term_claims.groupby("INSURER")["CPR Q1 2022"].agg(sum),
    text=long_term_claims.groupby("INSURER")["CPR Q1 2022"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[1],
    textposition="outside",
    name="claims payment ratio (CPR) of Long Term claims",
)

data = [trace1, trace2, trace3] #combine three charts/columns
layout = go.Layout(barmode="group", title="Liability, Non-Liability and Long-Term Claims") #define how to display the columns
fig3 = go.Figure(data=data, layout=layout)
fig3.update_layout(
    title=dict(x=0.5), #center the title
    yaxis_title="claims Paymet ratio",#setup the x-axis title
    xaxis_title="INSURER", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig3.update_traces(texttemplate="%{text:.2s}") #text formart

Q1
fig4= px.bar(Q1, 
             x=Q1.groupby('INSURER')['CLOSED'].agg(sum),
             y=Q1['INSURER'].unique(), 
             labels={
                     "y": "INSURER",
                     "x": "PAID CLAIMS AND CLAIMS CLOSED "
                 },
              color = Q1.groupby('INSURER')['CLOSED'].agg(sum),
              color_continuous_scale=px.colors.sequential.Sunset,
              #color_discrete_sequence=['rgb(253,180,98)','rgb(190,186,218)'],
              text = Q1.groupby('INSURER')['CLOSED'].agg(sum),
             title = 'PAID CLAIMS AND CLAIMS CLOSED AS OUTSTANDING CLAIMS',
              #,barmode = 'group'
              orientation = 'h'
             )
fig4.update_layout( title = dict(x=0.5), paper_bgcolor="#BDBDBD")
fig4.update_traces(texttemplate = '%{text:.2s}')

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🚓", style={'fontSize': "30px",'textAlign': 'center'}, className="header-emoji"), #emoji
                html.H1(
                    children="IRA Q1 2022 CLAIMS SETTLEMENT",style={'textAlign': 'center'}, className="header-title" 
                ), #Header title
                html.H2(
                    children="Analyze claims Numbers"
                    " by INSURER listed by IRA"
                    " in Quarter one of 2022",
                    className="header-description", style={'textAlign': 'center'},
                ),
            ],
            className="header",style={'backgroundColor':'#F5F5F5'},
        ), #Description below the header
        
        
        # html.Div(
        #     children=[
        #         html.Div(children = 'INSURER', style={'fontSize': "24px"},className = 'menu-title'),
        #         dcc.Dropdown(
        #             id = 'INSURER',
        #             options = [
        #                 {'label': INSURER, 'value':INSURER}
        #                 for INSURER in Q1.INSURER.unique()
        #             ], #'Insurer' is the filter
        #             value ='INSURER',
        #             clearable = False,
        #             searchable = False,
        #             className = 'dropdown', style={'fontSize': "24px",'textAlign': 'center'},
        #         ),
        #     ],
        #     className = 'menu',
        # ), #the dropdown function
        
        html.Div(
            children=[
                html.Div(
                children = dcc.Graph(
                    id = 'scatter',
                    figure = fig2,
                  #  config={"displayModeBar": False},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'bar',
                    figure = fig1,
                    #config={"displayModeBar": False},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'bibar',
                    figure = fig3,
                    #config={"displayModeBar": False},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'barscene',
                    figure = fig4,
                    #config={"displayModeBar": False},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
        ],
        className = 'double-graph',
        ), 
    ]
) #Four graphs


# @app.callback(
#     Output("scatter", "figure"), #the output is the scatterchart
#     [Input("INSURER", "value")], #the input is the year-filter
# )
# def update_charts(INSURER):
#     filtered_data = Q1[Q1["INSURER"] == INSURER] #the graph/dataframe will be filterd by "Insurer"
scatter = px.scatter(
        Q1,
        y="PAID",
        x="REVISED",
        size="C/F",
        color="C/F",
        color_continuous_scale=px.colors.sequential.Plotly3,
        title="claims brought forward(B/F)",
    )
scatter.update_layout(
        xaxis_tickangle=30,
        title=dict(x=0.5),
        xaxis_tickfont=dict(size=9),
        yaxis_tickfont=dict(size=9),
        margin=dict(l=500, r=20, t=50, b=20),
        paper_bgcolor="LightSteelblue",
)
# @app.callback(
#     Output("bar", "figure"),
#     [Input("INSURER-filter", "value")],
# )
# def update_charts(INSURER):
#     data = Q1[Q1["INSURER"] == INSURER]
#     bar = px.bar(
#         data,
#         y=data.groupby("INSURER")["CPR Q1 2022"].agg(sum),
#         x=data["INSURER"].unique(),
#         color=data.groupby("INSURER")["CPR Q1 2022"].agg(sum),
#         color_continuous_scale=px.colors.sequential.RdBu,
#         text=data.groupby("INSURER")["CPR Q1 2022"].agg(sum),
#         title="Claim Numbers per Industry claim classification",
#         orientation="v",
#     )
#     bar.update_layout(
#         title=dict(x=0.5), margin=dict(l=550, r=20, t=60, b=20), paper_bgcolor="#D6EAF8"
#     )
#     bar.update_traces(texttemplate="%{text:.2s}")
#     return bar
# @app.callback(
#     Output("bibar", "figure"),
#     [Input("INSURER", "value")],
# )
# def update_charts(INSURER):
#     filtered_liability_claims = liability_claims[liability_claims["INSURER"] == INSURER]
#     filtered_non_liability_claims = non_liability_claims[non_liability_claims["INSURER"] == INSURER]
#     filtered_long_term_claims=long_term_claims[long_term_claims["INSURER"]== INSURER]
#     trace1 = go.Bar(
#         y=filtered_liability_claims["ICPR Q4 2021"].unique(),
#         x=filtered_liability_claims.groupby("INSURER")["CPR Q1 2022"].agg(sum),
#         text=filtered_liability_claims.groupby("INSURER")["Industry"].agg(sum),
#         textposition="outside",
#         marker_color=px.colors.qualitative.Dark24[0],
#         name="Industry outlook on liability Claims",
#     )
#     trace2 = go.Bar(
#         y=filtered_non_liability_claims["CPR Q4 2021"].unique(),
#         x=filtered_non_liability_claims.groupby("INSURER")["CPR Q1 2022"].agg(sum),
#         text=filtered_non_liability_claims.groupby("INSURER")["Industry"].agg(sum),
#         textposition="outside",
#         marker_color=px.colors.qualitative.Dark24[1],
#         name="Industry outlook on non liability claims",
#     )
#     trace3=go.Bar(
#         y=filtered_long_term_claims["CPR Q4 2021"].unique(),
#         x=filtered_long_term_claims.groupby("INSURER")["CPR Q1 2022"].agg(sum),
#         text=filtered_long_term_claims.groupby("INSURER")["CPR Q1 2022"].agg(sum),
#         textposition="outside",
#         marker_color=px.colors.qualitative.Dark24[1],
#         name="Industry outlook on long term claims",
#     )

#     data = [trace1, trace2,trace3]
#     layout = go.Layout(barmode="group", title="liability vs non liablity vs long term claims")
#     bibar = go.Figure(data=data, layout=layout)
#     bibar.update_layout(
#         title=dict(x=0.5),
#         xaxis_title="CPR Q1 2022",
#         yaxis_title="INSURER",
#         paper_bgcolor="aliceblue",
#         margin=dict(l=20, r=20, t=60, b=20),
#     )
#     bibar.update_traces(texttemplate="%{text:.2s}")
#     return bibar
# @app.callback(
#     Output("barscene", "figure"),
#     [Input("INSURER", "value")],
# )
# def update_charts(INSURER):
#     filtered_data = Q1[Q1["INSURER"] == INSURER]
#     barscene = px.bar(
#         filtered_data,
#         x=filtered_data.groupby("INSURER")["CLOSED"].agg(sum),
#         y=filtered_data["INSURER"].unique(),
#         labels={"x": "PAID CLAIMS AND CLAIMS CLOSED AS OUTSTANDING CLAIMS", "y": "INSURER"},
#         color=filtered_data.groupby("INSURER")["CLOSED"].agg(sum),
#         color_continuous_scale=px.colors.sequential.Sunset,
#         # color_discrete_sequence=['rgb(253,180,98)','rgb(190,186,218)'],
#         text=filtered_data.groupby("INSURER")["CLOSED"].agg(sum),
#         title="claims Paid and closed as outstanding claims",
#         # ,barmode = 'group'
#         orientation="h",
#     )
#     barscene.update_layout(title=dict(x=0.5), paper_bgcolor="#BDBDBD")
#     barscene.update_traces(texttemplate="%{text:.2s}")
#     return barscene
# def update_live(app_intervals,TVtog, BVtog, VVtog, config):

#     sWS_ParamConfig = json.loads(config)
#     print(sWS_ParamConfig)

#     SupPres = float(sWS_ParamConfig['supplyPressure']['lowerLimit']),
#     TestPres = float(sWS_ParamConfig['supplyPressure']['upperLimit']),
#     flo = float(sWS_ParamConfig['leakRate']['lowerLimit']),
#     SupPresMax = float(sWS_ParamConfig['supplyPressure']['upperLimit']),
#     TestPresMax = float(sWS_ParamConfig['leakRate']['upperLimit']),
#     floMax = float(sWS_ParamConfig['leakRate']['upperLimit']), 
#     print(floMax)    
#     return TVtog, BVtog, VVtog, SupPres, TestPres, flo, SupPresMax, TestPresMax, floMax   
#     ##if not using virtual environment

if __name__ == '__main__':
    app.run_server(debug = True)



