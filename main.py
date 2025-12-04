import pandas as pd
import seaborn as sns
import plotly.express as px 
import numpy as np 
from dash import dcc,Input,Output,callback,Dash,html,dash_table
import figures

df = pd.read_excel('dataset.xlsx',sheet_name='HR_Analysis')

df.drop_duplicates(inplace=True)


education = df.groupby(by='EducationField').count()['EmpID'].reset_index()


    


age_group = df.groupby(by='AgeGroup').count()['EmpID'].reset_index()

salary_slab = df.groupby(by='SalarySlab').count()['EmpID'].reset_index()

roles_agg = df.groupby(['JobRole', 'JobSatisfaction']).size().reset_index(name='Count')
pivot_table = pd.pivot_table(
    roles_agg,
    values='Count',
    index='JobRole',
    columns='JobSatisfaction',
    aggfunc='sum',
    fill_value=0
)
pivot_table['Total'] = pivot_table.sum(axis=1)

# Calculate vertical total (sum across columns)
pivot_table.loc['Total'] = pivot_table.sum(axis=0)
pivot_table.reset_index(inplace=True)
pivot_table.drop(columns='JobSatisfaction', inplace=True, errors='ignore')
print(pivot_table)
years_company = df.loc[df['Attrition'] == 'Yes'].groupby(by='YearsAtCompany').count()['EmpID'].reset_index()

attrition_gender = df.loc[df['Attrition'] == 'Yes',['EmpID','Gender']].groupby(by='Gender').count().reset_index()



salarySlab_crt = px.bar(salary_slab,y='SalarySlab',x='EmpID')
salarySlab_crt.update_traces(
    marker_color='#003A9E'
)
salarySlab_crt.update_layout(
    plot_bgcolor = '#E6E6E6',
    paper_bgcolor = '#E6E6E6',
    title_x=0.5,
    font=dict(
        family='Arial, sans-serif',
        color='#003A9E'
    ),
    margin=dict(l=0, r=0, t=0, b=0),
)
salarySlab_crt.update_traces(
    textposition='inside',  # Position text labels outside the bars
    textfont=dict(
        family='Arial, sans-serif',
        size=12,
        color='white'  # Set text color
    ),
)
salarySlab_crt.update_xaxes(
    showgrid=False,
    linecolor='#E6E6E6',  # Set x-axis line color
    linewidth=2,  
    title=None,
)

salarySlab_crt.update_yaxes(
    showgrid=False,
    linecolor='#E6E6E6',  # Set x-axis line color
    linewidth=2,  
    title=None,
)

age_group_crt= px.bar(age_group,x='AgeGroup',y='EmpID')
age_group_crt.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    plot_bgcolor = '#E6E6E6',
    paper_bgcolor = '#E6E6E6',
    font=dict(
        family='Arial, sans-serif',
        color='#003A9E'
    ),
)
age_group_crt.update_traces(
    text=age_group['AgeGroup'],
    textposition='inside',  # Position text labels outside the bars
    textfont=dict(
        family='Arial, sans-serif',
        size=12,
        color='white'  # Set text color
    ),
    marker_color='#003A9E'
)
age_group_crt.update_xaxes(
    linecolor='#E6E6E6',  # Set x-axis line color
    linewidth=2,  
    
    showgrid=False,
    title=None,
    showticklabels=False
)

age_group_crt.update_yaxes(
    title=None,
    linecolor='#E6E6E6',  # Set x-axis line color
    linewidth=2,  
    showgrid=False,
)

app = Dash(__name__,external_stylesheets=['./assets/style.css'])

app.layout = html.Main(
    id='body',
    children= [
        html.H1(
        id='dashboard-title',
        children=['HR ANALYTICS DASHBOARD']
    ), 
        html.Div(
        id='wrapper',
        children=[
            html.Div(
                id="main-section",
                children=[
                    html.Div(
                id='quick-stats',
                children=[
                    html.Div(
                        id="totalEmp-wrap",
                        className='quick-container',
                        children=[
                            html.H4('Total Employees'), 
                            html.H2(
                                id='totalEmp',
                                children=[]
                            )
                        ]
                    ),html.Div(
                        id="attr_total",
                        className='quick-container',
                        children=[
                            html.H4('Total Attrition'), 
                            html.H2(
                                id='attrCount',
                                children=[]
                                )
                        ]
                    ),
                    html.Div(
                        className='quick-container',
                        children=[
                            html.H4('Attrition Rate'), 
                            html.H2(
                                id='attrRate',
                                children=None
                                )
                        ]
                    ),
                    html.Div(
                        id="avgAge",
                        className='quick-container',
                        children=[
                            html.H4('Avg Age'), 
                            html.H2(
                                id='avgAge', 
                                children=[]
                            )
                        ]
                    ),
                    html.Div(
                        className='quick-container',
                        id="avgSly",
                        children=[
                            html.H4('Avg Salary'), 
                            html.H2(
                                id='avgSalary',
                                children = []
                                )
                        ]
                    ),
                    html.Div(
                        id="avgYrs",
                        className='quick-container',
                        children=[
                            html.H4('Avg Years At Company'), 
                            html.H2(
                                id='avgYear',
                                children=[]
                            )
                        ]
                    ),
                    
                    ]
                ), 
                html.Div(
                    id="graph-set1",
                    children=[
                        html.Div(
                            id='chart-container',
                            children=[
                                html.H1(
                                    id='chart-header', 
                                    children=[
                                        'Attrition By Education'
                                    ]
                                ),
                                dcc.Graph(
                                    id='fig1', 
                                    figure=None,
                                ),
                            ]
                        ),
                        html.Div(
                            id='chart-container2',
                            children=[
                                html.H1(
                                    id='chart-header2', 
                                    children=[
                                        'Attrition By Age Group'
                                    ]
                                ),
                                dcc.Graph(
                                    id='fig2', 
                                    figure=None
                                )
                            ]
                        )
                        
                    ]
                ),
                html.Div(
                    id="graph-set2",
                    children=[
                        dcc.Graph(
                            id='fig3', 
                            figure=None
                        ),
                        dcc.Graph(
                            id='fig4', 
                            figure=salarySlab_crt
                        )
                    ]
                )
                ]
                ),       
                html.Div(
                    id='aside',
                    children=[
                        html.Div(
                            className='filter-area',
                            children= dcc.Dropdown(
                                placeholder ='Select Department',
                                options=df['Department'].unique(), value=None,
                                id='department-dropdown', 
                            ), 
                            
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    id='dataTable', 
                                    children=[]
                                ),
                                html.Div(
                                    id='gender-stat-wrapper',
                                    children=[
                                        html.H3(
                                            id='gender-stat-title',
                                            children =[
                                                'Attrition By Gender'
                                            ]
                                        ),
                                        html.Div(
                                        id='gender-stat',
                                        children=[
                                            html.Div(
                                                id='female',
                                                children=[
                                                    html.H3('Female'), 
                                                    html.H2(
                                                        children=[
                                                            f'{attrition_gender.loc[attrition_gender['Gender'] == 'Female','EmpID'].item()}'
                                                        ]
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                id='male',
                                                children=[
                                                    html.H3('Male'), 
                                                    html.H2(
                                                        children=[
                                                            f'{attrition_gender.loc[attrition_gender['Gender'] == 'Male','EmpID'].item()}'
                                                        ]
                                                    )
                                                ]
                                            ),
                                        ]
                                    )
                                    ]
                                    ),                                
                                
                            ]
                        )
                    ]
                )
            ]
    )
    ]
)

figuresClass = figures.Figures(df)

@app.callback(
    Output(component_id='totalEmp',component_property='children'),
    Output(component_id='avgSalary',component_property='children'),
    Output(component_id='attrCount',component_property='children'),
    Output(component_id='attrRate',component_property='children'),
    Output(component_id='avgYear',component_property='children'),
    Output(component_id='avgAge',component_property='children'),
    Output(component_id='fig1',component_property='figure'),
    Output(component_id='fig2',component_property='figure'),
    Output(component_id='fig3',component_property='figure'),
    Output(component_id='dataTable',component_property='children'),
    Input(component_id='department-dropdown',component_property='value'),
    allow_duplicate=True
)

def updateValue(value):
    print(value)
    totalEmp = figuresClass.update_total(value)
    avgSalary = figuresClass.update_avgSalary(value)
    avgCount = figuresClass.update_attrCount(value)
    avgRate = figuresClass.update_attrRate(value)
    avgYear = figuresClass.update_avgYear(value)
    avgAge = figuresClass.update_avgAge(value)
    eduChart = figuresClass.update_eduChart(value)
    ageGroup = figuresClass.update_ageGroup(value)
    yearsCompany = figuresClass.update_yearsCompany(value)
    role_table = figuresClass.update_dataTable(value)
    return totalEmp,avgSalary,avgCount,avgRate,avgYear,avgAge,eduChart,ageGroup,yearsCompany,role_table


if __name__ == "__main__":
    app.run_server(debug=True)