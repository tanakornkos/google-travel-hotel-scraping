from playwright.sync_api import sync_playwright
import pandas as pd
import csv
from datetime import datetime, timedelta

def read_csv_as_strings(file_path):
    rows_as_strings = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            row_as_string = ','.join(row)
            rows_as_strings.append(row_as_string)
    return rows_as_strings


def fill_dates(page, checkin_date, checkout_date):
    checkin_selector = 'input.TP4Lpb.eoY5cb.j0Ppje[placeholder="Check-in"]'
    checkout_selector = 'input.TP4Lpb.eoY5cb.j0Ppje[placeholder="Check-out"]'
    div_date='div.GYgkab.YICvqf.M8oMHb'
    checkin_date_holder=page.locator(div_date).nth(4)
    checkout_date_holder=page.locator(div_date).nth(5)
    try:
        checkin_show=checkin_date_holder.get_attribute('data-value')
        checkout_show=checkout_date_holder.get_attribute('data-value')
        print(f'check in show: {checkin_show}')
        checkin_input = page.locator(checkin_selector).nth(2)
        if checkin_input.is_visible():
            checkin_input.fill(checkin_date)
            page.keyboard.press("Enter")
        # Fill check-out date
        checkout_input = page.locator(checkout_selector).nth(2)
        if checkout_input.is_visible():
            checkout_input.fill(checkout_date)
            page.keyboard.press("Enter")
        if checkin_date!= checkin_show and checkout_date != checkout_show:
        # Fill check-in date
            checkin_input = page.locator(checkin_selector).nth(2)
            if checkin_input.is_visible():
                checkin_input.fill(checkin_date)
            page.keyboard.press("Enter")
        # Fill check-out date
            checkout_input = page.locator(checkout_selector).nth(2)
            if checkout_input.is_visible():
                checkout_input.fill(checkout_date)
            page.keyboard.press("Enter")

        print(f'check in:{checkin_date}, Check out: {checkout_date}')
    except:
        print('fill date Error')
def search_hotel(page, hotel_name):
    try:
        

        if page.get_by_role("combobox", name="Search for places, hotels and more").is_visible():
            print('search box is visible')
            page.get_by_placeholder("Search for places, hotels and more").first.click()
            page.get_by_role("combobox", name="Search for places, hotels and more").fill(str(hotel_name))
            page.keyboard.press("Enter")
        else:
            print('search box is not visible')
            
            page.get_by_label("Clear").first.click()
            page.get_by_role("combobox", name="Search for places, hotels and more").fill(str(hotel_name))
            page.keyboard.press("Enter")
        return True
    except Exception as e:
        print(f"Error searching for hotel: {e}")
        return False
    
def click_firstnum_a_element(page, selector, timeout,N):
    try:
        print(f"Waiting for selector: {selector} to be present")
        page.wait_for_selector(selector, timeout=timeout)
        print('wait for selector done')
        first_a_locator = page.locator(selector).nth(N)
        print('first locator done')
        if first_a_locator and first_a_locator.is_visible():
            print("Element is visible, proceeding to click")
            first_a_locator.click(force=True)
            print("Click successful")
        else:
            print("Element is not visible after waiting or not found")
        return first_a_locator.inner_text()
    except Exception:
        print("Error clicking first hotel link")
        return False


def extract_ota_data(page, hotel_name, checkin_date, checkout_date):
    OTA_dict = {'Hotel': hotel_name, 'Checkin Date': checkin_date, 'Checkout Date': checkout_date, 'Agoda': '', 'Booking.com': ''}

    try:
        OTAs = 'div.IJxDxc'  # This targets the div with the specified class
        
        # Extract from other OTAs
        divs = page.locator(OTAs)  # Correct usage of locator
        OTAs_count = divs.count()
        print(f"Found {OTAs_count} OTA divs")
        
        for i in range(OTAs_count):
            div = divs.nth(i)  # Get the nth div element
            
            # Locate the span inside the div
            OTA_name_span = div.locator('span.FjC1We.ogfYpf.zUyrwb')
            OTA_price_span = div.locator('span.MW1oTb')
            
            # Ensure spans exist before extracting content
            if OTA_name_span.count() > 0 and OTA_price_span.count() > 0:
                OTA_name = OTA_name_span.nth(0).text_content()  # Get the text of the first span element
                OTA_price = OTA_price_span.nth(0).text_content()  # Get the price text
                
                # Clean the price to extract only digits
                OTA_price_cleaned = ''.join(filter(str.isdigit, OTA_price))
                
                # Check if OTA name matches either Agoda or Booking.com
                if OTA_name in ['Agoda', 'Booking.com']:
                    OTA_dict[OTA_name] = OTA_price_cleaned
                    print(f"Found OTA: {OTA_name} with price: {OTA_price_cleaned}")

        return OTA_dict

    except Exception as e:
        print(f"Error: {e}")
        return OTA_dict

def main(file_path,CheckinDates):
    dates_list = read_checkin_dates(file_path)
    OTA_list = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        page_url = 'https://www.google.com/travel/search?q=hotel&ts=CAESCgoCCAMKAggDEAAqBwoFOgNUSEI&ved=0CAAQ5JsGahcKEwiwiNq-oPGIAxUAAAAAHQAAAAAQSQ&ictx=3&hl=en-TH&gl=th&g2lb=2503771%2C2503781%2C4814050%2C4874190%2C4893075%2C4965990%2C10210221%2C72277293%2C72302247%2C72317059%2C72406588%2C72414906%2C72421566%2C72462234%2C72470899%2C72471280%2C72472051%2C72473841%2C72485658%2C72486593%2C72494250%2C72513422%2C72513513%2C72520080%2C72536387%2C72538597%2C72543209%2C72549171%2C72556203%2C72565685%2C72570850%2C72582843%2C72582855%2C72600943%2C72602734&qs=CAAgACgA&ap=KigKEgkZmg-izLEyQBE9npYva7hYQBISCZAf06HM5jJAET2elg8FxlhAMAA'
        page.goto(page_url, timeout=100000)
        page.wait_for_load_state('domcontentloaded')
        click_price=False
        count_hotel = 0
        for dates in dates_list:
            try:    
                hotel_name, checkin_date, checkout_date = dates   
                
                count_hotel += 1
                if click_price:
                    element=page.locator('//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-INsAgc VfPpkd-LgbsSe-OWXEXe-dgl2Hf Rj2Mlf OLiIxf PDpWxe P62QJc LQeN7 rRDaU xnu6rd QGRmIf"]')
                    element.click(force=True)
                search_hotel(page, hotel_name)
                page.wait_for_load_state("networkidle")
                click_price=click_firstnum_a_element(page, '//*[@id="prices"]', 5000, 0)
                
                if page.get_by_placeholder('No results').count() ==0 :
                    print(f"Element div.q0amnf.AdWm1c is visible, just pass")
                    
                
                    while not click_price:
                        for i in range(3):
                            print(f"searching {hotel_name} {i}.")
                            try:
                                arail_text = page.locator('//a[@class="PVOOXe"]').nth(i).get_attribute('aria-label')

                                first_two_words = ' '.join(arail_text.split()[:2])
                                print(f"Arail label: {first_two_words}")
                                if ' '.join(hotel_name.split()[:2]) == first_two_words:
                                    page.locator('div.uaTTDe.BcKagd.bLc2Te.Xr6b1e').nth(i).click(force=True)
                                    page.wait_for_load_state("networkidle")
                                    click_price=click_firstnum_a_element(page, '//*[@id="prices"]', 5000, 0)
                                    break
                            except Exception as e:
                                print(f"searching {first_two_words}not equal {hotel_name}. Error: {e}")
                                pass
                            if i == 2:
                                click_price=True
                                break
                click_price=click_firstnum_a_element(page, '//*[@id="prices"]', 5000, 0)
                page.wait_for_load_state("networkidle")
                if click_price:
                    OTA_data = loop_fill_date(page, hotel_name, CheckinDates)  # Collect data for all dates
                    OTA_list.extend(OTA_data)  # Add to the main list

                print(f"Processed hotel {count_hotel}: {hotel_name}")
                
            except Exception as e:
                print(f"Error processing hotel {count_hotel}: {hotel_name}. Error: {e}")
        browser.close()
        save_data(OTA_list)

def loop_fill_date(page, hotel_name, CheckinDates):
    OTA_list = []  # Initialize an empty list to hold OTA data
    for checkin_date_str in CheckinDates:
        try:
            checkin_date = datetime.strptime(checkin_date_str, '%m/%d/%Y')

            # Calculate the check-out date (1 day after check-in)
            checkout_date = checkin_date + timedelta(days=1)
            # Format the dates for further use in the desired output format
            checkout_date_str = checkout_date.strftime('%d/%m/%Y')  # Format as 'dd/mm/yyyy'
            checkin_date_str = checkin_date.strftime('%d/%m/%Y')    # Format as 'dd/mm/yyyy'
            print(checkin_date_str, checkout_date_str)
            # Use the formatted dates as needed
            # For example, filling dates in a page
            fill_dates(page, checkin_date_str, checkout_date_str)
            page.keyboard.press("Enter")
            page.wait_for_load_state('domcontentloaded')
            
            OTA_dict = extract_ota_data(page, hotel_name, checkin_date_str, checkout_date_str)
            OTA_list.append(OTA_dict)  # Append each dictionary to the list
            
            print(f"Processed date: {checkin_date.strftime('%m/%d/%Y')}")
        except (ValueError, TypeError, AttributeError) as e:
            print(f"Error processing date: {checkin_date_str}. Error: {e}")

    return OTA_list  # Return the list of dictionaries


def read_checkin_dates(file_path):
    dates_list = []  # Initialize an empty list
    with open(file_path, mode='r') as file:  # Open the CSV file
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row if your CSV has one
        for row in csv_reader:  # Iterate over each row
            hotel_name = row[0]  # Extract hotel name
            checkin_date_str = row[1]  # Extract check-in date
            checkin_date = datetime.strptime(checkin_date_str, '%m/%d/%Y')  # Convert string to datetime
            checkout_date = checkin_date + timedelta(days=1)  # Calculate check-out date
            dates_tuple = (hotel_name, checkin_date.strftime('%m/%d/%Y'), checkout_date.strftime('%m/%d/%Y'))  # Convert to tuple
            dates_list.append(dates_tuple)  # Append tuple to the list
    return dates_list  # Return the list of tuples


def save_data(OTA_list):
    df = pd.DataFrame(OTA_list)
    df.to_excel('shoprateResult.xlsx', index=False) # Filepath of Shoprate Result here**
    


        
    

CheckinDates = [
    "9/25/2024",
    "9/26/2024",
    "9/27/2024",
    "9/28/2024",
    "9/29/2024",
    "10/23/2024",
    "10/24/2024",
    "10/25/2024",
    "10/26/2024",
    "10/27/2024",
    "11/20/2024",
    "11/21/2024",
    "11/22/2024",
    "11/23/2024",
    "11/24/2024",
    "12/12/2024",
    "12/13/2024",
    "12/14/2024",
    "12/30/2024",
    "12/31/2024",
    "1/24/2025",
    "1/25/2025",
    "1/28/2025",
    "1/29/2025",
    "1/30/2025",
    "2/12/2025",
    "2/13/2025",
    "2/14/2025",
    "2/15/2025",
    "2/16/2025"
]

# CheckinDates = [datetime.strptime(date, "%m/%d/%Y").strftime("%d/%m/%Y") for date in CheckinDates]

# CheckinDates=["12/31/2024"]
file_path = 'C:\\Users\\kusze\\Documents\\favstay\\shoprate\\shopratePKT.csv' # File path of Shoprate Input here**
if __name__ == '__main__':
    main(file_path,CheckinDates)
