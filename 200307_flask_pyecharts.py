#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as pd
import json
from neo4j import GraphDatabase

from flask import Flask
import numpy as np
from random import randrange

from flask import Flask, render_template
# pyechart imports
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import CurrentConfig
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.charts import Graph, Page
from pyecharts.faker import Collector

from pyecharts import options as opts
from pyecharts.charts import Bar

# 关于 CurrentConfig，可参考 [基本使用-全局变量]
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))





C = Collector()
app = Flask(__name__, static_folder="templates")


# In[18]:


#@C.funcs

def graph_SP(nodes, links, categories) -> Graph:
        

    b = (
        Graph()
        .add(
            "Name: ",
            nodes,
            links,
            categories,
            repulsion=300,
            linestyle_opts=opts.LineStyleOpts(curve=0),
            label_opts=opts.LabelOpts(is_show=False),
            
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title="Graph-BSD"),


        )
    )
    return b



# In[19]:


# get links

def get_links(company, driver):
    
    with driver.session() as session:
        p = session.run(
            "MATCH p=(s:shareholder)-[h:holds ]->(n:company) where n.Symbol='"+company+"' return p"
            #" MATCH (n:company) WHERE n.Symbol = '"+company+"' RETURN n"

                )
        #print(p.value()[0])
        company_result = p.values()
        

    
    return company_result






# In[22]:



@app.route("/")
def index():
    
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', '1'))# not sure why ram cannot be released. See if it is due to the driver.




    company = 'MMM'

    
    company_result =get_links(company, driver)# now the data format is a string list
    
    nodes = []
    links = []
    for relationship in company_result:# get each individual string
        start = relationship[0].start # the tuple structure of this string can be disseminated in to start and end. It seems to be the built in function of neo4J
        end = relationship[0].end
        start_parsed = [json.loads(str(start).split("properties=")[1].split(">")[0].replace("'",'"').replace('\\', ''))] # parsing string into dict
        end_parsed = [json.loads(str(end).split("properties=")[1].split(">")[0].replace("'",'"').replace('\\', ''))]

        nodes.append(start_parsed[0])
        links.append({"source":start_parsed[0]["Stakeholder"], "target": end_parsed[0]["Symbol"]})
    
    #company_parsed = [json.loads(str(company_result).split("properties=")[1].split(">")[0].replace("'",'"').replace('\\', ''))]
    

    categories = []
    c = graph_SP(nodes, links, categories)
    
    
    
    return Markup(c.render_embed())
    


# In[24]:



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', use_reloader=False)


# In[ ]:




