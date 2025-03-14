import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_website(url):
    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        st.error(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract data (modify this part based on the website structure)
    data = []
    for item in soup.find_all('h2'):  # Example: extracting all <h2> tags
        title = item.get_text(strip=True)
        data.append({'Title': title})

    return data

def main():
    st.title("Web Scraper")
    
    # Prompt user for the website URL
    url = st.text_input("Enter the website URL to scrape:")

    if st.button("Scrape"):
        if url:
            # Scrape the website
            scraped_data = scrape_website(url)

            if scraped_data:
                # Convert the scraped data into a DataFrame
                df = pd.DataFrame(scraped_data)

                # Display the DataFrame
                st.write("### Scraped Data:")
                st.dataframe(df)

                # Save the DataFrame to a CSV file
                df.to_csv('scraped_data.csv', index=False)
                st.success("Data saved to 'scraped_data.csv'.")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()
