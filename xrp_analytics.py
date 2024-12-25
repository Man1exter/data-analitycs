import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    def __init__(self, total_supply, circulating_supply):
        super().__init__()
        self.setWindowTitle("XRP Analytics")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Displaying the supply information
        try:
            total_label = QLabel(f"Total Supply of XRP: {total_supply}")
            circulating_label = QLabel(f"Circulating Supply of XRP: {circulating_supply}")
            layout.addWidget(total_label)
            layout.addWidget(circulating_label)
        except Exception as e:
            print(f"Error displaying supply information: {e}")
            return

        # Plotting the data
        try:
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
        except Exception as e:
            print(f"Error plotting data: {e}")
            return

# Create and display the application
if __name__ == "__main__":
    total_supply = 100000000  # Example value, replace with actual data
    circulating_supply = 50000000  # Example value, replace with actual data

    app = QApplication(sys.argv)
    window = MainWindow(total_supply, circulating_supply)
    window.show()

    print("Application has started. Close the application window to continue.")
    sys.exit(app.exec())