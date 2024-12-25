import sys
import requests
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XRP Cryptocurrency Analytics")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Fetch XRP data
        try:
            response = requests.get('https://api.coingecko.com/api/v3/coins/ripple')
            data = response.json()
            total_supply = data['market_data']['total_supply']
            circulating_supply = data['market_data']['circulating_supply']
        except Exception as e:
            print(f"Error fetching data: {e}")
            return

        # Display total and circulating supply
        total_label = QLabel(f"Total Supply of XRP: {total_supply}")
        circulating_label = QLabel(f"Circulating Supply of XRP: {circulating_supply}")
        layout.addWidget(total_label)
        layout.addWidget(circulating_label)

        # Plotting the data
        fig = Figure(figsize=(12, 4))
        ax = fig.add_subplot(111)
        labels = ['Total Supply', 'Circulating Supply']
        values = [total_supply, circulating_supply]
        ax.bar(labels, values)
        ax.set_title('XRP Supply')
        ax.grid(True)

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        fig.tight_layout()

# Create and display the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()

print("Application has started. Close the application window to continue.")
sys.exit(app.exec())