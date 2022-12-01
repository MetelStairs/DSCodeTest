import pandas as pd

def ohlc_df_creator(trade_data, freq_input):
    trade_data.set_index(['TradeDateTime'], inplace=True)
    trade_data.index = pd.to_datetime(trade_data.index, dayfirst=True)

    trade_data['TradeDateTime'] = pd.to_datetime(trade_data['TradeDateTime'].dt.strftime("%m/%d")
    trade_data.set_index(['TradeDateTime'], inplace=True)

    # Renaming emissions so they are the same product like stated in the notes
    trade_data['Product'] = trade_data['Product'].str.replace('Emission - Venue B', 'Emission - Venue A')
    trade_data['Product'] = trade_data['Product'].str.replace('Emission - Venue A', 'Emission')

    resampled_data = trade_data['Price'].resample(freq_input, origin='07:00').ohlc(_method='ohlc')
    return

trade_data = pd.read_csv("DSCodeTest/Trades.csv")

freq_input = "15Min"

ohlc_df_creator(trade_data, freq_input)

#input for user is freq and products
# if user chooses 1d then use all time else get rid of anything other than 7-15
# remove all other products and then make new dataframe for each unique contract