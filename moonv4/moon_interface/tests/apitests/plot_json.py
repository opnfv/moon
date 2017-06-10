import argparse
import logging
import json
import plotly
from plotly.graph_objs import Scatter, Layout
import plotly.figure_factory as ff


logger = None


def init():
    global logger, HOST, PORT
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action='store_true', help="verbose mode")
    parser.add_argument("--host",
                        help="Set the name of the host to test (default: 172.18.0.11).",
                        default="172.18.0.11")
    parser.add_argument("--port", "-p",
                        help="Set the port of the host to test (default: 38001).",
                        default="38001")
    parser.add_argument("--test-only", "-t", action='store_true', dest='testonly', help="Do not generate graphs")
    parser.add_argument("--write", "-w", help="Write test data to a JSON file", default="/tmp/data.json")
    parser.add_argument("--input", "-i", help="Get data from a JSON input file")
    parser.add_argument("--legend", "-l", help="Set the legend (default: 'rbac,rbac+session')",
                        default='rbac,rbac+session')
    parser.add_argument("--distgraph", "-d",
                        help="Show a distribution graph instead of a linear graph",
                        action='store_true')
    parser.add_argument("--request-per-second", help="Number of requests per seconds",
                        type=int, dest="request_second", default=1)
    parser.add_argument("--limit", help="Limit request to LIMIT", type=int)
    parser.add_argument("--write-image", help="Write the graph to file IMAGE", dest="write_image")
    parser.add_argument("--write-html", help="Write the graph to HTML file HTML", dest="write_html", default="data.html")
    args = parser.parse_args()

    FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
    logging.basicConfig(
        format=FORMAT,
        level=logging.INFO)

    logger = logging.getLogger(__name__)

    HOST = args.host
    PORT = args.port
    return args


def get_delta(time_data):
    time_delta = list()
    time_delta_sum1 = 0
    for key in time_data:
        time_delta.append(time_data[key]['delta'])
        time_delta_sum1 += time_data[key]['delta']
    time_delta_average1 = time_delta_sum1 / len(time_data.keys())
    return time_delta, time_delta_average1


def write_graph(legend=None, input=None, image_file=None, html_file=None):
    logger.info("Writing graph")
    legends = legend.split(",")
    result_data = []
    for _input in input.split(","):
        current_legend = legends.pop(0)
        time_data2 = json.load(open(_input))
        time_delta2, time_delta_average2 = get_delta(time_data2)
        for key in time_data2.keys():
            if key in time_data2:
                time_delta2.append(time_data2[key]['delta'])
            else:
                time_delta2.append(None)
        data2 = Scatter(
            x=list(range(len(time_data2.keys()))),
            y=time_delta2,
            name=current_legend,
            line=dict(
                color='rgb(255, 192, 118)',
                shape='spline')
        )
        result_data.append(data2)
        data2_a = Scatter(
            x=list(range(len(time_data2.keys()))),
            y=[time_delta_average2 for x in range(len(time_data2.keys()))],
            name=current_legend + " average",
            line=dict(
                color='rgb(255, 152, 33)',
                shape='spline')
        )
        result_data.append(data2_a)

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


def write_distgraph(legend=None, input=None, image_file=None, html_file=None):

    logger.info("Writing graph")
    legends = legend.split(",")
    result_data = []

    for _input in input.split(","):
        logger.info("Analysing input {}".format(_input))
        time_data2 = json.load(open(_input))
        time_delta2, time_delta_average2 = get_delta(time_data2)
        result_data.append(time_delta2)

    # Create distplot with custom bin_size
    if len(legends) < len(result_data):
        for _cpt in range(len(result_data)-len(legends)):
            legends.append("NC")
    fig = ff.create_distplot(result_data, legends, bin_size=.2)

    # Plot!
    plotly.offline.plot(
        fig,
        image="svg",
        image_filename=image_file,
        image_height=1000,
        image_width=1200,
        filename=html_file
    )
    return 0


def main():
    args = init()
    if args.distgraph:
        write_distgraph(legend=args.legend, input=args.input, image_file=args.write_image,
                        html_file=args.write_html)
    else:
        write_graph(legend=args.legend, input=args.input, image_file=args.write_image,
                    html_file=args.write_html)


if __name__ == "__main__":
    main()
