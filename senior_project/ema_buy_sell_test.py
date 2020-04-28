import plotly.graph_objects as go
from plotly.offline import plot
import pandas as pd
import talib._ta_lib as ta
from datetime import datetime
import numpy

df = pd.read_csv('E:\\senior_project\\CEI_get_barset_data.csv')


#index = df.index
'''for i in range(len(df['time'])):
    df['time'][i] = df['time'][i].rsplit('-',1)[0]'''
    #print(i)


#print(df['time'])


df['ema5'] = ta.EMA(df['close'], timeperiod=5)
df['ema15'] = ta.EMA(df['close'], timeperiod=15)
df['ema40'] = ta.EMA(df['close'], timeperiod=40)

col_names = ['ema5/ema15','ema5/ema40','ema15/ema40', 'buy_signal', 'sell_signal']
new_df = pd.DataFrame(columns=col_names, index=[0])

buy_signals = []
sell_signals = []
for i in range(len(df['close'])):
	x = (df['ema5'][i]-df['ema15'][i])/df['ema15'][i]*100
	y = (df['ema5'][i]-df['ema40'][i])/df['ema40'][i]*100
	z = (df['ema15'][i]-df['ema40'][i])/df['ema40'][i]*100
	new_df.loc[i] = [x,y,z,False,False]
#new_df.to_csv('E:\senior_project\CEI_percentages.csv')
check_true = False

for i in range(1, len(df['close'])):
	if df['ema5'][i] > df['ema15'][i] and df['ema5'][i] > df['ema40'][i] and df['ema15'][i] > df['ema40'][i] and (df['ema5'][i] - df['low'][i]) > 0.03 * df['high'][i]: # TODO change the sell signal for better sells
		if check_true == True:
			print(f'{check_true}: {i}: sell is true')
			sell_signals.append([df.index[i], df['high'][i]])
			new_df.loc[i, 'sell_signal'] = True
			check_true = False
		else:
			continue

	if ((df['ema5'][i]-df['ema15'][i])/df['ema15'][i]*100) > 2 and ((df['ema5'][i]-df['ema40'][i])/df['ema40'][i]*100) < 4 and ((df['ema5'][i]-df['ema40'][i])/df['ema5'][i]*100) > 0.35 and df['ema5'][i] > df['ema40'][i] and ((df['ema15'][i]-df['ema40'][i])/df['ema40'][i]*100) < 0.5:
		if check_true == False:
			print(f'{check_true}: {i}: buy is true')
			buy_signals.append([df.index[i], df['low'][i]])
			new_df.loc[i, 'buy_signal'] = True
			check_true = True
		else:
			continue


#print(new_df.head(80))
new_df.to_csv('E:\\senior_project\\CEI_percentages.csv')

candle = go.Candlestick(
    x=df.index,
	open = df['open'],
	close = df['close'],
	high = df['high'],
	low = df['low'],
	name = "Candlesticks")
	# plot MAs
fema = go.Scatter(x=df.index,y = df['ema5'], name = "Fast EMA", line = dict(color = ('rgba(102, 255, 205, 50)')))
mema = go.Scatter(x=df.index,y = df['ema15'], name = "Medium EMA", line = dict(color = ('rgba(255, 255, 51, 50)')))
sema = go.Scatter(x=df.index,y = df['ema40'], name = "Slow EMA", line = dict(color = ('rgba(227, 66, 189, 50)')))
buys = go.Scatter(x=[item[0] for item in buy_signals], y=[item[1] for item in buy_signals],name = "Buy Signals",mode = "markers", fillcolor=('rgba(1, 255, 1, 50)')) # TODO make these the data frame varaibles and not the list
sells = go.Scatter(x=[item[0] for item in sell_signals], y=[item[1] for item in sell_signals], name='Sell Signals', mode='markers', fillcolor=('rgba(1, 1, 255, 50)'))

data = [candle, fema, mema, sema, buys, sells]

fig = go.Figure(data = data)

plot(fig)
#fig.write_html('E:\\senior_project\\buy_graph.html')

#print(df)