from bokeh.io import output_file, show
from selenium import webdriver
from bokeh.palettes import GnBu3, OrRd3
from bokeh.plotting import figure,show
from bokeh.models import ColumnDataSource
from bokeh.io import export_png

# 导入颜色模块

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
years = ["2015", "2016", "2017"]
exports = {'fruits' : fruits,
           '2015'   : [2, 1, 4, 3, 2, 4],
           '2016'   : [5, 3, 4, 2, 4, 6],
           '2017'   : [3, 2, 4, 4, 5, 3]}
imports = {'fruits' : fruits,
           '2015'   : [-1, 0, -1, -3, -2, -1],
           '2016'   : [-2, -1, -3, -1, -2, -2],
           '2017'   : [-1, -2, -1, 0, -2, -2]}

p = figure(y_range=fruits, plot_height=350, x_range=(-16, 16), title="图书馆/课程次数对比图")

p.hbar_stack(years, y='fruits', height=0.9, color=GnBu3, source=ColumnDataSource(exports),
             legend=["%s exports" % x for x in years])      # 绘制出口数据堆叠图

p.hbar_stack(years, y='fruits', height=0.9, color=OrRd3, source=ColumnDataSource(imports),
             legend=["%s imports" % x for x in years])      # 绘制进口数据堆叠图，这里值为负值

p.y_range.range_padding = 0.2     # 调整边界间隔
p.ygrid.grid_line_color = None   
p.legend.location = "top_left"
p.axis.minor_tick_line_color = None
p.outline_line_color = None
export_png(p, filename="a.png")
show(p)