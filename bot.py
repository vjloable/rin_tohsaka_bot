#Imports
import os														#OS
import sys														#SYSTEM
import traceback												#TRACEBACK
import time														#TIME
import asyncio													#ASYNCIO
import discord													#DISCORD API
from discord.ext import commands
bot = commands.Bot(command_prefix='r!')
import psycopg2													#DATABASE HANDLING
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
DEV = os.environ['DEV']

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ CORE EVENTS ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
@bot.event
async def on_command_error(msg, error):
	if isinstance(error, commands.CommandOnCooldown):
		await msg.send(":clock5: | **COOLDOWN: Retry again in {:.2f}s.**".format(error.retry_after))
		return

@bot.event
async def on_ready():
	print('Logged in as...')
	print("Bot:",bot.user.name)
	print("User_ID:",bot.user.id)
	print("Connection >> ", conn)
	print('Changing presence...')
	await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name='with Daddy'))

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ COGS ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
extensions = ['cogs.economy']

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ STANDARD COMMANDS ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def now(msg):
	clt = time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime())
	await msg.send("```python\n['SERVER TIME']\n\nAsia/Manila UTC +08:00\n#>\t{}```".format(clt))
'''
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def daily(msg):
	user = "'%"+str(msg.author.id)+">%';"
	cur.execute("SELECT isDailyClaimed FROM kidz WHERE usr_id LIKE "+(user))
	claim_status = bool((cur.fetchall())[0][0])
	if claim_status:
		gmt = time.localtime()
		hrs, mins, secs = 23 - gmt[3], 59 - gmt[4], 59 - gmt[5]
		''
		if hrs == 1:
			hrs = "**1 hour**"
		if mins == 1:
			mins = "**1 minute**"
		if secs == 1:
			secs = "**1 second**"
		''
		#WRITE CODE HERE
		await msg.send(":gift: | **{}**, you still have to wait {}, {} and {} for your next daily reward.".format(msg.author.name,hrs,mins,secs))
	else:
		cur.execute("UPDATE kidz SET isDailyClaimed = true WHERE usr_id LIKE "+(user))
		cur.execute("SELECT mono FROM kidz WHERE usr_id LIKE "+(user))
		money = int((cur.fetchall())[0][0])
		cur.execute("UPDATE kidz SET mono = {} WHERE usr_id LIKE ".format(money + 50)+(user))
		await msg.send(":gift: | **{}**, you received :yen: 50 credits.".format(msg.author.name))
	conn.commit()
'''
@bot.command()
async def wallet(msg, user:str=None):
	money = 0;
	if user is None:
		newuser = "'%"+str(msg.author.id)+">%';"
		cur.execute("SELECT mono FROM kidz WHERE usr_id LIKE "+(newuser))
		money = int((cur.fetchall())[0][0])
	else:
		user = "'%"+(user)[3:-1]+"%';"
		cur.execute("SELECT mono FROM kidz WHERE usr_id LIKE "+(user))
		money = int((cur.fetchall())[0][0])

	if money == 0:
		await msg.send(":credit_card: | **Wallet is empty**")
	elif money == 1:
		await msg.send(":credit_card: | **{:s} credit**".format(str(money)))
	else:
		await msg.send(":credit_card: | **{:s} credits**".format(str(money)))
	conn.commit()

@bot.command()
async def myid(msg):
	args = str(msg.message.content).split()
	await msg.send(msg.author.id)
	print((str(args[1]))[3:-1])

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def greet(msg):
	await msg.send(":smiley: :wave: Hello, there!")

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ DEV COMMANDS ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
@bot.command()
async def access(msg):
	if(msg.author.id == int(DEV)):
		await msg.send(":white_check_mark: ACCESS GRANTED :white_check_mark:")
		print("-=-=-ACCESS GRANTED-=-=-")

		try:
			cur.execute("SELECT * FROM kidz;")
			dataset = (cur.fetchall())
			embed = discord.Embed(title="|| BANK ACCOUNTS", color=0xff2020)
			for tag, data in enumerate(dataset):
				embed.add_field(name="[ "+(str(tag+1))+" ] - UserID: "+str(data[1])+"", value="Money: "+str(data[2]), inline=False)
			await msg.send(embed=embed)
			conn.commit()
		except psycopg2.InternalError:
			#conn.rollback()
			pass
	else:
		await msg.send(":no_entry: ACCESS DENIED :no_entry:")
		print("-x-x-ACCESS DENIED-x-x-")
		pass

@bot.command()
async def create(msg):
	if(msg.author.id == int(DEV)):
		await msg.send(":white_check_mark: ACCESS GRANTED :white_check_mark:")
		print("-=-=-ACCESS GRANTED-=-=-")
		try:
			args = str(msg.message.content).split(" ")[1:]
			usr, val = str(args[0]), int(args[1])
			cur.execute("INSERT INTO kidz (usr_id, mono) VALUES (%s, %s);",(usr, val))
			print("\nINSERTED the VALUES INTO TABLE kidz...")
			print("UserID:",usr," | Value:",str(val),"\n")
			conn.commit()
		except psycopg2.IntegrityError:
			await msg.send(":lock: | Username already exists. Try again")
			conn.rollback()
			pass
	else:
		await msg.send(":no_entry: ACCESS DENIED :no_entry:")
		print("-x-x-ACCESS DENIED-x-x-")
		pass

@bot.command()
async def test(msg):
	if(msg.author.id == int(DEV)):
		await msg.send(":white_check_mark: ACCESS GRANTED :white_check_mark:")
		print("-=-=-ACCESS GRANTED-=-=-")
		TZ = os.environ['TZ']
		time.tzset()
		await msg.send(time.localtime())
		cur.execute("SELECT * FROM kidz;")
		await msg.send((cur.fetchall()))	
	else:
		await msg.send(":no_entry: ACCESS DENIED :no_entry:")
		print("-x-x-ACCESS DENIED-x-x-")
		pass

BOT_TOKEN = os.environ['BOT_TOKEN']
bot.run(BOT_TOKEN)
