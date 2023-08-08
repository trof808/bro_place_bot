from decouple import config
from telegram import Update 
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import logging
from calculate_time_until import calculate_time_until
from telegram.constants import ParseMode

BOT_TOKEN= config('BOT_TOKEN')
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
        )

async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")

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
    await context.bot.send_message(chat_id='262093856', text=f"""
@{job.data} Напоминаю про спор со страшим псом\. \n
Для победы тебе нужно набрать массу к назначенному времени, чтобы сделать 20 чистых отжиманий иначе касарь должен псу или маме 
До окончания спора осталось: \n  <b>{days} дней {hours} часов {minutes} минут {seconds} секунд</b> \n
Надеюсь ты сегодня сделал все, чтобы приблизить себя к победе, потому что второй пес получает такие же мотивационные сообщения каждый день и стремиться к победе
                                   """)

async def set_bet_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    user = update.message.from_user
    try:
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(bet_reminder_text, interval=5, first=1, data=user.username)
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Run /start again")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='''
Здарова Пес! Если ты оказался в этом чате, значит ты истинный пес, можешь гордиться этим. \n
Тут будут всякие напоминания о каких-то событиях, спорах, умные мысли и главное напоминание о том, что ты пес
Если у тебя будут предложения по улучшению этого бота, пиши главному псу. Возможно ты хочешь чаще получать сообщения о том, что ты пес \n\n
А пока лови первую напоминалку
                                   ''')
    await set_bet_reminder(update, context)

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
