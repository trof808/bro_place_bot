from decouple import config
from telegram import Update 
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, ChatMemberHandler
import logging
from calculate_time_until import calculate_time_until
from telegram.constants import ParseMode
from extract_status_change import extract_status_change

BOT_TOKEN= config('BOT_TOKEN')
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
        )

def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def bet_reminder_text(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    days, hours, minutes, seconds = calculate_time_until(2023, 9, 1, 21, 00, 00)
    print()
    await context.bot.send_message(chat_id=job.data.get('chat_id'), text=f"""
Напоминаю про спор между псами 🐕 \n
Для победы младшему псу надо сделать 20 чистых отжиманий, старшему скинуть до 80 кг 
До окончания спора осталось: \n📅 {days} дней {hours} часов {minutes} минут {seconds} секунд 📅\n
Надеюсь, что каждый из вас сделал максимум для победы, потому что на кону целый касарь 💰
                                   \n
Можешь написать тут сколько ты сегодня собираешься сделать или уже сделал для победы
                                   """)

async def set_bet_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    user = update.message.from_user
    try:
        job_removed = remove_job_if_exists(str(chat_id), context)
        data = {'chat_id': chat_id}
        context.job_queue.run_repeating(bet_reminder_text, interval=28800, first=1, data=data)
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Run /start again")

async def greet_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = extract_status_change(update.chat_member)
    was_member, is_member = result
    print(was_member, is_member)
    if not was_member and is_member:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='''
            Здарова Пес! Если ты оказался в этом чате, значит ты истинный пес, можешь гордиться этим. \n
            Тут будут всякие напоминания о каких-то событиях, спорах, умные мысли и главное напоминание о том, что ты пес
            Если у тебя будут предложения по улучшению этого бота, пиши главному псу. Возможно ты хочешь чаще получать сообщения о том, что ты пес \n\n
            А пока лови первую напоминалку
                                   ''')
        await bet_reminder_text(context)
    else:
        return


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_bet_reminder(update, context)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_message.chat_id, text=update.message.text)

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    new_chat_memeber_handler = ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(new_chat_memeber_handler)

    application.run_polling()
