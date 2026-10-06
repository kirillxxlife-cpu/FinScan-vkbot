# ============================================================
#  VK BOT — ФИНСКАН v3.0
#  Фреймворк: vkbottle
#  Режим: Long Poll API
#  Гибкая система подбора офферов по ЦА
# ============================================================

import os
import re
import asyncio
from datetime import datetime

from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle import BaseStateGroup

# ================= НАСТРОЙКИ =================
GROUP_TOKEN = "vk1.a.ТВОЙ_ТОКЕН_СЮДА_ПОЛНОСТЬЮ"
GROUP_ID    = 38935595

bot = Bot(token=GROUP_TOKEN)
bot.labeler.vbml_ignore_case = True

# ============================================================
#  БАЗА ОФФЕРОВ — расширенная, с тегами для подбора
# ============================================================
OFFERS = {
    "zaymigo": {
        "name": "Займер",
        "url": "https://vk.cc/d1TuQm",
        "reason_0": "Первый займ под 0% для новых клиентов — возвращаешь ровно столько, сколько взял.",
        "reason_bad": "Дают даже с испорченной КИ — главное, чтобы не было открытых просрочек.",
        "tags": ["student", "working", "freelance", "good_credit", "first_time"],
        "weight": 0.9
    },
    "dobrozaym": {
        "name": "ДоброЗайм",
        "url": "https://vk.cc/d1TvN1",
        "reason_0": "Лояльный скоринг — одобряют даже там, где банки отказали.",
        "reason_bad": "Специально работают с просрочками — не отказывают автоматически.",
        "tags": ["working", "freelance", "bad_credit", "no_job"],
        "weight": 0.85
    },
    "krediska": {
        "name": "Кредиска",
        "url": "https://vk.cc/d1TwVC",
        "reason_0": "0% на первый займ — для тех, кто берёт впервые.",
        "reason_bad": "Гибкие условия для сложных случаев.",
        "tags": ["student", "first_time", "good_credit"],
        "weight": 0.8
    },
    "webbankir": {
        "name": "Webbankir",
        "url": "https://vk.cc/d1TDPS",
        "reason_0": "Стабильно одобряют студентам и тем, у кого нет официального дохода.",
        "reason_bad": "Лояльны к КИ — работают с просрочками до 90 дней.",
        "tags": ["student", "no_job", "bad_credit", "freelance"],
        "weight": 0.75
    },
    "turbozaym": {
        "name": "Турбозайм",
        "url": "https://vk.cc/d1TDw4",
        "reason_0": "0% первые 7 дней — успеваешь вернуть без переплаты.",
        "reason_bad": "Быстрое решение даже при плохой истории.",
        "tags": ["freelance", "working", "good_credit", "first_time"],
        "weight": 0.7
    },
    "bunnymoney": {
        "name": "BunnyMoney",
        "url": "https://vk.cc/d1TF5v",
        "reason_0": "Работает без 2-НДФЛ — для фрилансеров и самозанятых.",
        "reason_bad": "Одобряют с минимальным пакетом документов.",
        "tags": ["freelance", "student", "no_job", "bad_credit"],
        "weight": 0.7
    },
    "cashmagnet": {
        "name": "Кэшмагнит",
        "url": "https://vk.cc/d1TFpv",
        "reason_0": "Сложные случаи — их профиль. Без работы, без КИ, без проблем.",
        "reason_bad": "Берут тех, кого другие отвергли.",
        "tags": ["no_job", "bad_credit", "first_time"],
        "weight": 0.65
    },
    "dengi_srazu": {
        "name": "Деньги Сразу",
        "url": "https://vk.cc/d1TC6W",
        "reason_0": "Минимум бюрократии — одобрение за 5 минут.",
        "reason_bad": "Не требуют справок и поручителей.",
        "tags": ["working", "no_job", "bad_credit"],
        "weight": 0.75
    },
    "migcredit": {
        "name": "МигКредит",
        "url": "https://vk.cc/d1TCL1",
        "reason_0": "Лимиты до 100 000 ₽ — под крупные суммы.",
        "reason_bad": "Для тех, кому нужна сумма побольше.",
        "tags": ["working", "good_credit", "high_amount"],
        "weight": 0.85
    },
    "bystrodengi": {
        "name": "Быстроденьги",
        "url": "https://vk.cc/d1TBzn",
        "reason_0": "Классика рынка — стабильно одобряют.",
        "reason_bad": "Работают с разными категориями заёмщиков.",
        "tags": ["working", "freelance", "good_credit"],
        "weight": 0.7
    },
    "beriberu": {
        "name": "Бериберу",
        "url": "https://vk.cc/d1TBkm",
        "reason_0": "Простая анкета — минимум вопросов.",
        "reason_bad": "Не заваливают проверками.",
        "tags": ["freelance", "no_job", "bad_credit"],
        "weight": 0.65
    },
    "hurmacredit": {
        "name": "ХурмаКредит",
        "url": "https://vk.cc/d1TzWz",
        "reason_0": "Быстрое решение — для срочных случаев.",
        "reason_bad": "Не требуют идеальной истории.",
        "tags": ["freelance", "student", "good_credit"],
        "weight": 0.6
    },
    "davaka": {
        "name": "Давака",
        "url": "https://vk.cc/d1TEvz",
        "reason_0": "Запасной вариант, который всегда под рукой.",
        "reason_bad": "Если основные не подошли — этот точно сработает.",
        "tags": ["student", "no_job", "bad_credit"],
        "weight": 0.55
    }
}

# ============================================================
#  ГИБКАЯ СИСТЕМА ПОДБОРА — скоринг по ЦА
# ============================================================
def get_offers_for_user(state: dict) -> list:
    """
    Возвращает топ-2 оффера, отранжированных по скорингу.
    Учитывает статус, КИ, сумму и дополнительные факторы.
    """
    status = state.get("status") or ""
    credit = state.get("credit") or ""
    amount = state.get("amount") or ""

    # Формируем теги пользователя
    user_tags = []

    # Статус
    if status == "Студент":
        user_tags.append("student")
    elif status == "Работаю":
        user_tags.append("working")
    elif status == "Фриланс":
        user_tags.append("freelance")
    elif status == "Без работы":
        user_tags.append("no_job")

    # КИ
    if credit == "Идеальная":
        user_tags.append("good_credit")
    elif credit == "Были просрочки":
        user_tags.append("bad_credit")
    elif credit == "Никогда не брал":
        user_tags.append("first_time")

    # Сумма
    if amount == "50.000 – 100.000 ₽":
        user_tags.append("high_amount")
    elif amount == "до 15.000 ₽":
        user_tags.append("low_amount")

    # Скоринг
    scored = []
    for key, offer in OFFERS.items():
        score = 0.0
        for tag in offer["tags"]:
            if tag in user_tags:
                score += 1.0
        # Вес оффера — базовый приоритет
        score += offer["weight"]
        # Бонус за точное совпадение по КИ
        if credit == "Были просрочки" and "bad_credit" in offer["tags"]:
            score += 0.5
        if credit == "Никогда не брал" and "first_time" in offer["tags"]:
            score += 0.3
        # Бонус за совпадение по сумме
        if amount == "50.000 – 100.000 ₽" and "high_amount" in offer["tags"]:
            score += 0.4

        scored.append((score, key, offer))

    # Сортируем по убыванию
    scored.sort(key=lambda x: x[0], reverse=True)

    # Возвращаем топ-2
    result = []
    for score, key, offer in scored[:2]:
        # Выбираем reason в зависимости от КИ
        reason_key = "reason_bad" if credit == "Были просрочки" else "reason_0"
        result.append({
            "key": key,
            "name": offer["name"],
            "url": offer["url"],
            "reason": offer.get(reason_key, offer.get("reason_0", "")),
            "score": round(score, 2)
        })

    return result

# ============================================================
#  СОСТОЯНИЯ
# ============================================================
class Form(BaseStateGroup):
    STATUS   = "status"
    CREDIT   = "credit"
    AMOUNT   = "amount"
    CONFIRM  = "confirm"
    PHONE    = "phone"

# ============================================================
#  ХРАНИЛИЩЕ (для продакшена — SQLite, для старта — память)
# ============================================================
user_data = {}

def get_data(peer_id: int) -> dict:
    if peer_id not in user_data:
        user_data[peer_id] = {
            "status": None, "credit": None, "amount": None,
            "phone": None, "name": None, "startedAt": None
        }
    return user_data[peer_id]

# ============================================================
#  КЛАВИАТУРЫ
# ============================================================
def kb_start():
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("💸 Да, давай", payload={"cmd": "go"}), color=KeyboardButtonColor.POSITIVE)
    return kb.get_json()

def kb_status():
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("🎓 Студент", payload={"cmd": "status_student"}), color=KeyboardButtonColor.PRIMARY)
    kb.row()
    kb.add(Text("💼 Работаю", payload={"cmd": "status_working"}), color=KeyboardButtonColor.PRIMARY)
    kb.row()
    kb.add(Text("💻 Фриланс", payload={"cmd": "status_freelance"}), color=KeyboardButtonColor.PRIMARY)
    kb.row()
    kb.add(Text("🏠 Временно без работы", payload={"cmd": "status_nojob"}), color=KeyboardButtonColor.SECONDARY)
    return kb.get_json()

def kb_credit():
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("✅ Идеальная", payload={"cmd": "credit_good"}), color=KeyboardButtonColor.POSITIVE)
    kb.row()
    kb.add(Text("⚠️ Были просрочки", payload={"cmd": "credit_bad"}), color=KeyboardButtonColor.NEGATIVE)
    kb.row()
    kb.add(Text("🆕 Никогда не брал", payload={"cmd": "credit_none"}), color=KeyboardButtonColor.PRIMARY)
    return kb.get_json()

def kb_amount():
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("до 15.000 ₽", payload={"cmd": "amount_low"}), color=KeyboardButtonColor.PRIMARY)
    kb.row()
    kb.add(Text("15.000 – 50.000 ₽", payload={"cmd": "amount_mid"}), color=KeyboardButtonColor.PRIMARY)
    kb.row()
    kb.add(Text("50.000 – 100.000 ₽", payload={"cmd": "amount_high"}), color=KeyboardButtonColor.PRIMARY)
    return kb.get_json()

def kb_confirm():
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("✅ Да, всё верно", payload={"cmd": "confirm_yes"}), color=KeyboardButtonColor.POSITIVE)
    kb.row()
    kb.add(Text("❌ Изменить", payload={"cmd": "confirm_edit"}), color=KeyboardButtonColor.NEGATIVE)
    return kb.get_json()

def kb_phone():
    kb = Keyboard(one_time=True, inline=False)
    kb.add(Text("📱 Отправить номер", payload={"cmd": "phone_start"}), color=KeyboardButtonColor.PRIMARY)
    return kb.get_json()

def kb_main():
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("🔥 Офферы под 0%", payload={"cmd": "zero_loans"}), color=KeyboardButtonColor.POSITIVE)
    kb.row()
    kb.add(Text("🏠 Начать заново", payload={"cmd": "restart"}), color=KeyboardButtonColor.SECONDARY)
    return kb.get_json()

# ============================================================
#  ХЕНДЛЕРЫ
# ============================================================

@bot.on.message(text="/start")
async def start_handler(message: Message):
    peer_id = message.peer_id
    data = get_data(peer_id)
    data["name"] = (await bot.api.users.get(user_ids=message.from_id))[0].first_name
    data["startedAt"] = datetime.now().isoformat()

    await bot.state_dispenser.set(peer_id, Form.STATUS)
    await message.answer(
        f"{data['name']}, привет.\n\n"
        "Если ты здесь — скорее всего, деньги нужны срочно: не хватает до зарплаты, "
        "банк отказал, или просто не хочется просить у знакомых.\n\n"
        "Я подбираю займы в МФО с лицензией ЦБ РФ. Одобрение — от 5 минут, деньги на карту. "
        "Без справок, без поручителей, без походов в офис.\n\n"
        "Три коротких вопроса — и я скажу, где тебе точно одобрят. Поехали?",
        keyboard=kb_start()
    )

# ---------- GO ----------
@bot.on.message(payload={"cmd": "go"})
async def go_handler(message: Message):
    peer_id = message.peer_id
    data = get_data(peer_id)
    await bot.state_dispenser.set(peer_id, Form.STATUS)
    await message.answer(
        f"{data['name']}, первый вопрос — самый важный.\n\n"
        "Кто ты сейчас по статусу?\n\n"
        "Это не для проверки — это чтобы понять, куда тебе скорее всего одобрят. "
        "Студентам, фрилансерам и людям без официального дохода тоже дают, просто в других МФО.",
        keyboard=kb_status()
    )

# ---------- STATUS ----------
@bot.on.message(payload={"cmd": "status_student"})
@bot.on.message(payload={"cmd": "status_working"})
@bot.on.message(payload={"cmd": "status_freelance"})
@bot.on.message(payload={"cmd": "status_nojob"})
async def status_handler(message: Message):
    peer_id = message.peer_id
    data = get_data(peer_id)
    cmd = message.payload.get("cmd")

    map_status = {
        "status_student": "Студент",
        "status_working": "Работаю",
        "status_freelance": "Фриланс",
        "status_nojob": "Без работы"
    }
    data["status"] = map_status.get(cmd)

    # Триггеры: снятие стыда + соцдоказательство + калиброванная лесть
    praise = {
        "Студент": "Студенты сейчас самые подкованные — многие МФО дают специальные условия.",
        "Работаю": "С постоянным доходом тебе открыты почти все — это твой козырь.",
        "Фриланс": "Фриланс — жёстко, но ты сам себе работодатель. Многие МФО это признают.",
        "Без работы": "Ничего страшного, это временно. Есть МФО, где одобряют и без 2-НДФЛ."
    }.get(data["status"], "")

    await bot.state_dispenser.set(peer_id, Form.CREDIT)
    await message.answer(
        f"{data['name']}, зафиксировал: {data['status']}. {praise}\n\n"
        "Теперь про кредитную историю.\n\n"
        "Если были просрочки — это не приговор. Есть МФО, которые специально работают с такими клиентами. "
        "Просто у них чуть выше ставка, но одобрение приходит в тот же день.\n\n"
        "Как у тебя с КИ?",
        keyboard=kb_credit()
    )

# ---------- CREDIT ----------
@bot.on.message(payload={"cmd": "credit_good"})
@bot.on.message(payload={"cmd": "credit_bad"})
@bot.on.message(payload={"cmd": "credit_none"})
async def credit_handler(message: Message):
    peer_id = message.peer_id
    data = get_data(peer_id)
    cmd = message.payload.get("cmd")

    map_credit = {
        "credit_good": "Идеальная",
        "credit_bad": "Были просрочки",
        "credit_none": "Никогда не брал"
    }
    data["credit"] = map_credit.get(cmd)

    # Мимикрия / отражение
    reflect = {
        "Идеальная": "Идеальная КИ — это твой главный козырь, тебе дадут лучшие условия.",
        "Были просрочки": "С просрочками работают МФО с лояльным скорингом. Не переживай.",
        "Никогда не брал": "Чистая история — это тоже плюс, тебя увидят как нового клиента и дадут 0%."
    }.get(data["credit"], "")

    await bot.state_dispenser.set(peer_id, Form.AMOUNT)
    await message.answer(
        f"{reflect}\n\n"
        "Сколько нужно? Выбери диапазон — я подберу МФО, где лимиты начинаются именно с таких сумм.\n\n"
        "Совет: бери ровно столько, сколько нужно, и на срок, который точно закроешь. "
        "Тогда переплата будет минимальной.",
        keyboard=kb_amount()
    )

# ---------- AMOUNT ----------
@bot.on.message(payload={"cmd": "amount_low"})
@bot.on.message(payload={"cmd": "amount_mid"})
@bot.on.message(payload={"cmd": "amount_high"})
async def amount_handler(message: Message):
    peer_id = message.peer_id
    data = get_data(peer_id)
    cmd = message.payload.get("cmd")

    map_amount = {
        "amount_low": "до 15.000 ₽",
        "amount_mid": "15.000 – 50.000 ₽",
        "amount_high": "50.000 – 100.000 ₽"
    }
    data["amount"] = map_amount.get(cmd)

    summary = (
        f"Итак, {data['name']}:\n"
        f"• Статус: {data['status']}\n"
        f"• КИ: {data['credit']}\n"
        f"• Сумма: {data['amount']}\n\n"
        "Всё верно?"
    )

    await bot.state_dispenser.set(peer_id, Form.CONFIRM)
    await message.answer(summary, keyboard=kb_confirm())

# ---------- CONFIRM ----------
@bot.on.message(payload={"cmd": "confirm_yes"})
async def confirm_handler(message: Message):
    peer_id = message.peer_id
    data = get_data(peer_id)

    await bot.state_dispenser.set(peer_id, Form.PHONE)
    await message.answer(
        f"{data['name']}, отлично.\n\n"
        "Оставь номер телефона — пришлю подборку под тебя лично.\n\n"
        "🔒 По этому номеру мы не звоним без твоего согласия. Только чтобы отправить ссылку.",
        keyboard=kb_phone()
    )

@bot.on.message(payload={"cmd": "confirm_edit"})
async def confirm_edit_handler(message: Message):
    peer_id = message.peer_id
    data = get_data(peer_id)
    data["status"] = None
    data["credit"] = None
    data["amount"] = None
    await bot.state_dispenser.set(peer_id, Form.STATUS)
    await message.answer("Ок, начнём заново.", keyboard=kb_status())

# ---------- PHONE ----------
@bot.on.message(payload={"cmd": "phone_start"})
async def phone_ask_handler(message: Message):
    await message.answer("Напиши номер в формате +7 900 123-45-67.")

@bot.on.message(state=Form.PHONE)
async def phone_input_handler(message: Message):
    peer_id = message.peer_id
    data = get_data(peer_id)
    text = message.text.strip() if message.text else ""

    digits = re.sub(r"\D", "", text)

    if len(digits) >= 10:
        data["phone"] = text

        # --- ГИБКИЙ ПОДБОР ОФФЕРОВ ---
        offers = get_offers_for_user(data)

        if not offers:
            await message.answer("Не удалось подобрать оффер. Попробуй ещё раз /start")
            return

        primary = offers[0]
        backup  = offers[1] if len(offers) > 1 else None

        msg = (
            f"{data['name']}, готово! Вот твой вариант:\n\n"
            f"🏆 {primary['name']}\n"
            f"💡 {primary['reason']}\n"
            f"👉 {primary['url']}\n\n"
        )

        if backup:
            msg += (
                f"🔄 Запасной вариант (если этот не подойдёт):\n"
                f"👉 {backup['url']}\n\n"
            )

        msg += (
            "Что делать прямо сейчас:\n"
            "1️⃣ Открой ссылку\n"
            "2️⃣ Заполни анкету (2–3 минуты)\n"
            "3️⃣ Дождись одобрения — обычно 5–15 минут\n"
            "4️⃣ Деньги упадут на карту в тот же день\n\n"
            "⚡ Ставки 0% для новых клиентов — ограниченное время.\n\n"
            "⚠️ Реклама. ПСК от 0% до 292% годовых. Оценивайте риски."
        )

        await bot.state_dispenser.delete(peer_id)
        await message.answer(msg, keyboard=kb_main())

    else:
        await message.answer(
            f"{data['name']}, формат немного другой. Скинь так: +7 900 123-45-67"
        )

# ---------- ZERO LOANS ----------
@bot.on.message(payload={"cmd": "zero_loans"})
async def zero_loans_handler(message: Message):
    peer_id = message.peer_id
    data = get_data(peer_id)
    name = data.get("name", "друг")

    await message.answer(
        f"{name}, вот займы под 0% для новых клиентов.\n\n"
        "Это предложения, где первый займ можно взять без процентов — "
        "возвращаешь ровно ту сумму, которую взял.\n\n"
        "Как не переплатить:\n"
        "1️⃣ Бери только ту сумму, которую точно вернёшь.\n"
        "2️⃣ Верни в срок — обычно 7–30 дней.\n"
        "3️⃣ Проверь ПСК в договоре.\n"
        "4️⃣ Не подключай платные доп. услуги.\n\n"
        "👇 Выбирай МФО:",
        keyboard=kb_main()
    )

# ---------- RESTART ----------
@bot.on.message(payload={"cmd": "restart"})
async def restart_handler(message: Message):
    peer_id = message.peer_id
    data = get_data(peer_id)
    data["status"] = None
    data["credit"] = None
    data["amount"] = None
    await bot.state_dispenser.set(peer_id, Form.STATUS)
    await message.answer("Начинаем заново!", keyboard=kb_status())

# ============================================================
#  ЗАПУСК
# ============================================================
if __name__ == "__main__":
    bot.run_forever()
