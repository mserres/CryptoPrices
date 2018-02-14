import sys
import datetime
import urllib.request as ur
import json

def main(argv):

	tickers = ["BTC_USD", "ETH_USD", "LTC_USD", "IOTA_USD", "XRP_USD", "ZEC_USD", "DASH_USD"]
	exchanges = ["bitstamp", "bitfinex", "kraken", "cex.io", "anx"]

	alert = 0
	message = ""
	prices = []
	date = str(datetime.datetime.now())

	for ticker in tickers:
		for exchange in exchanges:
			prices.append(get_prices(exchange, ticker))

	message = message + date

	for i, ticker in enumerate(tickers):
		bid = []
		ask = []
		message = message + "\n\n" + ticker + "\n\n"

		for j, exchange in enumerate(exchanges):
			message = message + exchange + "[Bid, Ask]: " + str(prices[len(exchanges)*i+j]) + "\n"
			bid.append(float(prices[len(exchanges)*i+j][0]))
			ask.append(float(prices[len(exchanges)*i+j][1]))

		if round(100*((float(max(ask))/float(min(i for i in bid if i > 0)))-1), 3) > 8:
			alert = 1

		message = message + "\nBest Buy: " + exchanges[ask.index(min(i for i in ask if i > 0))] + " @ " + str(min(i for i in ask if i > 0)) + " " +\
				"Best Sell: " + exchanges[bid.index(max(bid))] + " @ " + str(max(bid)) + " " + \
				"Delta: " + str(round(float(max(bid)) - float(min(float(i) for i in ask if float(i) > 0)),3)) + " " + \
				"Ratio: %s%%" %round(100*((float(max(bid))/float(min(i for i in ask if i > 0)))-1), 3)

	print(message)
	print("")
	print("Alert: " + str(alert))
	print("")

	export_html(date, tickers, exchanges, prices)

	#if alert:
		#email_alert("Cryptocurrencies prices update", message)

def get_prices(exchange, ticker):

	url = 0

	if exchange == "bitstamp":
		if ticker == "BTC_USD":
			url = "https://www.bitstamp.net/api/v2/ticker/btcusd/"
		elif ticker == "ETH_USD":
			url = "https://www.bitstamp.net/api/v2/ticker/ethusd/"
		elif ticker == "LTC_USD":
			url = "https://www.bitstamp.net/api/v2/ticker/ltcusd/"
		elif ticker == "IOTA_USD":
			url = 0
		elif ticker == "XRP_USD":
			url = "https://www.bitstamp.net/api/v2/ticker/xrpusd/"
		elif ticker == "ZEC_USD":
			url = 0
		elif ticker == "DASH_USD":
			url = 0

	elif(exchange=="bitfinex"):
		if ticker == "BTC_USD":
			url = "https://api.bitfinex.com/v1/pubticker/btcusd"
		elif ticker == "ETH_USD":
			url = "https://api.bitfinex.com/v1/pubticker/ethusd"
		elif ticker == "LTC_USD":
			url = "https://api.bitfinex.com/v1/pubticker/ltcusd"
		elif ticker == "IOTA_USD":
			url = "https://api.bitfinex.com/v1/pubticker/iotusd"
		elif ticker == "XRP_USD":
			url = "https://api.bitfinex.com/v1/pubticker/xrpusd"
		elif ticker == "ZEC_USD":
			url = "https://api.bitfinex.com/v1/pubticker/zecusd"
		elif ticker == "DASH_USD":
			url = "https://api.bitfinex.com/v1/pubticker/dshusd"

	elif(exchange=="kraken"):
		if ticker == "BTC_USD":
			url = "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"
		elif ticker == "ETH_USD":
			url = "https://api.kraken.com/0/public/Ticker?pair=ETHUSD"
		elif ticker == "LTC_USD":
			url = "https://api.kraken.com/0/public/Ticker?pair=LTCUSD"
		elif ticker == "IOTA_USD":
			url = 0
		elif ticker == "XRP_USD":
			url = "https://api.kraken.com/0/public/Ticker?pair=XRPUSD"
		elif ticker == "ZEC_USD":
			url = "https://api.kraken.com/0/public/Ticker?pair=ZECUSD"
		elif ticker == "DASH_USD":
			url = "https://api.kraken.com/0/public/Ticker?pair=DASHUSD"

	elif exchange == "cex.io":
		if ticker == "BTC_USD":
			url = "https://cex.io/api/ticker/BTC/USD"
		elif ticker == "ETH_USD":
			url = "https://cex.io/api/ticker/ETH/USD"
		elif ticker == "LTC_USD":
			url = 0
		elif ticker == "IOTA_USD":
			url = 0
		elif ticker == "XRP_USD":
			url = "https://cex.io/api/ticker/XRP/USD"
		elif ticker == "ZEC_USD":
			url = "https://cex.io/api/ticker/ZEC/USD"
		elif ticker == "DASH_USD":
			url = "https://cex.io/api/ticker/DASH/USD"

	elif exchange == "anx":
		if ticker == "BTC_USD":
			url = "https://anxpro.com/api/2/btcusd/money/ticker"
		elif ticker == "ETH_USD":
			url = 0
		elif ticker == "LTC_USD":
			url = 0
		elif ticker == "IOTA_USD":
			url = 0
		elif ticker == "XRP_USD":
			url = 0
		elif ticker == "ZEC_USD":
			url = 0
		elif ticker == "DASH_USD":
			url = 0

	data = ['0', '0']

	if url:
		opener = AppURLopener()

		try:
			response = opener.open(url).read()

			if exchange == "bitstamp":
				data = [json.loads(response)['bid'], json.loads(response)['ask']]
			elif(exchange=="bitfinex"):
				data = [json.loads(response)['bid'], json.loads(response)['ask']]
			elif(exchange=="kraken"):
				if ticker == "BTC_USD":
					name = "XXBTZUSD"
				elif ticker == "ETH_USD":
					name = "XETHZUSD"
				elif ticker == "LTC_USD":
					name = "XLTCZUSD"
				elif ticker == "XRP_USD":
					name = "XXRPZUSD"
				elif ticker == "ZEC_USD":
					name = "XZECZUSD"
				elif ticker == "DASH_USD":
					name = "DASHUSD"
				data = [json.loads(response)['result'][name]['b'][0], json.loads(response)['result'][name]['a'][0]]
			elif exchange == "cex.io":
				data = [json.loads(response)['bid'], json.loads(response)['ask']]
			elif exchange == "anx":
				data = [json.loads(response)['data']['buy']['value'], json.loads(response)['data']['sell']['value']]

			data = [float(i) for i in data]
			data = ['%.3f' % point for point in data]

		except Exception as e:
			print(str(e))
			pass

	return data

class AppURLopener(ur.FancyURLopener):
    version = "Mozilla/5.0"

def export_html(date, tickers, exchanges, prices):
	output = open("../web/prices/exchanges-prices.html", 'w')
	output.truncate()
	output.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta name="HandheldFriendly" content="true">
<title>Exchanges Prices</title>
<link rel="stylesheet" type="text/css" href="stylesheets/page.css" />
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">

	google.charts.load('current', {'packages':['table']});
	google.charts.setOnLoadCallback(drawTable);

	function drawTable() {
		var data = new google.visualization.DataTable();
		data.addColumn('string', 'Pair');
		data.addColumn('string', 'Exchange');
		data.addColumn('number', 'Bid');
		data.addColumn('number', 'ask');
		data.addRows([""")

	message = []

	for i, ticker in enumerate(tickers):

		bid = []
		ask = []

		for j, exchange in enumerate(exchanges):

			bid.append(float(prices[len(exchanges) * i + j][0]))
			ask.append(float(prices[len(exchanges) * i + j][1]))

			if float(prices[len(exchanges) * i + j][0]) > 0:
				output.write("['" + ticker + "', '" + exchange + "', " + str(prices[len(exchanges) * i + j][0]) + ", " + str(prices[len(exchanges) * i + j][1]) + "]," + "\n")

		message.append(ticker + " Buy: " + exchanges[ask.index(min(i for i in ask if i > 0))] + " @ " + str(
			min(i for i in ask if i > 0)) + " " + \
				  "Sell: " + exchanges[bid.index(max(bid))] + " @ " + str(max(bid)) + " " + \
				  "Delta: " + str(round(float(max(bid)) - float(min(float(i) for i in ask if float(i) > 0)), 3)) + " " + \
				  "Ratio: %s%%" % round(100 * ((float(max(bid)) / float(min(i for i in ask if i > 0))) - 1), 3))

	output.write("""]);

		var formatter = new google.visualization.NumberFormat({negativeColor: 'red', negativeParens: true, pattern: '###,##0.000'});
		formatter.format(data, 2); 
		formatter.format(data, 3); 

		// var percentage = new google.visualization.NumberFormat({suffix: '%', negativeColor: 'red', negativeParens: true, fractionDigits: 0, pattern: '###,##0.00'});
		// percentage.format(data, 4); 

		var table = new google.visualization.Table(document.getElementById('table_div'));

		table.draw(data, { 'width': '100%' });
		// table.draw(data);
	}

	</script>

</head>

<body bgcolor="#FFFFFF">

<!-- HEADER -->
<table class="head-wrap" bgcolor="#FFFFFF   ">
	<tr>
		<td></td>
		<td class="header container" >

				<div class="content">
				<table bgcolor="#FFFFFF">
					<tr>
						<td><img src="images/bitfolios-logo.png" /></td>
						<td align="right"><h6 class="collapse">Welcome back!</h6></td>
					</tr>
				</table>
				</div>
		</td>
		<td></td>
	</tr>
</table><!-- /HEADER -->


<!-- BODY -->
<table class="body-wrap">
	<tr>
		<td></td>
		<td class="container" bgcolor="#FFFFFF">

		<div class="content">
		<table>
			<tr>
				<td align="center">""")
	output.write("Exchange Prices")
	output.write("""</td>
			</tr>
			<tr>
				<td align="center">Last update: """)

	output.write(date)
	output.write(""" UTC</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td><div id="table_div"></div></td>
			</tr>
			<tr>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>""")

	for m in message:
		output.write("<p>" + m + "</p>\n")

	output.write("""</td>
			</tr>
		</table>
		</div><!-- /content -->

		</td>
		<td></td>
	</tr>
</table><!-- /BODY -->

<!-- FOOTER -->
<table class="footer-wrap">
	<tr>
		<td></td>
		<td class="container">

				<!-- content -->
				<div class="content">
				<table>
				<tr>
					<td align="center">
					</td>
				</tr>
			</table>
				</div><!-- /content -->

		</td>
		<td></td>
	</tr>
</table><!-- /FOOTER -->

</body>
</html>""")
	output.close()


if __name__ == "__main__":
	main(sys.argv[1:])