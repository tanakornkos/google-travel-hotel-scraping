
# Google Travel Hotel pricing Scraping

This script is designed to scrape hotel prices from Google Travel for a list of hotels and dates. It uses the Playwright library to automate the process of searching for hotels, filling in dates, and extracting prices from various online travel agencies (OTAs).


## Features

- CSV Input: Reads data from a CSV file where the input values (such as dates) can be stored.
- Date Filling: Automatically fills check-in and check-out date fields on web forms.
- Web Scraping: Uses Playwright to interact with web elements and extract data.


## Requirements

Python 3.7+

Playwright library 
```bash
  pip install playwright
```
Pandas library 
```bash
  pip install pandas
```
CSV library 
```bash
  pip install csv
```



## Features

1. Clone the repository and navigate to the project directory.
2. Install the required libraries by running 
 ```bash
  pip install -r requirements.txt
```
3. Update the CheckinDates list in the script with the desired dates.
4. Update the file_path variable with the path to your hotel list CSV file.
5. Run the script using python main.py.

## Input Table file_path .csv
file_path:
HotelName | Date |
--- | --- 
Hotel Something | mm/dd/YYYY

## Output Table save_data .xlsx
Shoprate Result:
Hotel	| Checkin Date| Checkout Date | Agoda	| Booking.com | 
--- | ---  | --- | --- | ---  
Hotel Something |  dd/mm/YYYY | dd/mm/YYYY | PriceTHB | PriceTHB

