from main import *

class cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases=['setdaily'], pass_context=True)
    async def set_daily_reward(self, ctx, amount: float):
        daily_reward = format(amount, '.2f')
        c.execute(f"UPDATE server SET daily = {daily_reward} WHERE id = {ctx.guild.id}") #sets daily_reward variable for server in database
        conn.commit()
        await ctx.send(f"Set daily reward to  ${daily_reward}");

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
        #print("BRUH")
        #print(c.execute(f'SELECT bal FROM user WHERE id = {get_ID(ctx)}').fetchone())
        if check_initialization(ctx, c) == False:
            await ctx.send(f"You already initilized")
            return
        c.execute("""INSERT INTO user VALUES (?, 100000, '{"trade":[]}', '2020-01-1 00:00:00.00')""",(str(get_ID(ctx)),)) #adding user to database
        conn.commit()
        await ctx.send(f"You can now play! Starting balance: {get_balance(ctx, c)}")

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
        #"order": counter,
        loadedValue = {"id": stock, "quantity": num, "currentMarket": current_price, "totalPurchase": final_price}

        print((get_balance(ctx,c)))
        msg = await bot.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author) #checks if user replies with yes or no
        if msg.content.lower().startswith("y"):
            if get_balance(ctx, c) >= final_price:
                c.execute("""UPDATE user SET stock=?, bal=? WHERE id=?;""",(str(append_stock(ctx, loadedValue, c)), get_balance(ctx, c) - final_price,str(get_ID(ctx))))
                conn.commit()
                await ctx.send(f"Purchased {num} share(s) of {stock} for ${final_price}. ({stock}: ${current_price})")
            else:
                await ctx.send(f"Not enough funds. Missing ${final_price - get_balance(ctx,c)}")
        elif msg.content.lower().startswith("n"):
            await ctx.send("Purchase cancelled")
        else:
            await ctx.send("Wrong command")

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


def setup(bot):
    bot.add_cog(cmd(bot))
