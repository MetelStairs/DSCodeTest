import pandas as pd

def ohlc_df_creator(input_data, freq_input, product):
    input_data.set_index(['TradeDateTime'], inplace=True)
    input_data.index = pd.to_datetime(input_data.index, dayfirst=True)

    # Renaming emissions so they are the same product like stated in the notes
    input_data['Product'] = input_data['Product'].str.replace('Emission - Venue B', 'Emission - Venue A')
    input_data['Product'] = input_data['Product'].str.replace('Emission - Venue A', 'Emission')

    # renaming the product if its emission to match with the data and also checks to see if the input is valid
    if product == "Emission - Venue B" or product == "Emission - Venue A":
        product = "Emission"
        print("Emission Selected")
    elif product == "Energy":
        print("Energy Selected")
    else:
        print("No valid product selection, please enter one of the following:")
        print("Emission - Venue B, Emission - Venue A or Energy")
        return

    # grab the data of only the desired product
    selected_product = input_data[input_data.Product == product]

    # saves all the unique contracts
    contracts = selected_product["Contract"].unique()
    contracts_dictionary = {}
    # loops for each unique contract
    for i in contracts:
        # i contract selected
        selected_product_contract = selected_product[selected_product.Contract == i]
        # different time frequencys have different start, 1D 0AM and the rest 7AM
        if freq_input == "1D":
            print(freq_input, " chosen")
            # Gets high of time frequency
            high = selected_product_contract['Price'].resample(freq_input).max().dropna()
            # Gets low of time frequency
            low = selected_product_contract['Price'].resample(freq_input).min().dropna()
            # Gets open of time frequency
            first = selected_product_contract['Price'].resample(freq_input).first().dropna()
            # gets close of time frequency
            last = selected_product_contract['Price'].resample(freq_input).last().dropna()
            # Gets quantity of time frequency
            quantity = selected_product_contract['Quantity'].resample(freq_input).sum().dropna()

        elif freq_input == "15MIN" or freq_input == "1H":
            print(freq_input, " chosen")
            selected_product_contract = selected_product_contract.between_time('7:00', '17:00')
            high= selected_product_contract['Price'].resample(freq_input, origin='07:00').max().dropna()
            low= selected_product_contract['Price'].resample(freq_input, origin='07:00').min().dropna()
            first= selected_product_contract['Price'].resample(freq_input, origin='07:00').first().dropna()
            last = selected_product_contract['Price'].resample(freq_input, origin='07:00').last().dropna()
            quantity = selected_product_contract['Quantity'].resample(freq_input, origin='07:00').sum().dropna()
            # Trims the quantiy between times otherwise fills time outside with 0's
            quantity = quantity.between_time('7:00', '17:00')
        else:
            print("No valid time was selected, please choose between: 15MIN, 1H or 1D")
            return

        # Merges all of the columns together
        final_products = pd.concat([first,high,low,last,quantity], axis=1)
        #  renames the col names
        final_products.columns = ['Open', 'High', 'Low', 'Close', 'Quantity']

        print(i, "Dataframe Created!")
        # saves the DF to a dictionary incase there are multiple DF's due to more than one contract
        contracts_dictionary[i] = final_products
    return contracts_dictionary

trade_data = pd.read_csv("DSCodeTest/Trades.csv")
# product choice
# Emission - Venue B
# Emission - Venue A
# Energy

product = "Emission - Venue A"

# input choice
# 15MIN
# 1H
# 1D
freq_input = "15MIN"

# Data gets ouputed as a dictionary to handle more than one contract
dataframe_for_candlegraph = ohlc_df_creator(trade_data, freq_input.upper(), product)

