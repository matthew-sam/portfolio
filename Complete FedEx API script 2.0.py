import pantab
import pandas as pd
import requests
import tableauserverclient as TSC
from tableauhyperapi import HyperProcess, Connection, Telemetry, TableDefinition, SqlType
from concurrent.futures import ThreadPoolExecutor

def insert_api_column_all(df):
    # Filter rows based on conditions
    filtered_df = df[(df['Company'] == 'RDA') & ((df['Carrier_Name'] == 'FED.EX FREIGHT') | (df['Carrier_Name'] == 'FEDERAL EXPRESS (PARCEL)'))]

    # Extract tracking numbers
    tracking_numbers = filtered_df['Delivery_Tracking_Num'].tolist()


    # Batch size 
    batch_size = 30

    # Initialize a list to store batches of tracking numbers
    tracking_batches = []

    # Iterate through the tracking column and create batches
    for i in range(0, len(tracking_numbers), batch_size):
        batch = tracking_numbers[i:i + batch_size]
        tracking_batches.append(batch)

    # Calculate the total number of batches
    total_batches = len(tracking_batches)

    # Divide the batches into three groups (batch_group_1, batch_group_2, and batch_group_3)
    batch_group_1 = tracking_batches[:total_batches // 4]
    batch_group_2 = tracking_batches[total_batches // 4: 2 * (total_batches // 4)]
    batch_group_3 = tracking_batches[2 * (total_batches // 4): 3 * (total_batches // 4)]
    batch_group_4 = tracking_batches[3 * (total_batches // 4):]



    # Function to get authorization
    def getBearerAuthorization():
        url = "https://apis.fedex.com/oauth/token"
        payload = " " # pulled from FedEx Developer site
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(url, data=payload, headers=headers)

        if response.status_code == 200:
            authorization = response.json()["access_token"]
            return authorization
        else:
            raise Exception(f"Authorization request failed with status code {response.status_code}")
    
    # Function to make the API request for a set of tracking numbers
    def make_api_request(tracking_numbers, token, url):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        }

        payload = {
            "trackingInfo": [
                {
                    "trackingNumberInfo": {
                        "trackingNumber": num 
                    }
                }
                for num in tracking_numbers
            ],
            "includeDetailedScans": True
        }

        response = requests.post(url, json=payload, headers=headers)

        # List to store estimated delivery dates
        est_delivery_dates = []

        if response.status_code == 200:
            try:
                # Parse the JSON response
                data = response.json()
            
                # Process the tracking information for each tracking number in the response
                for complete_track_result in data["output"]["completeTrackResults"]:
                    for track_result in complete_track_result["trackResults"]:
                        est_delivery_date = None
                    
                        # Process the date and times for the tracking number
                        # est delivery exist only when package is in transit
                        for event in track_result.get("dateAndTimes", []):
                            if event["type"] == "ESTIMATED_DELIVERY":
                                est_delivery_date = event["dateTime"]
                                break
                            elif event["type"] == "ACTUAL_DELIVERY":
                                est_delivery_date = event["dateTime"]
                                break
                                            
                        # Append the estimated delivery date or "Missing Info" to the list
                        est_delivery_dates.append(est_delivery_date or "Missing Info")
                    
            except KeyError:
                est_delivery_dates.append("Data structure not as expected") 
            
        else:
            est_delivery_dates.append(f"API request failed with status code {response.status_code}")

        return est_delivery_dates  # Return the list of estimated delivery dates

    # Function to make 4 api request at once
    def make_api_requests_batch_group(batch_group, token, url):
        results = []
        for tracking_numbers in batch_group:
            est_delivery_dates = make_api_request(tracking_numbers, token, url)
            results.append(est_delivery_dates)
        return results



    # Variables and Parameters
    token = getBearerAuthorization()
    url = "https://apis.fedex.com/track/v1/trackingnumbers"

    # List to store results for all sets
    all_est_delivery_dates = []

    

    with ThreadPoolExecutor(max_workers=4) as executor:
        results_batch_group_1 = executor.submit(make_api_requests_batch_group, batch_group_1, token, url)
        results_batch_group_2 = executor.submit(make_api_requests_batch_group, batch_group_2, token, url)
        results_batch_group_3 = executor.submit(make_api_requests_batch_group, batch_group_3, token, url)
        results_batch_group_4 = executor.submit(make_api_requests_batch_group, batch_group_4, token, url)

    # Get the results when needed
    all_est_delivery_dates.extend(results_batch_group_1.result())
    all_est_delivery_dates.extend(results_batch_group_2.result())
    all_est_delivery_dates.extend(results_batch_group_3.result())
    all_est_delivery_dates.extend(results_batch_group_4.result())
    

    
    # Flatten the result list
    result_dates = [date for sublist in all_est_delivery_dates for date in sublist]

    # Initialize an index for tracking result_dates
    result_index = 0

    # Loop through each row in the filtered DataFrame
    for index, row in filtered_df.iterrows():
        if result_index < len(result_dates):
            df.loc[index, 'result'] = result_dates[result_index]
            result_index += 1
        else:
            # Handle the case where there are no more results
            df.loc[index, 'result'] = 'No more results from API'

    # If there are remaining results, you can store them in a separate list or handle them differently
    remaining_results = result_dates[result_index:]

    # Fill in the remaining rows with 'Not a FedEX Tracking Number'
    df.loc[df['result'].isna(), 'result'] = 'Not a FedEX Tracking Number'

    # Display the final DataFrame
    return df





# test to see if function works out
# get table name (for some reason writing in 'Extract' directly doesn't work)
def get_table_names_from_hyper(hyper_file_path):
    with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(endpoint=hyper.endpoint, database=hyper_file_path) as connection:
            schema_names = connection.catalog.get_schema_names()
            table_names = []

            for schema_name in schema_names:
                tables_in_schema = connection.catalog.get_table_names(schema=schema_name)
                table_names.extend(tables_in_schema)

    return table_names

# call hyper file
hyper_file_path = 'C:\\Users\\matthew.sam\\Downloads\\Python\\FedEx API\\Data\\Extracts\\Sales_Order _sagex3_.hyper'
all_table_names = get_table_names_from_hyper(hyper_file_path)

# Select a specific table name from the list which is just 'Extract'
table_name = all_table_names[0] 

# Read data from the Hyper file into a DataFrame using the selected table name
df = pantab.frame_from_hyper(hyper_file_path, table=table_name)#.query('Company=="RDA" and Carrier_Name=="FED.EX FREIGHT"').head(100)

print(insert_api_column_all(df))
