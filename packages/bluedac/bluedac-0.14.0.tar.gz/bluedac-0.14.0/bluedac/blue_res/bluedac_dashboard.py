from aws_cdk import aws_cloudwatch as cw

class Bluedac_Dashboard(cw.Dashboard):

    # Translation map for str -> cw.Stats
    str_to_stat = {
        "average": cw.Stats.AVERAGE,
        "sum": cw.Stats.SUM,
        "maximum": cw.Stats.MAXIMUM,
        "minimum": cw.Stats.MINIMUM,
        "iqm": cw.Stats.IQM,
        "count": cw.Stats.SAMPLE_COUNT
    }

    def __init__(self, stack, dashboard_name):
        super().__init__(stack, dashboard_name)

    def append_metrics(self, metrics: list):
        for metric in metrics:
            match metric["type"]:
                case "TextWidget":
                    self.add_widgets(
                        cw.TextWidget (
                            markdown = metric["text"],
                            width = 24,
                            height = 2
                        )
                    )
                case "GraphWidget":
                    self.add_widgets(
                        cw.GraphWidget(
                            title=f"Lambda {metric["metric"]}",
                            width=8,
                            statistic=Bluedac_Dashboard.str_to_stat[metric["statistic"]],
                            left=[metric["resource"].metric(metric["metric"], period=metric["duration"])]
                        )
                    )