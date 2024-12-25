import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Poland vs Others")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Load data
        try:
            df = pd.read_csv('data.csv')
        except Exception as e:
            print(f"Error loading data: {e}")
            return

        # Wykres 1: Polska vs inne kraje
        fig1 = Figure(figsize=(12, 4))
        ax1 = fig1.add_subplot(111)
        try:
            country_counts = df['Kraj'].value_counts()
            ax1.bar(country_counts.index, country_counts.values)
            ax1.set_title('Polska vs inne kraje')
            ax1.legend()
            ax1.grid(True)
        except KeyError as e:
            print(f"Error processing data for plot 1: {e}")
            return

        canvas1 = FigureCanvas(fig1)
        layout.addWidget(canvas1)

        # Wykres 2: Kategorie produktów
        fig2 = Figure(figsize=(12, 4))
        ax2 = fig2.add_subplot(111)
        try:
            category_counts = df['Kategoria'].value_counts()
            ax2.bar(category_counts.index, category_counts.values)
            ax2.set_title('Najpopularniejsze kategorie produktów')
            ax2.tick_params(axis='x', rotation=45)
        except KeyError as e:
            print(f"Error processing data for plot 2: {e}")
            return

        canvas2 = FigureCanvas(fig2)
        layout.addWidget(canvas2)

        fig1.tight_layout()
        fig2.tight_layout()

# Tworzenie i wyświetlanie aplikacji
app = QApplication(sys.argv)
window = MainWindow()
window.show()

print("Aplikacja została uruchomiona. Zamknij okno aplikacji, aby kontynuować.")
sys.exit(app.exec_())