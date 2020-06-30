# Open-Market
Welcome to Open Market! A discord stock market game.

This bot allows you to purchase, sell, and view stocks with a virtual balance.

Data is pulled from Finnhub API (Need your Finnhub token and Discord bot token)

## How to Use
Calling .init will initialize you to the game.

**.setdaily [amount]** (must have StockMaster role) sets daily reward amount (defaults to $100)

**.getdaily** gives you the set reward every 24 hours

**.bal** shows your balance

**.buy [stock symbol] [quantity]** purchases a stock

**.sell [stock symbol] [quantity]** sells a stock

**.stock [stock symbol]** gets current value of a stock

**.info [stock symbol] [days]** shows you important information about a stock from the past number of days

**.graph [stock symbol] [days]** graphs stock history that many days back

**.hist [number]** shows the last number of transactions


### Dependencies (If you want to clone the bot)
[Discord.py](https://github.com/Rapptz/discord.py)

[Finnhub API](https://github.com/Finnhub-Stock-API/finnhub-python)

[Dotenv](https://pypi.org/project/python-dotenv/)

[Requests](https://pypi.org/project/requests/)

[Pandas](https://pandas.pydata.org/)

[MatPlotLib](https://matplotlib.org/)

