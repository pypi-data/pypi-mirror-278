import os
import sys

import Orange.data
from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output

from PyQt5 import uic
from AnyQt.QtWidgets import QApplication, QLabel

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\","/"):
    from Orange.widgets.orangecontrib.AAIT.utils import shared_functions
    from Orange.widgets.orangecontrib.AAIT.llm import generation
else:
    from orangecontrib.AAIT.utils import shared_functions
    from orangecontrib.AAIT import generation


class OWSelectMWE(widget.OWWidget):
    name = "Query LLM"
    description = "Generate a response to a query with a LLM"
    icon = "icons/owqueryllm.svg"
    gui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/owqueryllm.ui")
    want_control_area = False


    def __init__(self):
        super().__init__()
        # Path management
        self.current_ows = ""
        shared_functions.setup_shared_variables(self)
        model_name = "LLM_Query.gguf"
        self.model_path = os.path.join(os.path.dirname(os.path.dirname(self.current_ows)), "Models", model_name)
        # TODO changer path pour get_local_store_path from MetManagements.py

        # Qt Management
        self.setFixedWidth(470)
        self.setFixedHeight(300)
        uic.loadUi(self.gui, self)
        self.label_description = self.findChild(QLabel, 'Description')
        self.label_description.setText("This widget generates an answer on the column 'prompt' of your input data.")

        # Data Management
        self.data = None

    def run(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_widget = OWSelectMWE()
    my_widget.show()
    app.exec_()
