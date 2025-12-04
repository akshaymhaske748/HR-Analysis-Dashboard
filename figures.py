import plotly.express as px
import pandas as pd 
from dash import dash_table
class Figures:
    def __init__(self, df):
        self.df = df

    def update_total(self, value):
        # print(type(value))
        if value == None:
            total_emp = self.df['EmpID'].count()  # Count all employees
        else:
            total_emp = self.df[self.df['Department'] == value]['EmpID'].count()  # Filter by department and count
        print(total_emp)
        return total_emp

    def update_avgSalary(self, value):
        if value == None:
            avg_salary = int(self.df['MonthlyIncome'].mean())
        else: 
            avg_salary = int(self.df.loc[self.df['Department'] == value]['MonthlyIncome'].mean())
        
        print(avg_salary)
        return f'€{round(avg_salary/1000, 1)}K'
    
    def update_attrCount(self,value):
        if value == None:
            attrition_count = self.df.loc[self.df['Attrition'] == 'Yes','EmpID'].count()
        else:
            attrition_count = self.df.loc[(self.df['Attrition'] == 'Yes') & (self.df['Department'] == value),'EmpID'].count()
            
        return attrition_count
    
    def update_attrRate(self,value):
        attrRate = float((self.update_attrCount(value)/self.update_total(value)) * 100)
        return round(attrRate,2)
    
    def update_avgAge(self, value):
        if value == None:
            avg_age = int(self.df['Age'].mean())
        else:
            avg_age = int(self.df.loc[self.df['Department'] == value]['Age'].mean())
        return avg_age
    
    
    def update_avgYear(self,value):
        if value == None:
            avg_year = int(self.df['YearsAtCompany'].mean())
        else:
            avg_year = int(self.df.loc[self.df['Department'] == value]['YearsAtCompany'].mean())
        return avg_year
    
    def update_eduChart(self, value):
        edu_cat_color = {
                'Life Sciences' : '#DDB600',
                'Medical' : '#F700A3', 
                'Marketing' : '#0083FF',
                'Technical Degree': '#666666',
                'Other' : '#2A00B4', 
                'Human Resources':'#F86014'
            }
        if value == None:
            education = self.df.groupby(by='EducationField').count()['EmpID'].reset_index()    
        else: 
            education = self.df.loc[self.df['Department'] == value].groupby(by='EducationField').count()['EmpID'].reset_index()    
            
        
        education_crt = px.pie(education,values='EmpID',names='EducationField',hole=0.7,color='EducationField' ,color_discrete_map=edu_cat_color)
        education_crt.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor = '#E6E6E6',
            paper_bgcolor = '#E6E6E6',
            font=dict(
                family='Arial, sans-serif',
                color='#003A9E'
            ),
        )

        education_crt.update_traces(
            textinfo = 'none'
        )
        
        return education_crt
    
    
    def update_yearsCompany(self, value):
        if value == None:
            years_company = self.df.loc[self.df['Attrition'] == 'Yes'].groupby(by='YearsAtCompany').count()['EmpID'].reset_index()
        else:
            years_company = self.df.loc[(self.df['Attrition'] == 'Yes') & (self.df['Department'] == value)].groupby(by='YearsAtCompany').count()['EmpID'].reset_index()

        companyYears_crt = px.line(years_company,x='YearsAtCompany',y='EmpID')
        companyYears_crt.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor = '#E6E6E6',
            paper_bgcolor = '#E6E6E6',
            font=dict(
                family='Arial, sans-serif',
                color='#003A9E'
            ),
        )
        companyYears_crt.update_traces(
            fill='tozeroy', 
            fillcolor='#8E8FAA',
            textfont=dict(
                family='Arial, sans-serif',
                size=12,
                color='white'  # Set text color
            ),
            line=dict(
                width=3, 
                color='#003A9E'
                )
        )
        companyYears_crt.update_xaxes(
            linecolor='#E6E6E6',  # Set x-axis line color
            linewidth=2,  
            showgrid=False,
            title=None
        )
        companyYears_crt.update_yaxes(
            showgrid=False,
            linecolor='#E6E6E6',  # Set x-axis line color
            linewidth=2,  
            title=None
        )
        
        return companyYears_crt
    
    def update_ageGroup(self, value):
        if value == None:
            age_group = self.df.groupby(by='AgeGroup').count()['EmpID'].reset_index()
        else:
            age_group = self.df.loc[self.df['Department'] == value].groupby(by='AgeGroup').count()['EmpID'].reset_index()
        
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
        
        return age_group_crt
    
    def update_dataTable(self,value):
        if value == None:
            roles_agg = self.df.loc[self.df['Attrition'] == 'Yes'].groupby(['JobRole', 'JobSatisfaction']).size().reset_index(name='Count')
        else:
            roles_agg = self.df.loc[(self.df['Department'] == value) & (self.df['Attrition'] == 'Yes')].groupby(['JobRole', 'JobSatisfaction']).size().reset_index(name='Count')
        
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
        roleTable = dash_table.DataTable(
                                    columns=[{"name": f'{i}', "id": f'{i}'} for i in pivot_table.columns],
                                    data=pivot_table.to_dict('records'),
                                    style_cell={'textAlign': 'left', 'padding': '10px 5px'},
                                ),
        return roleTable