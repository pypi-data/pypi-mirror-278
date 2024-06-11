from typing import Optional, Union, Dict, List, Tuple, Callable, Sequence
from cycler import cycler
from itertools import cycle

import numpy as np
import matplotlib

from quickstats import AbstractObject, semistaticmethod
from quickstats.plots import get_color_cycle, get_cmap
from quickstats.plots.color_schemes import QUICKSTATS_PALETTES
from quickstats.plots.template import (single_frame, ratio_frame,
                                       parse_styles, format_axis_ticks,
                                       parse_analysis_label_options, centralize_axis,
                                       create_transform, draw_multiline_text,
                                       CUSTOM_HANDLER_MAP)
from quickstats.utils.common_utils import combine_dict, insert_periodic_substr
from quickstats.maths.statistics import bin_center_to_bin_edge, get_hist_comparison_data, select_binned_data
from quickstats.maths.statistics import HistComparisonMode
from quickstats.maths.numerics import get_mask, get_subsequences
from .core import PlotFormat, ErrorDisplayFormat

class AbstractPlot(AbstractObject):
    
    STYLES = {}
    
    COLOR_CYCLE = "default"
    
    COLOR_PALLETE = {}
    COLOR_PALLETE_SEC = {}
    
    CONFIG = {
        "xlabellinebreak": 50,
        "ylabellinebreak": 50,
        'ratio_line_styles':{
            'color': 'gray',
            'linestyle': '--',
            'zorder': 0
        },        
    }
    
    @property
    def hep_data(self):
        return self._hep_data
    
    def __init__(self,
                 color_pallete:Optional[Dict]=None,
                 color_pallete_sec:Optional[Dict]=None,
                 color_cycle:Optional[Union[List, str, "ListedColorMap"]]=None,
                 styles:Optional[Union[Dict, str]]=None,
                 analysis_label_options:Optional[Dict]=None,
                 figure_index:Optional[int]=None,
                 config:Optional[Dict]=None,
                 verbosity:Optional[Union[int, str]]='INFO'):
        super().__init__(verbosity=verbosity)
        
        self.color_pallete     = combine_dict(self.COLOR_PALLETE, color_pallete)
        self.color_pallete_sec = combine_dict(self.COLOR_PALLETE_SEC, color_pallete_sec)
            
        self.styles = combine_dict(self.STYLES, styles)
        self.styles = parse_styles(self.styles)
        
        if analysis_label_options is None:
            self.analysis_label_options = None
        else:
            self.analysis_label_options = parse_analysis_label_options(analysis_label_options)

        self.reset_legend_data()
        
        self.figure_index = figure_index
        
        self.config = combine_dict(AbstractPlot.CONFIG, self.CONFIG)
        if config is not None:
            self.config = combine_dict(self.config, config)

        self.set_color_cycle(color_cycle)
            
        self.annotation_list = []
        
        self._hep_data = {}
    
    def reset_legend_data(self):
        self.legend_data = {}
        self.legend_data_sec = {}
        self.legend_data_ext = {}
        self.legend_order = self.get_default_legend_order()
        
    def add_annotation(self, text:str, **kwargs):
        self.annotation_list.append({"text": text, **kwargs})
        
    def set_color_cycle(self, color_cycle:Optional[Union[List, str, "ListedColorMap"]]=None):
        if color_cycle is None:
            color_cycle = self.COLOR_CYCLE
        self.cmap = get_cmap(color_cycle)
        self.color_cycle = cycle(self.cmap.colors)
        
    def get_hep_data(self):
        return combine_dict(self.hep_data)
        
    def get_colors(self):
        return get_color_cycle(self.cmap).by_key()['color']
        
    def get_default_legend_order(self):
        return []
    
    def get_styles(self, name:str):
        return self.styles.get(name, {})
    
    @semistaticmethod
    def resolve_handle_label(self, handle):
        if isinstance(handle, matplotlib.container.Container):
            label = handle.get_label()
            if label.startswith('_'):
                return self.resolve_handle_label(handle[0])
        elif isinstance(handle, list):
            return self.resolve_handle_label(handle[0])
        elif isinstance(handle, tuple):
            _, label = self.resolve_handle_label(handle[0])
            handle = tuple([h[0] if (isinstance(h, list) and len(h) == 1) \
                            else h for h in handle])
        elif hasattr(handle, 'get_label'):
            label = handle.get_label()
        else:
            raise RuntimeError('unable to extract label from the handle')
        return handle, label
                      
    def update_legend_handles(self, handles:Dict, sec:bool=False,
                              idx:Optional[int]=None):
        if idx is None:
            if not sec:
                legend_data = self.legend_data
            else:
                legend_data = self.legend_data_sec
        else:
            if idx not in self.legend_data_ext:
                self.legend_data_ext[idx] = {}
            legend_data = self.legend_data_ext[idx]
            
        for key in handles:
            handle = handles[key]
            handle, label = self.resolve_handle_label(handle)
            if label and not label.startswith('_'):
                legend_data[key] = {
                    'handle': handle,
                    'label': label
                }
                
    def add_legend_decoration(self, decorator, targets:List[str]):
        for key, legend_data in self.legend_data.items():
            if key not in targets:
                continue
            handle = legend_data["handle"]
            if isinstance(handle, (list, tuple)):
                new_handle = (*handle, decorator)
            else:
                new_handle = (handle, decorator)
            legend_data["handle"] = new_handle

    def get_legend_handles_labels(self, sec:bool=False,
                                  idx:Optional[Union[int, List[int]]]=None):
        handles = []
        labels = []
        if idx is None:
            if not sec:
                legend_data = self.legend_data
            else:
                legend_data = self.legend_data_sec        
            for key in self.legend_order:
                if key in legend_data:
                    handle = legend_data[key]['handle']
                    label = legend_data[key]['label']
                    handles.append(handle)
                    labels.append(label)
        else:
            if isinstance(idx, int):
                indices = [idx]
            else:
                indices = idx
            for index in indices:
                legend_data = self.legend_data_ext[index]
                for key in self.legend_order:
                    if key in legend_data:
                        handle = legend_data[key]['handle']
                        label = legend_data[key]['label']
                        handles.append(handle)
                        labels.append(label)
        return handles, labels
    
    def draw_frame(self, ratio:bool=False, **kwargs):
        if ratio:
            frame_method = ratio_frame
        else:
            frame_method = single_frame
        ax = frame_method(styles=self.styles,
                          prop_cycle=get_color_cycle(self.cmap),
                          analysis_label_options=self.analysis_label_options,
                          figure_index=self.figure_index,
                          **kwargs)
        for annotation_kwargs in self.annotation_list:
            annotation_kwargs = combine_dict(self.styles['annotation'], annotation_kwargs)
            if isinstance(ax, tuple):
                ax[0].annotate(**annotation_kwargs)
            else:
                ax.annotate(**annotation_kwargs)
        self.figure = matplotlib.pyplot.gcf()
        return ax
    
    def draw_axis_labels(self, ax, xlabel:Optional[str]=None, ylabel:Optional[str]=None,
                         xlabellinebreak:Optional[int]=None, ylabellinebreak:Optional[int]=None,
                         combined_styles:Optional[Dict]=None,
                         title:Optional[str]=None):
        if combined_styles is None:
            combined_styles = self.styles
        if xlabel is not None:
            if (xlabellinebreak is not None) and (xlabel.count("$") < 2):
                xlabel = insert_periodic_substr(xlabel, xlabellinebreak)
            ax.set_xlabel(xlabel, **combined_styles['xlabel'])
        if ylabel is not None:
            if (ylabellinebreak is not None) and (ylabel.count("$") < 2):
                ylabel = insert_periodic_substr(ylabel, ylabellinebreak)            
            ax.set_ylabel(ylabel, **combined_styles['ylabel'])
        if title is not None:
            ax.set_title(title, **self.styles['title'])

    def draw_text(self, ax, text:str, x, y,
                  dy:float=0.05,
                  transform_x:str="axis",
                  transform_y:str="axis",
                  **kwargs):
        styles = combine_dict(self.styles['text'], kwargs)
        draw_multiline_text(ax, x, y, text, dy=dy,
                            transform_x=transform_x,
                            transform_y=transform_y,
                            **styles)

    def draw_cbar_label(self, cbar, cbarlabel:Optional[str]=None,
                        combined_styles:Optional[Dict]=None):
        if combined_styles is None:
            combined_styles = self.styles
        if cbarlabel is not None:
            cbar.set_label(cbarlabel, **combined_styles['cbarlabel'])
            
    def draw_axis_components(self, ax, xlabel:Optional[str]=None, ylabel:Optional[str]=None,
                             ylim:Optional[Tuple[float]]=None, xlim:Optional[Tuple[float]]=None,
                             xticks:Optional[List]=None, yticks:Optional[List]=None,
                             xticklabels:Optional[List]=None, yticklabels:Optional[List]=None,
                             combined_styles:Optional[Dict]=None,
                             title:Optional[str]=None):
        if combined_styles is None:
            combined_styles = self.styles
        self.draw_axis_labels(ax, xlabel, ylabel,
                              xlabellinebreak=self.config["xlabellinebreak"],
                              ylabellinebreak=self.config["ylabellinebreak"],
                              combined_styles=combined_styles,
                              title=title)
        
        format_axis_ticks(ax, **combined_styles['axis'],
                          xtick_styles=combined_styles['xtick'],
                          ytick_styles=combined_styles['ytick'])
        
        if ylim is not None:
            ax.set_ylim(*ylim)
        if xlim is not None:
            ax.set_xlim(*xlim)
        if xticks is not None:
            ax.set_xticks(xticks)
        if yticks is not None:
            ax.set_yticks(yticks)
        if xticklabels is not None:
            ax.set_xticklabels(xticklabels)
        if yticklabels is not None:
            ax.set_yticklabels(yticklabels)                
    
    def set_axis_range(self, ax,
                       xmin:Optional[float]=None, xmax:Optional[float]=None,
                       ymin:Optional[float]=None, ymax:Optional[float]=None,
                       ypad:Optional[float]=None):
        xlim = list(ax.get_xlim())
        ylim = list(ax.get_ylim())
        if xmin is not None:
            xlim[0] = xmin
        if xmax is not None:
            xlim[1] = xmax
        if ypad is not None:
            if ypad < 0 or ypad > 1:
                raise ValueError('"ypad" must be between 0 and 1')
            if ax.get_yaxis().get_scale() == "log":
                if ylim[0] <= 0:
                    raise ValueError("ymin must be positive in a logscale plot")
                ylim[1] = (ylim[1] ** (1 + ypad)) / (ylim[0] ** ypad)
            else:
                ylim[1] = ylim[0] + (ylim[1] - ylim[0]) / (1 - ypad)
        if ymin is not None:
            ylim[0] = ymin
        if ymax is not None:
            ylim[1] = ymax
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
    
    @staticmethod
    def close_all_figures():
        matplotlib.pyplot.close()
        
    def decorate_comparison_axis(self, ax, xlabel:str="", ylabel:str="", 
                                 mode:Union[HistComparisonMode, str]="ratio",
                                 ylim:Optional[Sequence]=None,
                                 ypad:Optional[float]=0.1,
                                 draw_ratio_line:bool=True):
        mode = HistComparisonMode.parse(mode)
        if ylim is not None:
            ax.set_ylim(ylim)
        do_centralize_axis = ylim is None
        if mode == HistComparisonMode.RATIO:
            if do_centralize_axis:
                centralize_axis(ax, which="y", ref_value=1, padding=ypad)
            if draw_ratio_line:
                ax.axhline(1, **self.config['ratio_line_styles'])
        elif mode == HistComparisonMode.DIFFERENCE:
            if do_centralize_axis:
                centralize_axis(ax, which="y", ref_value=0, padding=ypad)
            if draw_ratio_line:
                ax.axhline(0, **self.config['ratio_line_styles'])
        # set default ylabel if not given
        if not ylabel:
            if mode == HistComparisonMode.RATIO:
                ylabel = "Ratio"
            elif mode == HistComparisonMode.DIFFERENCE:
                ylabel = "Difference"
        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel)

    def _draw_hist_from_binned_data(self, ax, x, y,
                                    xerr=None, yerr=None,
                                    bin_edges:Optional[np.ndarray]=None,
                                    hide:Optional[Union[Tuple[float, float], Callable]]=None,
                                    styles:Optional[Dict]=None):
        styles = combine_dict(self.styles['hist'], styles)
        # assume uniform binning
        if bin_edges is None:
            bin_center = np.array(x)
            bin_edges = bin_center_to_bin_edge(bin_center)
        bins, range = bin_edges, (bin_edges[0], bin_edges[1])
        if hide is not None:
            mask = get_mask(x, y, [hide])
            y[mask] = 0.
        hist_y, _, handle = ax.hist(x, bins, range=range,
                                    weights=y, **styles)
        assert np.allclose(y, hist_y)
        return handle

    def _draw_stacked_hist_from_binned_data(self, ax, x_list, y_list,
                                            bin_edges:Optional[np.ndarray]=None,
                                            hide_list:Optional[List[Union[Tuple[float, float], Callable]]]=None,
                                            styles:Optional[Dict]=None):
        styles = combine_dict(self.styles['hist'], styles)
        if bin_edges is None:
            bin_edges_list = []
            for x in x_list:
                bin_center = np.array(x)
                bin_edges = bin_center_to_bin_edge(bin_center)
                bin_edges_list.append(bin_edges)
        
            if not all(np.array_equal(bin_edges, bin_edges_list[0]) \
                       for bin_edges in bin_edges_list):
                raise RuntimeError('subhistograms in a stacked histogram have different binnings')
            bin_edges = bin_edges_list[0]
        bins, range = bin_edges, (bin_edges[0], bin_edges[1])
        if hide_list is not None:
            assert len(hide_list) == len(x_list)
            for i, hide in enumerate(hide_list):
                if hide is None:
                    continue
                mask = get_mask(x_list[i], y_list[i], [hide])
                y_list[i][mask] = 0.
        hist_y, _, handles = ax.hist(x_list, bins, range=range,
                                     weights=y_list, stacked=True,
                                     **styles)
        #assert ...
        return hist_y, handles
        
    def _draw_errorbar(self, ax, x, y,
                       xerr=None, yerr=None,
                       hide:Optional[Union[Tuple[float, float], Callable]]=None,
                       styles:Optional[Dict]=None):
        styles = combine_dict(self.styles['errorbar'], styles)
        if hide is not None:
            mask = ~get_mask(x, [hide])
            x, y, xerr, yerr = select_binned_data(mask, x, y, xerr, yerr)            
        handle = ax.errorbar(x, y, xerr=xerr, yerr=yerr, **styles)
        return handle

    def _draw_fill_from_binned_data(self, ax, x, y,
                                    xerr=None, yerr=None,
                                    bin_edges:Optional[np.ndarray]=None,
                                    hide:Optional[Union[Tuple[float, float], Callable]]=None,
                                    styles:Optional[Dict]=None):
        styles = combine_dict(self.styles['fill_between'], styles)
        # assume uniform binning
        if bin_edges is None:
            bin_center = np.array(x)
            bin_edges = bin_center_to_bin_edge(bin_center)
        if yerr is None:
            yerr = 0.
        indices = np.arange(len(x))
        if hide is not None:
            mask = ~get_mask(x, y, [hide])
            sections_indices = get_subsequences(indices, mask, min_length=2)
        else:
            sections_indices = [indices]
        handles = []
        for section_indices in sections_indices:
            mask = np.full(x.shape, False)
            mask[section_indices] = True
            x_i, y_i, xerr_i, yerr_i = select_binned_data(mask, x, y, xerr, yerr)
            # extend to edge
            x_i[0] = bin_edges[section_indices[0]]
            x_i[-1] = bin_edges[section_indices[-1] + 1]
            if isinstance(yerr_i, tuple):
                yerrlo = y_i - yerr_i[0]
                yerrhi = y_i + yerr_i[1]
            else:
                yerrlo = y_i - yerr_i
                yerrhi = y_i + yerr_i
            handle = ax.fill_between(x_i, yerrlo, yerrhi, **styles)
            handles.append(handle)
        return handles[0]

    def _draw_shade_from_binned_data(self, ax, x, y,
                                     xerr=None, yerr=None,
                                     bin_edges:Optional[np.ndarray]=None,
                                     hide:Optional[Union[Tuple[float, float], Callable]]=None,
                                     styles:Optional[Dict]=None):
        styles = combine_dict(styles)
        # assume uniform binning
        if bin_edges is None:
            bin_center = np.array(x)
            bin_edges = bin_center_to_bin_edge(bin_center)
        bin_widths = np.diff(bin_edges)
        if yerr is None:
            yerr = 0.
        if hide is not None:
            mask = ~get_mask(x, y, [hide])
            x, y, xerr, yerr = select_binned_data(mask, x, y, xerr, yerr)
            bin_widths = bin_widths[mask]
        if isinstance(yerr, tuple):
            height = yerr[0] + yerr[1]
            bottom = y - yerr[0]
        else:
            height = 2 * yerr
            bottom = y - yerr
        handle = ax.bar(x=x, height=height, bottom=bottom,
                        width=bin_widths, **styles)
        return handle
        
    def draw_binned_data(self, ax, data,
                         draw_data:bool=True,
                         draw_error:bool=True,
                         bin_edges:Optional[np.ndarray]=None,
                         plot_format:Union[PlotFormat, str]='errorbar',
                         error_format:Union[ErrorDisplayFormat, str]='errorbar',
                         styles:Optional[Dict]=None,
                         hide:Optional[Union[Tuple[float, float], Callable]]=None,
                         error_styles:Optional[Dict]=None):
        if (not draw_data) and (not draw_error):
            raise ValueError('can not draw nothing')
        if styles is None:
            styles = {}
        if error_styles is None:
            error_styles = {}
        plot_format  = PlotFormat.parse(plot_format)
        error_format = ErrorDisplayFormat.parse(error_format)
        handle, error_handle = None, None
        
        x, y = data['x'], data['y']
        xerr, yerr = data.get('xerr', 0), data.get('yerr', 0)
        
        if draw_data:
            if plot_format == PlotFormat.HIST:
                handle = self._draw_hist_from_binned_data(ax, x, y,
                                                          bin_edges=bin_edges,
                                                          hide=hide,
                                                          styles=styles)
            elif plot_format == PlotFormat.ERRORBAR:
                if (not draw_error) or (error_format != ErrorDisplayFormat.ERRORBAR):
                    handle = self._draw_errorbar(ax, x, y,
                                                 hide=hide,
                                                 styles=styles)
                else:
                    handle = self._draw_errorbar(ax, x, y,
                                                 xerr=xerr, yerr=yerr,
                                                 hide=hide,
                                                 styles=styles)
            else:
                raise RuntimeError(f'unsupported plot format: {plot_format.name}')
                
        if draw_error:
            if error_format == ErrorDisplayFormat.FILL:
                error_handle = self._draw_fill_from_binned_data(ax, x, y, yerr=yerr,
                                                                hide=hide,
                                                                styles={**error_styles,
                                                                        "zorder": -1})
            elif error_format == ErrorDisplayFormat.SHADE:
                error_handle = self._draw_shade_from_binned_data(ax, x, y, yerr=yerr,
                                                                 bin_edges=bin_edges,
                                                                 hide=hide,
                                                                 styles={**error_styles,
                                                                        "zorder": -1})
            elif ((error_format == ErrorDisplayFormat.ERRORBAR) and
                 ((not draw_data) or (plot_format !=PlotFormat.ERRORBAR))):
                error_handle = self._draw_errorbar(ax, x, y,
                                                   xerr=xerr, yerr=yerr,
                                                   hide=hide,
                                                   styles={**error_styles,
                                                           "marker": 'none'})
        if isinstance(handle, list):
            handle = handle[0]
        handles = tuple([h for h in [handle, error_handle] if h is not None])
        return handles

    def draw_stacked_binned_data(self, ax, data,
                                 draw_data:bool=True,
                                 draw_error:bool=True,
                                 bin_edges:Optional[np.ndarray]=None,
                                 plot_format:Union[PlotFormat, str]='errorbar',
                                 error_format_list:Union[ErrorDisplayFormat, str]='errorbar',
                                 styles:Optional[Dict]=None,
                                 hide_list:Optional[Union[Tuple[float, float], Callable]]=None,
                                 error_styles_list:Optional[Dict]=None):
        if (not draw_data) and (not draw_error):
            raise ValueError('can not draw nothing')
        n_component = len(data['x'])
        if styles is None:
            styles = {}
        if error_styles_list is None:
            error_styles_list = [{}] * n_component
        plot_format  = PlotFormat.parse(plot_format)
        error_format_list = [ErrorDisplayFormat.parse(fmt) for fmt in error_format_list]
        handles, error_handles = None, None
        
        x_list, y_list = data['x'], data['y']
        xerr_list, yerr_list = data.get('xerr', None), data.get('yerr', None)
        if draw_data:
            if plot_format == PlotFormat.HIST:
                plot_func = self._draw_stacked_hist_from_binned_data
                hist_y, handles = plot_func(ax, x_list, y_list,
                                            bin_edges=bin_edges,
                                            hide_list=hide_list,
                                            styles=styles)
            else:
                raise RuntimeError(f'unsupported format for stacked plot: {plot_format.name}')
        if draw_error:
            error_handles = []
            def get_component(obj, index):
                if obj is not None:
                    return obj[index]
                return None
            for i in range(n_component):
                error_format = error_format_list[i]
                x, y = x_list[i], hist_y[i]
                xerr = get_component(xerr_list, i)
                yerr = get_component(yerr_list, i)
                hide = get_component(hide_list, i)
                error_styles = get_component(error_styles_list, i)
                if error_format == ErrorDisplayFormat.FILL:
                    error_handle = self._draw_fill_from_binned_data(ax, x, y, yerr=yerr,
                                                                    hide=hide,
                                                                    styles={**error_styles,
                                                                            "zorder": -1})
                elif error_format == ErrorDisplayFormat.SHADE:
                    error_handle = self._draw_shade_from_binned_data(ax, x, y, yerr=yerr,
                                                                     bin_edges=bin_edges,
                                                                     hide=hide,
                                                                     styles={**error_styles,
                                                                            "zorder": -1})
                elif error_format == ErrorDisplayFormat.ERRORBAR:
                    error_handle = self._draw_errorbar(ax, x, y,
                                                       xerr=xerr, yerr=yerr,
                                                       hide=hide,
                                                       styles={**error_styles,
                                                               "marker": 'none'})
                error_handles.append(error_handle)
        if error_handles is None:
            return handles
        if handles is None:
            return error_handles
        handles = [(handle, error_handle) for handle, error_handle in zip(handles, error_handles)]
        return handles    

    def draw_legend(self, ax, handles=None, labels=None,
                    handler_map=None, idx=None, **kwargs):
        if (handles is None) and (labels is None):
            handles, labels = self.get_legend_handles_labels(idx=idx)
        if handler_map is not None:
            handler_map = {**CUSTOM_HANDLER_MAP, **handler_map}
        else:
            handler_map = CUSTOM_HANDLER_MAP
        styles = {**self.styles['legend'], **kwargs}
        styles['handler_map'] = handler_map
        ax.legend(handles, labels, **styles)