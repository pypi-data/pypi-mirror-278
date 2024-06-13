import seaborn as sns
import random
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statsmodels.api as sm
from matplotlib.patches import Patch
from plotdelice.stats import add_significance_bars

def prepare_data(df, x_group, 
                  palette,colors):
    color_map = sns.color_palette(palette, n_colors=len(np.unique(df[x_group])))
    if colors:
        color_dic = {cond: color for cond, color in zip(np.unique(df[x_group]), colors)}
    else:
        color_dic = {cond: color for cond, color in zip(np.unique(df[x_group]), color_map)}
    labels = [i for i in color_dic]
    colors = [i for i in color_dic.values()]
    return color_dic, labels, colors

def prepare_data_colorby(df, x_group, palette, colors, colorby):
    if colors is None:
        unique_colors = df[colorby].unique()
        color_palette = sns.color_palette(palette, len(unique_colors))
        color_dic = {k: color_palette[i] for i, k in enumerate(unique_colors)}
    else:
        color_dic = {k: colors[i] for i, k in enumerate(df[colorby].unique())}
    labels = df[colorby].unique()
    colors = [color_dic[val] for val in df[colorby]]
    return color_dic, labels, colors

def plot_violin(df, x_group, y_variable, color_dic, labels, colors, violin_width, violin_edge_color, point_size, jitter,figsize=None,fontsize=20,fw='bold'):
    
    if figsize:
        fig, axs = plt.subplots(figsize=figsize)
    else:
        fig, axs = plt.subplots()

    for i, cond in enumerate(color_dic):
        data_to_plot = df[y_variable][df[x_group] == cond]
        x_values = [i + 1] * len(data_to_plot)
        x_jittered = [val + (jitter * (2 * (random.random() - 0.5))) for val in x_values]

        parts = plt.violinplot(data_to_plot, [i + 1], showmedians=False, showextrema=False, widths=violin_width)
        for pc in parts['bodies']:
            pc.set_facecolor('white')
            pc.set_edgecolor(violin_edge_color)
            pc.set_linewidths(2)
            pc.set_alpha(1)

        plt.hlines(np.mean(df[y_variable][df[x_group] == cond]), i + 0.8, i + 1.2, color='red', linewidth=2, alpha=1)
        print("{:>10} mean: {:>45}".format(cond, np.mean(df[y_variable][df[x_group] == cond])))

        plt.scatter(x_jittered, df[y_variable][df[x_group] == cond], color=colors[i], alpha=1, s=point_size, edgecolors='black', zorder=3)

    plt.xticks(range(1, len(labels) + 1), labels, fontsize=fontsize,weight=fw)
    plt.yticks(fontsize=fontsize,weight=fw)
    return fig, axs

def plot_scatter(df, x_group, y_variable, color_dic, labels,colorby, point_size, figsize=None,fontsize=20,fw='bold',add_regression=None,marker=None):
    
    if figsize:
        fig, axs = plt.subplots(figsize=figsize)
    else:
        fig, axs = plt.subplots()

    if add_regression=='linear':
        x_with_const = sm.add_constant(df[x_group])
        model = sm.OLS(df[y_variable], x_with_const).fit()
        r_squared = model.rsquared
        print("R^2: ",r_squared)
        sns.regplot(
            x=df[x_group],
            y=df[y_variable],
            scatter=False,
            ax=axs,
            color='gray',
            label=f"$R^2={r_squared:.2f}$",
            
        )
    if add_regression=='logx':
        x_with_const = sm.add_constant(df[x_group])
        model = sm.OLS(df[y_variable], np.log(x_with_const)).fit()
        r_squared = model.rsquared
        print("R^2: ",r_squared)
        sns.regplot(
            x=df[x_group],
            y=df[y_variable],
            scatter=False,
            ax=axs,
            color='gray',
            logx=True,
            label=f"$R^2={r_squared:.2f}$"   
        )
    
    if marker != None:
        
        for label in labels:
            subset = df[df[colorby] == label]
            
            mscatter(x=subset[x_group] ,
                    y=subset[y_variable],
                    c=color_dic[subset[colorby]],
                    ax=axs,
                    m=subset[marker],
                    s=point_size
                    )
    else:
        for label in labels:
            subset = df[df[colorby] == label]
            sns.scatterplot(x=subset[x_group] ,
                            y=subset[y_variable],
                            hue=subset[colorby],
                            palette=color_dic,
                            s=point_size,
                            edgecolor="black",
                            ax=axs,
                            legend='auto',
                            )

    
    return fig, axs

def mscatter(x,y, ax=None, m=None, **kw):
    import matplotlib.markers as mmarkers
    ax = ax or plt.gca()
    sc = ax.scatter(x,y,**kw)
    if (m is not None) and (len(m)==len(x)):
        paths = []
        for marker in m:
            if isinstance(marker, mmarkers.MarkerStyle):
                marker_obj = marker
            else:
                marker_obj = mmarkers.MarkerStyle(marker)
            path = marker_obj.get_path().transformed(
                        marker_obj.get_transform())
            paths.append(path)
        sc.set_paths(paths)
    return sc


def violinplot_delice(df, x_group, y_variable, violin_width=0.85, y_label=None, palette="PuRd", violin_edge_color="black", point_size=10, jitter=0.05, title=None, title_loc="left", title_size=10,colors=None, xlabel=None,figsize=None,fontsize=20,fw='bold'):
    if y_label is None:
        y_label = y_variable
    try:
        df = df.sort_values(by=x_group,ascending=False)
    except:
        pass

    color_dic, labels, colors = prepare_data(df, x_group, palette,colors)
    fig, axs = plot_violin(df, x_group, y_variable, color_dic, labels, colors, violin_width, violin_edge_color, point_size, jitter,figsize=figsize,fontsize=fontsize,fw=fw)
    add_significance_bars(df, x_group, y_variable, labels, axs,fontsize=fontsize)
          

    # Change the line weight
    axs.spines['bottom'].set_linewidth(2)
    axs.spines['left'].set_linewidth(2) 
    axs.spines[['right', 'top']].set_visible(False)
    plt.xticks(range(1, len(color_dic) + 1))
    plt.xlabel(xlabel, fontsize=fontsize,weight=fw)
    plt.ylabel(y_label, fontsize=fontsize,weight=fw)
    plt.title(title, loc=title_loc, fontsize=title_size, weight=fw)
    plt.show()

    return fig, axs

def scatterplot_delice(df, x_group, y_variable, colorby, violin_width=0.85, y_label=None, palette="PuRd", violin_edge_color="black", point_size=10, jitter=0.05, title=None, title_loc="left", title_size=10, colors=None, x_label=None, figsize=None, fontsize=20, fw='bold', add_regression=True,marker=None):
    if y_label is None:
        y_label = y_variable
    if x_label is None:
        x_label = x_group
    try:
        df = df.sort_values(by=x_group, ascending=False)
    except:
        pass

    color_dic, labels, colors = prepare_data_colorby(df, colorby, palette, colors, colorby)
    fig, ax = plot_scatter(df, x_group, y_variable, color_dic, labels,colorby, point_size, figsize=figsize, fontsize=fontsize, fw=fw, add_regression=add_regression,marker=marker)

    # Change the line weight
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines[['right', 'top']].set_visible(False)
    
    plt.yticks(fontsize=fontsize-5,weight=fw)
    plt.xticks(fontsize=fontsize-5,weight=fw)
    plt.xlabel(x_label, fontsize=fontsize, weight=fw)
    plt.ylabel(y_label, fontsize=fontsize, weight=fw)
    plt.title(title, loc=title_loc, fontsize=title_size, weight=fw)
    plt.show()

    return fig, ax

def multiplot_delice(df,x_group,x_variable,y_variable,violin_width=0.85,y_label=None,x_label=None,palette="PuRd",violin_edge_color="black",point_size=10,jitter=0.05,title=None,title_loc="left",title_size=10,offset_f=0.5,spacing=2,plottype='box'):
    if y_label == None:
        y_label = y_variable
    if x_label == None:
        x_label = x_variable

    color_map = sns.color_palette(palette, n_colors=len(np.unique(df[x_group])))
    color_dic = {cond: color for cond, color in zip(np.unique(df[x_group]), color_map)}

    labels = [i for i in color_dic]

    # plot settings
    fig, axs = plt.subplots(figsize=(12, 8))
    colors = [i for i in color_dic.values()]

    # Test every combination
    # Check from the outside pairs of boxes inwards
    ls = list(range(1, len(labels) + 1))
    combinations = [(ls[x], ls[x + y]) for y in reversed(ls) for x in range((len(ls) - y))]
    significant_combinations = []
    for combination in combinations:
        for cond2 in np.unique(df[x_variable]):
            data1 = df[y_variable][(df[x_group] == labels[combination[0] - 1]) & (df[x_variable] == cond2)]
            data2 = df[y_variable][(df[x_group] == labels[combination[1] - 1]) & (df[x_variable] == cond2)]
            
            # Significance
            U, p = stats.ttest_ind(data1, data2, alternative='two-sided')
            
            # bonferroni correction
            
            p_adj = p * len(combinations)
            print("{}: {} mean:{} x {} mean:{:<30} padj: {:<20}  p-val: {:<10}".format(
                cond2,
                labels[combination[0] - 1],
                np.mean(data1),
                labels[combination[1] - 1],
                np.mean(data2),
                p_adj,
                p
        ))

        if p_adj < 0.05:
            significant_combinations.append([combination, p_adj])
        else:
            continue
            significant_combinations.append([combination, p_adj])
        #print(f"{list(groups.keys())[combination[0]-1]} - {list(groups.keys())[combination[1]-1]} | {p}")

    # individual points
    offset= -offset_f
    for i,cond in enumerate(color_dic):
       
        data_to_plot = df[y_variable][df[x_group]==cond]
        x_values = df[x_variable][df[x_group]==cond]
        x_jittered = [val*spacing+offset + (jitter * (2 * (random.random() - 0.5))) for val in x_values]
        
        # mean
        for x_val in x_values:
            
            if plottype == 'box':
                # box
                parts = plt.boxplot(df[y_variable][(df[x_group]==cond) & (df[x_variable]==x_val)],positions=[x_val*spacing+offset],widths=violin_width,showcaps=False,showfliers=False,meanprops=dict(linestyle=None, linewidth=0, color='blue'))

            if plottype == 'violin':
                parts = plt.violinplot(df[y_variable][(df[x_group]==cond) & (df[x_variable]==x_val)],[x_val*spacing+offset],showmedians=False,showextrema=False, widths=violin_width)
                # customize
                for pc in parts['bodies']:
                    pc.set_facecolor('white')
                    pc.set_edgecolor(violin_edge_color)
                    pc.set_linewidths(2)
                    pc.set_alpha(1)
                plt.hlines(np.mean(df[y_variable][(df[x_group]==cond) & (df[x_variable]==x_val)]), x_val*spacing+offset-violin_width/2, x_val*spacing+offset-1+violin_width, color='red', linewidth=2, alpha=1, )
            if plottype == 'dots':
                plt.hlines(np.mean(df[y_variable][(df[x_group]==cond) & (df[x_variable]==x_val)]), x_val*spacing+offset-violin_width/2, x_val*spacing+offset-1+violin_width, color='red', linewidth=2, alpha=1, )

        # print("{:>10} mean: {:>45}".format(cond,np.mean(data_to_plot)))
        
        # points
        plt.scatter(x_jittered, data_to_plot, color = colors[i], alpha=1, s=point_size, edgecolors='black',zorder=3,label=cond)


        offset+=2*offset_f

    # add signif bars

    # Get the y-axis limits
    bottom, top = plt.ylim()
    y_range = top - bottom
    for i, significant_combination in enumerate(significant_combinations):
        # Columns corresponding to the datasets of interest
        x1 = significant_combination[0][0]
        x2 = significant_combination[0][1]
        # What level is this bar among the bars above the plot?
        level = len(significant_combinations) - i
        # Plot the bar
        bar_height = (y_range * 0.07 * level) + top + 0.4
        bar_tips = bar_height - (y_range * 0.02)
        plt.plot(
            [x1, x1, x2, x2],
            [bar_tips, bar_height, bar_height, bar_tips], lw=1, c='k'
        )
        # Significance level
        p = significant_combination[1]
        if p < 0.001:
            sig_symbol = '***'
        elif p < 0.01:
            sig_symbol = '**'
        elif p < 0.05:
            sig_symbol = '*'
        else:
            sig_symbol = "ns"
        text_height = bar_height + (y_range * 0.01)
        plt.text((x1 + x2) * 0.5, text_height, sig_symbol, ha='center', va='bottom', c='k', weight='bold')

    # custom 
    axs.spines[['right', 'top']].set_visible(False)
    # Change the x-axis line weight
   #axs.spines['bottom'].set_linewidth(2)  

    # Change the y-axis line weight
    #axs.spines['left'].set_linewidth(2) 
    plt.xticks(range(0, spacing*len(np.unique(x_values)),spacing), np.unique(x_values),weight='bold')
    plt.xlabel(x_label,fontsize=20)
    plt.ylabel(y_label, fontsize=20)
    plt.title(title, loc=title_loc, fontsize=title_size)
    plt.legend(fontsize=15,markerscale=2.5,loc='best')
    plt.show()
    
    return fig,axs

def barplot_delice(df, x_group, y_variable, y_label=None,x_label=None, palette="PuRd", colors=None, bar_width=0.5, bar_edge_color="black", point_size=10, jitter=0.05, title=None, title_loc="left", title_size=10,label_rotation=45, bar_edge_width=3,errorbar_width=2,figsize=None,fontsize=20,scatter=True,fw='bold',stats=True):
    
    if figsize:
        fig, axs = plt.subplots(figsize=figsize)
    else:
        fig, axs = plt.subplots()
    if y_label is None:
        y_label = y_variable
    if x_label is None:
        x_label = x_group

    color_map = sns.color_palette(palette, n_colors=len(np.unique(df[x_group])))

    if colors:
        color_dic = {cond: color for cond, color in zip(np.unique(df[x_group]), colors)}
    else:
        color_dic = {cond: color for cond, color in zip(np.unique(df[x_group]), color_map)}

    labels = [i for i in color_dic]
    colors = [i for i in color_dic.values()]

    # Individual bar plots
    for i, cond in enumerate(color_dic):
        data_to_plot = df[y_variable][df[x_group] == cond]
        mean = np.mean(data_to_plot)
        std = np.std(data_to_plot)

        # Plot bar with thicker edges
        axs.bar(i + 1, mean, color=colors[i],width=bar_width, edgecolor=bar_edge_color,linewidth=bar_edge_width)
        
        # Plot error bars with thicker edges
        plt.errorbar(i + 1, mean, yerr=std, fmt='none', ecolor=bar_edge_color, elinewidth=errorbar_width, capsize=5, capthick=errorbar_width)

        # Mean
        #plt.scatter([i + 1], [mean], color='red', zorder=3)
        print("{:>10} mean: {:>45}".format(cond, mean))

        # Individual points with jitter
        if scatter:
            x_jittered = [i + 1 + (jitter * (2 * (random.random() - 0.5))) for _ in data_to_plot]
            plt.scatter(x_jittered, data_to_plot, color=colors[i], alpha=1, s=point_size, edgecolors='black', zorder=3)

    if stats:
        add_significance_bars(df, x_group, y_variable, labels, axs,fontsize=fontsize)
   
    # Customization
    axs.spines[['right', 'top']].set_visible(False)
    axs.spines['bottom'].set_linewidth(2)  
    axs.spines['left'].set_linewidth(2) 
    # Adjust x-ticks
    axs.set_xticks(range(1, len(labels) + 1))
    axs.set_xticklabels(labels, rotation=label_rotation, ha='center',weight='bold',fontsize=fontsize-5)
    plt.yticks(fontsize=fontsize,weight=fw)
    
    plt.xlabel(x_label, fontsize=fontsize, weight='bold')
    plt.ylabel(y_label, fontsize=fontsize, weight='bold')
    plt.title(title, loc=title_loc, fontsize=title_size,weight=fw)
    plt.show()

    return fig, axs

def boxplot_delice(df, x_group, y_variable, y_label=None,x_label=None,fontsize=16, palette="PuRd", colors=None, bar_width=0.5,sbars=None, bar_edge_color="black", point_size=10, jitter=0.05, title=None, title_loc="left", title_size=10,label_rotation=45, bar_edge_width=3,errorbar_width=2,fw='bold'):
    if y_label is None:
        y_label = y_variable
    if x_label is None:
        x_label = x_group

    color_map = sns.color_palette(palette, n_colors=len(np.unique(df[x_group])))

    if colors:
        color_dic = {cond: color for cond, color in zip(np.unique(df[x_group]), colors)}
    else:
        color_dic = {cond: color for cond, color in zip(np.unique(df[x_group]), color_map)}

    labels = [i for i in color_dic]

    # Plot settings
    fig, axs = plt.subplots()
    colors = [i for i in color_dic.values()]

    # Test every combination
    # Check from the outside pairs of boxes inwards
    ls = list(range(1, len(labels) + 1))
    combinations = [(ls[x], ls[x + y]) for y in reversed(ls) for x in range((len(ls) - y))]
    significant_combinations = []
    for combination in combinations:
        data1 = df[y_variable][df[x_group] == labels[combination[0] - 1]]
        data2 = df[y_variable][df[x_group] == labels[combination[1] - 1]]
        # Significance
        U, p = stats.ttest_ind(data1, data2, alternative='two-sided')
        
        # Bonferroni correction
        p_adj = p * len(combinations)
        print("{} x {:<30}   padj: {:<2}  p-val: {:<10}".format(
            labels[combination[0] - 1],
            labels[combination[1] - 1],
            p_adj,
            p
        ))

        if p_adj < 0.05:
            significant_combinations.append([combination, p_adj])
        else:
            # significant_combinations.append([combination, p_adj])
            continue

    # Individual bar plots
    for i, cond in enumerate(color_dic):
        data_to_plot = df[y_variable][df[x_group] == cond]
        mean = np.mean(data_to_plot)
        std = np.std(data_to_plot)

        x_values = [i + 1] * len(data_to_plot)
        x_jittered = [val + (jitter * (2 * (random.random() - 0.5))) for val in x_values]
            
        # mean
        plt.hlines(np.mean(df[y_variable][df[x_group]==cond]), i + 0.8, i + 1.2, color='black', linewidth=2, alpha=1, )
        print("{:>10} mean: {:>45}".format(cond,np.mean(df[y_variable][df[x_group]==cond])))
        # points
        plt.scatter(x_jittered, df[y_variable][df[x_group]==cond], color = colors[i], alpha=1, s=point_size, edgecolors='black',zorder=3)
        print("{:>10} mean: {:>45}".format(cond, mean))

        # Individual points with jitter
        # x_jittered = [i + 1 + (jitter * (2 * (random.random() - 0.5))) for _ in data_to_plot]
        # plt.scatter(x_jittered, data_to_plot, color=colors[i], alpha=1, s=point_size, edgecolors='black', zorder=3)

    # Adjust x-ticks
    axs.set_xticks(range(1, len(labels) + 1))
    axs.set_yticklabels(fontsize=fontsize-5)
    plt.yticks(fontsize=fontsize,weight=fw)

    # Add signif bars
    if sbars:
        add_significance_bars(df, x_group, y_variable, labels, axs,fontsize=fontsize)

    # Customization
    # axs.spines[['right', 'top']].set_visible(False)
    axs.spines['bottom'].set_linewidth(2)  
    axs.spines['left'].set_linewidth(2) 
    plt.xlabel(x_label,fontsize=fontsize-5)
    plt.ylabel(y_label,fontsize=fontsize)
    plt.title(title, loc=title_loc, fontsize=title_size)
    plt.show()

    return fig, axs

def markerplot_delice(pcadf,x_var,y_var,colorby,svgcol, title='',palette='Blues', fontsize=20, fw='bold', outline_thickness=2, figsize=(15,10), markersize=20, add_regression=None):
    """
    Plot PCA data points with custom markers and specified properties.

    Parameters:
    - pcadf: DataFrame containing 'PC 1', 'PC 2', and 'true_label' columns
    - df: DataFrame containing 'spine coords' column with custom marker shapes
    - title: Title of the plot
    - fontsize: Font size for the labels and title
    - fw: Font weight for the labels and title
    - outline_thickness: Thickness of the marker outlines
    """
    pcadf = pcadf.sort_values(by=colorby)
    # Generate a colormap
    cmap = sns.color_palette(palette, n_colors=len(np.unique(pcadf[colorby])))
    
    # Create a mapping from labels to colors
    unique_labels = np.unique(pcadf[colorby])
    label_to_color = {cond: color for cond, color in zip(unique_labels, cmap)}

    # Create a plot
    fig, axs = plt.subplots(figsize=figsize)

    # Plot each data point with custom markers and black outlines
    for x, y, labels, sc in zip(pcadf[x_var], pcadf[y_var], pcadf[colorby], pcadf[svgcol]):
        smiley = sc
        color = label_to_color[labels]
        smiley.vertices -= smiley.vertices.mean(axis=0)
        axs.plot(x, y, marker=smiley, color=color, markersize=markersize)

    if add_regression=='linear':
        x_with_const = sm.add_constant(pcadf[x_var])
        model = sm.OLS(pcadf[y_var], x_with_const).fit()
        r_squared = model.rsquared
        print("R^2: ",r_squared)
        sns.regplot(
            x=pcadf[x_var],
            y=pcadf[y_var],
            scatter=False,
            ax=axs,
            color='gray',
            label=f"$R^2={r_squared:.2f}$",
            
        )
    if add_regression=='logx':
        x_with_const = sm.add_constant(pcadf[x_var])
        model = sm.OLS(pcadf[y_var], np.log(x_with_const)).fit()
        r_squared = model.rsquared
        print("R^2: ",r_squared)
        sns.regplot(
            x=pcadf[x_var],
            y=pcadf[y_var],
            scatter=False,
            ax=axs,
            color='gray',
            logx=True,
            label=f"$R^2={r_squared:.2f}$"   
        )

    # Create custom legend
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=label_to_color[label], markersize=20, label=label) for label in unique_labels]
    
    # Add regression line handle if regression is added
    if add_regression is not None:
        regression_handle = Patch(color='gray', label=f"$R^2={r_squared:.2f}$")
        handles.append(regression_handle)
    axs.legend(handles=handles, title='', frameon=False, prop={'weight': fw})

    # Change the line weight
    axs.spines['bottom'].set_linewidth(2)
    axs.spines['left'].set_linewidth(2) 
    axs.spines[['right', 'top']].set_visible(False)
    plt.yticks(fontsize=fontsize,weight=fw)
    plt.xticks(fontsize=fontsize,weight=fw)
    plt.xlabel(x_var, fontsize=fontsize, weight=fw)
    plt.ylabel(y_var, fontsize=fontsize, weight=fw)
    plt.title(title, weight=fw)

    # plt.show()
    return fig, axs