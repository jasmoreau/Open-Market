from main import *

print(addition(2,2))
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

    @commands.command()
    async def init(self, ctx):
        #print("BRUH")
        #print(c.execute(f'SELECT bal FROM user WHERE id = {get_ID(ctx)}').fetchone())
        if get_ID(ctx) in str(c.execute(f'SELECT id FROM user').fetchall()): #checking if user is already in database
            await ctx.send("User already initialized")
            return
        c.execute(f"INSERT INTO user VALUES ('{get_ID(ctx)}', 100000, '', '')") #adding user to database
        conn.commit()
        await ctx.send(f"You can now play! Starting balance: {get_balance(ctx)}")

    @commands.command()
    async def buy(self, ctx, stock: str, num: float):
        stock = stock.upper()
        current_price = finnhub_client.quote(stock).c #get the current price of a stock
        if current_price <= 0:
            await ctx.send("Stock does not exist. Try again!")
            return
        await ctx.send(f'Buy {num} share(s) of {stock} for {current_price}? Reply with y/n')
        msg = await bot.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author) #checks if user replies with yes or no
        if msg.content.lower().startswith("y"):
            c.execute(f"INSERT INTO user VALUES ({get_ID(ctx)})")
            conn.commit()
            await ctx.send(f"Purchased {num} share(s) of {stock} for {current_price}")
        else:
            await ctx.send("Purchase cancelled")

def setup(bot):
    bot.add_cog(cmd(bot))
