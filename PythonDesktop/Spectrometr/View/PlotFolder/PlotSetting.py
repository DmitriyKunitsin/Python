class PlotSetting:
    markers = (
    ('.', 'point'),
    (',', 'pixel'),
    ('o', 'circle'),
    ('v', 'triangle_down'),
    ('^', 'triangle_up'),
    ('<', 'triangle_left'),
    ('>', 'triangle_right'),
    ('1', 'tri_down'),
    ('2', 'tri_up'),
    ('3', 'tri_left'),
    ('4', 'tri_right'),
    ('8', 'octagon'),
    ('s', 'square'),
    ('p', 'pentagon'),
    ('P', 'plus_filled'),
    ('*', 'star'),
    ('h', 'hexagon1'),
    ('H', 'hexagon2'),
    ('+', 'plus'),
    ('x', 'x'),
    ('X', 'x_filled'),
    ('D', 'diamond'),
    ('d', 'thin_diamond'),
    ('|', 'vline'),
    ('_', 'hline')
)
    '''
        **Markers**

        =============   ===============================
        character       description
        =============   ===============================
        ``'.'``         point marker
        ``','``         pixel marker
        ``'o'``         circle marker
        ``'v'``         triangle_down marker
        ``'^'``         triangle_up marker
        ``'<'``         triangle_left marker
        ``'>'``         triangle_right marker
        ``'1'``         tri_down marker
        ``'2'``         tri_up marker
        ``'3'``         tri_left marker
        ``'4'``         tri_right marker
        ``'8'``         octagon marker
        ``'s'``         square marker
        ``'p'``         pentagon marker
        ``'P'``         plus (filled) marker
        ``'*'``         star marker
        ``'h'``         hexagon1 marker
        ``'H'``         hexagon2 marker
        ``'+'``         plus marker
        ``'x'``         x marker
        ``'X'``         x (filled) marker
        ``'D'``         diamond marker
        ``'d'``         thin_diamond marker
        ``'|'``         vline marker
        ``'_'``         hline marker
        =============   ===============================
    
        **Line Styles**

        =============    ===============================
        character        description
        =============    ===============================
        ``'-'``          solid line style
        ``'--'``         dashed line style
        ``'-.'``         dash-dot line style
        ``':'``          dotted line style
        =============    ===============================

        Example format strings::

            'b'    # blue markers with default shape
            'or'   # red circles
            '-g'   # green solid line
            '--'   # dashed line with default color
            '^k:'  # black triangle_up markers connected by a dotted line

        **Colors**

        The supported color abbreviations are the single letter codes

        =============    ===============================
        character        color
        =============    ===============================
        ``'b'``          blue
        ``'g'``          green
        ``'r'``          red
        ``'c'``          cyan
        ``'m'``          magenta
        ``'y'``          yellow
        ``'k'``          black
        ``'w'``          white
        =============    ===============================
    '''
    lines = ('solid', 'dashed', 'dash-dot', 'dotted')
    colors = ('blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white')
    def __init__(self, color='green', marker='diamond', linestyle='dashed'):
        self.color = color
        self.marker = marker
        self.linestyle = linestyle
    def get_plot_parag(self, color='green', marker='diamond', linestyle='dashed'):
        """
            :param color: Цвет графика (по умолчанию None).
            :param marker: Маркер графика (по умолчанию None).
            :param linestyle: Стиль линии графика (по умолчанию None).
            :return: Возвращает параметры графика в виде словаря.
        """
        plot_params = {
            'color': color if color is not None else self.color,
            'marker': marker if marker is not None else self.marker,
            'linestyle': linestyle if linestyle is not None else self.linestyle
        }
        return plot_params

    def get_all_markers():
        '''Список всех маркров
        
        :return: Возвращает весь кортеж доступных маркеров
        '''
        return [marker for marker in PlotSetting.markers]
    def get_all_line():
        '''Список всех линий
        
        :return: Возвращает весь кортеж доступных линий
        '''
        return [line for line in PlotSetting.lines]
    def get_all_colors():
        '''Список всех цветов
        
        :return: Возвращает весь кортеж доступных цветов
        '''
        return [color for color in PlotSetting.colors]