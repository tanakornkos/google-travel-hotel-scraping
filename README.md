
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
 ```bash
CheckinDates = [
    "9/25/2024",
    "9/26/2024"
    ]
```
4. Update the file_path variable with the path to your hotel list CSV file.
5. Run the script using python main.py.

## Input 
Table file_path .csv as
file_path:
HotelName | Checkin-Date |
--- | --- 
Hotel 1 | 09/25/2024
Hotel 2 | 09/25/2024

## Output 
The script will output an Excel file named shoprateResult.xlsx containing the scraped data.
Table save_data .xlsx
 as Shoprate Result:
Hotel	| Checkin Date| Checkout Date | Agoda	| Booking.com | 
--- | ---  | --- | --- | ---  
Hotel 1 |  09/25/2024 | 09/26/2024 | PriceTHB | PriceTHB
Hotel 1 |  09/26/2024 | 09/27/2024 | PriceTHB | PriceTHB
Hotel 2 |  09/25/2024 | 09/26/2024 | PriceTHB | PriceTHB
Hotel 2 |  09/26/2024 | 09/27/2024 | PriceTHB | PriceTHB


## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://drive.google.com/file/d/1KqmKB8y0BCFsavThNPuRz3UGPokbZvkm/view?usp=sharing)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/tanakorn-kosawanichkarn-55b476233/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://x.com/zentn10)



