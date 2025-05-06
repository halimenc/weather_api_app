import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
#first install PyQt5 

# Define the main WeatherApp class inheriting from QWidget
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        # Create UI components
        self.city_label= QLabel("Enter a city name: ", self)
        self.city_input= QLineEdit(self)
        self.get_weather_button= QPushButton("Get Weather ",self)
        self.temp_label= QLabel(self)
        self.emoji_label= QLabel(self)
        self.description_label= QLabel(self)
        self.initUI()  # Initialize the UI layout and styles

    def initUI(self):
        self.setWindowTitle("Weather App") # Set window title

        vbox = QVBoxLayout() # Use vertical box layout

        # Add widgets to the layout
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox) # Apply layout to the main window

        # Center align the widgets
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # Assign object names for styling
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temp_label.setObjectName("temp_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Define style sheet for widgets
        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
                }

            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            
            QLineEdit#city_input{
                font-size: 30px;
            }

            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }

            QLabel#temp_label{
                font-size: 50px;
            }

            QLabel#emoji_label{
                font-size: 50px;
                font-family: "Segoe UI Emoji";
            }

            QLabel#description_label{
                font-size: 50px;
            }   
        """ )

        # Connect button click to weather function
        self.get_weather_button.clicked.connect(self.get_weather)

    # Function to fetch weather data from API
    def get_weather(self):
        api_key="551d2641dada89a61d7027297ba54518"
        city=self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response= requests.get(url)
            response.raise_for_status()
            data=response.json()

            if data["cod"]==200:
                self.display_weather(data)
 
        # Handle various HTTP errors
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request: \nPlease check your input!")
                case 401:
                    self.display_error("Unauthorized: \nInvalid API key!")
                case 403:
                    self.display_error("Forbidden: \nAccess is denied!")
                case 404:
                    self.display_error("Not found: \nCity not found!")
                case 500:
                    self.display_error("Internal server error: \nPlease try again later!")
                case 502:
                    self.display_error("Bad gateway: \nInvalid response from server!")
                case 503:
                    self.display_error("Service Unavaible: \nServer is down!")
                case 504:
                    self.display_error("Gateway timeout: \nNo response from server!")
                case _:
                    self.display_error(f"Http error occured: \n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\n Please check your internet")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error\nThe request timeout")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects Error\n Check the URL")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error\n{req_error}")

     # Show error message on the UI                   
    def display_error(self, message):
        self.temp_label.setStyleSheet("font-size: 30px;")
        self.temp_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()


    def display_weather(self, data):
        self.temp_label.setStyleSheet("font-size: 75px;")      
        temperature_k= data["main"]["temp"]
        temperature_c=temperature_k-273.15
        temperature_f=(temperature_k*9/5)-459.67
        weather_id= data["weather"][0]["id"]
        weather_description=data["weather"][0]["description"]

        # Set temperature, emoji, and description on UI
        self.temp_label.setText(f"{temperature_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    # Static method to return emoji based on weather ID
    @staticmethod
    def get_weather_emoji(weather_id):

        if 200<= weather_id <=232:
            return " ⛈️ "
        elif 300<= weather_id <=321:
            return " 🌦️ "
        elif 500<= weather_id <=531:
            return " 🌧️ "
        elif 600<= weather_id <=622:
            return " ❄️ "
        elif 701<= weather_id <=741:
            return "🌫️"
        elif weather_id ==762:
            return "🌋"
        elif weather_id ==771:
            return "💨"
        elif weather_id ==762:
            return "🌪️"
        elif weather_id ==800:
            return " ☀️ "
        elif 801<= weather_id <=804:
            return " ☁️"
        else:
            return "🦊"

# Entry point of the program
if __name__=="__main__":
    app=QApplication(sys.argv)
    Weather_App=WeatherApp()
    Weather_App.show()
    sys.exit(app.exec_())


            
        

