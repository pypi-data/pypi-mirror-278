# Author: Yu-Xin Tian, 2024-6-11 Version 0.0.1

from sympy import *
import numpy as np
import os, pickle
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import copy
import matplotlib.ticker as ticker
from matplotlib import rcParams

from IPython.display import display
from IPython.display import Math
from sympy.printing import latex

import string

def gen_letters(nums):
    # 生成大写字母
    uppercase_letters = string.ascii_uppercase

    # 列出36个大写字母
    letters = []
    for i in range(nums):
        if i < 26:
            letters.append(uppercase_letters[i])
        else:
            div, mod = divmod(i - 26, 26)
            letters.append(uppercase_letters[div] + uppercase_letters[mod])
    return letters


def gen_romans(nums):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
        ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
        ]
    roman_lists = []
    for num in range(1, nums+1):
        roman_num = ''
        i = 0
        while num > 0:
            for _ in range(num // val[i]):
                roman_num += syb[i]
                num -= val[i]
            i += 1
        roman_lists.append(roman_num)
    return roman_lists


def mathshow(latex_code):
    display(Math(latex_code) )


def showlatex(sym):
    print(latex(sym, mode='inline'))


def mathprint(sym):
    mathshow(latex(sym))


config = {
    "font.family":'serif',
    "font.size": 12,
    "mathtext.fontset":'stix',
    "font.serif": ['SimSun'],
}
rcParams.update(config)
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

c_list = ['blue', 'gold', 'green', 'red', 'darkgoldenrod', 'darkcyan', 'indigo',
          'chocolate', 'olivedrab', 'teal', 'navy', 'firebrick','darkgreen', 'purple', 'cadetblue']
m_list = ['o','s', '*', 'P', 'X', 'D', 'p', 'x', '8', '2', 'H', '+', '|', '<', '>', '^', 'v', ',']
ls_list = ['-', (0, (1, 10)), (0, (5, 10)),'-.','--', ':', (0, (3, 10, 1, 10, 1, 10)), (5, (10, 3)), (0, (5, 5)), (0, (5, 1))]
locations = {
    'best': 0,
    'northeast': 1,
    'northwest': 2,
    'southwest':3,
    'southeast':4,
    'east':7,
    'west':6,
    'south':8,
    'north':9,
    'center':10
}

def exist_file(file_dir):
    return os.path.exists(file_dir)


def save_var(the_var, file_dir):
    with open(file_dir, 'wb') as f:
        pickle.dump(the_var, f)


def get_var(file_dir):
    if not exist_file(file_dir):
        print('文件不存在！')
        return
    else:
        with open(file_dir, 'rb') as f:
            loaded_var = pickle.load(f)
        return loaded_var


def data_lines(data, label_x=None, x_name=None, y_name=None, save_dir=None,
               location='best', ncol=1, fsize=14, figsize=[5, 4], xt_rotation=0,
               xrotation=0, yrotation=90, linestyles=None, linewidth=1, markers=m_list, markersize=3.5,colors=c_list,
               isgrid=False, xpad=3, ypad=3, xlabelpad=3, ylabelpad=3):
    """
    - data: 传入的数据，列表或np.array均可。（必须）
    - label_x: 横轴刻度标签，默认连续数字。
    - x_name: 横轴名称标签，默认'$x$'。
    - y_name: 纵轴名称标签，默认'$y$'。
    - save_dir=None: 图片保存路径，字符串。默认None，不保存。
    - location: 图例的方位，可以选填的内容有'best','northeast','northwest','southwest','southeast','east','west','south','north','center'。默认值为'best'，表示自动安排至合适的位置。
    - ncol: 图例的列数，默认为1列，即竖着排布。
    - fsize: 图片中字号的大小，默认值为14。
    - figsize: 图片的大小，写成`[宽, 高]`的形式。默认为`[5, 4]`。
    - xt_rotation: 横轴刻度标签旋转角度。用于刻度为年份，横着挤不下的情况，可以设成45度，错开排布。默认不旋转，即0度。
    - xrotation: 横轴名字标签旋转角度，默认值0，基本不需要动。
    - yrotation: 纵轴名字标签旋转角度，默认值90，字是正的。如果y轴的名字较长，不好看，可以设成0，字是竖倒着写的，紧贴y轴，但看的话需要歪脖子，专治脊椎不好使哈。
    - linestyles: 一组线的形状，`[]`列表形式去写，在多线图中用于按顺序制定每个线的形状。如实线'-'，点横线'-.'，虚线'--'，点线':'。默认值为None，表示取工具内的线型列表`ls_list`得第一个，即实线'-'。
      本工具中提供的线型列表如下：
      ``ls_list = ['-', (0, (1, 10)), (0, (5, 10)),'-.','--', ':', (0, (3, 10, 1, 10, 1, 10)), (5, (10, 3)), (0, (5, 5)), (0, (5, 1))]``
      关于线型的详细说明：
         https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html#linestyles

    - linewidth: 线粗。字面意思，没啥好说的，默认值为1。
    - markers: 一组标记符号，`[]`列表形式去写，在多线图中用于按顺序制定每个线的标记符号。工具内的标记符号列表`m_list`。如果只有一条线，就取`m_list`中的第一个，即圆点'o'。
      本工具中提供的标记符号列表如下：
      ``m_list = ['o','s', '*', 'P', 'X', 'D', 'p', 'x', '8', '2', 'H', '+', '|', '<', '>', '^', 'v', ',']``
      关于标记符号的详细说明：
          https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers

    - markersize: 标记符号的大小，默认3.5。
    - colors: 一组颜色，`[]`列表形式去写，在多线图中用于按顺序制定每个线的颜色（包含标记符号的颜色）。工具内的颜色列表`c_list`。如果只有一条线，就取`c_list`中的第一个，即蓝色'blue'。
      本工具中提供的颜色列表如下：
      ``c_list = ['blue', 'gold', 'green', 'red', 'darkgoldenrod', 'darkcyan', 'indigo',
              'chocolate', 'olivedrab', 'teal', 'navy', 'firebrick','darkgreen', 'purple', 'cadetblue']``
      关于颜色的详细说明：
        https://matplotlib.org/stable/gallery/color/named_colors.html#base-colors
    - isgrid: 是否要网格。要就填True，不要就是False，默认不要。
    - xpad=3, ypad=3, xlabelpad=3, ylabelpad=3: 分别为横轴刻度值距离横轴的距离、纵轴刻度值距离纵轴的距离、横轴名字标签距离横轴刻度的距离、纵轴名字标签距离纵轴刻度的距离。默认值3,3,3,3。如果挤了不好看了，再微调此参数，一般不用动。
    """
    fig, ax = plt.subplots(figsize=figsize)
    plt.xticks(fontsize=fsize - 1, fontname='times new roman', rotation = xt_rotation)
    plt.yticks(fontsize=fsize - 1, fontname='times new roman')

    data_names = list(data.keys())
    data_num = len(data_names)

    the_x = [i+1 for i in range(len(data[data_names[0]]))]
        
    plt.xlim(the_x[0], the_x[1])
    
    if x_name is None:
        x_name = '$x$'
    
    if len(the_x) > 10:
        labelevery = int(len(the_x)/10)
    else:
        labelevery = 1
            
    if label_x is None:
        label_x = []
            
        for i_, x_ in enumerate(the_x):
            if i_ % labelevery == 0:
                label_x.append(str(x_))
            else:
                label_x.append('')
    else:
        for i_, _ in enumerate(the_x):
            if i_ % labelevery != 0:
                label_x[i_] = ''
            else:
                label_x[i_] = str(label_x[i_])

    ax.set_xticks(the_x)
    ax.set_xticklabels(label_x, fontsize=fsize-1, fontname = 'times new roman')

    if data_num == 1:
        if y_name is None:
            y_name = data_names[0]
        ys = data[data_names[0]]
        ax.plot(the_x, ys, linestyle='-', c='k', linewidth=linewidth, marker='o', markersize=markersize)
        y_min = np.min(ys)
        y_max = np.max(ys)
    else:
        if y_name is None:
            y_name = '$y$'
        for j, em in enumerate(data_names):
            if linestyles is None:
                the_ls = '-'
            else:
                the_ls = linestyles[j]
                
            ys = data[em]
            
            if len(the_x) > 10:
                markevery = int(len(the_x)/10)
                ax.plot(the_x, ys, linestyle=the_ls, c=colors[j], linewidth=linewidth, marker=markers[j], markersize=markersize, markevery = markevery, label=em)
            else:
                ax.plot(the_x, ys, linestyle=the_ls, c=colors[j], linewidth=linewidth, marker=markers[j], markersize=markersize,label=em)
                
            y_min_now = np.min(ys)
            y_max_now = np.max(ys)
            if j ==0:
                y_max = y_max_now
                y_min = y_min_now
            else:
                if y_max_now > y_max:
                    y_max = y_max_now
                if y_min_now < y_min:
                    y_min = y_min_now
            
    judge_y = max(abs(y_max),abs(y_min))
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    if judge_y >= 5000:
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0),useMathText=True)

    if data_num >1:
        ax.legend(loc=locations[location], fontsize=fsize - 1, ncol=ncol)

    ax.set_ylabel(y_name, fontsize=fsize, fontweight='bold', rotation=yrotation, labelpad=ylabelpad)
    ax.set_xlabel(x_name, fontsize=fsize, fontweight='bold', rotation=xrotation, labelpad=xlabelpad)

    # 设置刻度
    ax.tick_params(axis='x', direction='in', pad=xpad)
    ax.tick_params(axis='y', direction='in', pad=ypad)

    ax.grid(isgrid)

    fig.tight_layout()
    if save_dir is not None:
        if save_dir[-4:] == '.svg':
            plt.savefig(save_dir)
        else:
            plt.savefig(save_dir, dpi=600)
    return plt


def draw_lines(expressions, assigns, the_var, ranges, x_name, y_name, save_dir=None, location='best', ncol=1, fsize=14, figsize=[5, 4],
           xt_rotation=0, xrotation=0, yrotation=90, linestyles=None, linewidth=1, markers=m_list, markersize=3.5, colors=c_list,
           isgrid=False, x_lim=None, y_lim=None, xpad=3, ypad=3, xlabelpad=3, ylabelpad=3):
    """
    - expressions: Symbol表达式，字典形式传入。（必须）
    - assigns: 表达式参数赋值，字典形式。
    - the_var: 要分析的参数；
    - ranges: 要分析的参数的取值。[初始,结束,间隔]
    - x_name: 横轴名称标签，默认'$x$'。
    - y_name: 纵轴名称标签，默认'$y$'。
    - save_dir=None: 图片保存路径，字符串。默认None，不保存。
    - location: 图例的方位，可以选填的内容有'best','northeast','northwest','southwest','southeast','east','west','south','north','center'。默认值为'best'，表示自动安排至合适的位置。
    - ncol: 图例的列数，默认为1列，即竖着排布。
    - fsize: 图片中字号的大小，默认值为14。
    - figsize: 图片的大小，写成`[宽, 高]`的形式。默认为`[5, 4]`。
    - xt_rotation: 横轴刻度标签旋转角度。用于刻度为年份，横着挤不下的情况，可以设成45度，错开排布。默认不旋转，即0度。
    - xrotation: 横轴名字标签旋转角度，默认值0，基本不需要动。
    - yrotation: 纵轴名字标签旋转角度，默认值90，字是正的。如果y轴的名字较长，不好看，可以设成0，字是竖倒着写的，紧贴y轴，但看的话需要歪脖子，专治脊椎不好使哈。
    - linestyles: 一组线的形状，`[]`列表形式去写，在多线图中用于按顺序制定每个线的形状。如实线'-'，点横线'-.'，虚线'--'，点线':'。默认值为None，表示取工具内的线型列表`ls_list`得第一个，即实线'-'。
      本工具中提供的线型列表如下：
      ``ls_list = ['-', (0, (1, 10)), (0, (5, 10)),'-.','--', ':', (0, (3, 10, 1, 10, 1, 10)), (5, (10, 3)), (0, (5, 5)), (0, (5, 1))]``
      关于线型的详细说明：
         https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html#linestyles
    - linewidth: 线粗。字面意思，没啥好说的，默认值为1。
    - markers: 一组标记符号，`[]`列表形式去写，在多线图中用于按顺序制定每个线的标记符号。工具内的标记符号列表`m_list`。如果只有一条线，就取`m_list`中的第一个，即圆点'o'。
      本工具中提供的标记符号列表如下：
      ``m_list = ['o','s', '*', 'P', 'X', 'D', 'p', 'x', '8', '2', 'H', '+', '|', '<', '>', '^', 'v', ',']``
      关于标记符号的详细说明
           https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers

    - markersize: 标记符号的大小，默认3.5。
    - colors: 一组颜色，`[]`列表形式去写，在多线图中用于按顺序制定每个线的颜色（包含标记符号的颜色）。工具内的颜色列表`c_list`。如果只有一条线，就取`c_list`中的第一个，即蓝色'blue'。
      本工具中提供的颜色列表如下：
      ``c_list = ['blue', 'gold', 'green', 'red', 'darkgoldenrod', 'darkcyan', 'indigo',
              'chocolate', 'olivedrab', 'teal', 'navy', 'firebrick','darkgreen', 'purple', 'cadetblue']``
      关于颜色的详细说明：
         https://matplotlib.org/stable/gallery/color/named_colors.html#base-colors

    - isgrid: 是否要网格。要就填True，不要就是False，默认不要。
    - xpad=3, ypad=3, xlabelpad=3, ylabelpad=3: 分别为横轴刻度值距离横轴的距离、纵轴刻度值距离纵轴的距离、横轴名字标签距离横轴刻度的距离、纵轴名字标签距离纵轴刻度的距离。默认值3,3,3,3。如果挤了不好看了，再微调此参数，一般不用动。
    - x_lim: 横轴显示的范围，以`[起始值,结束值]`的形式去写。默认None，根据数据自动安排。除非不好看再调，一般不动该参数。
    - y_lim: 纵轴显示的范围，以`[起始值,结束值]`的形式去写。默认None，根据数据自动安排。除非不好看再调，一般不动该参数。举个例子，“2.2 画单条曲线图”部分不太好看：
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_ylabel(y_name, fontsize=fsize, fontweight='bold', rotation=yrotation, labelpad=ylabelpad)
    ax.set_xlabel(x_name, fontsize=fsize, fontweight='bold', rotation=xrotation, labelpad=xlabelpad)

    plt.xticks(fontsize=fsize - 1, fontname='times new roman', rotation = xt_rotation)
    plt.yticks(fontsize=fsize - 1, fontname='times new roman')

    exp_names = list(expressions.keys())
    exp_num = len(exp_names)
    
    ranges_ = [ranges[0], ranges[1]+ranges[2], ranges[2]]
    if x_lim is None:
        plt.xlim(ranges[0], ranges[1])
    else:
        plt.xlim(x_lim[0], x_lim[1])
     
    if y_lim is not None:
        plt.ylim(y_lim[0], y_lim[1])

    if exp_num == 1:
        xs = []
        ys = []
        the_exp = expressions[exp_names[0]]
        assigned_exp = the_exp.subs(assigns)
        for i in np.arange(*ranges_):
            xs.append(i)
            ys.append(assigned_exp.subs({the_var:i}).evalf())
        ax.plot(xs, ys, linestyle='-', c='k', linewidth=linewidth, marker=None)
        y_min = np.min(ys)
        y_max = np.max(ys)
    else:
        for j, em in enumerate(exp_names):
            xs = []
            ys = []
            the_exp = expressions[exp_names[j]]
            assigned_exp = the_exp.subs(assigns)
            for i in np.arange(*ranges_):
                xs.append(i)
                ys.append(assigned_exp.subs({the_var: i}).evalf())

            if linestyles is None:
                the_ls = '-'
            else:
                the_ls = linestyles[j]
            
            if len(xs) > 10:
                markevery = int(len(xs)/10)
                ax.plot(xs, ys, linestyle=the_ls, c=colors[j], linewidth=linewidth, marker=markers[j], markersize=markersize, markevery = markevery, label=em)
            else:
                ax.plot(xs, ys, linestyle=the_ls, c=colors[j], linewidth=linewidth, marker=markers[j], markersize=markersize,label=em)
                
                
            y_min_now = np.min(ys)
            y_max_now = np.max(ys)
            if j ==0:
                y_max = y_max_now
                y_min = y_min_now
            else:
                if y_max_now > y_max:
                    y_max = y_max_now
                if y_min_now < y_min:
                    y_min = y_min_now
            
    judge_y = max(abs(y_max),abs(y_min))
    judge_x = max(abs(np.max(xs)),abs(np.min(xs)))
    if judge_y >= 5000:
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0), useMathText=True)
    if judge_x >= 5000:
        plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0), useMathText=True)

    # 设置刻度
    ax.tick_params(axis='x', direction='in', pad=xpad)
    ax.tick_params(axis='y', direction='in', pad=ypad)

    if exp_num >1:
        ax.legend(loc=locations[location], fontsize=fsize - 1, ncol=ncol)
    ax.grid(isgrid)

    fig.tight_layout()
    if save_dir is not None:
        if save_dir[-4:] == '.svg':
            plt.savefig(save_dir)
        else:
            plt.savefig(save_dir, dpi=600)
    return plt


def draw_3D(expressions, assigns, the_var_x, start_end_x, the_var_y, start_end_y,
            x_name, y_name, z_name, save_dir=None, color_alpha=0.8, linestyles=ls_list,
            linewidth=0.2, location='best', ncol=1, fsize=14, figsize=[7, 5],
            precision=1000, xrotation=0, yrotation=0, zrotation=90, isgrid=True, density=100,
            colors=c_list, edgecolor=None, x_lim=None, y_lim=None, z_lim=None, elevation=15,
            azimuth=45, roll=0, left_margin=0, bottom_margin=0, right_margin=1,
            top_margin=1, xpad=1, ypad=1, zpad=5, xlabelpad=2, ylabelpad=2, zlabelpad=12):
    """
    - expressions: Symbol表达式，字典形式传入。（必须）
    - assigns: 表达式参数赋值，字典形式。
    - the_var_x/the_var_y: 要分析的参数1/2；
    - start_end_x/start_end_y: 要分析的参数1/2的取值。[初始,结束]
    - x_name: x轴名称标签，默认'$x$'。
    - y_name: y轴名称标签，默认'$y$'。
    - z_name: z轴名称标签，默认'$z$'。
    - save_dir=None: 图片保存路径，字符串。默认None，不保存。
    - color_alpha: 曲面的透明度。取值范围0到1，浮点数。0表示全透明，1表示完全不透明。默认取0.8。
    - linestyles: 一组线的形状，`[]`列表形式去写，在多线图中用于按顺序制定每个线的形状。如实线'-'，点横线'-.'，虚线'--'，点线':'。默认值为None，表示取工具内的线型列表`ls_list`得第一个，即实线'-'。
      本工具中提供的线型列表如下：
      ``ls_list = ['-', (0, (1, 10)), (0, (5, 10)),'-.','--', ':', (0, (3, 10, 1, 10, 1, 10)), (5, (10, 3)), (0, (5, 5)), (0, (5, 1))]``
      关于线型的详细说明：
          https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html#linestyles

    - linewidth: 线粗。字面意思，没啥好说的，默认值为1。
    - location: 图例的方位，可以选填的内容有'best','northeast','northwest','southwest','southeast','east','west','south','north','center'。默认值为'best'，表示自动安排至合适的位置。
    - ncol: 图例的列数，默认为1列，即竖着排布。
    - fsize: 图片中字号的大小，默认值为14。
    - figsize: 图片的大小，写成`[宽, 高]`的形式。默认为`[5, 4]`。
    - precision: 绘画的精细程度。默认取1000，表示画 $1000 \times 1000$ 个点。该值越大，运行速度越慢，太大没必要，根据个人情况权衡。
    - xrotation/yrotation: x/y轴名字标签旋转角度，默认值0，基本不需要动。
    - zrotation: Z轴名字标签旋转角度，默认值90，字是正的。如果Z轴的名字较长，不好看，可以设成0，字是竖倒着写的，紧贴Z轴，但看的话需要歪脖子，专治脊椎不好使哈。
    - colors: 一组颜色，`[]`列表形式去写，在多线图中用于按顺序制定每个线的颜色（包含标记符号的颜色）。工具内的颜色列表`c_list`。如果只有一条线，就取`c_list`中的第一个，即蓝色'blue'。
      本工具中提供的颜色列表如下：
      ``c_list = ['blue', 'gold', 'green', 'red', 'darkgoldenrod', 'darkcyan', 'indigo',
              'chocolate', 'olivedrab', 'teal', 'navy', 'firebrick','darkgreen', 'purple', 'cadetblue']``
      关于颜色的详细说明：
          https://matplotlib.org/stable/gallery/color/named_colors.html#base-colors
    - isgrid: 是否要网格。要就填True，不要就是False，默认不要。
    - xpad=3, ypad=3, xlabelpad=3, ylabelpad=3: 分别为横轴刻度值距离横轴的距离、纵轴刻度值距离纵轴的距离、横轴名字标签距离横轴刻度的距离、纵轴名字标签距离纵轴刻度的距离。默认值3,3,3,3。如果挤了不好看了，再微调此参数，一般不用动。
    - x_lim: 横轴显示的范围，以`[起始值,结束值]`的形式去写。默认None，根据数据自动安排。除非不好看再调，一般不动该参数。
    - y_lim: 纵轴显示的范围，以`[起始值,结束值]`的形式去写。默认None，根据数据自动安排。除非不好看再调，一般不动该参数。举个例子，“2.2 画单条曲线图”部分不太好看：

    - edgecolor: 曲面上线框的颜色。若为None，则曲面上不画线。当该参数不为None时，参数`linestyles`，`linewidth`和`density`才起作用。
    - density: 曲面上画线的密度，也就是曲面横纵方向各画多少根线。默认100。
    - elevation: 仰角 (elevation)。定义了观察者与 xy 平面之间的夹角，也就是观察者与 xy 平面之间的旋转角度。当elevation为正值时，观察者向上倾斜，负值则表示向下倾斜。默认15度。可根据美观与否微调。
    - azimuth: 方位角 (azimuth)。定义了观察者绕 z 轴旋转的角度。它决定了观察者在 xy 平面上的位置。azim 的角度范围是 −180 到 180 度，其中正值表示逆时针旋转，负值表示顺时针。默认45度。可根据美观与否微调。
    - roll: 滚动角 (roll)。 定义了绕观察者视线方向旋转的角度。它决定了观察者的头部倾斜程。默认0度，不需要动。
    - left_margin=0, bottom_margin=0, right_margin=1, top_margin=1: 左、下、右、上的图片留白，默认分别为0,0,1,1。不需要动，除非不好看。

    """

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(left=left_margin, bottom=bottom_margin, right=right_margin, top=top_margin)
    plt.xticks(fontsize=fsize - 1, fontname='times new roman')
    plt.yticks(fontsize=fsize - 1, fontname='times new roman')

    ax.yaxis.set_rotate_label(False)
    ax.xaxis.set_rotate_label(False)
    ax.zaxis.set_rotate_label(False)
    ax.set_ylabel(y_name, fontsize=fsize, fontweight='bold', rotation=yrotation, labelpad=ylabelpad)
    ax.set_xlabel(x_name, fontsize=fsize, fontweight='bold', rotation=xrotation, labelpad=xlabelpad)
    ax.set_zlabel(z_name, fontsize=fsize, fontweight='bold', rotation=zrotation, labelpad=zlabelpad)

    # 设置刻度
    ax.tick_params(axis='x', direction='in', pad=xpad)
    ax.tick_params(axis='y', direction='in', pad=ypad)
    ax.tick_params(axis='z', direction='in', pad=zpad)

    # Define the range for x and y
    x_ = np.linspace(start_end_x[0], start_end_x[1], precision)
    y_ = np.linspace(start_end_y[0], start_end_y[1], precision)
    x, y = np.meshgrid(x_, y_)

    exp_names = list(expressions.keys())
    exp_num = len(exp_names)

    if len(x_) > density:
        rstride = int(len(x_) / density)
    else:
        rstride = 1

    if len(y_) > density:
        cstride = int(len(y_) / density)
    else:
        cstride = 1

    if exp_num == 1:
        the_exp = expressions[exp_names[0]]
        assigned_exp = the_exp.subs(assigns)
        the_func = lambdify((the_var_x, the_var_y), assigned_exp, 'numpy')
        z = the_func(x, y)
        if isinstance(z, float):
            z = np.ones(x.shape, dtype=float) * z
        ax.plot_surface(x, y, z, color=colors[0], edgecolor=None, alpha=color_alpha)
        z_min = np.min(z)
        z_max = np.max(z)
    else:
        legend_elements = []
        his_zs = []

        get_order_func = lambda x_, y_: covert_orders(expressions=expressions, assigns=assigns,
                                              the_var1=the_var_x, the_var2=the_var_y,
                                              X=x_, Y=y_, reverse=False) # 越来越大
        Z_judge, _, map_order = get_order_func(x, y)  # value: relationship

        remove_values = []
        use_values = []
        dropout = 0.01
        for em in map_order.keys():
            count = np.count_nonzero(Z_judge == em)
            if count / (precision ** 2) <= dropout:
                remove_values.append(em)
            else:
                use_values.append(em)

        for em in remove_values:
            indices = np.where(Z_judge == em)
            rows, cols = indices
            for row, col in zip(rows, cols):
                if (col < precision - 1) and (Z_judge[row, col] in remove_values):
                    for c_add in range(1, precision - col):
                        try_value = Z_judge[row, col + c_add]
                        if try_value not in remove_values:
                            Z_judge[row, col] = try_value
                            break
                if (col >= precision - 1) and (Z_judge[row, col] in remove_values):
                    for c_add in range(1, col):
                        try_value = Z_judge[row, col - c_add]
                        if try_value not in remove_values:
                            Z_judge[row, col] = try_value
                            break
                if (row < precision - 1) and (Z_judge[row, col] in remove_values):
                    for r_add in range(1, precision - row):
                        try_value = Z_judge[row + r_add, col]
                        if try_value not in remove_values:
                            Z_judge[row, col] = try_value
                            break
                if (row >= precision - 1) and (Z_judge[row, col] in remove_values):
                    for r_add in range(1, row):
                        try_value = Z_judge[row - r_add, col]
                        if try_value not in remove_values:
                            Z_judge[row, col] = try_value
                            break


        for j, em in enumerate(exp_names):
            the_exp = expressions[exp_names[j]]
            assigned_exp = the_exp.subs(assigns)
            the_func = lambdify((the_var_x, the_var_y), assigned_exp, 'numpy')
            z = the_func(x, y)
            if isinstance(z, float):
                z = np.ones(x.shape, dtype=float) * z

            legend_elements.append(Patch(facecolor=colors[j], edgecolor=edgecolor, alpha=color_alpha,
                                         label=em, linestyle=linestyles[j], linewidth = linewidth))
            his_zs.append(z)

            z_min_now = np.min(z)
            z_max_now = np.max(z)
            if j == 0:
                z_max = z_max_now
                z_min = z_min_now
            else:
                if z_max_now > z_max:
                    z_max = z_max_now
                if z_min_now < z_min:
                    z_min = z_min_now

        for key_ in use_values:
            value_ = map_order[key_]
            #print(key_, value_)
            # 画图区域
            mask = (Z_judge==key_)
            for the_order in value_:
                # 按顺序画
                the_z = copy.deepcopy(his_zs[the_order])
                the_z = the_z.astype(float)
                the_z[~mask] = np.nan

                ax.plot_surface(x, y, the_z, color=colors[the_order], alpha=color_alpha, edgecolor=edgecolor,
                                linestyle=ls_list[the_order], linewidth=linewidth, rstride=rstride, cstride=cstride)
                del the_z

    ax.view_init(elev=elevation, azim=azimuth, roll=roll)

    ax.set_zticks(np.linspace(z_min, z_max, 10))
    for label in ax.get_zticklabels():
        label.set_fontname('Times New Roman')
        label.set_fontsize(fsize - 1)

    judge = abs(z_max - z_min)
    if judge < 0.0001:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.5f'))
    elif judge < 0.001:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.4f'))
    elif judge < 0.01:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))
    elif judge < 1:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
    elif judge >= 1 and judge < 10:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    else:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.0f'))

    if exp_num > 1:
        ax.legend(handles=legend_elements, loc=locations[location], fontsize=fsize - 1, ncol=ncol)

    ax.grid(isgrid)

    if x_lim is None:
        ax.set_xlim(start_end_x[1], start_end_x[0])
    else:
        ax.set_xlim(x_lim[0], x_lim[1])

    if y_lim is None:
        ax.set_ylim(start_end_y[0], start_end_y[1])
    else:
        ax.set_ylim(y_lim[0], y_lim[1])

    if z_lim is not None:
        ax.set_zlim(z_lim[0], z_lim[1])

    # fig.tight_layout()
    if save_dir is not None:
        if save_dir[-4:] == '.svg':
            plt.savefig(save_dir)
        else:
            plt.savefig(save_dir, dpi=600)
    return plt


def who_max(expressions, assigns, the_var1, the_var2, X, Y):
    exp_names = list(expressions.keys())
    exp_num = len(exp_names)

    res_list = []
    for i in range(exp_num):
        the_exp = expressions[exp_names[i]]
        assigned_exp = the_exp.subs(assigns)
        the_func = lambdify((the_var1, the_var2), assigned_exp, 'numpy')
        exp_value = the_func(X, Y)
        if isinstance(exp_value, float):
            exp_value = np.ones(X.shape, dtype=float)*exp_value
        res_list.append(exp_value)

    Z_list = []
    for ii in range(len(res_list[0])):
        tmp = []
        for jj in range(len(res_list[0][0])):
            _index = np.argmax([em[ii][jj] for em in res_list])
            tmp.append(_index)
        Z_list.append(tmp)

    return np.array(Z_list)


def who_max_point(expressions, assigns, the_var1, the_var2, _x, _y):
    exp_names = list(expressions.keys())
    exp_num = len(exp_names)

    Z_list = []
    for i in range(exp_num):
        the_exp = expressions[exp_names[i]]
        assigned_exp = the_exp.subs(assigns)
        exp_value = assigned_exp.subs({the_var1: _x, the_var2: _y})
        Z_list.append(exp_value.evalf())
    Z_index = np.argmax(Z_list)
    return Z_index


def order_types(exp_names, values, reverse=True):
    return_val = ""
    # 获取排序后元素的索引 reverse=True默认降序
    sorted_indices = sorted(range(len(values)), key=lambda x: values[x], reverse=reverse)
    for _i, em in enumerate(sorted_indices):
        if reverse:
            if _i == 0:
                last_value = values[em]
                return_val += r"$" + exp_names[em][1:-1]
            else:
                cur_value = values[em]
                if cur_value == last_value:
                    return_val += r" = " + exp_names[em][1:-1]
                else:
                    return_val += r" > " + exp_names[em][1:-1]
                last_value = cur_value
        else:
            if _i == 0:
                last_value = values[em]
                return_val += r"$" + exp_names[em][1:-1]
            else:
                cur_value = values[em]
                if cur_value == last_value:
                    return_val += r" = " + exp_names[em][1:-1]
                else:
                    return_val += r" < " + exp_names[em][1:-1]
                last_value = cur_value
    return return_val + r"$", sorted_indices


def covert_orders(expressions, assigns, the_var1, the_var2, X, Y, reverse=True):
    exp_names = list(expressions.keys())
    exp_num = len(exp_names)
    map_dict = {}  # value: relationship
    map_order = {}  # value: order

    res_list = []
    for i in range(exp_num):
        the_exp = expressions[exp_names[i]]
        assigned_exp = the_exp.subs(assigns)
        the_func = lambdify((the_var1, the_var2), assigned_exp, 'numpy')
        exp_value = the_func(X, Y)
        if isinstance(exp_value, float):
            exp_value = np.ones(X.shape, dtype=float) * exp_value
        res_list.append(exp_value)

    value_ldata = []
    index_point = 0
    for ii in range(len(res_list[0])):
        tmp = []
        for jj in range(len(res_list[0][0])):
            compare_list = [em[ii][jj] for em in res_list]
            latex_res, the_order = order_types(exp_names, compare_list, reverse=reverse)
            if latex_res not in map_dict.values():
                map_dict[index_point] = latex_res
                map_order[index_point] = the_order
                tmp.append(index_point)
                index_point += 1
            else:
                reversed_dict = {v: k for k, v in map_dict.items()}
                tmp.append(reversed_dict[latex_res])
        value_ldata.append(tmp)

    return np.array(value_ldata), map_dict, map_order  # value: relationship


def covert_orders_point(expressions, assigns, the_var1, the_var2, _x, _y, reverse=True):
    exp_names = list(expressions.keys())
    exp_num = len(exp_names)

    Z_list = []
    for i in range(exp_num):
        the_exp = expressions[exp_names[i]]
        assigned_exp = the_exp.subs(assigns)
        exp_value = assigned_exp.subs({the_var1: _x, the_var2: _y})
        Z_list.append(exp_value.evalf())
    latex_res, _ = order_types(exp_names, Z_list, reverse=reverse)
    return latex_res

def get_contour_centers(contourf_set):
    centers = []
    for collection in contourf_set.collections:
        for path in collection.get_paths():
            # 获取路径的顶点
            vertices = path.vertices
            # 计算路径的质心
            centroid = np.mean(vertices, axis=0)
            centers.append(centroid)
    return centers


def draw_max_area(expressions, assigns, the_var_x, start_end_x, the_var_y,
                 start_end_y, x_name, y_name, texts=None, save_dir=None,
                 precision=1000, fsize=14, figsize=[5, 4], theme='sci',
                 xrotation=0, yrotation=90, linewidths=0.1, isgrid=False
                 , xpad=3, ypad=3, xlabelpad=3, ylabelpad=5):
    """
        - expressions: Symbol表达式，字典形式传入。（必须）
        - assigns: 表达式参数赋值，字典形式。
        - the_var_x/the_var_y: 要分析的参数1/2；
        - start_end_x/start_end_y: 要分析的参数1/2的取值。[初始,结束]
        - x_name: x轴名称标签。
        - y_name: y轴名称标签。

        - save_dir=None: 图片保存路径，字符串。默认None，不保存。
        - linewidth: 线粗。字面意思，没啥好说的，默认值为1。
        - fsize: 图片中字号的大小，默认值为14。
        - figsize: 图片的大小，写成`[宽, 高]`的形式。默认为`[5, 4]`。
        - precision: 绘画的精细程度。默认取1000，表示画 $1000 \times 1000$ 个点。该值越大，运行速度越慢，太大没必要，根据个人情况权衡。
        - xrotation/yrotation: x/y轴名字标签旋转角度，基本不需要动。

        - isgrid: 是否要网格。要就填True，不要就是False，默认不要。
        - xpad=3, ypad=3, xlabelpad=3, ylabelpad=3: 分别为横轴刻度值距离横轴的距离、纵轴刻度值距离纵轴的距离、横轴名字标签距离横轴刻度的距离、纵轴名字标签距离纵轴刻度的距离。默认值3,3,3,3。如果挤了不好看了，再微调此参数，一般不用动。
        - texts: 表达式expressions中的函数值若分别达到最大，则相应区域应分别标记的文本，以`[]`形式写。默认None，按照expressions提供的名字标记。注意：标签个数和expressions中的函数顺序要对应。
        - theme: 主题。即各区域的配色方案。一般sci论文要保证黑白打印出来能看清，因此，默认值为'sci'，表示符合学术论文美感的灰度配色方案。若``theme=None``，则表示全白色。
          用户可以以列表`['颜色名称或16进制颜色值']`的形式提供一套配色方案，例如：`theme=['#ffffff', '#F0F0F0', '#E6E6E6', '#DCDCDC', '#D2D2D2', '#C8C8C8', '#BEBEBE', '#B4B4B4',
         '#AAAAAA', '#A0A0A0', '#969696', '#919191', '#8C8C8C', '#878787', '#828282', '#7D7D7D', '#787878', '#6E6E6E', '#646464']`。

         工具中（确切地说是Python的Matplotlib）提供了现成的配色方案（例如'viridis', 'plasma', 'inferno', 'magma', 'cividis'等），具体完整方案和效果列示如下：
         https://matplotlib.org/stable/_images/sphx_glr_colormap_reference_001.png
         https://matplotlib.org/stable/_images/sphx_glr_colormap_reference_002.png
         https://matplotlib.org/stable/_images/sphx_glr_colormap_reference_003.png
         https://matplotlib.org/stable/_images/sphx_glr_colormap_reference_004.png
         https://matplotlib.org/stable/_images/sphx_glr_colormap_reference_005.png
         https://matplotlib.org/stable/_images/sphx_glr_colormap_reference_006.png
         https://matplotlib.org/stable/_images/sphx_glr_colormap_reference_007.png
    """

    if theme == 'sci':
        theme = ['#ffffff', '#F0F0F0', '#E6E6E6', '#DCDCDC', '#D2D2D2', '#C8C8C8', '#BEBEBE', '#B4B4B4', '#AAAAAA',
                 '#A0A0A0', '#969696', '#919191', '#8C8C8C', '#878787', '#828282', '#7D7D7D', '#787878', '#6E6E6E', '#646464']
    fig, ax = plt.subplots(figsize=figsize)

    ax.set_ylabel(y_name, fontsize=fsize, fontweight='bold', rotation=yrotation, labelpad=ylabelpad)
    ax.set_xlabel(x_name, fontsize=fsize, fontweight='bold', rotation=xrotation, labelpad=xlabelpad)

    plt.xticks(fontsize=fsize - 1, fontname='times new roman')
    plt.yticks(fontsize=fsize - 1, fontname='times new roman')

    exp_names = list(expressions.keys())
    exp_num = len(exp_names)

    if exp_num <= 1:
        print('表达式个数必须大于2！')
        return None

    x_points = np.linspace(start_end_x[0], start_end_x[1], precision)
    y_points = np.linspace(start_end_y[0], start_end_y[1], precision)
    X, Y = np.meshgrid(x_points, y_points)

    Z_func = lambda x_, y_: who_max(expressions=expressions, assigns=assigns,
                                          the_var1=the_var_x, the_var2=the_var_y, X=x_, Y=y_)

    Z = Z_func(X,Y)
    if isinstance(theme, list):
        contourf_set = ax.contourf(X, Y, Z, levels=exp_num, colors=theme, alpha=1)
    elif theme is not None:
        contourf_set = ax.contourf(X, Y, Z, levels=exp_num, cmap=theme, alpha=1)
    else:
        contourf_set = ax.contourf(X, Y, Z, levels=exp_num, colors='w', alpha=1)
    ax.contour(X, Y, Z, levels=exp_num, colors='k', linewidths=linewidths)

    centers = get_contour_centers(contourf_set)

    # 打印结果
    record_centers = {}
    for center in centers:
        value = who_max_point(expressions, assigns, the_var_x, the_var_y, center[0], center[1])
        if value in record_centers.keys():
            new_center = [(record_centers[value][0] + center[0]) / 2, (record_centers[value][1] + center[1]) / 2]
            record_centers[value] = new_center
        else:
            record_centers[value] =center

    for k_, c_ in record_centers.items():
        print(f"区域 {k_}: 中心坐标 = {c_}")
        if texts is None:
            the_text = exp_names[int(k_)]
        else:
            the_text = texts[int(k_)]
        ax.text(c_[0], c_[1], the_text, fontsize=fsize - 1)

    ax.grid(isgrid)

    # 设置刻度
    ax.tick_params(axis='x', direction='in', pad=xpad)
    ax.tick_params(axis='y', direction='in', pad=ypad)
    
    judge_y = max(abs(np.max(y_points)),abs(np.min(y_points)))
    judge_x = max(abs(np.max(x_points)),abs(np.min(x_points)))
    if judge_y >= 5000:
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0), useMathText=True)
    if judge_x >= 5000:
        plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0), useMathText=True)

    fig.tight_layout()
    if save_dir is not None:
        if save_dir[-4:] == '.svg':
            plt.savefig(save_dir)
        else:
            plt.savefig(save_dir, dpi=600)
    return plt


def draw_detail_area(expressions, assigns, the_var_x, start_end_x, the_var_y,
                 start_end_y, x_name, y_name, save_dir=None, precision=1000, fsize=14, figsize=[7, 4], theme='sci',
                 xrotation=0, yrotation=90, linewidths=0.1, isgrid=False, xpad=3, ypad=3,
                 xlabelpad=3, ylabelpad=5, prefix=r'$\rm{Region}$', numbers='roman', reverse=True, remove_eq=True, dropout=0.01):
    """
        - expressions: Symbol表达式，字典形式传入。（必须）
        - assigns: 表达式参数赋值，字典形式。
        - the_var_x/the_var_y: 要分析的参数1/2；
        - start_end_x/start_end_y: 要分析的参数1/2的取值。[初始,结束]
        - x_name: x轴名称标签。
        - y_name: y轴名称标签。

        - save_dir=None: 图片保存路径，字符串。默认None，不保存。
        - linewidth: 线粗。字面意思，没啥好说的，默认值为1。
        - fsize: 图片中字号的大小，默认值为14。
        - figsize: 图片的大小，写成`[宽, 高]`的形式。默认为`[5, 4]`。
        - precision: 绘画的精细程度。默认取1000，表示画 $1000 \times 1000$ 个点。该值越大，运行速度越慢，太大没必要，根据个人情况权衡。
        - xrotation/yrotation: x/y轴名字标签旋转角度，基本不需要动。

        - isgrid: 是否要网格。要就填True，不要就是False，默认不要。
        - xpad=3, ypad=3, xlabelpad=3, ylabelpad=3: 分别为横轴刻度值距离横轴的距离、纵轴刻度值距离纵轴的距离、横轴名字标签距离横轴刻度的距离、纵轴名字标签距离纵轴刻度的距离。默认值3,3,3,3。如果挤了不好看了，再微调此参数，一般不用动。

        - theme: 主题。即各区域的配色方案。一般sci论文要保证黑白打印出来能看清，因此，默认值为'sci'，表示符合学术论文美感的灰度配色方案。若``theme=None``，则表示全白色。
          用户可以以列表`['颜色名称或16进制颜色值']`的形式提供一套配色方案， 例如：`theme=['#ffffff', '#F0F0F0', '#E6E6E6', '#DCDCDC', '#D2D2D2', '#C8C8C8', '#BEBEBE', '#B4B4B4',
         '#AAAAAA', '#A0A0A0', '#969696', '#919191', '#8C8C8C', '#878787', '#828282', '#7D7D7D', '#787878', '#6E6E6E', '#646464']`。

         工具中（确切地说是Python的Matplotlib）提供了现成的配色方案（例如'viridis', 'plasma', 'inferno', 'magma', 'cividis'等），具体完整方案和效果列示如下：
         https://matplotlib.org/stable/_images/sphx_glr_colormap_reference_001.png
         https://matplotlib.org/stable/_images/sphx_glr_colormap_reference_002.png
         https://matplotlib.org/stable/_images/sphx_glr_colormap_reference_003.png
         https://matplotlib.org/stable/_images/sphx_glr_colormap_reference_004.png
         https://matplotlib.org/stable/_images/sphx_glr_colormap_reference_005.png
         https://matplotlib.org/stable/_images/sphx_glr_colormap_reference_006.png
         https://matplotlib.org/stable/_images/sphx_glr_colormap_reference_007.png

        - prefix: 前缀。可以是``"区域"``也可以是``"$\rm{Region}$"``，默认``"$\rm{Region}$"``，是以LaTeX格式写的新罗马字体的英文，显示为"$\rm{Region}$"。
        - numbers: 序号标记风格。有三种可选："roman", "letter" 和"number"，分别表示罗马数字、大写英文字母和阿拉伯数字。默认"roman"。
        - reverse: 默认True，表示降序排布，即$A>B>C...$的形式。若为False，则升序排布$A<B<C...$。
        - remove_eq: 是否不考虑等式？默认True，不带等式。若为False，则带等式，如$A>B=C>D..$。
        - dropout: 点数占比小于多少不考虑？用于排除一些边界部分十分微小的区域。默认0.01。这个参数不要去动。
    """


    if theme == 'sci':
        theme = ['#ffffff', '#F0F0F0', '#E6E6E6', '#DCDCDC', '#D2D2D2', '#C8C8C8', '#C3C3C3', '#BEBEBE', '#B9B9B9',
                 '#B4B4B4', '#AFAFAF', '#AAAAAA', '#A5A5A5', '#A0A0A0', '#9B9B9B', '#969696', '#919191', '#8C8C8C',
                 '#878787', '#828282', '#7D7D7D', '#787878', '#6E6E6E', '#646464', '#646464', '#5F5F5F', '#5A5A5A',
                 '#5A5A5A', '#565656', '#525252', '#4E4E4E', '#4A4A4A', '#464646', '#424242', '#3E3E3E', '#3A3A64'] # 36

    if numbers == 'roman':
        # 列出前36个罗马数字
        numerals = gen_romans(36)
    elif numbers == 'letter':
        numerals = gen_letters(36)
    else:
        numerals = [str(i+1) for i in range(36)]

    fig, ax = plt.subplots(figsize=figsize)

    ax.set_ylabel(y_name, fontsize=fsize, fontweight='bold', rotation=yrotation, labelpad=ylabelpad)
    ax.set_xlabel(x_name, fontsize=fsize, fontweight='bold', rotation=xrotation, labelpad=xlabelpad)

    plt.xticks(fontsize=fsize - 1, fontname='times new roman')
    plt.yticks(fontsize=fsize - 1, fontname='times new roman')

    exp_names = list(expressions.keys())
    exp_num = len(exp_names)

    if exp_num <= 1:
        print('表达式个数必须大于2！')
        return None

    x_points = np.linspace(start_end_x[0], start_end_x[1], precision)
    y_points = np.linspace(start_end_y[0], start_end_y[1], precision)
    X, Y = np.meshgrid(x_points, y_points)

    Z_func = lambda x_, y_: covert_orders(expressions=expressions, assigns=assigns,
                                          the_var1=the_var_x, the_var2=the_var_y,
                                          X=x_, Y=y_, reverse=reverse)
    Z, map_dict, map_order = Z_func(X, Y)  # value: relationship

    remove_values = []
    if remove_eq:
        map_dict_new = {}
        for _i, value in enumerate(map_dict.values()):
            if '=' not in value:
                map_dict_new[list(map_dict.keys())[_i]] = value
            else:
                # 添加踢出列表
                remove_values.append(list(map_dict.keys())[_i])
    else:
        map_dict_new = map_dict

    final_map_dict = {}
    for em in map_dict_new.keys():
        count = np.count_nonzero(Z==em)
        if count/(precision**2) > dropout:
            final_map_dict[em] = map_dict_new[em]
        else:
            # 添加踢出列表
            remove_values.append(em)

    for em in remove_values:
        indices = np.where(Z==em)
        # 获取索引的行和列
        rows, cols = indices
        # 循环遍历索引，将值替换为附近的值
        for row, col in zip(rows, cols):
            # 找到附近的值，这里优先选择下边的值，若到头了，则选择上面的值。一点点看，直到那个值不在 `剔除列表中`,若选不着，就换个方向来。
            if (col < precision - 1) and (Z[row, col] in remove_values):
                for c_add in range(1, precision - col):
                    try_value = Z[row,col+c_add]
                    if try_value not in remove_values:
                        Z[row, col] = try_value
                        break
            if (col >= precision - 1) and (Z[row, col] in remove_values):
                for c_add in range(1, col):
                    try_value = Z[row,col-c_add]
                    if try_value not in remove_values:
                        Z[row, col] = try_value
                        break
            if (row < precision - 1) and (Z[row, col] in remove_values):
                for r_add in range(1, precision - row):
                    try_value = Z[row+r_add,col]
                    if try_value not in remove_values:
                        Z[row, col] = try_value
                        break
            if (row >= precision - 1) and (Z[row, col] in remove_values):
                for r_add in range(1, row):
                    try_value = Z[row-r_add,col]
                    if try_value not in remove_values:
                        Z[row, col] = try_value
                        break

    case_num = len(final_map_dict.keys())

    # 更新Z内的数据成连续数值
    for _jj, k in enumerate(final_map_dict.keys()):
        mask = (Z == k)
        Z[mask] = _jj

    if isinstance(theme, list):
        contourf_set = ax.contourf(X, Y, Z, levels=case_num, colors=theme, alpha=1)
    elif theme is not None:
        contourf_set = ax.contourf(X, Y, Z, levels=case_num, cmap=theme, alpha=1)
    else:
        contourf_set = ax.contourf(X, Y, Z, levels=case_num, colors='w', alpha=1)

    ax.contour(X, Y, Z, levels=case_num, colors='k', linewidths=linewidths)

    centers = get_contour_centers(contourf_set)

    # 打印结果
    record_centers = {}
    for center in centers:
        latex_value = covert_orders_point(expressions, assigns, the_var_x, the_var_y,
                                          center[0], center[1], reverse=reverse)
        if latex_value in record_centers.keys():
            new_center = [(record_centers[latex_value][0] + center[0]) / 2, (record_centers[latex_value][1] + center[1]) / 2]
            record_centers[latex_value] = new_center
        else:
            record_centers[latex_value] = center

    ii = 0

    legend_texts = ""
    for k_, c_ in record_centers.items():
        print(f"区域 {k_}: 中心坐标 = {c_}")
        the_text = prefix + r' $\rm{' + numerals[ii] + r'}$'
        if k_ == 0:
            legend_texts = prefix + r' $\rm{' + numerals[ii] + r'}$: ' + k_
        else:
            legend_texts += '\n' + prefix + r' $\rm{' + numerals[ii] + r'}$: ' + k_
        ax.text(c_[0], c_[1], the_text, fontsize=fsize - 2, ha='center', va='center')
        ii += 1

    plt.text(1.05, 0.5, legend_texts, fontsize=fsize - 2, ha='left', va='center', transform=plt.gca().transAxes)

    ax.grid(isgrid)

    # 设置刻度
    ax.tick_params(axis='x', direction='in', pad=xpad)
    ax.tick_params(axis='y', direction='in', pad=ypad)

    judge_y = max(abs(np.max(y_points)), abs(np.min(y_points)))
    judge_x = max(abs(np.max(x_points)), abs(np.min(x_points)))
    if judge_y >= 5000:
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=True)
    if judge_x >= 5000:
        plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0), useMathText=True)

    fig.tight_layout()
    if save_dir is not None:
        if save_dir[-4:] == '.svg':
            plt.savefig(save_dir)
        else:
            plt.savefig(save_dir, dpi=600)
    return plt

