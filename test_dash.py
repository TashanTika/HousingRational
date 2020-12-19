# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# import pandas as pd
# import plotly.graph_objs as go
# import config_p24
# import plotly.express as px

# mapbox_token = (config_p24.mapbox_token)
# df = pd.read_excel(config_p24.dash_ready)
# selected_location = "Morningside"
# location = df["Location"].drop_duplicates()
# app = dash.Dash()


# app.layout = html.Div([
#                         dcc.Graph(id="graph"),
#                         dcc.Dropdown(id="type_picker",
#                         options=[
#                             {'label': 'Morningside', 'value': 'Morningside'},
#                             {'label': 'Esplanade', 'value': 'Esplanade'},
#                         ],
#                         value='Morningside',)


# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)

# #make the call back work

# #use map    
# @app.callback(Output('graph', 'figure'),
#               [Input('type_picker', 'value')])
# def update_figure(selected_location):    
#     df_new = df.loc[(df["Location"] == selected_location)]
    
#     fig = px.scatter(
#         df_new, x="Price", y="Size",  
#         hover_data=['Address'])
#     return fig
    
    
    
    
    # data = [
    #     dict(
    #         lat=df_new["lat"],
    #         lon=df_new["lon"],
    #         text=df_new["Address"],
    #         type="scattermapbox",
    #         hoverinfo="text",
    #         marker=dict(size=5, color="white", opacity=0),
    #     )
    # ]
    
    # layout = dict(
    #     mapbox=dict(
    #         layers=[],
    #         accesstoken=mapbox_token,
    #         style="mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz",
    #         zoom=30,
    #     ),
    #     hovermode="closest",
    #     margin=dict(r=0, l=0, t=0, b=0),
    #     dragmode="lasso",
    # )
        
        
    # # data = [go.Scattermapbox(lat=df_new["lat"], 
    # #                          lon=df_new["lon"],
    # #                          mode="markers", 
    # #                          marker=dict(size=8),
    # #                          text=df_new["Address"])]
    
    # # layout = go.Layout(autosize=True, 
    # #                    hovermode="closest", 
    # #                    mapbox=dict(bearing=0,pitch=0, zoom=30),
    # #                    mapbox_style="open-street-map")
    
    # fig = dict(data=data, layout=layout)    

    # return fig
    
    
 #From pull reuest fixed by neer !!   
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import config_p24
import plotly.express as px

mapbox_token = (config_p24.mapbox_token)
df = pd.read_excel(config_p24.dash_ready)
app = dash.Dash()


app.layout = html.Div([
                        dcc.Dropdown(id="location_picker",                                                                                                                 
                                    options=[{'label': i, 'value': i} for i in df["Location"].unique()], #fixed this using https://community.plotly.com/t/how-to-populate-a-dropdown-from-unique-values-in-a-pandas-data-frame/5543/2
                                    value='Morningside',),
                        dcc.Graph(id="map"),
                        dcc.Graph(id="scatter"),

])


#make the call back work
@app.callback(Output('scatter', 'figure'),
              [Input('location_picker', 'value')])
def update_scatter(selected_location):    
    df_new = df.loc[(df["Location"] == selected_location)]
    
    fig = px.scatter(
        df_new, x="Price", y="Size",  
        hover_data=['Address'])
    return fig

#use map    
@app.callback(Output('map', 'figure'),
              [Input('location_picker', 'value')])
def update_map(selected_location):    
    df_new = df.loc[(df["Location"] == selected_location)]
    
    data = [go.Scattermapbox(lat=df_new["lat"], 
                              lon=df_new["lon"],
                              mode="markers", 
                              marker=dict(size=8),
                              text=df_new["Address"])]
    
    layout = go.Layout(autosize=True, 
                        hovermode="closest", 
                        mapbox=dict(bearing=0,pitch=0, zoom=30, accesstoken=mapbox_token,),
                        mapbox_style="open-street-map")
    
    fig = dict(data=data, layout=layout)    
    return fig
    
if __name__ == '__main__':
    app.run_server(debug=False)    
    
   
#---------------------------------------------------------------------------------------------
#My Try 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import config_p24
import plotly.express as px

mapbox_token = (config_p24.mapbox_token)
df = pd.read_excel(config_p24.dash_ready)
app = dash.Dash()


app.layout = html.Div([
                        dcc.Dropdown(id="location_picker",                                                                                                                 
                                    options=[{'label': i, 'value': i} for i in df["Location"].unique()], #fixed this using https://community.plotly.com/t/how-to-populate-a-dropdown-from-unique-values-in-a-pandas-data-frame/5543/2
                                    value=input(""),),
                        dcc.Graph(id="map"),
                        dcc.Graph(id="scatter"),

])


#make the call back work
@app.callback(Output('scatter', 'figure'),
              [Input('location_picker', 'value')])
def update_scatter(selected_location):    
    df_new = df.loc[(df["Location"] == selected_location)]
    
    fig = px.scatter(
        df_new, x="Price", y="Size",  
        hover_data=['Address'])
    return fig

#use map    
@app.callback(Output('map', 'figure'),
              [Input('location_picker', 'value')])
def update_map(selected_location):    
    df_new = df.loc[(df["Location"] == selected_location)]
    
    data = [go.Scattermapbox(lat=df_new["lat"], 
                              lon=df_new["lon"],
                              mode="markers", 
                              textfont=dict(size=16, color='black'),
                              marker=dict(symbol ='marker', size=5, color='white'),
                              text=df_new["Address"])]
    
    layout = go.Layout(autosize=True, 
                        hovermode="closest", 
                        mapbox=dict(bearing=0,pitch=0, zoom=30, accesstoken=mapbox_token,),
                        mapbox_style="open-street-map")
    
    fig = dict(data=data, layout=layout)    
    return fig
    
if __name__ == '__main__':
    app.run_server(debug=False)    