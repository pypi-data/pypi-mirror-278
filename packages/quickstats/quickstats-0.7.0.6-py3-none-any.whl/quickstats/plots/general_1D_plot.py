from typing import Dict, Optional, Union, List, Tuple
import pandas as pd
import numpy as np

from quickstats.plots import AbstractPlot, StatPlotConfig
from quickstats.plots.core import color_to_rgba
from quickstats.plots.template import create_transform, handle_has_label
from quickstats.utils.common_utils import combine_dict

class General1DPlot(AbstractPlot):

    STYLES = {
        'fill_between': {
             'alpha': 0.3,
             'hatch': None,
             'linewidth': 1.0
        }
    }
    
    CONFIG = {
        'errorband_legend': True
    }
    
    def __init__(self, data_map:Union[pd.DataFrame, Dict[str, pd.DataFrame]],
                 label_map:Optional[Dict]=None,
                 styles_map:Optional[Dict]=None,
                 color_cycle=None,
                 styles:Optional[Union[Dict, str]]=None,
                 analysis_label_options:Optional[Dict]=None,
                 config:Optional[Dict]=None):
        
        self.data_map = data_map
        self.label_map = label_map
        self.styles_map = styles_map
        
        super().__init__(color_cycle=color_cycle,
                         styles=styles,
                         analysis_label_options=analysis_label_options,
                         config=config)
        
        self.stat_configs = {}
        
    def get_default_legend_order(self):
        if not isinstance(self.data_map, dict):
            return []
        else:
            return list(self.data_map)
        
    def configure_stats(self, stat_configs:List[StatPlotConfig],
                        targets:Optional[Union[str, List[str]]]=None,
                        extend:bool=True):
        if not isinstance(targets, list):
            targets = [targets]
        for target in targets:
            if extend and (target in self.stat_configs):
                self.stat_configs[target].extend(stat_configs)
            else:
                self.stat_configs[target] = stat_configs
        
    def draw_single_data(self, ax, data:pd.DataFrame,
                         xattrib:str, yattrib:str,
                         yerrloattrib:Optional[str]=None,
                         yerrhiattrib:Optional[str]=None,
                         stat_configs:Optional[List[StatPlotConfig]]=None,
                         styles:Optional[Dict]=None,
                         label:Optional[str]=None):
        data = data.reset_index()
        x, y = data[xattrib].values, data[yattrib].values
        indices = np.argsort(x)
        x, y = x[indices], y[indices]
        draw_styles = combine_dict(self.styles['plot'], styles)
        fill_styles = combine_dict(self.styles['fill_between'])
            
        if (yerrloattrib is not None) and (yerrhiattrib is not None):
            yerrlo = data[yerrloattrib][indices]
            yerrhi = data[yerrhiattrib][indices]
            handle_fill = ax.fill_between(x, yerrlo, yerrhi,
                                          **fill_styles)
        else:
            handle_fill = None
        
        handle_plot = ax.plot(x, y, **draw_styles, label=label)
        if isinstance(handle_plot, list) and (len(handle_plot) == 1):
            handle_plot = handle_plot[0]

        if handle_fill and ('color' not in fill_styles):
            plot_color = handle_plot.get_color()
            fill_color = color_to_rgba(plot_color)
            handle_fill.set_color(fill_color)
        
        if stat_configs is not None:
            stat_handles = []
            for stat_config in stat_configs:
                stat_config.set_data(y)
                stat_handle = stat_config.apply(ax, handle[0])
                stat_handles.append(stat_handle)
        else:
            stat_handles = None

        if self.config['errorband_legend'] and (handle_fill is not None):
            handles = (handle_plot, handle_fill)
        else:
            handles = handle_plot
        return handles, stat_handles
    
    def draw(self, xattrib:str, yattrib:str,
             yerrloattrib:Optional[str]=None,
             yerrhiattrib:Optional[str]=None,
             targets:Optional[List[str]]=None,
             xlabel:Optional[str]=None, ylabel:Optional[str]=None,
             ymin:Optional[float]=None, ymax:Optional[float]=None,
             xmin:Optional[float]=None, xmax:Optional[float]=None,
             ypad:Optional[float]=0.3,
             logx:bool=False, logy:bool=False,
             draw_stats:bool=True):
        
        ax = self.draw_frame(logx=logx, logy=logy)
        
        legend_order = []
        if isinstance(self.data_map, pd.DataFrame):
            if draw_stats and (None in self.stat_configs):
                stat_configs = self.stat_configs[None]
            else:
                stat_configs = None
            handle, stat_handles = self.draw_single_data(ax, self.data_map,
                                                         xattrib=xattrib,
                                                         yattrib=yattrib,
                                                         yerrloattrib=yerrloattrib,
                                                         yerrhiattrib=yerrhiattrib,
                                                         stat_configs=stat_configs,
                                                         styles=self.styles_map)
        elif isinstance(self.data_map, dict):
            if targets is None:
                targets = list(self.data_map.keys())
            if self.styles_map is None:
                styles_map = {k:None for k in self.data_map}
            else:
                styles_map = self.styles_map
            if self.label_map is None:
                label_map = {k:k for k in self.data_map}
            else:
                label_map = self.label_map
            handles = {}
            for target in targets:
                data = self.data_map[target]
                styles = styles_map.get(target, None)
                label = label_map.get(target, "")
                if draw_stats:
                    if target in self.stat_configs:
                        stat_configs = self.stat_configs[target]
                    elif None in self.stat_configs:
                        stat_configs = self.stat_configs[None]
                    else:
                        stat_configs = None
                else:
                    stat_configs = None
                handle, stat_handles = self.draw_single_data(ax, data, 
                                                             xattrib=xattrib,
                                                             yattrib=yattrib,
                                                             yerrloattrib=yerrloattrib,
                                                             yerrhiattrib=yerrhiattrib,
                                                             stat_configs=stat_configs,
                                                             styles=styles,
                                                             label=label)
                handles[target] = handle
                if stat_handles is not None:
                    for i, stat_handle in enumerate(stat_handles):
                        if handle_has_label(stat_handle):
                            handle_name = f"{target}_stat_handle_{i}"
                            handles[handle_name] = stat_handle
            legend_order.extend(handles.keys())
            self.update_legend_handles(handles)
        else:
            raise ValueError("invalid data format")
            
        self.legend_order = legend_order
        self.draw_legend(ax)
        
        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel)
        self.set_axis_range(ax, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, ypad=ypad)
        
        return ax
