#Imports
import os                                                       #OS lib
import time														#TIME
import discord                                                  #DISCORD API lib
from discord.ext import commands
bot = commands.Bot(command_prefix='r!')
import psycopg2													#DATABASE HANDLING
DATABASE_URL = os.environ['DATABASE_URL']                   
conn = psycopg2.connect(DATABASE_URL, sslmode='require')    
cur = conn.cursor()

@bot.event
async def on_command_error(msg, error):
	if isinstance(error, commands.CommandOnCooldown):
		await msg.send(":clock5: | **COOLDOWN: Retry again in {:.2f}s.**".format(error.retry_after))
		await msg.message.edit(delete_after = error.retry_after)
		return

@bot.event
async def on_ready():
	print('Logged in as...')
	print("Bot:",bot.user.name)
	print("User_ID:",bot.user.id)
	print("conn = ", conn)
	print('Changing presence...')
	await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name='with Daddy'))

@bot.command()
async def now(msg):
	dnt = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
	await msg.send("```python\n['SERVER TIME']\n\nAtlantic/Azores +00:00\n#>\t{}```".format(dnt))

@bot.command()
async def auth(msg, user):
	await msg.send(user.name)

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
async def create(msg):
	if(msg.author.id == 336068309789310979):
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
async def myid(msg):
	args = str(msg.message.content).split()
	await msg.send(msg.author.id)
	print((str(args[1]))[3:-1])

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def greet(msg):
	await msg.send(":smiley: :wave: Hello, there!")

@bot.command()
async def access(msg):
	if(msg.author.id == 336068309789310979):
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
BOT_TOKEN = os.environ['BOT_TOKEN']
bot.run(BOT_TOKEN)