# BotaniDex: Your Plant Care Assistant

**BotaniDex** is a Streamlit application designed to help users discover basic plant care instructions and check the safety of plants. The app interacts with the Perenual API to provide detailed information on various plant species, including their growth rates, care levels, and origin.

## Features

- **Basic Plant Care**: Search for a plant by name and receive essential care instructions, along with detailed insights.
- **Plant Safety Checker**: Quickly validate whether a plant is poisonous or safe for consumption.
- **Interactive Visualizations**: View growth rates, care levels, pruning schedules, and origin maps for plants.

## Installation

### Prerequisites

- Python 3.7 or higher
- [Streamlit](https://streamlit.io/)
- An API key from the [Perenual](https://perenual.com/docs) API

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/botanidex.git
   cd botanidex
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Add your API key:

Create a .env file in the project root and add your API key:
plaintext
Copy code
API_KEY=your_actual_api_key_here
Run the application:

bash
Copy code
streamlit run app.py
Usage
Basic Plant Care
Select "Basic Plant Care" from the sidebar.
Enter the name of the plant you want to search for.
Click "Search" to view basic information such as common name, watering needs, and sunlight requirements.
Check "Detailed Information" for more in-depth data, including propagation methods and growth rates.
Optionally, visualize the plant's growth rate, care level, pruning activity, and places of origin.
Plant Safety Checker
Select "Plant Safety Checker" from the sidebar.
Enter the name of the plant you want to check.
Choose between "Interactive Table" or "Info Boxes" for display format.
Click "Search Safety" to see if the plant is edible or poisonous.
Customization
Background Color: You can customize the app's background color using the color picker in the sidebar.
Contributing
Feel free to fork the repository and submit pull requests. Contributions, whether they are bug fixes, improvements, or new features, are welcome!
