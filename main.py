from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os, json

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

def read_data(id):
	with open(f"db/{id}.json", "r", encoding="utf8") as file:
		return json.load(file)

def write_data(id, data):
	with open(f"db/{id}.json", "w", encoding="utf-8") as file:
		json.dump(data, file, indent=4)

def remove_value(value, id):
	data = read_data(id)
	if value < 0:
		adding_obj = {"value": value}
	else:
		negative_value = value * -1
		adding_obj = {"value": negative_value}
	data["values"].append(adding_obj)
	write_data(id, data)

def add_value(value, id):
	data = read_data(id)
	adding_obj = {"value": value}
	data["values"].append(adding_obj)
	write_data(id, data)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	# Mensagem de apresentação: "/start"
	await update.message.reply_text(f"Olá, {update.effective_user.first_name} Bem-Vindo, eu sou um bot de finanças, pronto pra começar?")
	id = update.effective_user.id
	start_obj = {"values": []}
	write_data(id, start_obj)

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	# Funcão para adicionar saldo: "/add <value>"
	args = context.args
	if len(args) != 1:
		await update.message.reply_text("Use: /add <valor>")
		return
	value = args[-1]
	try:
		number = float(value)
		id = update.effective_user.id
		add_value(number, id)
		await update.message.reply_text(f"Adicionado mais: {value} ao seu saldo, detalhes em: /balance")
	except ValueError:
		await update.message.reply_text(f"O valor: {value} esta incorreto")

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	# Funcão para remover saldo: "/remove <value>"
	args = context.args
	if len(args) != 1:
		await update.message.reply_text("Use: /remove <valor>")
		return
	value = args[-1]
	try:
		number = float(value)
		id = update.effective_user.id
		remove_value(number, id)
		await update.message.reply_text(f"Foi removido do seu salvo mais: {value}, Para ver seu saldo, use: /balance")
	except ValueError:
		await update.message.reply_text(f"O valor: {value} esta incorreto")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_user.id
	data = read_data(id)
	values = data.get("values")
	pos_num = 0
	neg_num = 0
	for value in values:
		number_value = value.get("value")
		if number_value < 0:
			neg_num -= number_value
		else:
			pos_num += number_value
	result = pos_num - neg_num
	await update.message.reply_text(f"Você tem no momento {result} de saldo!")
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	# Mensagem que lista os comandos: "/help"
	await update.message.reply_text("Lista de comandos:\n\n/add -> Adicionar saldo\n/remove -> Remove saldo\n/balance -> Mostra quanto você tem no total")

def main():
	path_db = "db"
	if not os.path.exists(path_db):
		os.makedirs(path_db)
	application = ApplicationBuilder().token(BOT_TOKEN).build()
	application.add_handler(CommandHandler("start", start))
	application.add_handler(CommandHandler("help", help_command))
	application.add_handler(CommandHandler("add", add))
	application.add_handler(CommandHandler("remove", remove))
	application.add_handler(CommandHandler("balance", balance))
	application.run_polling()

if __name__ == "__main__":
	main()
