Real Estate Auction Scraper
Overview

This project is a web scraper designed to extract real estate auction data from a government website. It gathers property information, including addresses, auction dates, and property types, and provides a user-friendly interface to explore the data. This README provides an overview of the project's features, installation instructions, usage guide, and additional information.
Features

    Web Scraping: The scraper collects real estate auction data from a specified government website.
    Data Geocoding: It uses the Google Maps Geocoding API to convert property addresses into latitude and longitude coordinates.
    Interactive Map: The project includes an interactive map that displays property locations on a map.
    Filtering: Users can filter the data based on auction type and province.
    Data Export: The scraped and filtered data can be exported to CSV files for further analysis.

Installation

    Clone the Repository:

    bash

git clone https://github.com/yourusername/real-estate-auction-scraper.git
cd real-estate-auction-scraper

Install Dependencies:

bash

    pip install -r requirements.txt

    Set Up Google Maps API Key:
        You'll need to obtain a Google Maps Geocoding API key and set it as an environment variable. Refer to the project documentation for details.

Usage

    Run the Scraper:

    bash

    python main.py

    Access the Web Interface:
        Open a web browser and go to http://localhost:8501 to access the interactive web interface.

    Explore Data:
        Use the interface to filter and explore the scraped real estate auction data.

    Export Data:
        Export filtered data to CSV files for further analysis.

Project Structure

    main.py: The main script to run the web scraper and start the Streamlit web application.
    backend_program/: Contains the web scraping and geocoding logic.
    frontend_program/: Contains the Streamlit web application code.
    data/: Directory to store scraped and exported data.
    utils/: Utility functions and helper scripts.

Contributing

Contributions are welcome!

Contact

    If you have any questions or suggestions, please feel free to contact us at renzorico10@gmail.com

Feel free to modify and expand this README to include any additional information or details about your project that you think would be useful for others. The key is to provide clear and concise information so that users can quickly understand and use your project.
