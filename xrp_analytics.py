import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from textblob import TextBlob

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XRP Analytics")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Fetch and display data
        self.fetch_and_display_data()

        # Add a refresh button
        refresh_button = QPushButton("Refresh Data")
        refresh_button.clicked.connect(self.fetch_and_display_data)
        self.layout.addWidget(refresh_button)

    def fetch_and_display_data(self):
        # Clear the layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Fetch XRP data
        try:
            response = requests.get('https://api.coingecko.com/api/v3/coins/ripple')
            data = response.json()
            total_supply = data['market_data']['total_supply']
            circulating_supply = data['market_data']['circulating_supply']
            current_price = data['market_data']['current_price']['usd']
            market_cap = data['market_data']['market_cap']['usd']
            volume_24h = data['market_data']['total_volume']['usd']
        except Exception as e:
            print(f"Error fetching data: {e}")
            return

        # Display total and circulating supply
        total_label = QLabel(f"Total Supply of XRP: {total_supply}")
        circulating_label = QLabel(f"Circulating Supply of XRP: {circulating_supply}")
        price_label = QLabel(f"Current Price of XRP: ${current_price}")
        market_cap_label = QLabel(f"Market Cap of XRP: ${market_cap}")
        volume_24h_label = QLabel(f"24h Trading Volume of XRP: ${volume_24h}")
        self.layout.addWidget(total_label)
        self.layout.addWidget(circulating_label)
        self.layout.addWidget(price_label)
        self.layout.addWidget(market_cap_label)
        self.layout.addWidget(volume_24h_label)

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
            self.layout.addWidget(canvas)

            fig.tight_layout()
        except Exception as e:
            print(f"Error plotting data: {e}")
            return

        # Fetch and display news
        self.fetch_and_display_news()

    def fetch_and_display_news(self):
        try:
            news_api_key = 'YOUR_NEWS_API_KEY'  # Replace with your News API key
            news_url = f'https://newsapi.org/v2/everything?q=Ripple&apiKey={news_api_key}'
            response = requests.get(news_url)
            news_data = response.json()
            articles = news_data['articles'][:5]  # Get the top 5 news articles

            news_label = QLabel("Latest News about Ripple:")
            self.layout.addWidget(news_label)

            for article in articles:
                title = article['title']
                sentiment = TextBlob(title).sentiment.polarity
                sentiment_label = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
                news_item_label = QLabel(f"{title} (Sentiment: {sentiment_label})")
                self.layout.addWidget(news_item_label)
        except Exception as e:
            print(f"Error fetching news: {e}")

# Create and display the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    print("Application has started. Close the application window to continue.")
    sys.exit(app.exec())