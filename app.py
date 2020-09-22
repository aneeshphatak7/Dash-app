import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output, State
import dash_table
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import apyori as ap
from apyori import apriori 
import mlxtend as ml
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder
import plotly.graph_objs as go
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
url='https://raw.githubusercontent.com/aneeshphatak7/Dash-app/master/df4.csv'
empData = pd.read_csv(url,sep=",")
colnames = ['antecedents', 'consequents', 'antecedent support',
       'consequent support', 'support', 'confidence', 'lift', 'leverage',
       'conviction']
records = []
for i in range(0,len(empData)):
    records.append([str(empData.values[i,j]) 
    for j in range(0, len(empData.columns))])
    
te = TransactionEncoder()
te_ary = te.fit(records).transform(records)
df = pd.DataFrame(te_ary, columns=te.columns_)    



def SupervisedApriori(df,consequent,min_supp,min_conf,min_lift,max_length,sort_by):

        

    frequent_itemsets = apriori(df, min_support=min_supp, use_colnames=True,max_len=max_length)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_lift)
    rules=rules[(rules['confidence'] > min_conf)&(rules['consequents']=={consequent})].sort_values(by='confidence',ascending=False)

    return(rules)


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = html.Div(children=[
    html.H1('Change following parameters to observe changes in top rules and plot',style=dict(color='Orange',align='center',justify='center')),
     html.Br([]),
     html.Br([]),

   html.Div([ html.Div(children='''
        Min Confidence:     
    ''',
    style={'width':'10%','display': 'inline-block'
            }),
    html.Div(children='''
        Min Support:     
    ''',
    style={'width':'10%','display': 'inline-block'
            }),
    html.Div(children='''
        Min Lift:     
    ''',
    style={'width':'10%','display': 'inline-block'
            }),
    html.Div(children='''
        Consequents:     
    ''',
    style={'width':'10%','display': 'inline-block'
            }),
    html.Div(children='''
        Max_length:     
    ''',
    style={'width':'10%','display': 'inline-block'
            }),
    html.Div(children='''
        Sort_by:     
    ''',
    style={'width':'10%','display': 'inline-block'
            }),
 
 html.Div([
dcc.Input(
    placeholder='Enter Confidence: ',
    type='number',
    value=0.7,
    id = 'confidence',style={'width':'10%','display': 'inline-block'
            }
) ,
dcc.Input(
    placeholder='Enter Support',
    type='number',
    value=0.4,
    id = 'support',style={'width':'10%','display': 'inline-block'
            }
) ,

dcc.Input(
    placeholder='Enter Lift',
    type='number',
    value=1,
    id = 'lift',style={'width':'10%','display': 'inline-block'
            }
) ,        
dcc.Dropdown(
    placeholder='Enter Consequent',
    options = [
        {'label':'No','value':'Attrition=No'},{'label':'Yes','value':'Attrition=Yes'}],
    value='Attrition=No',
    id = 'Consequent', style={'width':'100px','display': 'inline-block'
            }
) ,        

dcc.Input(
    placeholder='Max_lenth',
    type='number',
    value=4,
    id = 'rules', style={'width':'10%','display': 'inline-block'
            }
) ,  
dcc.Dropdown(
    placeholder='sort by',
    options = [
        {'label':'lift','value':'lift'},{'label':'confidence','value':'confidence'},{'label':'support','value':'support'}],
    value='lift',
    id = 'Sort_by', style={'width':'150px','display': 'inline-block'
            }
) , 
   html.Button('Submit', id='submit-button-state', n_clicks=0),
    
    ]),
      
html.Div(id="table1"),]),
html.H3("Scatterplot for custom rules ",style=dict(color='Orange',align='center',justify='center')),
        html.Div(id='graphs'),

])
    
    
@app.callback(
    Output(component_id='table1',component_property='children'),
    [Input('submit-button-state', 'n_clicks')],
    [State(component_id='confidence', component_property='value'),
     State(component_id='support', component_property='value'),
     State(component_id='lift', component_property='value'),
     State(component_id='rules', component_property='value'),
     State(component_id='Consequent', component_property='value'),
    State(component_id='Sort_by', component_property='value'),
     ]
)
def update_datatable(n_clicksx,confidence,support,lift,rules,Consequent,Sort_by):

    y=SupervisedApriori(df,consequent = Consequent, min_supp=support, min_conf=confidence, min_lift=lift,max_length=rules,sort_by=Sort_by)
    
    
    y=y.head(5)
    
    sup_rules=y
    print(sup_rules.to_dict("rows"))
    sup_rules['antecedents']=sup_rules['antecedents'].apply(lambda x:list(x))
    sup_rules['consequents']=sup_rules['consequents'].apply(lambda x:list(x))

    
    print("++++++++++++++++++++++++++++++++++++++")
    print(sup_rules.to_dict("rows"))
    tab=html.Div(children=[html.Br([]),html.Label(children='Top 5 rules', style={'width': '60%', 'display': 'inline-block',
                                                                 'margin': 0, 'padding': '10px','color':'blue'}),
            dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in sup_rules.columns],
                    data=sup_rules.to_dict("rows"),
                    style_cell={'width': '250px',
                    'height': '70px',
                    'textAlign': 'left'})
                    ])
    return tab
    

    
@app.callback(
    Output(component_id='graphs',component_property='children'),
     [Input('submit-button-state', 'n_clicks')],
    [State(component_id='confidence', component_property='value'),
     State(component_id='support', component_property='value'),
     State(component_id='lift', component_property='value'),
     State(component_id='rules', component_property='value'),
     State(component_id='Consequent', component_property='value'),
     State(component_id='Sort_by', component_property='value')
     ]
)
def update_graph(nclick,confidence,support,lift,rules,Consequent,Sort_by):
    

     
    rules=SupervisedApriori(df,consequent = Consequent,min_supp=support, min_conf=confidence, min_lift=lift,max_length=rules,sort_by=Sort_by)
    sup=rules['support']
    conf=rules['confidence']
    lif=rules['lift']
    print(rules["support"])
    print(rules["confidence"])
    print(rules["lift"])

    return html.Div([
            dcc.Graph(
        id='ScatterPlot of Confidence Vs Support',
        figure={
                'data':[
                        go.Scatter(x=sup,
                         y= conf,
                        
                         
                         mode='markers',
                         marker=dict(
                                 color=lif,showscale=True,colorbar=dict(title='Lift'))

                                )
                        ],
                
                'layout': go.Layout(
                        title ='Scatterplot of Confidence vs Support for custom rules'
                        
                        )
                }
    )
                    ])
   

    

if __name__ == '__main__':
    app.run_server()

