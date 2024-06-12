from json import dumps
from IPython.display import Javascript, display

class Desmos:
    def __init__(self, api_key="dcb31709b452b1cf9dc26972add0fda6", height="480px", width="100%"):
        self.api_url = "https://www.desmos.com/api/v1.9/calculator.js?apiKey={0}".format(
            api_key)
        self.height = height 
        self.width = width # Note that it appears only height is honored
        self.expressions = list()

    def build_graph_lines(self):
        graph_lines = ""
        for item in self.expressions:                        
            line = 'calculator.setExpression('"{0}"');'.format(dumps(item))
            graph_lines = graph_lines + line
        return graph_lines
    
    def build_script(self) -> str:
        graph_lines = self.build_graph_lines()
        script = """
        element.style.height = '{0}';
        element.style.width = '{1}';
        var calculator = Desmos.GraphingCalculator(element);
        {2}
        """.format(self.height, self.width, graph_lines)
        return script

    def add_expression(self, value: dict):
        self.expressions.append(value)
        return self
    
    def add_latex(self, value: str):
        d = {"latex": value}
        return self.add_expression(d)

    def display(self):
        script = self.build_script()
        js = Javascript(script, lib=[self.api_url])
        display(js)

