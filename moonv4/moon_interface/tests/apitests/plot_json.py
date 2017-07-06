import os
import argparse
import logging
import json
import glob
import time
import datetime
import itertools
import plotly
from plotly.graph_objs import Scatter, Layout, Bar
import plotly.figure_factory as ff


logger = None


def init():
    global logger
    commands = {
        "graph": write_graph,
        "digraph": write_distgraph,
        "average": write_average_graph,
        "latency": write_latency,
        "request_average": write_request_average,
        "throughput": write_throughput,
        "global_throughput": write_global_throughput,
        "parallel_throughput": write_parallel_throughput,
    }
    parser = argparse.ArgumentParser()
    parser.add_argument("command",
                        help="Command to throw ({})".format(", ".join(commands.keys())))
    parser.add_argument("input", nargs="+", help="files to use with the form \"file1.json,file2.json,...\"")
    parser.add_argument("--verbose", "-v", action='store_true', help="verbose mode")
    parser.add_argument("--debug", "-d", action='store_true', help="debug mode")
    parser.add_argument("--write", "-w", help="Write test data to a JSON file", default="/tmp/data.json")
    parser.add_argument("--legend", "-l", help="Set the legend (by default get from the file names)")
    parser.add_argument("--titles", "-t",
                        help="Set the general title, x title and y title (ex: Title 1,Title X,Title Y)")
    # parser.add_argument("--request-per-second", help="Number of requests per seconds",
    #                     type=int, dest="request_second", default=1)
    # parser.add_argument("--limit", help="Limit request to LIMIT", type=int)
    parser.add_argument("--write-image", help="Write the graph to file IMAGE", dest="write_image")
    parser.add_argument("--write-html", help="Write the graph to HTML file HTML", dest="write_html", default="data.html")
    parser.add_argument("--plot-result",
                        help="Use specific data like Grant or Deny responses "
                             "('*' for all or 'Grant,Deny' to separate granted and denied responses)",
                        dest="plot_result",
                        default="*")
    args = parser.parse_args()

    FORMAT = '%(levelname)s %(message)s'

    if args.verbose:
        logging.basicConfig(
            format=FORMAT,
            level=logging.INFO)
    elif args.debug:
        logging.basicConfig(
            format=FORMAT,
            level=logging.DEBUG)
    else:
        logging.basicConfig(
            format=FORMAT,
            level=logging.WARNING)

    logger = logging.getLogger(__name__)

    # args.input = args.input[0]
    result_input = []
    for _input in args.input:
        if "*" in _input:
            filenames = glob.glob(_input)
            filenames.sort()
            result_input.append(",".join(filenames))
        else:
            result_input.append(_input)
    args.input = result_input

    if not args.legend:
        _legends = []
        for data in args.input:
            for filename in data.split(","):
                _legends.append(os.path.basename(filename).replace(".json", ""))
        args.legend = ",".join(_legends)

    return args, commands


def __get_legends(legend_str, default_length=10):
    if "|" in legend_str:
        secondary_legend = legend_str.split("|")[1].split(",")
    else:
        secondary_legend = ["average"] * default_length
    _legends = legend_str.split("|")[0].split(",")
    return _legends, secondary_legend


def get_delta_v1(time_data, result=None):
    time_delta = list()
    x_data = list()
    time_delta_sum1 = 0
    cpt = 0
    for key in time_data:
        if not result or 'result' not in time_data[key] or time_data[key]['result'].lower() == result.lower() or result == "*":
            time_delta.append(time_data[key]['delta'])
            time_delta_sum1 += time_data[key]['delta']
            if 'index' in time_data[key]:
                print("in index {}".format(time_data[key]['index']))
                x_data.append(time_data[key]['index'])
            else:
                x_data.append(cpt)
        cpt += 1
    time_delta_average1 = time_delta_sum1 / len(time_data.keys())
    return time_delta, time_delta_average1, x_data


def get_delta_v2(time_data, result=None):
    time_delta = list()
    x_data = list()
    time_delta_sum1 = 0
    cpt = 0
    for item in time_data:
        if not result or 'result' not in item or item['result'].lower() == result.lower() or result == "*":
            time_delta.append(item['delta'])
            time_delta_sum1 += item['delta']
            x_data.append(cpt)
        cpt += 1
    time_delta_average1 = time_delta_sum1 / len(time_data)
    return time_delta, time_delta_average1, x_data


def get_delta(time_data, result=None):
    if type(time_data) is dict:
        return get_delta_v1(time_data, result=result)
    if type(time_data) is list:
        return get_delta_v2(time_data, result=result)
    raise Exception("Time data has not a correct profile")


def get_latency_v1(time_data, result=None):
    time_delta = list()
    time_delta_sum1 = 0
    for key in time_data:
        if not result or 'result' not in time_data[key] or time_data[key]['result'].lower() == result.lower() or result == "*":
            time_delta.append(1/time_data[key]['delta'])
            time_delta_sum1 += time_data[key]['delta']
            logger.debug("Adding {} {}".format(1/time_data[key]['delta'], time_data[key]['delta']))
    time_delta_average1 = time_delta_sum1 / len(time_data.keys())
    return time_delta, 1/time_delta_average1


def get_latency_v2(time_data, result=None):
    time_delta = list()
    time_delta_sum1 = 0
    time_list = list()
    for item in time_data:
        if not result or 'result' not in item or item['result'].lower() == result.lower() or result == "*":
            time_delta.append(1/item['delta'])
            time_delta_sum1 += item['delta']
            time_list.append(item['end'])
    time_delta_average1 = time_delta_sum1 / len(time_data)
    return time_delta, 1/time_delta_average1, time_list


def get_latency(time_data, result=None):
    if type(time_data) is dict:
        return get_latency_v1(time_data, result=result)
    if type(time_data) is list:
        return get_latency_v2(time_data, result=result)
    raise Exception("Time data has not a correct profile")


def get_request_per_second_v1(time_data):
    result = {}
    _min = None
    _max = 0
    for key in time_data:
        start = str(time_data[key]['start']).split(".")[0]
        end = str(time_data[key]['end']).split(".")[0]
        middle = str(int((int(end) + int(start)) / 2))
        middle = end
        if not _min:
            _min = int(middle)
        if int(middle) < _min:
            _min = int(middle)
        if int(middle) > _max:
            _max = int(middle)
        if middle not in result:
            result[middle] = 1
        else:
            result[middle] += 1
    for cpt in range(_min+1, _max):
        if str(cpt) not in result:
            result[str(cpt)] = 0
            # result[str(cpt)] = (result[str(cpt - 1)] + result[str(cpt)]) / 2
            # result[str(cpt - 1)] = result[str(cpt)]
    return result


def get_request_per_second_v2(time_data):
    result = {}
    _min = None
    _max = 0
    for item in time_data:
        start = str(item['start']).split(".")[0]
        end = str(item['end']).split(".")[0]
        middle = str(int((int(end) + int(start)) / 2))
        middle = end
        if not _min:
            _min = int(middle)
        if int(middle) < _min:
            _min = int(middle)
        if int(middle) > _max:
            _max = int(middle)
        if middle not in result:
            result[middle] = 1
        else:
            result[middle] += 1
    for cpt in range(_min+1, _max):
        if str(cpt) not in result:
            result[str(cpt)] = 0
            # result[str(cpt)] = (result[str(cpt - 1)] + result[str(cpt)]) / 2
            # result[str(cpt - 1)] = result[str(cpt)]
    return result


def get_request_per_second(time_data):
    if type(time_data) is dict:
        return get_request_per_second_v1(time_data)
    if type(time_data) is list:
        return get_request_per_second_v2(time_data)
    raise Exception("Time data has not a correct profile")


def write_graph(legend=None, input=None, image_file=None, html_file=None, plot_result="", title=None):
    logger.info("Writing graph")
    cpt_max = 0
    logger.debug("legend={}".format(legend))
    for data in input:
        cpt_max += len(data.split(","))
    legends, secondary_legend = __get_legends(legend, cpt_max)
    logger.debug("legends={}".format(legends))
    result_data = []
    cpt_input = 0
    for data in input:
        for _input in data.split(","):
            try:
                current_legend = legends.pop(0)
            except IndexError:
                current_legend = ""
            time_data = json.load(open(_input))
            time_delta, time_delta_average2, x_data = get_delta(time_data)
            for item in time_data:
                if type(time_data) is dict:
                    time_delta.append(time_data[item]['delta'])
                else:
                    time_delta.append(item['delta'])
            data = Scatter(
                x=x_data,
                y=time_delta,
                name=current_legend,
                line=dict(
                    color="rgb({},{},{})".format(0, cpt_input * 255 / cpt_max, cpt_input * 255 / cpt_max),
                    # shape='spline'
                )
            )
            result_data.append(data)
            data_a = Scatter(
                x=list(range(len(time_data))),
                y=[time_delta_average2 for x in range(len(time_data))],
                name=current_legend + " average",
                line=dict(
                    color="rgb({},{},{})".format(255, cpt_input * 255 / cpt_max, cpt_input * 255 / cpt_max),
                    # shape='spline'
                )
            )
            result_data.append(data_a)
            cpt_input += 1

    if image_file:
        plotly.offline.plot(
            {
                "data": result_data,
                "layout": Layout(
                    title="Request times delta",
                    xaxis=dict(title='Requests'),
                    yaxis=dict(title='Request duration'),
                )
            },
            filename=html_file,
            image="svg",
            image_filename=image_file,
            image_height=1000,
            image_width=1200
        )
    else:
        plotly.offline.plot(
            {
                "data": result_data,
                "layout": Layout(
                    title="Request times delta",
                    xaxis=dict(title='Requests'),
                    yaxis=dict(title='Request duration'),
                )
            },
            filename=html_file,
        )
    return 0


def write_distgraph(legend=None, input=None, image_file=None, html_file=None, plot_result="", title=None):

    logger.info("Writing graph")
    _legends, secondary_legend = __get_legends(legend, len(input))
    result_data = []
    legends = []

    # FIXME: deals with multiple input
    input = input[0]
    for _input in input.split(","):
        logger.info("Analysing input {}".format(_input))
        current_legend = _legends.pop(0)
        for result in plot_result.split(","):
            time_data2 = json.load(open(_input))
            time_delta2, time_delta_average2, x_data = get_delta(time_data2, result=result)
            result_data.append(time_delta2)
            if result == "*":
                legends.append(current_legend)
            else:
                legends.append("{} ({})".format(current_legend, result))

    # Create distplot with custom bin_size
    if len(legends) < len(result_data):
        for _cpt in range(len(result_data)-len(legends)):
            legends.append("NC")
    fig = ff.create_distplot(result_data, legends, show_hist=False)

    # Plot!
    plotly.offline.plot(
        fig,
        # image="svg",
        # image_filename=image_file,
        # image_height=1000,
        # image_width=1200,
        filename=html_file
    )
    return 0


def write_average_graph(legend=None, input=None, image_file=None, html_file=None, plot_result="", title=None):

    logger.info("Writing average graph")
    _legends, secondary_legend = __get_legends(legend, len(input))
    all_data = []
    legends = []
    legend_done = False
    html_file = "latency_" + html_file

    cpt_input = 0
    cpt_max = len(input)
    for data in input:
        result_data = []
        for _input in data.split(","):
            logger.info("Analysing input {}".format(_input))
            if not legend_done:
                current_legend = _legends.pop(0)
            for result in plot_result.split(","):
                time_data2 = json.load(open(_input))
                time_delta2, time_delta_average2 = get_delta(time_data2, result=result)
                result_data.append(time_delta_average2)
                if not legend_done and result == "*":
                    legends.append(current_legend)
                elif not legend_done:
                    legends.append("{} ({})".format(current_legend, result))

        if not legend_done:
            if len(legends) < len(result_data):
                for _cpt in range(len(result_data)-len(legends)):
                    legends.append("NC")

        data = Scatter(
            x=legends,
            y=result_data,
            name=secondary_legend.pop(0),
            line=dict(
                color="rgb({},{},{})".format(158, cpt_input * 255 / cpt_max, cpt_input * 255 / cpt_max)
            )
        )
        all_data.append(data)
        legend_done = True
        cpt_input += 1
    if image_file:
        plotly.offline.plot(
            {
                "data": all_data,
                "layout": Layout(
                    title="Latency",
                    xaxis=dict(title='Request per second'),
                    yaxis=dict(title='Request latency'),
                )
            },
            filename=html_file,
            image="svg",
            image_filename=image_file,
            image_height=1000,
            image_width=1200
        )
    else:
        plotly.offline.plot(
            {
                "data": all_data,
                "layout": Layout(
                    title="Latency",
                    xaxis=dict(title='Requests'),
                    yaxis=dict(title='Request latency'),
                )
            },
            filename=html_file,
        )
    return 0


def __get_titles(title):
    if title:
        titles = title.split(",")
        try:
            title_generic = titles[0]
        except IndexError:
            title_generic = ""
        try:
            title_x = titles[1]
        except IndexError:
            title_x = ""
        try:
            title_y = titles[2]
        except IndexError:
            title_y = ""
    else:
        title_generic = ""
        title_x = ""
        title_y = ""
    return title_generic, title_x, title_y


def __get_time_axis(data):
    result_data = []
    start_time = None
    for item in data:
        if not start_time:
            start_time = item
        item = item - start_time
        millis = int(str(item).split('.')[-1][:6])
        t = time.gmtime(int(item))
        result_data.append(
            datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec, millis)
        )
    return result_data


def write_latency(legend=None, input=None, image_file=None, html_file=None, plot_result="", title=None):

    logger.info("Writing latency graph")
    _legends, secondary_legend = __get_legends(legend, len(input))
    all_data = []
    legends = []
    legend_done = False
    html_file = "latency_" + html_file
    title_generic, title_x, title_y = __get_titles(title)
    cpt_input = 0
    cpt_max = len(input)
    for data in input:
        result_data = []
        for _input in data.split(","):
            logger.info("Analysing input {}".format(_input))
            if not legend_done:
                current_legend = _legends.pop(0)
            for result in plot_result.split(","):
                time_data2 = json.load(open(_input))
                time_delta2, time_delta_average2, x_data = get_latency(time_data2, result=result)
                result_data.append(time_delta_average2)
                if not legend_done and result == "*":
                    legends.append(current_legend)
                elif not legend_done:
                    legends.append("{} ({})".format(current_legend, result))

        if not legend_done:
            if len(legends) < len(result_data):
                for _cpt in range(len(result_data)-len(legends)):
                    legends.append("NC")

        data = Scatter(
            x=legends,
            y=result_data,
            name=secondary_legend.pop(0),
            line=dict(
                color="rgb({},{},{})".format(158, cpt_input * 255 / cpt_max, cpt_input * 255 / cpt_max)
            )
        )
        all_data.append(data)
        legend_done = True
        cpt_input += 1
    if image_file:
        plotly.offline.plot(
            {
                "data": all_data,
                "layout": Layout(
                    title=title_generic,
                    xaxis=dict(title=title_x),
                    yaxis=dict(title=title_y),
                )
            },
            filename=html_file,
            image="svg",
            image_filename=image_file,
            image_height=1000,
            image_width=1200
        )
    else:
        plotly.offline.plot(
            {
                "data": all_data,
                "layout": Layout(
                    title=title_generic,
                    xaxis=dict(title=title_x),
                    yaxis=dict(title=title_y),
                    font=dict(
                        size=25
                    )
                )
            },
            filename=html_file,
        )
    return 0


def write_request_average(legend=None, input=None, image_file=None, html_file=None, plot_result="", title=None):
    logger.info("Writing average graph")
    _legends, secondary_legend = __get_legends(legend, len(input))
    result_data = []
    html_file = "request_average_" + html_file

    # FIXME: deals with multiple input
    input = input[0]
    for _input in input.split(","):
        logger.info("Analysing input {}".format(_input))
        current_legend = _legends.pop(0)
        time_data = json.load(open(_input))
        result = get_request_per_second(time_data)
        time_keys = list(result.keys())
        time_keys.sort()
        time_value = list(map(lambda x: result[x], time_keys))
        datetime_keys = list()
        for _time in time_keys:
            t = time.gmtime(int(_time))
            datetime_keys.append(datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))
        data = Bar(
            x=datetime_keys,
            y=time_value,
            name=current_legend,
        )
        result_data.append(data)
    plotly.offline.plot(
        {
            "data": result_data,
            "layout": Layout(
                title="Request per second",
                xaxis=dict(title='Time'),
                yaxis=dict(title='Request number'),
            )
        },
        filename=html_file,
    )


def write_throughput(legend=None, input=None, image_file=None, html_file=None, plot_result="", title=None):
    logger.info("Writing throughput graph")
    _legends, secondary_legend = __get_legends(legend, len(input))
    result_data = []
    html_file = "request_throughput_" + html_file
    title_generic, title_x, title_y = __get_titles(title)

    cpt_input = 0
    cpt_request = 0
    cpt_max = 0
    average_data_x = []
    average_data_y = []
    for _i in input:
        cpt_max += len(_i.split(","))

    for data in input:
        for _input in data.split(","):
            logger.info("Analysing input {}".format(_input))
            current_legend = _legends.pop(0)
            time_data = json.load(open(_input))
            result = get_request_per_second(time_data)
            time_keys = list(result.keys())
            time_keys.sort()
            time_value = list(map(lambda x: result[x], time_keys))
            index_list = list(map(lambda x: cpt_request + x, range(len(time_keys))))
            cpt_request += len(index_list)
            import itertools
            average_data_y.extend(
                [list(itertools.accumulate(result.values()))[-1]/len(result.values())]*len(result.values())
            )
            average_data_x.extend(index_list)
            data = Scatter(
                x=index_list,
                y=time_value,
                name=current_legend,
                line=dict(
                    color="rgb({},{},{})".format(0, cpt_input*255/cpt_max, cpt_input*255/cpt_max)
                ),
                mode="lines+markers"
            )
            result_data.append(data)
            cpt_input += 1
    data = Scatter(
        x=average_data_x,
        y=average_data_y,
        name="Average",
        line=dict(
            color="rgb({},{},{})".format(255, 0, 0)
        ),
        mode="lines"
    )
    logger.debug(average_data_x)
    logger.debug(average_data_y)
    result_data.append(data)
    plotly.offline.plot(
        {
            "data": result_data,
            "layout": Layout(
                title=title_generic,
                xaxis=dict(title=title_x),
                yaxis=dict(title=title_y),
                font=dict(
                    size=15
                )
            )
        },
        filename=html_file,
    )


def write_global_throughput(legend=None, input=None, image_file=None, html_file=None, plot_result="", title=None):
    logger.info("Writing global throughput graph")
    _legends, secondary_legend = __get_legends(legend, len(input))
    result_data = []
    # html_file = "request_throughput_" + html_file
    title_generic, title_x, title_y = __get_titles(title)

    cpt_input = 0
    cpt_global = 0
    cpt_max = 0
    average_data_x = []
    final_time_data = None
    average_data_y = []
    continuous_data_x = []
    continuous_data_y = []
    for _i in input:
        cpt_max += len(_i.split(","))

    for data in input:
        for _input in data.split(","):
            logger.info("Analysing input {}".format(_input))
            # current_legend = _legends.pop(0)
            _time_data = json.load(open(_input))
            result, average, time_data = get_latency(_time_data, plot_result)
            if not final_time_data:
                final_time_data = time_data
            continuous_data_y.extend(result)
            cpt_global += len(result)
            _cpt = 0
            for item in result:
                if len(average_data_y) <= _cpt:
                    average_data_y.append([item, ])
                    average_data_x.append(_cpt)
                else:
                    _list = average_data_y[_cpt]
                    _list.append(item)
                    average_data_y[_cpt] = _list
                _cpt += 1
            # time_keys = list(map(lambda x: x['url'], result))
            # time_keys.sort()
            # time_value = list(map(lambda x: result[x], time_keys))
            # index_list = list(map(lambda x: cpt_request + x, range(len(time_keys))))
            # cpt_request += len(index_list)
            # average_data_y.extend(
            #     [list(itertools.accumulate(result.values()))[-1]/len(result.values())]*len(result.values())
            # )
            # average_data_x.extend(index_list)
            cpt_input += 1
    data_continuous = Scatter(
        x=list(range(len(continuous_data_y))),
        y=continuous_data_y,
        name="continuous_data_y",
        line=dict(
            color="rgb({},{},{})".format(0, 0, 255)
        ),
        mode="lines"
    )
    for index, item in enumerate(average_data_y):
        av = list(itertools.accumulate(item))[-1]/len(item)
        average_data_y[index] = av

    average_data = []
    for cpt in range(len(time_data)):
        average_data.append([average_data_y[cpt], time_data[cpt]])

    sorted(average_data, key=lambda x: x[1])

    average_data_x = []
    start_time = None
    for item in map(lambda x: x[1], average_data):
        if not start_time:
            start_time = item
        item = item - start_time
        millis = int(str(item).split('.')[-1][:6])
        t = time.gmtime(int(item))
        average_data_x.append(
            datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec, millis)
        )

    data_average = Scatter(
        x=average_data_x,
        y=list(map(lambda x: x[0], average_data)),
        name="Average",
        line=dict(
            color="rgb({},{},{})".format(0, 0, 255)
        ),
        mode="lines"
    )
    plotly.offline.plot(
        {
            "data": [data_average, ],
            "layout": Layout(
                title=title_generic,
                xaxis=dict(title=title_x),
                yaxis=dict(title=title_y),
                font=dict(
                    size=15
                )
            )
        },
        filename="average_throughput_" + html_file,
    )
    plotly.offline.plot(
            {
                "data": [data_continuous, ],
                "layout": Layout(
                    title=title_generic,
                    xaxis=dict(title=title_x),
                    yaxis=dict(title=title_y),
                    font=dict(
                        size=15
                    )
                )
            },
            filename="continuous_throughput_" + html_file,
        )


def write_parallel_throughput(legend=None, input=None, image_file=None, html_file=None, plot_result="", title=None):
    logger.info("Writing global throughput graph")
    _legends, secondary_legend = __get_legends(legend, len(input))
    result_data = []
    title_generic, title_x, title_y = __get_titles(title)

    cpt_input = 0
    cpt_global = 0
    cpt_max = 0
    overhead_data = []
    MAX = 60
    for _i in input:
        cpt_max += len(_i.split(","))
    for data in input:
        for _input in data.split(","):
            logger.info("Analysing input {}".format(_input))
            current_legend = _legends.pop(0)
            _time_data = json.load(open(_input))
            result, average, time_data = get_latency(_time_data, plot_result)
            result = result[:MAX]
            cpt_global += len(result)
            if not overhead_data:
                for _data in result:
                    overhead_data.append(list())
            for _index, _data in enumerate(result):
                _item = overhead_data[_index]
                _item.append(_data)
                overhead_data[_index] = _item

            data_continuous = Scatter(
                x=__get_time_axis(time_data),
                # x=list(range(len(result))),
                y=result,
                name=current_legend,
                line=dict(
                    color="rgb({},{},{})".format(0, cpt_input * 255 / cpt_max, cpt_input * 255 / cpt_max)
                ),
                mode="lines"
            )
            cpt_input += 1
            result_data.append(data_continuous)

    for _index, _data in enumerate(overhead_data):
        if len(_data) == 2:
            _item = overhead_data[_index]
            overhead_data[_index] = 1-_item[1]/_item[0]
    data_overhead = Scatter(
        x=__get_time_axis(time_data),
        # x=list(range(len(result))),
        y=overhead_data,
        name="Overhead",
        line=dict(
            color="rgb({},{},{})".format(255, 0, 0)
        ),
        mode="lines"
    )
    # result_data.append(data_overhead)
    plotly.offline.plot(
            {
                "data": result_data,
                "layout": Layout(
                    title=title_generic,
                    xaxis=dict(title=title_x),
                    yaxis=dict(title=title_y),
                    font=dict(
                        size=20
                    )
                )
            },
            filename="parallel_throughput_" + html_file,
        )


def main():
    args, commands = init()
    if args.command in commands:
        commands[args.command](
            legend=args.legend,
            input=args.input,
            image_file=args.write_image,
            html_file=args.write_html,
            plot_result=args.plot_result,
            title=args.titles
        )
    else:
        logger.error("Unkwnon command: {}".format(args.command))


if __name__ == "__main__":
    main()
