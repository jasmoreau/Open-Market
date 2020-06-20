
def get_ID(ctx):
    return f'{str(ctx.guild.id) + str(ctx.message.author.id)}ID'

def get_balance(ctx, c):
    return c.execute("""SELECT bal FROM user WHERE id=?""", (get_ID(ctx),)).fetchone()

def append_stock(ctx, stock, c):
    import json
    record = c.execute("""SELECT stock FROM user WHERE id=?""",(get_ID(ctx),)).fetchone()
    trades = json.loads(str(record))
    trades["trade"].append(stock)
    trades = json.dumps(trades)

    #for ele in trades['trade']:
    #    print(ele)

    return trades
