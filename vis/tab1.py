from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Legend, RangeTool, Circle, Plot, BoxZoomTool, ResetTool, PanTool
from bokeh.models.widgets import RadioButtonGroup, Select, CheckboxGroup
from bokeh.layouts import column, row
from bokeh.models.layouts import TabPanel, Tabs
from bokeh.models import CustomJS, Div, DataRange1d, BoxAnnotation
from bokeh.models.nodes import Node
from bokeh.transform import cumsum

import numpy as np
import pandas as pd

last_update = 0

def tab1(df, embeddings=None, sentiment=None, data=None):
    df = df.drop(['Message'],axis=1)
    # subset = df[df.Conversation =='Angelita'].copy()
    subset = df.copy()
    subset['msg'] = 1
    subset['msg'] = subset['msg'].cumsum()
    subset = subset[subset.Conversation =='Angelita']

    data.index = subset.index

    reset_data = {x:[] for x in subset.columns.unique()}



    timeseries_figure = figure(x_axis_type='datetime', frame_height=300, frame_width=1000, 
                               title = 'Timeseries graph will go here', tools = 'pan')
    legend = Legend(items=[])
    timeseries_figure.add_layout(legend, 'right')

    src = ColumnDataSource(reset_data)
    renders = timeseries_figure.line(source=src, x='Datetime', y = 'msg')

    select = figure(title="scroll test", 
                    height=130,width=1000, y_range = timeseries_figure.y_range,
                    x_axis_type='datetime', y_axis_type=None,
                    tools="", toolbar_location=None)
    select.x_range.range_padding = 0
    select.x_range.bounds = 'auto'

    range_tool = RangeTool(x_range=timeseries_figure.x_range, start_gesture='pan')
    range_tool.overlay.fill_color = 'navy'
    range_tool.overlay.fill_alpha = 0.2
    range_tool.overlay.syncable=True

    select.line('Datetime','msg', source=src)
    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)          

    src.data.update(subset)

    # THIS IS MY WORKSPACE BELOW HERE!!!!!!

    subset['timestamp'] = (subset.Datetime - pd.Timestamp("1970-01-01")) // pd.Timedelta('1ms') # The range tool converts datetime's to floating point to plot the x-axis range
    sentiment['timestamp'] =  (subset.Datetime - pd.Timestamp("1970-01-01")) // pd.Timedelta('1ms')
    data['timestamp'] =  (subset.Datetime - pd.Timestamp("1970-01-01")) // pd.Timedelta('1ms')



    throttle_delay = 0.5
    import time

    def test_change1(attr, old, new):
        start = timeseries_figure.x_range.start
        end = timeseries_figure.x_range.end


        print(new, type(new))
        s = time.time()
        # Find the cumulative sums at the start and end timestamps
        # start_row = cumulative_language[cumulative_language['timestamp'] <= start].iloc[-1] if not cumulative_language[cumulative_language['timestamp'] <= start].empty else pd.Series([0, 0, 0], index=['timestamp', 'cumulative_ENGLISH', 'cumulative_SPANISH'])
        # end_row = cumulative_language[cumulative_language['timestamp'] <= end].iloc[-1] if not cumulative_language[cumulative_language['timestamp'] <= end].empty else pd.Series([0, 0, 0], index=['timestamp', 'cumulative_ENGLISH', 'cumulative_SPANISH'])

        # # Calculate the sum within the selected range using the difference of cumulative sums
        # english_sum = end_row['cumulative_ENGLISH'] - start_row['cumulative_ENGLISH']
        # spanish_sum = end_row['cumulative_SPANISH'] - start_row['cumulative_SPANISH']

        # view = pd.Series({'ENGLISH': english_sum, 'SPANISH': spanish_sum})
        # next_data = view.reset_index(name='value').rename(columns={'index': 'language'})
        # next_data['angle'] = next_data['value'] / next_data['value'].sum() * 2 * np.pi
        # next_data['color'] = ['navy', 'firebrick']
        # pie_source.data = next_data

        # Language
        view = subset[(subset.timestamp >= start) & (subset.timestamp <= end)][['ENGLISH', 'SPANISH']].sum()
        next_data = pd.Series(view, index=['ENGLISH', 'SPANISH']).reset_index(name='value').rename(columns={'index': 'language'})
        next_data['angle'] = next_data['value'] / next_data['value'].sum() * 2 * np.pi
        next_data['color'] = ['navy','firebrick']
        pie_source.data = next_data

        # view = subset[(subset.timestamp >= start) & (subset.timestamp <= end)][['ENGLISH','SPANISH']].sum().to_list()
        # bar_source.data = {'categories':['ENGLISH','SPANISH'], 'values':view}

        # sentiment
        data_sentiments = sentiment[(subset.timestamp >= start) & (subset.timestamp <= end)].groupby(by='Author').sum(sentiment_cols)
        src_sent_pos.data.update(data_sentiments[sentiment_cols_pos])
        src_sent_neg.data.update(-data_sentiments[sentiment_cols_neg])

        # positive_sentiment_data = {'Author': Author}
        # negative_sentiment_data = {'Author': Author}

        # for col in sentiment_cols_pos:
        #     positive_sentiment_data[col] = []
        # for col in sentiment_cols_neg:
        #     negative_sentiment_data[col] = []

        # for author in Author:
        #     author_cumulative = cumulative_sentiment[cumulative_sentiment['Author'] == author]

        #     start_row = author_cumulative[author_cumulative['timestamp'] <= start].iloc[-1] if not author_cumulative[author_cumulative['timestamp'] <= start].empty else pd.Series([0] * (len(sentiment_cols) + 2), index=['timestamp', 'Author', *[f'cumulative_{col}' for col in sentiment_cols]])
        #     end_row = author_cumulative[author_cumulative['timestamp'] <= end].iloc[-1] if not author_cumulative[author_cumulative['timestamp'] <= end].empty else pd.Series([0] * (len(sentiment_cols) + 2), index=['timestamp', 'Author', *[f'cumulative_{col}' for col in sentiment_cols]])

        #     for col in sentiment_cols_pos:
        #         positive_sentiment_data[col].append(end_row[f'cumulative_{col}'] - start_row[f'cumulative_{col}'])

        #     for col in sentiment_cols_neg:
        #         negative_sentiment_data[col].append(-(end_row[f'cumulative_{col}'] - start_row[f'cumulative_{col}']))

        # src_sent_pos.data = positive_sentiment_data
        # src_sent_neg.data = negative_sentiment_data
        
        print(time.time()-s)



    def test_change2(attr, old, new):
        # Topic
        global last_update
        current_time = time.time()
        if current_time - last_update >= throttle_delay:
            last_update = current_time

            subset_sp_filt = subset_sp[(subset_sp.timestamp >= start) & (subset_sp.timestamp <= end)]
            subset_en_filt = subset_en[(subset_en.timestamp >= start) & (subset_en.timestamp <= end)]

            new_data_sp = {
                'timestamp': subset_sp_filt['timestamp'].tolist(),
                'x': subset_sp_filt['x'].tolist(),
                'y': subset_sp_filt['y'].tolist(),
            }
            new_data_en = {
                'timestamp': subset_en_filt['timestamp'].tolist(),
                'x': subset_en_filt['x'].tolist(),
                'y': subset_en_filt['y'].tolist(),
            }
            scatter_src_sp.data = new_data_sp
            scatter_src_en.data = new_data_en





    timeseries_figure.x_range.on_change('start', test_change1)
    timeseries_figure.x_range.on_change('end', test_change1)
    # timeseries_figure.x_range.on_change('start', test_change2)
    # timeseries_figure.x_range.on_change('end', test_change2)

    # Language
    initial_view = subset[['ENGLISH', 'SPANISH']].sum()
    initial_data = pd.Series(initial_view, index=['ENGLISH', 'SPANISH']).reset_index(name='value').rename(columns={'index': 'language'})
    initial_data['angle'] = initial_data['value'] / initial_data['value'].sum() * 2 * np.pi
    initial_data['color'] = ['navy','firebrick']
    initial_data['percentage'] = initial_data['value']/initial_data.value.sum()
    print(initial_data)

    pie_source = ColumnDataSource(initial_data)
    test_pie_chart = figure(height=400, width=400, title="Language Distribution",
                        tools="hover", tooltips="@language: @value (@percentage{0.2f}%)",
                        x_range=(-0.5, 1.0))

    test_pie_chart.wedge(x=0, y=1, radius=0.4,
                        start_angle=cumsum('angle', include_zero=True),
                        end_angle=cumsum('angle'),
                        line_color="white", fill_color='color', legend_field='language',
                        source=pie_source)

    test_pie_chart.axis.axis_label = None
    test_pie_chart.axis.visible = False
    test_pie_chart.grid.grid_line_color = None

    # Language with cumsum

# 1. Calculate the cumulative sum of 'ENGLISH' and 'SPANISH' columns
    # cumulative_language = subset[['timestamp', 'ENGLISH', 'SPANISH']].copy()
    # cumulative_language['cumulative_ENGLISH'] = cumulative_language['ENGLISH'].cumsum()
    # cumulative_language['cumulative_SPANISH'] = cumulative_language['SPANISH'].cumsum()

    # # 2. Create a ColumnDataSource for the pie chart
    # initial_view = subset[['ENGLISH', 'SPANISH']].sum()
    # initial_data = pd.Series(initial_view, index=['ENGLISH', 'SPANISH']).reset_index(name='value').rename(columns={'index': 'language'})
    # initial_data['angle'] = initial_data['value'] / initial_data['value'].sum() * 2 * np.pi
    # initial_data['color'] = ['navy', 'firebrick']
    # pie_source = ColumnDataSource(initial_data)

    # # 3. Create the pie chart figure and glyph
    # test_pie_chart = figure(height=400, width=400, title="Language Distribution",
    #                     tools="hover", tooltips="@language: @value (@percentage{0.2f}%)",
    #                     x_range=(-0.5, 1.0))

    # test_pie_chart.wedge(x=0, y=1, radius=0.4,
    #                     start_angle=cumsum('angle', include_zero=True),
    #                     end_angle=cumsum('angle'),
    #                     line_color="white", fill_color='color', legend_field='language',
    #                     source=pie_source)

    # test_pie_chart.axis.axis_label = None
    # test_pie_chart.axis.visible = False
    # test_pie_chart.grid.grid_line_color = None

    # bar_source = ColumnDataSource(data={'categories':['ENGLISH','SPANISH'], 'values':subset[['ENGLISH','SPANISH']].sum().to_list()})


    # test_bar_chart = figure(x_range=['ENGLISH','SPANISH'],width=400, height=400)
    # test_bar_chart.vbar(x='categories', top='values', source=bar_source)

    # bar_source.data.update({'categories':['ENGLISH','SPANISH'], 'values':subset[['ENGLISH','SPANISH']].sum().to_list()})
    pie_source.data.update(initial_data)

    # Sentiment

    from bokeh.palettes import GnBu3, OrRd3

    sentiment_cols_pos = ['sentiment_Neutral', 'sentiment_Positive', 'sentiment_Very Positive']
    sentiment_cols_neg = ['sentiment_Negative', 'sentiment_Very Negative']
    sentiment_cols = [*sentiment_cols_pos, *sentiment_cols_neg]
    labels = ['neu','pos','pos!!','neg','neg!!']

    grouped_sentiments = sentiment.groupby(by='Author')
    data_sentiments = grouped_sentiments.sum(sentiment_cols)

    Author = sentiment.Author.unique().tolist()
    colors = (*GnBu3[::-1],*OrRd3[:2][::-1])
    stacked_bar_chart = figure(y_range=Author, height=400, width=400,title="Sentiment Analysis",
           toolbar_location=None)
    
    src_sent_pos = ColumnDataSource(data_sentiments[sentiment_cols_pos])
    src_sent_neg = ColumnDataSource(-data_sentiments[sentiment_cols_neg])

    stacked_bar_chart.hbar_stack(sentiment_cols, y='Author', height=0.9, color=colors, source=src_sent_pos,
                legend_label=[f"{s}" for s in labels])

    stacked_bar_chart.hbar_stack(sentiment_cols, y='Author', height=0.9, color=colors, source=src_sent_neg)

    stacked_bar_chart.y_range.range_padding = 0.1
    stacked_bar_chart.ygrid.grid_line_color = None
    stacked_bar_chart.legend.location = "top_left"
    stacked_bar_chart.axis.minor_tick_line_color = None
    stacked_bar_chart.outline_line_color = None

    #sentiment with cumsum

    # sentiment_cols_pos = ['sentiment_Neutral', 'sentiment_Positive', 'sen timent_Very Positive']
    # sentiment_cols_neg = ['sentiment_Negative', 'sentiment_Very Negative']
    # sentiment_cols = [*sentiment_cols_pos, *sentiment_cols_neg]
    # labels = ['neu', 'pos', 'pos!!', 'neg', 'neg!!']
    # Author = sentiment.Author.unique().tolist()
    # colors = (*GnBu3[::-1], *OrRd3[:2][::-1])

    # # 1. Calculate cumulative sums for sentiment columns
    # cumulative_sentiment = sentiment[['timestamp', 'Author', *sentiment_cols]].copy()
    # for col in sentiment_cols:
    #     cumulative_sentiment[f'cumulative_{col}'] = cumulative_sentiment.groupby('Author')[col].cumsum()
    
    # print(cumulative_sentiment)

    # # 2. Create ColumnDataSources for the stacked bar chart (initialized with empty data)
    # src_sent_pos = ColumnDataSource(dict(Author=Author, **{col: [0] * len(Author) for col in sentiment_cols_pos}))
    # src_sent_neg = ColumnDataSource(dict(Author=Author, **{col: [0] * len(Author) for col in sentiment_cols_neg}))

    # # 3. Create the stacked bar chart figure and glyphs
    # stacked_bar_chart = figure(y_range=Author, height=400, width=400, title="Sentiment Analysis",
    #                         toolbar_location=None)

    # stacked_bar_chart.hbar_stack(sentiment_cols_pos, y='Author', height=0.9, color=colors[:len(sentiment_cols_pos)],
    #                             source=src_sent_pos, legend_label=[f"{s}" for s in labels[:len(sentiment_cols_pos)]])

    # stacked_bar_chart.hbar_stack(sentiment_cols_neg, y='Author', height=0.9, color=colors[len(sentiment_cols_pos):],
    #                             source=src_sent_neg)

    # stacked_bar_chart.y_range.range_padding = 0.1
    # stacked_bar_chart.ygrid.grid_line_color = None
    # stacked_bar_chart.legend.location = "top_left"
    # stacked_bar_chart.axis.minor_tick_line_color = None
    # stacked_bar_chart.outline_line_color = None



    # src_sent_pos.data.update(data_sentiments[sentiment_cols_pos])
    # src_sent_neg.data.update(data_sentiments[sentiment_cols_neg])

    # Embedding

    # from hdbscan import HDBSCAN
    # from umap import UMAP
    # umap_model = UMAP(n_neighbors = 15, n_components = 2, min_dist = 0.0, metric = 'cosine', random_state =39)
    # hdbscan_model = HDBSCAN(min_cluster_size=150, metric='euclidean', cluster_selection_method='eom', prediction_data=True)
    # data = umap_model.fit_transform(embeddings, verbose=True)
    subset_sp = data[subset.SPANISH]
    subset_en = data[subset.ENGLISH]

                             
    scatter_src_sp = ColumnDataSource(subset_sp)
    scatter_src_en = ColumnDataSource(subset_en)

    scatter_plot = Plot(
        title=None, width=400, height=400,
        min_border=0,output_backend="webgl")
    scatter_plot.add_tools(BoxZoomTool(), ResetTool(), PanTool())
    glyph = Circle(x='x',y='y', radius=.02, fill_color='firebrick', line_color='firebrick',fill_alpha=0.2, line_alpha=0.2)
    scatter_plot.add_glyph(scatter_src_sp, glyph)
    glyph = Circle(x='x',y='y', radius=.02, fill_color='navy', line_color='navy',fill_alpha=0.2, line_alpha=0.2)
    scatter_plot.add_glyph(scatter_src_en, glyph)

    # scatter_src_sp.data.update(subset_sp)
    # scatter_src_en.data.update(subset_en)

    # print(len(data))
    # scatter_plot = figure(width=400, height=400)
    # scatter_plot.scatter(*data[subset.SPANISH].T,*data[subset.ENGLISH].T, size =np.ones(len(data))*.11, color = "navy", alpha=0.5)

    layout = column(row(column(timeseries_figure,select)), row(test_pie_chart,stacked_bar_chart, scatter_plot))
    tab = TabPanel(child=layout, title = 'This is a test')

    return tab

