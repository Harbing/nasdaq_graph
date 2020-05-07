from flask import Flask
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from neo4j import GraphDatabase


from random import randrange

from flask import Flask, render_template

from pyecharts import options as opts
from pyecharts.charts import Bar
import json
import os


from pyecharts.charts import Graph, Page
from pyecharts.faker import Collector





# 关于 CurrentConfig，可参考 [基本使用-全局变量]
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))

from pyecharts import options as opts
from pyecharts.charts import Bar

driver = GraphDatabase.driver(
            'bolt://localhost:7687', auth=('neo4j', '1'))
        with driver.session() as session:
            result = session.run("MATCH (c:company)" +
                                 " WHERE c.Symbol = $Symbol" +
                                 " CALL apoc.path.subgraphNodes(p,{relationshipFilter:'reference',maxLevel:5,uniqueness:'NODE_GLOBAL'}) YIELD node" +
                                 " return node", Symbol=request.form['Symbol'])

app = Flask(__name__, static_folder="templates")


def graph_weibo() -> Graph:
    with open(os.path.join("fixtures", "BSF_half_forpyecharts_category_resize_sqrt5.json"), "r", encoding="utf-8") as f: # with my json file it cannot take in. Not usre why
        j = json.load(f)
        nodes, links,  categories, cont = j # , mid, userl
    c = (
        Graph()
        .add(
            "",
            nodes,
            links,
            categories,
            repulsion=300,
            linestyle_opts=opts.LineStyleOpts(curve=0.2),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title="Graph-BSD"),
        )
    )
    return c


@app.route("/")
def index():
    c = graph_weibo()
    return Markup(c.render_embed())


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
