import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
import time

# Initialize the pytrends request
pytrends = TrendReq(hl='en-US', tz=360)

# Prompt the user to input keywords
keywords = input("Enter keywords separated by commas: ").split(',')

# Remove any leading/trailing whitespace from each keyword
keywords = [keyword.strip() for keyword in keywords]

# Build the payload with the keywords
pytrends.build_payload(keywords, cat=0, timeframe='today 5-y', geo='', gprop='')

# Sleep for a few seconds to avoid hitting rate limits
time.sleep(60)

# Get interest over time
data = pytrends.interest_over_time()

# Check if the data contains the necessary columns
if 'isPartial' in data.columns:
    data = data.drop(columns=['isPartial'])

# Plot the data
plt.figure(figsize=(14, 7))
for keyword in keywords:
    plt.plot(data.index, data[keyword], label=keyword)

# Customize the plot
plt.title('Google Trends Over Time')
plt.xlabel('Date')
plt.ylabel('Interest')
plt.legend(title='Keywords')
plt.grid(True)

# Display the plot
plt.show()