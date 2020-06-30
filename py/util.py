
def get_ID(ctx):
    return f'{str(ctx.guild.id) + str(ctx.message.author.id)}ID'

def get_balance(ctx, c):
    return round(c.execute("""SELECT bal FROM user WHERE id=?""", (get_ID(ctx),)).fetchone(),2)

def get_prefix(ctx, c):
    print(c.execute("""SELECT prefix FROM server WHERE id=?""", (str(ctx.guild.id),)).fetchone())
    return c.execute("""SELECT prefix FROM server WHERE id=?""", (str(ctx.guild.id),)).fetchone()

def append_stock(ctx, stock, c):
    import json
    record = c.execute("""SELECT stock FROM user WHERE id=?""",(get_ID(ctx),)).fetchone()
    trades = json.loads(str(record))
    trades["trade"].append(stock)
    trades = json.dumps(trades)
    return trades


def check_initialization(ctx, c):
    if get_ID(ctx) in str(c.execute(f'SELECT id FROM user').fetchall()): #checking if user is already in database
        return False
    return True

def check_24h(ctx, c, conn):
    from datetime import datetime, timedelta

    NUMBER_OF_SECONDS = 86400 # seconds in 24 hours
    first = str(c.execute("""SELECT time FROM user WHERE id=?""", (get_ID(ctx),)).fetchone()).replace("-", " ").replace(":", " ").replace(".", " ")
    first = datetime.strptime(first, "%Y %m %d %H %M %S %f")
    second = datetime.now()
    if (second - first).total_seconds() > NUMBER_OF_SECONDS: #finds difference between last claim and current
      c.execute(f'UPDATE user SET time = "{str(second)}" WHERE id = "{get_ID(ctx)}"')
      conn.commit()
      return False #False when 24 hours has passed
    else:
        time = (timedelta(seconds=((second-first).total_seconds())))
        time -= timedelta(microseconds=time.microseconds)
        remaining_time = timedelta(days=1)-time
        return remaining_time

def total_stocks(ctx, c, stock):
    import json
    record = c.execute("""SELECT stock FROM user WHERE id=?""", (get_ID(ctx),)).fetchone()
    trades = json.loads(str(record))
    trade = trades["trade"]
    total = 0
    for ele in trade:
        if stock == ele["id"]:
            total += ele["quantity"]
    return total

def total_stock_cost(ctx, c, stock):
    import json
    record = c.execute("""SELECT stock FROM user WHERE id=?""", (get_ID(ctx),)).fetchone()
    trades = json.loads(str(record))
    trade = trades["trade"]
    total = 0
    for ele in trade:
        if stock == ele["id"]:
            total += ele["totalPurchase"]
    return total

def check_not_role(ctx):
    if "StockMaster" in ctx.author.roles:
        return False
    return True

def print_history(ele):
        if ele["quantity"] > 0:
            return f"Bought {ele['quantity']} share(s) of {ele['id']} for ${ele['totalPurchase']}. ({ele['id']}: ${ele['currentMarket']})" + "\n"
        else:
            return f"Sold {ele['quantity']} share(s) of {ele['id']} for ${ele['totalPurchase']}. ({ele['id']}: ${ele['currentMarket']})" + "\n"

def is_integer(n):
    try:
        int(n)
        return True
    except ValueError:
        return False
