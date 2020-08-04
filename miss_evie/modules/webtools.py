import speedtest
import requests
import datetime
import platform

from psutil import cpu_percent, virtual_memory, disk_usage, boot_time
from platform import python_version
from telegram import __version__
from pythonping import ping as ping3
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from miss_evie import dispatcher, OWNER_ID
from miss_evie.modules.helper_funcs.filters import CustomFilters
from miss_evie.modules.helper_funcs.alternate import typing_action


@run_async
@typing_action
def ping(update, context):
    tg_api = ping3("api.telegram.org", count=5)
    google = ping3("google.com", count=5)
    text = "Average speed to:"
    text += "\nTG bot API server - `{}` ms".format(tg_api.rtt_avg_ms)
    text += "\nGoogle - `{}` ms".format(google.rtt_avg_ms)
    update.effective_message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    byte = 8
    power = 2 ** 10
    n = 1
    units = {1: "KB/s", 2: "MB/s", 3: "GB/s", 4: "TB/s"}
    while size > power:
        n += 1
        size /= power ** n

# convert bit to byte
        size /= byte

    return f"`{round(size, 2)}` {units[n]}"


@run_async
@typing_action
def get_bot_ip(update, context):
    """ Sends the bot's IP address, so as to be able to ssh in if necessary.
        OWNER ONLY.
    """
    res = requests.get("http://ipinfo.io/ip")
    update.message.reply_text(res.text)


@run_async
@typing_action
def speedtst(update, context):
    message = update.effective_message
    ed_msg = message.reply_text("Running high speed test . . .")
    test = speedtest.Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    google = ping3("google.com", count=5)

    context.bot.editMessageText(
        "Download - "
        f"{speed_convert(result['download'])} \n"
        "Upload - "
        f"{speed_convert(result['upload'])} \n"
        "Google - "
        f"{'`{}` ms'.format(google.rtt_avg_ms)}",
        update.effective_chat.id,
        ed_msg.message_id,
        parse_mode=ParseMode.MARKDOWN,
    )


@run_async
@typing_action
def system_status(update, context):
    uptime = datetime.datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    status = "<b>======[ SYSTEM INFO ]======</b>\n\n"
    status += "<b>System uptime:</b> <code>" + str(uptime) + "</code>\n"

    uname = platform.uname()
    status += "<b>System:</b> <code>" + str(uname.system) + "</code>\n"
    status += "<b>Node name:</b> <code>" + str(uname.node) + "</code>\n"
    status += "<b>Release:</b> <code>" + str(uname.release) + "</code>\n"
    status += "<b>Version:</b> <code>" + str(uname.version) + "</code>\n"
    status += "<b>Machine:</b> <code>" + str(uname.machine) + "</code>\n"
    status += "<b>Processor:</b> <code>" + str(uname.processor) + "</code>\n\n"

    mem = virtual_memory()
    cpu = cpu_percent()
    disk = disk_usage("/")
    status += "<b>CPU usage:</b> <code>" + str(cpu) + " %</code>\n"
    status += "<b>Ram usage:</b> <code>" + str(mem[2]) + " %</code>\n"
    status += "<b>Storage used:</b> <code>" + str(disk[3]) + " %</code>\n\n"
    status += "<b>Python version:</b> <code>" + python_version() + "</code>\n"
    status += "<b>Library version:</b> <code>" + str(__version__) + "</code>\n"
    context.bot.sendMessage(update.effective_chat.id, status, parse_mode=ParseMode.HTML)


IP_HANDLER = CommandHandler("ip", get_bot_ip, filters=Filters.chat(OWNER_ID))
PING_HANDLER = CommandHandler("ping", ping, filters=CustomFilters.sudo_filter)
SPEED_HANDLER = CommandHandler("speedtest", speedtst, filters=CustomFilters.sudo_filter)
SYS_STATUS_HANDLER = CommandHandler(
    "sysinfo", system_status, filters=CustomFilters.sudo_filter
)

dispatcher.add_handler(IP_HANDLER)
dispatcher.add_handler(SPEED_HANDLER)
dispatcher.add_handler(PING_HANDLER)
dispatcher.add_handler(SYS_STATUS_HANDLER)
