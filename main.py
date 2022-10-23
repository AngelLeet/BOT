from aiogram import Bot, Dispatcher, executor, types
from db.create_db_animal import db_animal
#from create_db_animal import db_animal
from db.create_db_food import db_food
from db.create_db_price import db_price, db_money_user, db_sell_price
from db.user_db_all import all_db
from db.screach_db import screach_db
from db.but_sell import sell_what
from life_time.chiken import chiken_life

import sqlite3
# function create db
db_animal()
db_food()
db_price()
db_sell_price()


# Initialize bot and dispatcher
bot = Bot(token='5411645313:AAHrjYA70qCo4oMlbkA10_AML_fLf4Xp1yc')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
	"""
	This handler will be called when user sends `/start` or `/help` command
	"""
	user_id = message.from_user.id
	all_db(user_id)
	db_money_user(user_id)
	await message.answer("хэй фермер тебе доступно 10000 рублей")

@dp.message_handler()
async def echo(message: types.Message):
	# old style:
	# await bot.send_message(message.chat.id, message.text)
	user_id = message.from_user.id
	if message.text.lower() == 'корова':
		info = 'cow'
		'''
		cur.execute("UPDATE animal SET cow=? WHERE userid=?", (cow, uId))
		conn.commit()
		cur.execute("INSERT INTO animal VALUES(?, ?);", animal)
		conn.commit()
		'''
		await message.answer(screach_db(user_id, info))
	elif message.text.lower() == 'купить корову':
		conn = sqlite3.connect('all.db')
		cur = conn.cursor()

		cur.execute("SELECT amount FROM cow WHERE id=:id", {"id": user_id})
		row = cur.fetchone()
		if row[0] == 0:
			cow_p = row[0] + 1
			cur.execute("UPDATE cow SET amount=? WHERE id=?", (cow_p, user_id))
			conn.commit()
		else:
			cow_p = row[0] + 1
			cur.execute("UPDATE cow SET amount=? WHERE id=?", (cow_p, user_id))
			conn.commit()
	elif message.text.lower() == 'купить курицу':

		#нужна функция покупки курицы, т.к. продажа уже реализована
		conn = sqlite3.connect('all.db')
		cur = conn.cursor()
		cur.execute("SELECT amount FROM chiken WHERE id=:id", {"id": user_id})
		row = cur.fetchone()
		if row[0] < 20:

			cur.execute("SELECT money_user FROM user_money WHERE id=:id", {"id": user_id})
			row_money = cur.fetchone()
			my_money = int(row_money[0])
			cur.execute("SELECT chiken FROM price_animal WHERE eda=:eda", {"eda": 'eda'})
			how = cur.fetchone()
			price_money = int(how[0])
			if my_money - price_money > 0:
				chiken_p = row[0] + 1
				remainder = my_money - price_money

				cur.execute("UPDATE user_money SET money_user=? WHERE id=?", (remainder, user_id))
				conn.commit()
				cur.execute("UPDATE chiken SET amount=? WHERE id=?", (chiken_p, user_id))
				conn.commit()
				life_time_chiken(user_id, 'chiken')
				await message.answer("остаток " +str(remainder)+ ": приобретена 1 курица")
		else:
			chiken_p = row[0] + 1
			cur.execute("UPDATE chiken SET amount=? WHERE id=?", (chiken_p, user_id))
			conn.commit()

	elif message.text.lower() == 'продать курицу':
		result = (sell_what('chiken', 0, user_id))
		chiken_info = screach_db(user_id, 'chiken')
		if result == None:
			await message.answer("у вас осталость 0 куриц")
		elif result != None:
			await message.answer("остаток "+str(result)+": продана 1 курица, их осталось: " + str(chiken_info))



def but_what():
	pass




if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
