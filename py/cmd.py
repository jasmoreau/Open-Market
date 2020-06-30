from main import *

class cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases=['setdaily'], pass_context=True)
    async def set_daily_reward(self, ctx, amount: float):
        if check_not_role(ctx):
            await ctx.send("Error: You do not have StockMaster role.")
            return
        daily_reward = format(amount, '.2f')
        c.execute(f"UPDATE server SET daily = {daily_reward} WHERE id = {ctx.guild.id}") #sets daily_reward variable for server in database
        conn.commit()
        await ctx.send(f"Set daily reward to  ${daily_reward}")

    @commands.command(aliases=['getdaily'])
    async def get_daily_reward(self, ctx):
        if check_initialization(ctx, c):
            await ctx.send(f"You need to {get_prefix(ctx, c)}init to initilize.")
            return
        if (check_24h(ctx, c, conn) == False):
            daily_reward = c.execute("""SELECT daily FROM server where id = ? """, (ctx.guild.id,)).fetchone()
            c.execute(f'UPDATE user SET bal = {get_balance(ctx, c)+daily_reward} WHERE id = "{get_ID(ctx)}"')
            conn.commit()
            await ctx.send(f"Daily reward of ${daily_reward}. Claim again in 24 hours. Balance: ${get_balance(ctx,c)}")
        else:
            await ctx.send(f"Has not been a day since you last claimed. Time remaining : {check_24h(ctx,c,conn)}")
        return

    @commands.command()
    async def init(self, ctx):
        if check_initialization(ctx, c) == False:
            await ctx.send(f"You are already initialized!")
            return
        c.execute("""INSERT INTO user VALUES (?, 100000, '{"trade":[]}', '2020-01-1 00:00:00.00')""",(str(get_ID(ctx)),)) #adding user to database
        conn.commit()
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name=f"User Initialized", value=f"""You can now play! Starting balance: {get_balance(ctx, c)}\n
        Call {get_prefix(ctx,c)}help for help getting started.""", inline=False)
        await ctx.send("", embed=embed)

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(color=0xff0000, url="https://github.com/jasmoreau/Open-Market")
        embed.add_field(name="Welcome to Open Market! A discord stock market game.",
        value=f"""Calling **{get_prefix(ctx,c)}init** will initialize you to the game.
        **{get_prefix(ctx,c)}setdaily [amount]** (must have StockMaster role) sets daily reward amount (defaults to $100).
        **{get_prefix(ctx,c)}getdaily** gives you the set reward every 24 hours
        **{get_prefix(ctx,c)}bal** shows your balance
        **{get_prefix(ctx,c)}buy [stock symbol] [quantity]** purchases a stock
        **{get_prefix(ctx,c)}sell [stock symbol] [quantity]** sells a stock
        **{get_prefix(ctx,c)}stock [stock symbol]** gets current value of a stock
        **{get_prefix(ctx,c)}info [stock symbol] [days]** shows you important information about a stock from the past number of days
        **{get_prefix(ctx,c)}graph [stock symbol] [days]** graphs stock history that many days back
        **{get_prefix(ctx,c)}hist [number]** shows the last number of transactions

        __Email m.jason77@gmail.com for help or error reporting.__
        [Github](https://github.com/jasmoreau/Open-Market)
        \nHave fun!
        """, inline=False)
        await ctx.send("", embed=embed)

    @commands.command()
    async def buy(self, ctx, stock: str, num: float):
        stock = stock.upper()
        current_price = round(finnhub_client.quote(stock).c,2) #get the current price of a stock
        final_price = round(current_price*num, 2)
        if check_initialization(ctx, c):
            await ctx.send(f"You need to {get_prefix(ctx, c)}init to initilize.")
            return
        if current_price == None:
            await ctx.send("Stock does not exist. Try again!")
            return
        await ctx.send(f'Buy {num} share(s) of {stock} for ${final_price}? ({stock}: ${current_price}) Reply with y/n')
        loadedValue = {"id": stock, "quantity": num, "currentMarket": current_price, "totalPurchase": final_price}

        msg = await bot.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author) #checks if user replies with yes or no
        if msg.content.lower().startswith("y"):
            if get_balance(ctx, c) >= final_price:
                c.execute("""UPDATE user SET stock=?, bal=? WHERE id=?;""",(str(append_stock(ctx, loadedValue, c)), get_balance(ctx, c) - final_price,str(get_ID(ctx))))
                conn.commit()
                await ctx.send(f"Purchased {num} share(s) of {stock} for ${final_price}. ({stock}: ${current_price})")
            else:
                await ctx.send(f"Not enough funds. Missing ${final_price - get_balance(ctx,c)}")
        else:
            await ctx.send("Purchase cancelled")

    @commands.command()
    async def sell(self, ctx, stock: str, num: float):
        stock = stock.upper()
        current_price = round(finnhub_client.quote(stock).c,2) #get the current price of a stock
        final_price = round(current_price*num, 2)
        if check_initialization(ctx, c):
            await ctx.send(f"You need to {get_prefix(ctx, c)}init to initilize.")
            return
        if current_price == None:
            await ctx.send("Stock does not exist. Try again!")
            return
        total = total_stocks(ctx,c,stock)
        if total < num:
            await ctx.send(f"You do not have enough shares. Your {stock} stock: {total}")
            return

        await ctx.send(f'Sell {num} share(s) of {stock} for ${final_price}? ({stock}: ${current_price}) Reply with y/n')
        loadedValue = {"id": stock, "quantity": (num*-1), "currentMarket": current_price, "totalPurchase": (-1)*final_price}

        msg = await bot.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author) #checks if user replies with yes or no
        if msg.content.lower().startswith("y"):
            c.execute("""UPDATE user SET stock=?, bal=? WHERE id=?;""",(str(append_stock(ctx, loadedValue, c)), get_balance(ctx, c) + final_price,str(get_ID(ctx))))
            conn.commit()
            runningSum = 0
            for ele in json.loads(c.execute("""SELECT stock FROM user WHERE id=?""",(get_ID(ctx),)).fetchone())["trade"]:
                if ele["id"] == stock:
                    runningSum += (ele["totalPurchase"])
            await ctx.send(f"Sold {num} share(s) of {stock} for ${final_price}. ({stock}: ${current_price}). Total profits/loss from {stock}: ${round(total_stocks(ctx,c, stock)*current_price - runningSum, 2)}")

        else:
            await ctx.send("Sale cancelled")

    @commands.command(aliases=['price', 'stock'])
    async def get_current_price(self, ctx, stock_name: str):
        stock_name = stock_name.upper()
        current_price = finnhub_client.quote(stock_name).c
        if current_price == None:
            await ctx.send("Stock does not exist. Try again!")
            return
        await ctx.send(f"Current price of {stock_name} is ${current_price}")

    @commands.command(aliases=['balance'])
    async def get_balance(self, ctx):
        if check_initialization(ctx, c):
            await ctx.send(f"You need to {get_prefix(ctx, c)}init to initilize.")
            return
        await ctx.send(f"Your balance is ${get_balance(ctx,c)}")
        return

    @commands.command(aliases=['hist'])
    async def get_history(self, ctx, temp="10"):
        if check_initialization(ctx, c):
            await ctx.send(f"You need to {get_prefix(ctx, c)}init to initilize.")
            return
        record = c.execute("""SELECT stock FROM user WHERE id=?""", (get_ID(ctx),)).fetchone()
        trades = json.loads(str(record))
        trade = trades["trade"]
        final = ""
        if is_integer(temp): #if .hist [int] then return the last [int] number of trades
            temp = int(temp)
            amount = temp
            if amount > len(trade):
                amount = len(trade)
            for num in range(amount,0,-1):
                ele = trade[(-1*num)]
                final += print_history(ele)
            await ctx.send(final)

        else: #if .hist [str] then return all history of stock
            stock = temp
            stock = stock.upper()
            for num in range(len(trade),0,-1):
                ele = trade[(-1*num)]
                if ele["id"] == stock:
                    final += print_history(ele)
            if len(final) == 0:
                await ctx.send(f"No history of {stock}. Make sure it is a number or a valid stock symbol.")
                return
            await ctx.send(final)

    @commands.command(aliases=['g', 'info'])
    async def graph(self, ctx, stock, day = 7):
        from dotenv import load_dotenv
        import requests
        import time
        import pandas as pd
        import json
        from datetime import datetime
        from matplotlib import pyplot as plt

        embed = discord.Embed(color=0xff0000)
        embed.add_field(name=f"Getting info over {stock.upper()}...", value="This may take a few seconds...", inline=False)
        await ctx.send("", embed=embed)
        t = day * 86400
        r = requests.get(f'https://finnhub.io/api/v1/stock/candle?symbol={stock}&resolution=1&from={int(time.time())-t}&to={int(time.time())}&format=json&token={os.getenv("FINNHUB_TOKEN")}')

        re = r.json()
        counter = 0
        arr = []
        for ele in re['t']:
            re['t'][counter] = str(datetime.utcfromtimestamp(ele).strftime('%Y-%m-%d-%H-%M-%S'))
            counter+=1

        stockdata_df = pd.DataFrame(re)
        plt.plot(stockdata_df['t'], stockdata_df['c'])
        plt.xlabel(f'Past {day} day(s)')
        plt.ylabel('Close Price')
        plt.title(f'{stock.upper()}')
        plt.savefig(f'{stock}{get_ID(ctx)}.png')

        file = discord.File(f"{stock}{get_ID(ctx)}.png", filename="image.png")
        embed=discord.Embed(color=0x007cdb)
        embed.set_image(url="attachment://image.png")
        embed.add_field(name=f"{stock.upper()} Stock History Past {day} day(s)",
            value=f"Last Closing Price: ${re['c'][-1]}\nChanged By: ${round(re['c'][-1] - re['c'][0], 2)} ({round(100*(re['c'][-1] - re['c'][0])/re['c'][0], 2)}%)\n{ctx.author.name}'s Change: ${round(total_stocks(ctx,c,stock)*re['c'][-1]-total_stock_cost(ctx, c, stock), 2)} ({round(100*(total_stocks(ctx,c,stock)*re['c'][-1]-total_stock_cost(ctx, c, stock))/total_stock_cost(ctx, c, stock), 2)}%)\nTotal Value of {ctx.author.name}'s {stock.upper()} Stocks: ${round(total_stocks(ctx,c,stock)*re['c'][-1], 2)} ({total_stocks(ctx,c,stock)} Shares)", inline=False)
        await ctx.send(file=file,embed=embed)

        return

def setup(bot):
    bot.add_cog(cmd(bot))
