def get_ID(ctx):
    return f'{str(ctx.guild.id) + str(ctx.message.author.id)}ID'

def get_balance(ctx):
    return c.execute(f'SELECT bal FROM user WHERE id = {get_ID(ctx)}').fetchone()

def addition(num1, num2):
    return num1 + num2
