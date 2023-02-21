import pathlib
from typing import Union, TypedDict
import asyncio
import sys

import httpx
import parsel
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

listners_path = pathlib.Path("./listners.txt")

running = False


class Sequence(TypedDict):
    white_distance: int
    minutes: list[int]
    messages_ids: dict[int, int]
    hours: list[int]


async def main():
    sequences: list[Sequence] = []
    last_id = None
    lock = False

    soma_esquerdo_1: Union[int, None] = None
    soma_direito_1: Union[int, None] = None
    soma_2_lados_1: Union[int, None] = None
    soma_2_esquerdo_1: Union[int, None] = None
    soma_2_direito_1: Union[int, None] = None
    soma_esquerdo_2: Union[int, None] = None
    soma_direito_2: Union[int, None] = None
    soma_2_lados_2: Union[int, None] = None
    soma_2_esquerdo_2: Union[int, None] = None
    soma_2_direito_2: Union[int, None] = None

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
            item_minute = int(item.css(".minute-table::text").get().split(":")[1])
            item_hour = int(item.css(".minute-table::text").get().split(":")[0])

            if item_number == 0:
                if not lock:
                    sequences.append({
                        "minutes": [],
                        "messages_ids": {},
                        "white_distance": -1,
                        "hours": []
                    })

                    lock = True

                for sequence in sequences:
                    for minute in sequence["minutes"]:
                        if item_minute >= minute - 1 and item_minute <= minute + 1:
                            for listner in listners_path.read_text().strip().split("\n"):
                                listner = int(listner.strip())
                                message_id = sequence["messages_ids"][listner]
                                item = selector.css(".double-single")[0]
                                await app.updater.bot.send_message(listner, f"Pagaaaa blazeee 🤑🤑🤑🤑🤑🤑🤑🤯🤯\n\n{item.css('.minute-table::text').get()}", reply_to_message_id=message_id)

                            if sequence in sequences:
                                sequences.remove(sequence)

                            sequences.append({
                                "minutes": [],
                                "messages_ids": {},
                                "white_distance": -1,
                                "hours": []
                            })

                            lock = True

                            break

            for sequence in sequences:
                if sequence["white_distance"] < 2:
                    sequence["white_distance"] += 1

                    if sequence["white_distance"] == 2:
                        items = selector.css(".double-single")

                        item1_number = int(items[0].css(".number-table::text").get())
                        item2_number = int(items[1].css(".number-table::text").get())
                        item3_minutes = int(items[2].css(".minute-table::text").get().split(":")[1])
                        item3_hours = int(items[2].css(".minute-table::text").get().split(":")[0])
                        item4_number = int(items[3].css(".number-table::text").get())
                        item5_number = int(items[4].css(".number-table::text").get())

                        soma_esquerdo_2 = item2_number + item3_minutes

                        if soma_esquerdo_2 >= 60:
                            soma_esquerdo_2 = soma_esquerdo_2 - 60

                        soma_direito_2 = item3_minutes + item4_number

                        if soma_direito_2 >= 60:
                            soma_direito_2 = soma_direito_2 - 60

                        soma_2_lados_2 = item2_number + item3_minutes + item4_number

                        if soma_2_lados_2 >= 60:
                            soma_2_lados_2 = soma_2_lados_2 - 60

                        soma_2_esquerdo_2 = item1_number + item2_number + item3_minutes

                        if soma_2_esquerdo_2 >= 60:
                            soma_2_esquerdo_2 = soma_2_esquerdo_2 - 60

                        soma_2_direito_2 = item3_minutes + item4_number + item5_number

                        if soma_2_direito_2 >= 60:
                            soma_2_direito_2 = soma_2_direito_2 - 60

                        if item1_number > 10:
                            item1_number = int(str(item1_number)[0]) + int(str(item1_number)[1])

                        if item2_number > 10:
                            item2_number = int(str(item2_number)[0]) + int(str(item2_number)[1])

                        if item4_number > 10:
                            item4_number = int(str(item4_number)[0]) + int(str(item4_number)[1])
                        
                        if item5_number > 10:
                            item5_number = int(str(item5_number)[0]) + int(str(item5_number)[1])

                        soma_esquerdo_1 = item2_number + item3_minutes

                        if soma_esquerdo_1 >= 60:
                            soma_esquerdo_1 = soma_esquerdo_1 - 60

                        soma_direito_1 = item3_minutes + item4_number

                        if soma_direito_1 >= 60:
                            soma_direito_1 = soma_direito_1 - 60

                        soma_2_lados_1 = item2_number + item3_minutes + item4_number

                        if soma_2_lados_1 >= 60:
                            soma_2_lados_1 = soma_2_lados_1 - 60

                        soma_2_esquerdo_1 = item1_number + item2_number + item3_minutes

                        if soma_2_esquerdo_1 >= 60:
                            soma_2_esquerdo_1 = soma_2_esquerdo_1 - 60

                        soma_2_direito_1 = item3_minutes + item4_number + item5_number

                        if soma_2_direito_1 >= 60:
                            soma_2_direito_1 = soma_2_direito_1 - 60

                        parte_1 = [soma_esquerdo_1, soma_direito_1, soma_2_lados_1, soma_2_esquerdo_1, soma_2_direito_1]
                        parte_2 = [soma_esquerdo_2, soma_direito_2, soma_2_lados_2, soma_2_esquerdo_2, soma_2_direito_2]

                        parte_1 = list(dict.fromkeys(parte_1))
                        parte_2 = list(dict.fromkeys(parte_2))

                        new_line = "\n"

                        for item in parte_1:
                            if item in parte_2:
                                parte_2.remove(item)

                        sequence["minutes"].extend([*parte_1, *parte_2])

                        for minute in sequence["minutes"]:
                            if minute <= item3_minutes:
                                if item3_hours == 23:
                                    sequence["hours"].append(0)
                                else:
                                    sequence["hours"].append(item3_hours + 1)
                            else:
                                sequence["hours"].append(item3_hours)

                        for listner in listners_path.read_text().strip().split("\n"):
                            listner = int(listner.strip())

                            message = await app.updater.bot.send_message(
                                listner,
                                f"""🔮Estamos sentido a presença do branco🔮

{new_line.join(map(str, parte_1))}

Minutos de recuperação 
{new_line.join(map(str, parte_2)) if len(parte_2) > 0 else "Sem opções"}

Boa sorte 🤑""")
                            sequence["messages_ids"][listner] = message.message_id
                elif len(sequence["minutes"]) > 0:
                    max_hour = max(sequence["hours"])
                    max_minutes = []

                    for c in range(len(sequence["minutes"])):
                        minute = sequence["minutes"][c]
                        hour = sequence["hours"][c]

                        if hour == max_hour:
                            max_minutes.append(minute)

                    if item_hour >= max_hour and item_minute > max(max_minutes) + 1:
                        for listner in listners_path.read_text().strip().split("\n"):
                            listner = int(listner.strip())
                            message_id = sequence["messages_ids"][listner]
                            await app.updater.bot.send_message(listner, "Loss ❌❌❌❌❌❌", reply_to_message_id=message_id)
                            lock = False

                        sequences.remove(sequence)

        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            print(e, exc_tb.tb_lineno)

        await asyncio.sleep(15)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global running

    if not running:
        running = True
        asyncio.create_task(main())
        print("Running...")

        for listner in listners_path.read_text().strip().split("\n"):
            if listner != "":
                listner = int(listner.strip())

                await app.updater.bot.send_message(listner, "Bot reiniciado")

    listners = listners_path.read_text().strip().split("\n")

    if str(update.message.chat_id) in listners:
        await update.message.reply_text(f"Você já está inscrito.")
        return

    listners_path.write_text(listners_path.read_text() + f"\n{update.message.chat_id}", encoding="utf-8")
    listners_path.write_text(listners_path.read_text().strip())

    await update.message.reply_text(f"Inscrição ativada, aguarde para receber as notificações.")

app = ApplicationBuilder().token("5873581129:AAG_3zua9tlXxJDAuqDcvxZE-puUTCRRQIs").build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
