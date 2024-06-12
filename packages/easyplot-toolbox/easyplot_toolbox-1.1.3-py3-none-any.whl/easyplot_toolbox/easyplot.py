"""easyplot tools for data visualization"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.lines import Line2D
import squarify
import pandas as pd
import joypy


def convert_si_to_inches_in_chart_size(width, height):
    """ 
    This function convert figure dimensions from meters to inches.
    
    Args:
        width (Float): figure width in SI units
        height (Float): figure height in SI units

    Returns:
        width (Float): figure width in inches units
        height (Float): figure height in inches units
    """

    # Converting dimensions
    width /= 2.54
    height /= 2.54

    return width, height


def save_chart_in_folder(name, extension, dots_per_inch):
    """ 
    This function saves graphics according to the selected extension.

    Args:
        name (String): Path + name figure
        extension (String): File extension
        dots_per_inch (Integer): The resolution in dots per inch

    Returns:
        None
    """

    # Saving figure
    plt.savefig(name + '.' + extension,
                dpi=dots_per_inch,
                bbox_inches='tight',
                transparent=True)


def keys_to_lower(d):
    """
    This function converts the keys of a Dictionary to lowercase.

    Args:
        d (Dictionary): Dataset

    Returns:
        d (Dictionary): Dataset with keys in lowercase
    """

    return {key.lower(): value for key, value in d.items()}


def histogram_chart(**kwargs):
    """
    This function shows a Boxplot and Histogram in a single chart.

    Args:
        plot_setup (Dictionary): Settings of chart (Dictionary with the following keys):
            name (String): Path + name figure (key required in plot_setup)
            width (Float): figure width in SI units (key required in plot_setup)
            height (Float): figure height in SI units (key required in plot_setup)
            extension (String): File extension (key required in plot_setup)
            dots_per_inch (Integer): The resolution in dots per inch (key required in plot_setup)
            x_axis_label (String): x axis label (key required in plot_setup)
            x_axis_size (Integer): x axis size (key required in plot_setup)
            y_axis_label (String): y axis label (key required in plot_setup)
            y_axis_size (Integer): y axis size (key required in plot_setup)
            axises_color (String): Axises color (key required in plot_setup)
            labels_size (Integer): Labels size (key required in plot_setup)
            labels_color (String): Labels color (key required in plot_setup)
            chart_color (String): Chart color (key required in plot_setup)
            bins (Integer): Range representing the width of a single bar (key required in plot_setup)
        dataset (List or array): Dataset
            
    Returns:
        None
    """

    # Setup
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    x_axis_label = plot_setup['x_axis_label']
    x_axis_size = plot_setup['x_axis_size']
    y_axis_label = plot_setup['y_axis_label']
    y_axis_size = plot_setup['y_axis_size']
    axises_color = plot_setup['axises_color']
    labels_size = plot_setup['labels_size']     
    labels_color = plot_setup['labels_color']
    chart_color = plot_setup['chart_color']
    bins = int(plot_setup['bins']) 
    # kDE = plot_setup['kDE']
    dots_per_inch = plot_setup['dots_per_inch'] 
    extension = plot_setup['extension']
    
    # Dataset
    data = kwargs.get('dataset')
 
    # Plot
    [w, h] = convert_si_to_inches_in_chart_size(w, h)
    sns.set(style = 'ticks')
    fig, (ax_box, ax_hist) = plt.subplots(2, figsize=(w, h), sharex=True, gridspec_kw={'height_ratios': (.15, .85)})
    sns.boxplot(data=data, ax=ax_box, color=chart_color, orient="h")
    sns.histplot(data=data, ax=ax_hist, color=chart_color, bins=bins)
    ax_box.set(yticks=[])
    ax_box.set(xlabel='')
    font = {'fontname': 'DejaVu Sans',
            'color':  labels_color,
            'weight': 'normal',
            'size': labels_size}
    ax_hist.set_ylabel(y_axis_label, fontdict=font)
    ax_hist.set_xlabel(x_axis_label, fontdict=font)
    ax_hist.tick_params(axis='x', labelsize=x_axis_size, colors=axises_color)
    ax_hist.tick_params(axis='y', labelsize=y_axis_size, colors=axises_color)
    plt.grid()
    sns.despine(ax=ax_hist)
    sns.despine(ax=ax_box, left=True)
    plt.tight_layout()

    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)

    # Show figure
    plt.show()


def line_chart(**kwargs):
    """
    This function shows a multiple lines in single chart.

    Args:
        plot_setup (Dictionary): Settings of chart (Dictionary with the following keys):
            name (String): Path + name figure (key required in plot_setup)
            width (Float): figure width in SI units (key required in plot_setup)
            height (Float): figure height in SI units (key required in plot_setup)
            extension (String): File extension (key required in plot_setup)
            dots_per_inch (Integer): The resolution in dots per inch (key required in plot_setup)
            marker (List): List of markers. See <a href="https://matplotlib.org/stable/gallery/lines_bars_and_markers/marker_reference.html#sphx-glr-gallery-lines-bars-and-markers-marker-reference-py" target="_blank">gallery</a> (key required in plot_setup)
            marker_size (List): List of marker sizes (key required in plot_setup)
            line_width (List): List of line widths (key required in plot_setup)
            line_style (List): List of line styles. See <a href="https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html" target="_blank">gallery</a> (key required in plot_setup) 
            x_axis_label (String): x axis label (key required in plot_setup)
            x_axis_size (Integer): x axis size (key required in plot_setup)
            y_axis_label (String): y axis label (key required in plot_setup)
            y_axis_size (Integer): y axis size (key required in plot_setup)
            axises_color (String): Axises color (key required in plot_setup)
            labels_size (Integer): Labels size (key required in plot_setup)
            labels_color (String): Labels color (key required in plot_setup)
            chart_color (List): List of chart_colors (key required in plot_setup)
            x_limit (List): x axis limits (key required in plot_setup)
            y_limit (List): y axis limits (key required in plot_setup)
            on_grid (Boolean): Grid on or off (key required in plot_setup)
            y_log (Boolean): y log scale (key required in plot_setup)
            x_log (Boolean): x log scale (key required in plot_setup)
            legend (List): List of legends (key required in plot_setup)
            legend_location (String): Legend location (key required in plot_setup)
            size_legend (Integer): Legend size (key required in plot_setup)
        dataset (Dictionary): Dataset with the following
            x0 (List or array): x axis values for the first line (key required in dataset)
            y0 (List or array): y axis values for the first line (key required in dataset)
            x1 (List or array): x axis values for the second line (key required in dataset)
            y1 (List or array): y axis values for the second line (key required in dataset)
            xn (List or array): x axis values for the n-th line (key required in dataset)
            yn (List or array): y axis values for the n-th line (key required in dataset)

    Returns:
        None
    """

    # Chart setup
    plot_setup = kwargs.get('plot_setup')
    plot_setup = keys_to_lower(plot_setup)
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    extension = plot_setup['extension']
    dots_per_inch = plot_setup['dots_per_inch']
    marker = plot_setup['marker']
    marker_size = plot_setup['marker_size']
    line_width = plot_setup['line_width']
    line_style = plot_setup['line_style']
    y_axis_label = plot_setup['y_axis_label']
    x_axis_label = plot_setup['x_axis_label']
    labels_size = plot_setup['labels_size']
    labels_color = plot_setup['labels_color']
    x_axis_size = plot_setup['x_axis_size']
    y_axis_size = plot_setup['y_axis_size']
    axises_color = plot_setup['axises_color']
    x_limit = plot_setup['x_limit']
    y_limit = plot_setup['y_limit']
    colors = plot_setup['chart_color']
    grid = plot_setup['on_grid']
    y_log_scale = plot_setup['y_log']
    x_log_scale = plot_setup['x_log']
    legend = plot_setup['legend']
    loc_legend = plot_setup['legend_location']
    size_legend = plot_setup['size_legend']

    # Dataset
    dataset = kwargs.get('dataset')
    data = keys_to_lower(dataset)
    x_dataset = []
    y_dataset = []
    number_of_plots = int(len(data) / 2)
    for I in range(number_of_plots):
        x_column_name = f'x{I}'
        y_column_name = f'y{I}'
        x_dataset.append(data[x_column_name])
        y_dataset.append(data[y_column_name])

    # Plot
    w, h = convert_si_to_inches_in_chart_size(w, h)
    _, ax = plt.subplots(1, 1, figsize = (w, h), sharex=True)
    for k in range(number_of_plots):
        if len(legend) == 1:
            if legend[0] is None:
                ax.plot(x_dataset[k],
                        y_dataset[k],
                        marker=marker[k],
                        linestyle=line_style[k],
                        linewidth=line_width[k],
                        markersize=marker_size[k],
                        color=colors[k])
            else:
                ax.plot(x_dataset[k],
                        y_dataset[k],
                        marker=marker[k],
                        linestyle=line_style[k],
                        linewidth=line_width[k],
                        markersize=marker_size[k],
                        color=colors[k],
                        label=legend[k])
        else:
            ax.plot(x_dataset[k],
                    y_dataset[k],
                    marker=marker[k],
                    linestyle=line_style[k],
                    linewidth=line_width[k],
                    markersize=marker_size[k],
                    color=colors[k],
                    label=legend[k])
    if x_limit is not None:
        plt.xlim(x_limit[0], x_limit[1])
    if y_limit is not None:
        plt.ylim(y_limit[0], y_limit[1])
    if y_log_scale:
        ax.semilogy()
    if x_log_scale:
        ax.semilogx()
    font = {'fontname': 'DejaVu Sans',
            'color':  labels_color,
            'weight': 'normal',
            'size': labels_size}
    ax.set_ylabel(y_axis_label, fontdict=font)
    ax.set_xlabel(x_axis_label, fontdict=font)
    ax.tick_params(axis='x', labelsize=x_axis_size, colors=axises_color)
    ax.tick_params(axis='y', labelsize=y_axis_size, colors=axises_color)
    if grid is True:
        ax.grid(color='grey', linestyle='-.', linewidth=1, alpha=0.20)
    if len(legend) == 1:
        if legend[0] is None:
            pass
        else:
            plt.legend(loc=loc_legend,
                       prop={'size': size_legend})
    else:
        plt.legend(loc=loc_legend,
                   prop={'size': size_legend})
    plt.tight_layout()

    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)

    # Show figure
    plt.show()


def scatter_chart(**kwargs):    
    """
    This function shows a scatter chart.

    Args:
        plot_setup (Dictionary): Setup chart Dictionary with the following keys:
            name (String): Path + name figure (key required in plot_setup)
            width (Float): Figure width in SI units (key required in plot_setup)
            height (Float): Figure height in SI units (key required in plot_setup)
            extension (String): File extension (key required in plot_setup)
            dots_per_inch (Integer): The resolution in dots per inch (key required in plot_setup)
            marker_size (List): List of marker sizes (key required in plot_setup)
            color_map (String or List): String for color map values or list of colors in scatterplot. See <a href="https://matplotlib.org/stable/gallery/color/colormap_reference.html" target="_blank">gallery</a> (key required in plot_setup)
            y_axis_label (String): y axis label (key required in plot_setup)
            y_axis_size (Integer): y axis size (key required in plot_setup)
            x_axis_label (String): x axis label (key required in plot_setup)
            x_axis_size (Integer): x axis size (key required in plot_setup)
            labels_size (Integer): Labels size (key required in plot_setup)
            labels_color (String): Labels color (key required in plot_setup)
            axises_color (String): Axises color (key required in plot_setup)
            on_grid (Boolean): Grid on or off (key required in plot_setup)
            y_log (Boolean): y log scale (key required in plot_setup)
            x_log (Boolean): x log scale (key required in plot_setup)
            legend (List): List of legends (key required in plot_setup)
            legend_location (String): Legend location (key required in plot_setup)
            size_legend (Integer): Legend size (key required in plot_setup)
        dataset (Dictionary): Dataset. Add key 'colorbar' for colorbar in scatterplot
            x0 (List or array): x axis values for the first line (key required in dataset)
            y0 (List or array): y axis values for the first line (key required in dataset)
            x1 (List or array): x axis values for the second line (key required in dataset)
            y1 (List or array): y axis values for the second line (key required in dataset)
            xn (List or array): x axis values for the n-th line (key required in dataset)
            yn (List or array): y axis values for the n-th line (key required in dataset)
            colorbar (List): List of colorbar values (key required in dataset when colorbar is used. If not, it is not necessary)
    Returns:
        None
    """

    # Setup
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    marker_size = plot_setup['marker_size']
    color_map = plot_setup['color_map']
    y_axis_label = plot_setup['y_axis_label']
    y_axis_size = plot_setup['y_axis_size']
    x_axis_label = plot_setup['x_axis_label']
    x_axis_size = plot_setup['x_axis_size']
    labels_size = plot_setup['labels_size']  
    labels_color = plot_setup['labels_color']
    axises_color = plot_setup['axises_color']
    grid = plot_setup['on_grid']
    y_log_scale = plot_setup['y_log']
    x_log_scale = plot_setup['x_log']
    dots_per_inch = plot_setup['dots_per_inch']
    extension = plot_setup['extension']

    # Dataset
    data = kwargs.get('dataset')

    # Plot
    w, h = convert_si_to_inches_in_chart_size(w, h)
    fig, ax = plt.subplots(1, 1, figsize=(w, h), sharex=True)
    
    if isinstance(color_map, str):
        az = ax.scatter(data['x0'], data['y0'], c=data['colorbar'], marker='o', s=marker_size, cmap=color_map)
        cbar = fig.colorbar(az)
        cbar.ax.tick_params(labelsize=y_axis_size)
    else:
        legend = plot_setup['legend']
        loc_legend = plot_setup['legend_location']
        size_legend = plot_setup['size_legend']
        x_dataset = []
        y_dataset = []
        number_of_plots = int(len(data) / 2)
        for I in range(number_of_plots):
            x_column_name = f'x{I}'
            y_column_name = f'y{I}'
            x_dataset.append(data[x_column_name])
            y_dataset.append(data[y_column_name])
        for k in range(number_of_plots):
            if len(color_map) == 1:
                ax.scatter(x_dataset[k], y_dataset[k], marker='o', s=marker_size, c=color_map[0], label=legend[0])
            else:
                ax.scatter(x_dataset[k], y_dataset[k], marker='o', s=marker_size, c=color_map[k], label=legend[k])
        if len(legend) == 1:
            if legend[0] is None:
                pass
            else:
                plt.legend(loc=loc_legend,
                       prop={'size': size_legend})
        else:
            plt.legend(loc=loc_legend,
                    prop={'size': size_legend})
    if y_log_scale:
        ax.semilogy()
    if x_log_scale:
        ax.semilogx()
    font = {'fontname': 'DejaVu Sans',
                'color':  labels_color,
                'weight': 'normal',
                'size': labels_size}
    ax.set_ylabel(y_axis_label, fontdict=font)
    ax.set_xlabel(x_axis_label, fontdict=font)
    ax.tick_params(axis='x', labelsize=x_axis_size, colors=axises_color, labelrotation=0, direction='out', which='both', length=10)
    ax.tick_params(axis='y', labelsize=y_axis_size, colors=axises_color)
    if grid == True:
        ax.grid(color='grey', linestyle='-', linewidth=1, alpha=0.20)

    plt.tight_layout()

    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)

    # Show figure
    plt.show()


def bar_chart(**kwargs):
    """
    This function creates a bar chart.

    Args:
        plot_setup (Dictionary): Setup chart Dictionary with the following keys:
            name (String): Path + name figure (key required in plot_setup)
            width (Float): Figure width in SI units (key required in plot_setup)
            height (Float): Figure height in SI units (key required in plot_setup)
            extension (String): File extension (key required in plot_setup)
            dots_per_inch (Integer): The resolution in dots per inch (key required in plot_setup)
            y_axis_label (String): y axis label (key required in plot_setup)
            x_axis_label (String): x axis label (key required in plot_setup)
            labels_size (Integer): Labels size (key required in plot_setup)
            labels_color (String): Labels color (key required in plot_setup)
            x_axis_size (Integer): x axis size (key required in plot_setup)
            y_axis_size (Integer): y axis size (key required in plot_setup)
            axises_color (String): Axises color (key required in plot_setup)
            on_grid (Boolean): Grid on or off (key required in plot_setup)
            y_log (Boolean): y log scale (key required in plot_setup)
            x_log (Boolean): x log scale (key required in plot_setup)
            colors (List): List of colors for the bars (key required in plot_setup)
            bar width (Float): Width of each bar (key required in plot_setup)
            opacity (Float): Opacity of the bars (key required in plot_setup)
  
    Returns:
        None
    """

    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    bar_width = plot_setup['bar width']
    opacity = plot_setup['opacity']
    y_axis_label = plot_setup['y_axis_label']
    x_axis_label = plot_setup['x_axis_label']
    x_axis_size = plot_setup['x_axis_size']
    y_axis_size = plot_setup['y_axis_size']
    axises_color = plot_setup['axises_color']
    labels_size = plot_setup['labels_size']
    labels_color = plot_setup['labels_color']
    colors = plot_setup['colors']
    grid = plot_setup['on_grid']  
    y_log_scale = plot_setup['y_log']
    extension = plot_setup['extension']
    dots_per_inch = plot_setup['dots_per_inch']
    
    # data
    data = dataset['dataset']
    data_names = list(data.columns)
    data_names = [i.upper() for i in data_names]
    data.columns = data_names
    x = list(data['X'])
    y = data.drop(['X'], axis = 1, inplace = False)
    legend = list(y.columns)
    legend = [i.lower() for i in legend]
    y.columns = legend
    n_l, n_c = y.shape
   
    # Plot
    [w, h] = convert_si_to_inches_in_chart_size(w, h)
    fig, ax = plt.subplots(1, 1, figsize = (w, h))
    
    # Create the bar chart for each category
    pos = np.arange(len(x))
    
    for i, category in enumerate(legend):
        ax.bar(pos + bar_width * i, list(y[category]), width = bar_width, alpha = opacity, color = colors[i], label = category) #, error_kw = error_plot_setup)
    font = {'fontname': 'DejaVu Sans',
                'color':  labels_color,
                'weight': 'normal',
                'size': labels_size}
    ax.set_ylabel(y_axis_label, fontdict=font)
    ax.set_xlabel(x_axis_label, fontdict=font)
    ax.tick_params(axis = 'x', labelsize = x_axis_size, colors = axises_color)
    ax.tick_params(axis = 'y', labelsize = y_axis_size, colors = axises_color)
    if n_c > 1:
        maxx = pos + bar_width * (n_c - 1)
        minn = pos
        pos_t_extension = pos  + (maxx - minn) / 2
        ax.set_xticks(pos_t_extension, x)
    else:
        pos_t_extension = pos
        ax.set_xticks(pos_t_extension, x)
    ax.set_xticklabels(x)
    ax.legend()
    if y_log_scale:
        ax.semilogy()

    if grid == True:
        ax.grid(color = 'grey', linestyle = '-', linewidth = 1, alpha = 0.20, axis = 'y')
    plt.tight_layout()

    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)


def pizza_chart(**kwargs):
    """
    This function creates a pie chart.

    Args:
        plot_setup (Dictionary): Setup chart Dictionary with the following keys:
            name (String): Path + name figure (key required in plot_setup)
            width (Float): Figure width in SI units (key required in plot_setup)
            height (Float): Figure height in SI units (key required in plot_setup)
            text color (String): Color of the text extensions (key required in plot_setup)
            text font size (Integer): Font size of the text extensions (key required in plot_setup)
            colors (List): List of colors for the pie slices (key required in plot_setup)
            size_legend (Integer): Font size of the legend (key required in plot_setup)
            dots_per_inch (Integer): The resolution in dots per inch (key required in plot_setup)
            extension (String): File extension (key required in plot_setup)
                
    Returns:
        None
    """

    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    textension_color = plot_setup['text color']
    textension_font_size = plot_setup['text font size']
    colors = plot_setup['colors']
    legend_size = plot_setup['size_legend']
    dots_per_inch = plot_setup['dots_per_inch']
    extension = plot_setup['extension']
    
    # dataset
    data = dataset['dataset']
    data_names = list(data.columns)
    data_names = [i.upper() for i in data_names]
    data.columns = data_names
    elements = list(data['CATEGORY'])
    values = list(data['VALUES'])
    
    # Creating autopct arguments
    def func(pct, allvalues):
        absolute = int(pct / 100.*np.sum(allvalues))
        return "{:.2f}%\n({:d})".format(pct, absolute)
        
    # Plot
    w, h = convert_si_to_inches_in_chart_size(w, h)
    fig, ax = plt.subplots(1, 1, figsize=(w, h), subplot_kw={'aspect': 'equal'})
    wedges, textensions, autotextensions = ax.pie(values, autopct=lambda pct: func(pct, values), textprops={'color': textension_color}, colors=colors)
    ax.legend(wedges, elements, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=legend_size)
    plt.setp(autotextensions, size=textension_font_size, weight='bold')
    
    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)


def radar_chart(**kwargs):
    """
    This function creates a radar chart.

    Args:
        plot_setup (dictionary): Setup chart dictionary with the following keys:
            name (string): Path + name figure (key required in plot_setup)
            width (float): Figure width in SI units (key required in plot_setup)
            height (float): Figure height in SI units (key required in plot_setup)
            text size (integer): Font size of the radar divisions (key required in plot_setup)
            div color (string): Color of the radar divisions (key required in plot_setup)
            radar color (list): List of colors for the radar lines and areas (key required in plot_setup)
            opacity (float): Opacity of the radar areas (key required in plot_setup)
            background (string): Color of the polar background (key required in plot_setup)
            legend size (integer): Font size of the legend (key required in plot_setup)
            dots_per_inch (integer): The resolution in dots per inch (key required in plot_setup)
            extension (string): File extension (key required in plot_setup)
            
    Returns:
        None
    """
    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    width = plot_setup['width']
    height = plot_setup['height']
    radar_div_size = plot_setup['text size']
    radar_div_color = plot_setup['div color']
    radar_color = plot_setup['radar color']
    opacity = plot_setup['opacity']
    polar_color = plot_setup['background']
    size_legend = plot_setup['legend size']
    dots_per_inch = plot_setup['dots_per_inch']
    extension = plot_setup['extension']
    
    # Data
    data = dataset['dataset']
    data_names = list(data.columns)
    data_names = [i.lower() for i in data_names]
    data.columns = data_names
    
    if 'group' not in data.columns or len(data.columns) == 1:
        print("Error: There are no category columns in the DataFrame or they are missing after data manipulation.")
        return
    
    y = data.drop(['group'], axis=1, inplace=False)
    min_value = min(list(y.min()))
    max_value = max(list(y.max()))
    n_div = 5
    interval = (max_value - min_value) / (n_div - 1)
    radar_div = [round(min_value + i * interval, 0) for i in range(n_div)]
    radar_label = [str(div) for div in radar_div]

    # Plot
    w, h = convert_si_to_inches_in_chart_size(width, height)
    fig, ax = plt.subplots(1, 1, figsize=(w, h), subplot_kw={'projection': 'polar'})
    categories = list(data)[1:]
    n = len(categories)
    angles = [n / float(n) * 2 * np.pi for n in range(n)]
    angles += angles[:1]
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)  
    plt.xticks(angles[:-1], categories, size=radar_div_size)  
    ax.set_rlabel_position(180 / n)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')
    plt.yticks(radar_div, radar_label, color=radar_div_color, size=radar_div_size)
    max_value = max(list(data.max())[1:])
    plt.ylim(0, max_value)
    for i in range(len(list(data['group']))):
        group = list(data['group'])
        values = data.iloc[i].drop('group').values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=2, linestyle='--', label=group[i], c=radar_color[i])
        ax.fill(angles, values, radar_color[i], alpha=opacity)
    ax.set_facecolor(polar_color)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), prop={'size': size_legend})

    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)


def heatmap_chart(**kwargs):
    """
    This function creates a heatmap chart.

    Args:
        plot_setup (dictionary): Setup chart dictionary with the following keys:
            name (string): Path + name figure (key required in plot_setup)
            width (float): Figure width in SI units (key required in plot_setup)
            height (float): Figure height in SI units (key required in plot_setup)
            extension (string): File extension (key required in plot_setup)
            dots_per_inch (integer): The resolution in dots per inch (key required in plot_setup)
            mask (boolean): Whether to use a mask for the upper triangle (key required in plot_setup)
            line_widths (float): Width of the lines between cells (key required in plot_setup)
            color map (string or list): Color map for the heatmap (key required in plot_setup)
            line color (string): Color of the lines between cells (key required in plot_setup)
            annot (boolean): Whether to annotate each cell with the correlation value (key required in plot_setup)
            annot size font (integer): Font size of the annotations (key required in plot_setup)
            
    Returns:
        None
    """

    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    extension = plot_setup['extension']
    dots_per_inch = plot_setup['dots_per_inch']
    escada = plot_setup['mask']
    line_widths = plot_setup['line_widths']
    color_map =  plot_setup['color map']
    line_color = plot_setup['line color']
    annot =  plot_setup['annot']
    annot_size_font = plot_setup['annot size font']
    annot_font_weight = 'bold'

    # Dataset
    data = dataset['dataset']
    correlations = data.corr()
    
    # Plot
    w, h = convert_si_to_inches_in_chart_size(w, h)
    fig, ax = plt.subplots(1, 1, figsize=(w, h), sharex=True)
    if escada:
        mask = np.triu(np.ones_like(correlations))
    else:
        mask = None  
    sns.heatmap(correlations, center=0, linewidths=line_widths, xticklabels=True,
                linecolor=line_color, annot=annot, vmin=-1, vmax=1,
                annot_kws={'fontsize': annot_size_font, 'fontweight': annot_font_weight},
                cmap=color_map, mask=mask, ax=ax)
    plt.gca().invert_yaxis()
    ax.tick_params(axis='y', rotation=0)   

    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)


def treemap_chart(**kwargs):
    """
    This function creates a treemap chart.

    Args:
        plot_setup (dictionary): Setup chart dictionary with the following keys:
            name (string): Path + name figure (key required in plot_setup)
            width (float): Figure width in SI units (key required in plot_setup)
            height (float): Figure height in SI units (key required in plot_setup)
            dots_per_inch (integer): The resolution in dots per inch (key required in plot_setup)
            extension (string): File extension (key required in plot_setup)
            colors (list): List of colors for the treemap (key required in plot_setup)
            labels (list): List of labels for the treemap (key required in plot_setup)
            label size (integer): Font size of the labels (key required in plot_setup)
            
    Returns:
        None
    """

    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    width = plot_setup['width']
    height = plot_setup['height']
    dots_per_inch = plot_setup['dots_per_inch']
    extension = plot_setup['extension']
    colors = plot_setup['colors']
    labels = plot_setup['labels']
    label_size = plot_setup['label size']

    # Dataset and other information
    values = dataset['dataset']['values']

    
    # Plot
    w, h = convert_si_to_inches_in_chart_size(width, height)
    fig, ax = plt.subplots(1, 1, figsize=(w, h), sharex=True)
    percentage = []
    for value in values:
        percentage.append(round(value * 100 / sum(values), 2))
    labels_with_percentage = []
    for i in range(len(values)):
        labels_with_percentage.append(labels[i] + '\n' + str(percentage[i]) + '%')
    squarify.plot(sizes=values, label=labels_with_percentage, color=colors, ec='white', text_kwargs={'fontsize': label_size})
    ax.axis('off')

    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)


def join_hist_chart(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-9.html
    """

    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    width = plot_setup['width']
    height = plot_setup['height']
    x_axis_size = plot_setup['x_axis_size']
    x_axis_color = plot_setup['X axIS color']
    OVERLAP = 0
    dots_per_inch = plot_setup['dots_per_inch']
    extension = plot_setup['extension']
    
    # dataset
    data = dataset['dataset']
    data_nameS = List(data.columns)
    data_nameS = [i.upper() for i in data_nameS]
    data.columns = data_nameS
    
    # Plot
    w, h = convert_si_to_inches_in_chart_size(width, height)
    fig, ax = joypy.joyplot(data, overlap = OVERLAP)
    plt.tick_params(axis = 'x', labelsize = x_axis_size, colors = x_axis_color)
    plt.tick_params(axis = 'y', labelsize = x_axis_size, colors = x_axis_color)
    
    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)
   

def multiple_lines_chart(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-10.html
    """
    
    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    extension = plot_setup['extension']
    dots_per_inch = plot_setup['dots_per_inch']
    marker = plot_setup['marker']
    marker_size = plot_setup['marker_size']
    line_width = plot_setup['line_width']
    line_style = plot_setup['line_style']
    Y0_axIS_LABEL = plot_setup['Y0 axIS LABEL']
    Y1_axIS_LABEL = plot_setup['Y1 axIS LABEL']
    x_axis_label = plot_setup['x_axis_label']
    labels_size = plot_setup['labels_size']     
    x_axis_size = plot_setup['x_axis_size']
    y_axis_size = plot_setup['y_axis_size']
    colors = plot_setup['chart_color']
    grid = plot_setup['on_grid']
    y_log_scale = plot_setup['y_log']
    x_log_scale = plot_setup['x_log']
    legend = plot_setup['legend']
    loc_legend = plot_setup['legend_location']
    size_legend = plot_setup['size_legend']
    
    # dataset and others information
    data = dataset['dataset']
    data_nameS = List(data.columns)
    data_nameS = [i.upper() for i in data_nameS]
    data.columns = data_nameS
    X = List(data['X'])
    Y = data.drop(['X'], axis = 1, inplace = False)
    
    # Plot
    w, h = convert_si_to_inches_in_chart_size(w, h)
    fig, ax = plt.subplots(1, 1, figsize = (w, h), sharex = True)
    ax.plot(X, Y['Y0'], marker = marker[0],  linestyle = line_style[0], linewidth = line_width, markersize = marker_size, label = legend[0], color = colors[0])
            
    if y_log_scale:
        ax.semilogy()
    if x_log_scale:
        ax.semilogx()
    fontx = {'fontname': 'DejaVu Sans',
            'color':  '#000000',
            'weight': 'normal',
            'size': labels_size}
    fonty0 = {'fontname': 'DejaVu Sans',
            'color':  colors[0],
            'weight': 'normal',
            'size': labels_size}
    ax.set_xlabel(x_axis_label, fontDictionary = fontx)  
    ax.set_ylabel(Y0_axIS_LABEL, fontDictionary = fonty0)
    ax.tick_params(axis = 'x', labelsize = x_axis_size, colors = '#000000')
    ax.tick_params(axis = 'y', labelsize = y_axis_size, colors = colors[0])
    plt.legend(loc_legend = loc_legend, prop = {'size': size_legend})
    ax2 = ax.twinx()
    fonty1 = {'fontname': 'DejaVu Sans',
            'color':  colors[1],
            'weight': 'normal',
            'size': labels_size}
    ax2.set_ylabel(Y1_axIS_LABEL, fontDictionary = fonty1)
    ax2.plot(X, Y['Y1'], marker = marker[1],  linestyle = line_style[1], linewidth = line_width, markersize = marker_size, label = legend[1], color = colors[1])
    ax2.tick_params(axis = 'y', labelsize = y_axis_size, labelcolor = colors[1])
    if grid == True:
        ax.grid(color = 'grey', linestyle = '-.', linewidth = 1, alpha = 0.20)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    plt.legend(h1+h2, l1+l2, loc_legend = loc_legend, prop = {'size': size_legend})
    
    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)
    

def regplot_chart(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-11.html
    """

    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    marker_size = plot_setup['marker_size']
    color_map = plot_setup['SCATTER color']
    line_color = plot_setup['line color']
    ORDER = plot_setup['ORDER'] 
    y_axis_label = plot_setup['y_axis_label']
    y_axis_size = plot_setup['y_axis_size']
    x_axis_label = plot_setup['x_axis_label']
    x_axis_size = plot_setup['x_axis_size']
    labels_size = plot_setup['labels_size']  
    labels_color = plot_setup['labels_color']
    axises_color = plot_setup['axises_color']
    grid = plot_setup['on_grid']
    y_log_scale = plot_setup['y_log']
    x_log_scale = plot_setup['x_log']
    dots_per_inch = plot_setup['dots_per_inch']
    extension = plot_setup['extension']

    # data
    data = dataset['dataset']
    data_nameS = List(data.columns)
    data_nameS = [i.upper() for i in data_nameS]
    data.columns = data_nameS
    X = data['X']
    Y = data['Y']
    
    # Plot
    w, h = convert_si_to_inches_in_chart_size(w, h)
    fig, ax = plt.subplots(1, 1, figsize = (w, h))   
    IM = sns.regplot(x = X, y = Y,
                    scatter_kws = {"color": color_map, "alpha": 0.20, "s": marker_size},
                    line_kws = {"color": line_color},
                    ci = 99, order = ORDER) # 99% level
    if y_log_scale:
        ax.semilogy()
    if x_log_scale:
        ax.semilogx()
    FONT = {'fontname': 'DejaVu Sans',
            'color':  labels_color,
            'weight': 'normal',
            'size': labels_size}
    ax.set_ylabel(y_axis_label, fontDictionary = FONT)
    ax.set_xlabel(x_axis_label, fontDictionary = FONT)   
    ax.tick_params(axis = 'x', labelsize = x_axis_size, colors = axises_color, labelrotation = 0, direction = 'out', which = 'both', length = 10)
    ax.tick_params(axis = 'y', labelsize = y_axis_size, colors = axises_color)
    if grid == True:
        ax.grid(color = 'grey', linestyle = '-', linewidth = 1, alpha = 0.20)
    
    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)


def scatter_line_chart(**kwargs):
    """
    This function shows a multiple lines and scatter points in single chart.

    Args:
        plot_setup (Dictionary): Setup chart Dictionary with the following keys:
            name (String): Path + name figure (key required in plot_setup)
            width (Float): figure width in SI units (key required in plot_setup)
            height (Float): figure height in SI units (key required in plot_setup)
            extension (String): File extension (key required in plot_setup)
            dots_per_inch (Integer): The resolution in dots per inch (key required in plot_setup)
            marker (List): List of markers. See <a href="https://matplotlib.org/stable/gallery/lines_bars_and_markers/marker_reference.html#sphx-glr-gallery-lines-bars-and-markers-marker-reference-py" target="_blank">gallery</a> (key required in plot_setup)
            marker_size (List): List of marker sizes (key required in plot_setup)
            line_width (List): List of line widths (key required in plot_setup)
            line_style (List): List of line styles. See <a href="https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html" target="_blank">gallery</a> (key required in plot_setup) 
            x_axis_label (String): x axis label (key required in plot_setup)
            x_axis_size (Integer): x axis size (key required in plot_setup)
            y_axis_label (String): y axis label (key required in plot_setup)
            y_axis_size (Integer): y axis size (key required in plot_setup)
            axises_color (String): Axises color (key required in plot_setup)
            labels_size (Integer): Labels size (key required in plot_setup)
            labels_color (String): Labels color (key required in plot_setup)
            chart_color (List): List of chart_colors (key required in plot_setup)
            x_limit (List): x axis limits (key required in plot_setup)
            y_limit (List): y axis limits (key required in plot_setup)
            on_grid (Boolean): Grid on or off (key required in plot_setup)
            y_log (Boolean): y log scale (key required in plot_setup)
            x_log (Boolean): x log scale (key required in plot_setup)
            legend line (List): List of legends (key required in plot_setup)
            legend scatter (List): List of legends (key required in plot_setup)
            legend_location (String): Legend location (key required in plot_setup)
            size_legend (Integer): Legend size (key required in plot_setup)
        dataset_line (Dictionary): Dataset with the following
            x0 (List or array): x axis values for the first line (key required in dataset)
            y0 (List or array): y axis values for the first line (key required in dataset)
            x1 (List or array): x axis values for the second line (key required in dataset)
            y1 (List or array): y axis values for the second line (key required in dataset)
            xn (List or array): x axis values for the n-th line (key required in dataset)
            yn (List or array): y axis values for the n-th line (key required in dataset)
        dataset_sc (Dictionary): Dataset with the following
            x0 (List or array): x axis values for the first line (key required in dataset)
            y0 (List or array): y axis values for the first line (key required in dataset)
            x1 (List or array): x axis values for the second line (key required in dataset)
            y1 (List or array): y axis values for the second line (key required in dataset)
            xn (List or array): x axis values for the n-th line (key required in dataset)
            yn (List or array): y axis values for the n-th line (key required in dataset)

    Returns:
        None
    """

    # Chart setup
    plot_setup = kwargs.get('plot_setup')
    plot_setup = keys_to_lower(plot_setup)
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    extension = plot_setup['extension']
    dots_per_inch = plot_setup['dots_per_inch']
    marker = plot_setup['marker_line']
    marker_size = plot_setup['marker_size_line']
    marker_size_scatter = plot_setup['marker_size_scatter']
    line_width = plot_setup['line_width']
    line_style = plot_setup['line_style']
    y_axis_label = plot_setup['y_axis_label']
    x_axis_label = plot_setup['x_axis_label']
    labels_size = plot_setup['labels_size']
    labels_color = plot_setup['labels_color']
    x_axis_size = plot_setup['x_axis_size']
    y_axis_size = plot_setup['y_axis_size']
    axises_color = plot_setup['axises_color']
    x_limit = plot_setup['x_limit']
    y_limit = plot_setup['y_limit']
    colors = plot_setup['chart_color_line']
    color_map = plot_setup['color_map']
    grid = plot_setup['on_grid']
    y_log_scale = plot_setup['y_log']
    x_log_scale = plot_setup['x_log']
    legend = plot_setup['legend_line']
    legend_sc = plot_setup['legend_scatter']
    loc_legend = plot_setup['legend_location']
    size_legend = plot_setup['size_legend']

    # Dataset
    dataset = kwargs.get('dataset_line')
    data = keys_to_lower(dataset)
    dataset_sc = kwargs.get('dataset_sc')
    data_sc = keys_to_lower(dataset_sc)
    x_dataset = []
    y_dataset = []
    number_of_plots = int(len(data) / 2)
    for I in range(number_of_plots):
        x_column_name = f'x{I}'
        y_column_name = f'y{I}'
        x_dataset.append(data[x_column_name])
        y_dataset.append(data[y_column_name])
    x_dataset_sc = []
    y_dataset_sc = []
    number_of_plots_sc = int(len(data_sc) / 2)
    for I in range(number_of_plots_sc):
        x_column_name = f'x{I}'
        y_column_name = f'y{I}'
        x_dataset_sc.append(data_sc[x_column_name])
        y_dataset_sc.append(data_sc[y_column_name])
    # Plot
    w, h = convert_si_to_inches_in_chart_size(w, h)
    _, ax = plt.subplots(1, 1, figsize = (w, h), sharex=True)
    for k in range(number_of_plots):
        if len(legend) == 1:
            if legend[0] is None:
                ax.plot(x_dataset[k],
                        y_dataset[k],
                        marker=marker[k],
                        linestyle=line_style[k],
                        linewidth=line_width[k],
                        markersize=marker_size[k],
                        color=colors[k])
            else:
                ax.plot(x_dataset[k],
                        y_dataset[k],
                        marker=marker[k],
                        linestyle=line_style[k],
                        linewidth=line_width[k],
                        markersize=marker_size[k],
                        color=colors[k],
                        label=legend[k])
        else:
            ax.plot(x_dataset[k],
                    y_dataset[k],
                    marker=marker[k],
                    linestyle=line_style[k],
                    linewidth=line_width[k],
                    markersize=marker_size[k],
                    color=colors[k],
                    label=legend[k])
    for k in range(number_of_plots_sc):
        if len(color_map) == 1:
            ax.scatter(x_dataset_sc[k], y_dataset_sc[k], marker='o', s=marker_size_scatter[0], c=color_map[0], label=legend_sc[0])
        else:
            ax.scatter(x_dataset_sc[k], y_dataset_sc[k], marker='o', s=marker_size_scatter[k], c=color_map[k], label=legend_sc[k])
    if len(legend) == 1:
        if legend[0] is None:
            pass
        else:
            plt.legend(loc=loc_legend,
                    prop={'size': size_legend})
    else:
        plt.legend(loc=loc_legend,
                prop={'size': size_legend})
    if x_limit is not None:
        plt.xlim(x_limit[0], x_limit[1])
    if y_limit is not None:
        plt.ylim(y_limit[0], y_limit[1])
    if y_log_scale:
        ax.semilogy()
    if x_log_scale:
        ax.semilogx()
    font = {'fontname': 'DejaVu Sans',
            'color':  labels_color,
            'weight': 'normal',
            'size': labels_size}
    ax.set_ylabel(y_axis_label, fontdict=font)
    ax.set_xlabel(x_axis_label, fontdict=font)
    ax.tick_params(axis='x', labelsize=x_axis_size, colors=axises_color)
    ax.tick_params(axis='y', labelsize=y_axis_size, colors=axises_color)
    if grid is True:
        ax.grid(color='grey', linestyle='-.', linewidth=1, alpha=0.20)
    if len(legend) == 1:
        if legend[0] is None:
            pass
        else:
            plt.legend(loc=loc_legend,
                       prop={'size': size_legend})
    else:
        plt.legend(loc=loc_legend,
                   prop={'size': size_legend})
    plt.tight_layout()

    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)

    # Show figure
    plt.show()


def contour_chart(dataset, plot_setup):    
    
    # Setup
    name = plot_setup['name']
    dots_per_inch = plot_setup['dots_per_inch']
    extension = plot_setup['extension']
    TITLE = plot_setup['TITLE']
    LEVELS = plot_setup['LEVELS']
    
    # data
    X = dataset['X']
    Y = dataset['Y']
    Z = dataset['Z']

    # Filled contour
    fig, ax = plt.subplots()
    cnt = ax.contourf(X, Y, Z, levels = LEVELS)

    # color bar
    cbar = ax.figure.colorbar(cnt, ax = ax)
    cbar.ax.set_ylabel(TITLE, rotation = -90, va = "bottom")

    save_chart_in_folder(name, extension, dots_per_inch)


if __name__ == "__main__":
    pass