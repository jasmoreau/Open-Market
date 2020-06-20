
def get_ID(ctx):
    return f'{str(ctx.guild.id) + str(ctx.message.author.id)}ID'

def get_balance(ctx, c):
    return c.execute("""SELECT bal FROM user WHERE id=?""", (get_ID(ctx),)).fetchone()

def get_prefix(ctx, c):
    print(c.execute("""SELECT prefix FROM server WHERE id=?""", (str(ctx.guild.id),)).fetchone())
    return c.execute("""SELECT prefix FROM server WHERE id=?""", (str(ctx.guild.id),)).fetchone()

def append_stock(ctx, stock, c):
    import json
    record = c.execute("""SELECT stock FROM user WHERE id=?""",(get_ID(ctx),)).fetchone()
    print(record)
    print(str(record))
    trades = json.loads(str(record))
    trades["trade"].append(stock)
    trades = json.dumps(trades)

    #for ele in trades['trade']:
    #    print(ele)

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
    if (second - first).total_seconds() > NUMBER_OF_SECONDS:
      c.execute(f'UPDATE user SET time = "{str(second)}" WHERE id = "{get_ID(ctx)}"')
      conn.commit()
      return False #do something
    else:
        time = (timedelta(seconds=((second-first).total_seconds())))
        time -= timedelta(microseconds=time.microseconds)
        remaining_time = timedelta(days=1)-time
        return remaining_time
