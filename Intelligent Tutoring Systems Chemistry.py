import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit, QGridLayout, QToolTip
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from rdflib import Graph

# Path to the RDF file
rdf_file = 'final_project_period.rdf'

# Global variable for element data
element_data = {}

# Hardcoded color mapping for all atomic numbers
hardcoded_colors = {
    1: "#FF9999", 2: "#FF9999", 3: "#FF9999", 4: "#FF9999", 5: "#FFFF99",
    6: "#FFFF99", 7: "#FFFF99", 8: "#FFFF99", 9: "#FFFF99", 10: "#FF9999",
    11: "#FF9999", 12: "#FF9999", 13: "#FFFF99", 14: "#FFFF99", 15: "#FFFF99",
    16: "#FFFF99", 17: "#FFFF99", 18: "#FF9999", 19: "#FF9999", 20: "#FF9999",
    21: "#87CEFA", 22: "#87CEFA", 23: "#87CEFA", 24: "#87CEFA", 25: "#87CEFA",
    26: "#87CEFA", 27: "#87CEFA", 28: "#87CEFA", 29: "#87CEFA", 30: "#87CEFA",
    31: "#FFFF99", 32: "#FFFF99", 33: "#ADFF2F", 34: "#FFFF99", 35: "#FFFF99",
    36: "#FF9999", 37: "#FF9999", 38: "#FF9999", 39: "#87CEFA", 40: "#87CEFA",
    41: "#87CEFA", 42: "#87CEFA", 43: "#87CEFA", 44: "#87CEFA", 45: "#87CEFA",
    46: "#87CEFA", 47: "#87CEFA", 48: "#87CEFA", 49: "#FFFF99", 50: "#FFFF99",
    51: "#ADFF2F", 52: "#FFFF99", 53: "#FFFF99", 54: "#FF9999", 55: "#FF9999",
    56: "#FF9999", 57: "#90EE90", 58: "#90EE90", 59: "#90EE90", 60: "#90EE90",
    61: "#90EE90", 62: "#90EE90", 63: "#90EE90", 64: "#90EE90", 65: "#90EE90",
    66: "#90EE90", 67: "#90EE90", 68: "#90EE90", 69: "#90EE90", 70: "#90EE90",
    71: "#90EE90", 72: "#87CEFA", 73: "#87CEFA", 74: "#87CEFA", 75: "#87CEFA",
    76: "#87CEFA", 77: "#87CEFA", 78: "#87CEFA", 79: "#87CEFA", 80: "#87CEFA",
    81: "#FFFF99", 82: "#FFFF99", 83: "#ADFF2F", 84: "#FFFF99", 85: "#FFFF99",
    86: "#FF9999", 87: "#FF9999", 88: "#FF9999", 89: "#90EE90", 90: "#90EE90",
    91: "#90EE90", 92: "#90EE90", 93: "#90EE90", 94: "#90EE90", 95: "#90EE90",
    96: "#90EE90", 97: "#90EE90", 98: "#90EE90", 99: "#90EE90", 100: "#90EE90",
    101: "#90EE90", 102: "#90EE90", 103: "#90EE90", 104: "#87CEFA", 105: "#87CEFA",
    106: "#87CEFA", 107: "#87CEFA", 108: "#87CEFA", 109: "#87CEFA", 110: "#87CEFA",
    111: "#87CEFA", 112: "#87CEFA", 113: "#FFFF99", 114: "#FFFF99", 115: "#FFFF99",
    116: "#FFFF99", 117: "#FFFF99", 118: "#FF9999",
}

# Load the RDF file
def load_rdf(file_path):
    try:
        g = Graph()
        g.parse(file_path, format="xml")
        print(f"RDF file loaded successfully from: {file_path}")
        return g
    except Exception as e:
        print(f"Error loading RDF file: {e}")
        return None

# Load element data from RDF file
def load_element_data(graph):
    global element_data
    query = """
    PREFIX : <http://periodic.org/ontology#>
    SELECT ?name ?atomicNumber ?symbol ?group ?period ?category ?state ?meltingPoint ?boilingPoint ?electronegativity
    WHERE {
        ?element rdf:type :Element ;
                 :hasAtomicNumber ?atomicNumber ;
                 :hasSymbol ?symbol .
        OPTIONAL { ?element :belongsToGroup ?group . }
        OPTIONAL { ?element :belongsToPeriod ?period . }
        OPTIONAL { ?element :hasCategory ?category . }
        OPTIONAL { ?element :hasState ?state . }
        OPTIONAL { ?element :hasMeltingPoint ?meltingPoint . }
        OPTIONAL { ?element :hasBoilingPoint ?boilingPoint . }
        OPTIONAL { ?element :hasElectronegativity ?electronegativity . }
        BIND(STRAFTER(STR(?element), "#") AS ?name)
    }
    """
    for row in graph.query(query):
        element_data[int(row.atomicNumber)] = {
            "name": row.name,
            "symbol": row.symbol,
            "atomicNumber": int(row.atomicNumber),
            "group": row.group.split("#")[-1] if row.group else "Unknown",
            "period": row.period.split("#")[-1] if row.period else "Unknown",
            "category": row.category.split("#")[-1] if row.category else "Unknown",
            "state": row.state.split("#")[-1] if row.state else "Unknown",
            "meltingPoint": row.meltingPoint or "Unknown",
            "boilingPoint": row.boilingPoint or "Unknown",
            "electronegativity": row.electronegativity or "Unknown",
        }
    print(f"Loaded {len(element_data)} elements.")

class PeriodicTableApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Intelligent Tutoring System for Chemistry (Periodic Table)")
        self.setGeometry(100, 100, 1200, 800)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)

        # Title label
        title_label = QLabel("Learn Your Periodic Table")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Periodic table grid
        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)

        # Results display
        self.results_display = QTextEdit()
        self.results_display.setFont(QFont("Arial", 12))
        self.results_display.setReadOnly(True)
        layout.addWidget(self.results_display)

        self.create_periodic_table_grid()

    def create_periodic_table_grid(self):
        periodic_table_layout = [
            [1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 2],
            [3, 4, None, None, None, None, None, None, None, None, None, None, 5, 6, 7, 8, 9, 10],
            [11, 12, None, None, None, None, None, None, None, None, None, None, 13, 14, 15, 16, 17, 18],
            [19, 20, None, None, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],
            [37, 38, None, None, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54],
            [55, 56, None, None, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86],
            [87, 88, None, None, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118],
            [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71],
            [89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103],
        ]

        for row_index, row in enumerate(periodic_table_layout):
            for col_index, atomic_number in enumerate(row):
                if atomic_number:
                    element = element_data.get(atomic_number, {})
                    btn_color = hardcoded_colors.get(atomic_number, "#D3D3D3")
                    btn_text = f"{element.get('symbol', '?')}\n{atomic_number}"
                    btn = QPushButton(btn_text)
                    btn.setStyleSheet(f"background-color: {btn_color}; font-size: 10px;")
                    btn.setToolTip(f"Name: {element.get('name', '?')}\nAtomic Number: {atomic_number}")
                    btn.clicked.connect(lambda _, num=atomic_number: self.display_element_details(num))
                    self.grid_layout.addWidget(btn, row_index, col_index)

    def display_element_details(self, atomic_number):
        element = element_data.get(atomic_number, {})
        self.results_display.clear()
        self.results_display.append(f"<b>Name:</b> {element.get('name', 'Unknown')}\n")
        self.results_display.append(f"Atomic Number: {element.get('atomicNumber', 'Unknown')}\n")
        self.results_display.append(f"Symbol: {element.get('symbol', 'Unknown')}\n")
        self.results_display.append(f"Group: {element.get('group', 'Unknown')}\n")
        self.results_display.append(f"Period: {element.get('period', 'Unknown')}\n")
        self.results_display.append(f"Category: {element.get('category', 'Unknown')}\n")
        self.results_display.append(f"State: {element.get('state', 'Unknown')}\n")
        self.results_display.append(f"Melting Point: {element.get('meltingPoint', 'Unknown')}\n")
        self.results_display.append(f"Boiling Point: {element.get('boilingPoint', 'Unknown')}\n")
        self.results_display.append(f"Electronegativity: {element.get('electronegativity', 'Unknown')}\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    graph = load_rdf(rdf_file)
    if graph:
        load_element_data(graph)

    main_window = PeriodicTableApp()
    main_window.show()

    sys.exit(app.exec())
