import time

import httpx
import parsel
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Inscrição ativada, aguarde para receber as notificações.")

app = ApplicationBuilder().token("5873581129:AAG_3zua9tlXxJDAuqDcvxZE-puUTCRRQIs").build()

app.add_handler(CommandHandler("start", start))

last_id = None
last_white_distance = 0

sum_2_3 = None
sum_3_4 = None
sum_1_3 = None
sim_3_5 = None
sum_2_3_4 = None

app.run_polling()

while True:
    try:
        response = httpx.get(
            "https://historicosblaze.com/br/blaze/doubles",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

        response.raise_for_status()
        selector = parsel.Selector(response.text)

        item = selector.css(".double-single")[0]

        item_id = item.xpath("./@data-id").get()

        if item_id == last_id:
            continue

        last_id = item_id

        item_number = int(item.css(".number-table::text").get())

        if item_number == 0:
            last_white_distance += 1
            continue
        elif last_white_distance == 2:
            last_white_distance = 0

            items = selector.css(".double-single")

            if sum_2_3:
                item1_number = int(items[0].css(".number-table::text").get())
                item2_number = int(items[1].css(".number-table::text").get())
                item3_minutes = int(items[2].css(".minute-table::text").get().split(":")[0])
                item4_number = int(items[3].css(".number-table::text").get())
                item5_number = int(items[4].css(".number-table::text").get())

                if item2_number > 10:
                    item2_number =  int(str(item2_number)[0]) + int(str(item2_number)[1])
                
                if item4_number > 10:
                    item4_number =  int(str(item4_number)[0]) + int(str(item4_number)[1])

                sum_2_3 = item2_number + item3_minutes
                sum_3_4 = item3_minutes + item4_number
                sum_1_3 = item1_number + item3_minutes
                sim_3_5 = item3_minutes + item5_number
                sum_2_3_4 = item2_number + item3_minutes + item4_number

    except Exception as e:
        print(e)

    time.sleep(15)
