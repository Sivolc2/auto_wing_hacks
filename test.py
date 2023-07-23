import openpyxl
from langchain.utilities import GoogleSerperAPIWrapper

import os


def search_product_to_excel(product, file_name):
    
    # Initialize API wrapper
    search = GoogleSerperAPIWrapper()
    
    # Get search results
    results = search.results(product)
    
    # Extract product info
    product_info = {}
    if 'knowledgeGraph' in results:
        knowledge_graph = results['knowledgeGraph']
        product_info['Title'] = knowledge_graph['title']
        product_info['Description'] = knowledge_graph['description']
        product_info['Description Source'] = knowledge_graph['descriptionSource']
        
    # Save to Excel        
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = 'Title'
    sheet['B1'] = 'Description' 
    sheet['C1'] = 'Description Source'
    sheet.append([product_info.get('Title'), 
                  product_info.get('Description'),
                  product_info.get('Description Source')])
    wb.save(file_name)

product = "iPhone 14" 
file_name = "iphone14_info.xlsx"

search_product_to_excel(product, file_name)





# with tabs[1]:
#     products = st.text_input("Enter comma-separated list of products")
    
#     if products:
#         products = [p.strip() for p in products.split(",")]

#         for product in products:
#             st.header(product)

#             # Get the result from the agent
#             # result = mrkl.run(product, tool="Search Google")

#             # result = mrkl.run(tool="Search Google")
#             result = mrkl.run(f"What are some options to buy {product}?", "SearchG")
#             # Assume result is a list of dictionaries for this example
#             df = pd.DataFrame(result)

#             # Summarize the data as required (this step depends on the structure and nature of your data)
#             # df = df.groupby(...).sum()  # Example summarization
            
#             file_name = f"{product.replace(' ','_')}.xlsx"

#             # Save to Excel
#             df.to_excel(file_name, index=False)

#             # Display the DataFrame
#             st.dataframe(df)

#             # Provide download link
#             st.download_button(
#                 label="📥 Download Results",
#                 data=df.to_excel(index=False, engine='openpyxl'),
#                 file_name=file_name,
#                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#             )

# with tabs[2]:

#     # Streamlit configurations

#     # Environment setup
#     os.environ["MAPBOX_API_KEY"] = "YOUR_MAPBOX_ACCESS_TOKEN"

#     # Create geocoder and directions clients
#     geocoder = Geocoder(access_token=os.environ["MAPBOX_API_KEY"])
#     directions = Directions(access_token=os.environ["MAPBOX_API_KEY"])

#     # Get coordinates by address
#     def get_location_by_address(address):
#         response = geocoder.forward(address)
#         if response.status_code == 200:
#             coordinates = response.json()['features'][0]['geometry']['coordinates']
#             return coordinates[::-1]
#         else:
#             return None

#     # Shipping times
#     shipping_times = {
#         'Drop-ship': timedelta(hours=3),
#         'Next day': timedelta(days=1),
#         'Weekly': timedelta(weeks=1),
#     }

#     # Read the data
#     data = pd.read_excel('suppliers_data.xlsx')

#     # Add location data
#     data['location'] = data['Address'].apply(lambda x: get_location_by_address(x))
#     data[['latitude', 'longitude']] = pd.DataFrame(data['location'].tolist(), index=data.index)

#     # Zip Code Input from User
#     zip_code = st.text_input("Enter your zip code:")

#     # Fetch Top 3 suppliers based on ETA
#     if zip_code:
#         customer_location = get_location_by_address(zip_code)
#         data['Distance'] = data['location'].apply(lambda x: geopy.distance.distance(x, customer_location).miles)

#         for method, time_delta in shipping_times.items():
#             data[f'ETA_{method}'] = data['location'].apply(lambda x: calculate_eta(x, customer_location, method))

#         data_top3 = data.nsmallest(3, 'Distance')

#         # Tabs
#         list_tab, map_tab = st.tabs(["List View", "Map View"])

#         with list_tab:
#             list_tab.write(data_top3)

#         with map_tab:
#             # Map Visualization
#             view_state = pdk.ViewState(
#                 latitude=data_top3['latitude'].mean(),
#                 longitude=data_top3['longitude'].mean(),
#                 zoom=11,
#                 pitch=0)

#             layer = pdk.Layer(
#                 'ScatterplotLayer',
#                 data_top3,
#                 get_position='[longitude, latitude]',
#                 get_color='[200, 30, 0, 160]',
#                 get_radius=200,
#                 pickable=True)

#             r = pdk.Deck(
#                 layers=[layer],
#                 initial_view_state=view_state,
#                 tooltip={
#                     "text": "{Address}\nETA_Drop-ship: {ETA_Drop-ship}\nETA_Next day: {ETA_Next day}\nETA_Weekly: {ETA_Weekly}"
#                 })

#             map_tab.pydeck_chart(r)

