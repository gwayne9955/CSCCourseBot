from intent_handling.signal import Signal


class LinkToFlowchart:

    def __init__(self):
        pass

    @staticmethod
    def execute():
        link = "https://flowcharts.calpoly.edu/downloads/mymap/17-19.52CSCBSU.pdf"
        answer = "To see the most recent CSC flowchart, visit {}"\
                 .format(link)
        return Signal.NORMAL, answer
