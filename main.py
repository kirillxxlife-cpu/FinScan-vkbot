# ============================================================
#  VK BOT — СУПЕР ЗАЙМ 0% | MONEY BOT  v5.0
#  Фреймворк: vkbottle | Long Poll API
#  Воронка с приёмами соц. инженерии
# ============================================================

import re
import json
from datetime import datetime

from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink

# ================= НАСТРОЙКИ =================
GROUP_TOKEN = "vk1.a.AOyP3eRdxp8yz4R6iUbbTN6xkTkwVkxfBSzNYeycoGh9VGJLMTrg6mj1ndPWoF9Gbd7XEAcl7VIFTLvM9qa33LqPyy5R-5qjRNsca0Q-9naOTm9W_n437r7RM3LKrWtYvo1CVj9CS0_D6bGqstOvsUsbF_jxxSAXBF4IzXUP3MKjW_iiwJJEr6FqgHEo_pnrY_aEjclWJzPbQS_JhZKVJw"# ============================================================
#  VK BOT — СУПЕР ЗАЙМ 0% | MONEY BOT  v5.0
#  Фреймворк: vkbottle | Long Poll API
#  Воронка с приёмами соц. инженерии
# ============================================================

import re
import json
from datetime import datetime

from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink

# ================= НАСТРОЙКИ =================
GROUP_TOKEN = "vk1.a.AOyP3eRdxp8yz4R6iUbbTN6xkTkwVkxfBSzNYeycoGh9VGJLMTrg6mj1ndPWoF9Gbd7XEAcl7VIFTLvM9qa33LqPyy5R-5qjRNsca0Q-9naOTm9W_n437r7RM3LKrWtYvo1CVj9CS0_D6bGqstOvsUsbF_jxxSAXBF4IzXUP3MKjW_iiwJJEr6FqgHEo_pnrY_aEjclWJzPbQS_JhZKVJw"    # ← ЗАМЕНИ на свой токен
GROUP_ID    = 38935595

bot = Bot(token=GROUP_TOKEN)
bot.labeler.vbml_ignore_case = True

# ============================================================
#  БАЗА ОФФЕРОВ
# ============================================================
OFFERS = {
    "zaymigo":    {"name": "Займер",       "url": "https://vk.cc/d1TuQm",
                   "reason_0": "Первый займ под 0% — возвращаешь ровно столько, сколько взял.",
                   "reason_bad": "Дают даже с испорченной КИ — главное, без открытых просрочек.",
                   "tags": ["student","working","freelance","good_credit","first_time"], "weight": 0.9},
    "dobrozaym":  {"name": "ДоброЗайм",    "url": "https://vk.cc/d1TvN1",
                   "reason_0": "Лояльный скоринг — одобряют там, где банки отказали.",
                   "reason_bad": "Специально работают с просрочками — не отказывают автоматом.",
                   "tags": ["working","freelance","bad_credit","no_job"], "weight": 0.85},
    "krediska":   {"name": "Кредиска",     "url": "https://vk.cc/d1TwVC",
                   "reason_0": "0% на первый займ — для тех, кто берёт впервые.",
                   "reason_bad": "Гибкие условия для сложных случаев.",
                   "tags": ["student","first_time","good_credit"], "weight": 0.8},
    "webbankir":  {"name": "Webbankir",    "url": "https://vk.cc/d1TDPS",
                   "reason_0": "Стабильно одобряют студентам и без официального дохода.",
                   "reason_bad": "Лояльны к КИ — работают с просрочками до 90 дней.",
                   "tags": ["student","no_job","bad_credit","freelance"], "weight": 0.75},
    "turbozaym":  {"name": "Турбозайм",    "url": "https://vk.cc/d1TDw4",
                   "reason_0": "0% первые 7 дней — успеваешь вернуть без переплаты.",
                   "reason_bad": "Быстрое решение даже при плохой истории.",
                   "tags": ["freelance","working","good_credit","first_time"], "weight": 0.7},
    "bunnymoney": {"name": "BunnyMoney",   "url": "https://vk.cc/d1TF5v",
                   "reason_0": "Работает без 2-НДФЛ — для фрилансеров и самозанятых.",
                   "reason_bad": "Одобряют с минимальным пакетом документов.",
                   "tags": ["freelance","student","no_job","bad_credit"], "weight": 0.7},
    "cashmagnet": {"name": "Кэшмагнит",    "url": "https://vk.cc/d1TFpv",
                   "reason_0": "Сложные случаи — их профиль. Без работы, без КИ, без проблем.",
                   "reason_bad": "Берут тех, кого другие отвергли.",
                   "tags": ["no_job","bad_credit","first_time"], "weight": 0.65},
    "dengi_srazu":{"name": "Деньги Сразу", "url": "https://vk.cc/d1TC6W",
                   "reason_0": "Минимум бюрократии — одобрение за 5 минут.",
                   "reason_bad": "Не требуют справок и поручителей.",
                   "tags": ["working","no_job","bad_credit"], "weight": 0.75},
    "migcredit":  {"name": "МигКредит",    "url": "https://vk.cc/d1TCL1",
                   "reason_0": "Лимиты до 100 000 ₽ — под крупные суммы.",
                   "reason_bad": "Для тех, кому нужна сумма побольше.",
                   "tags": ["working","good_credit","high_amount"], "weight": 0.85},
    "bystrodengi":{"name": "Быстроденьги", "url": "https://vk.cc/d1TBzn",
                   "reason_0": "Классика рынка — стабильно одобряют.",
                   "reason_bad": "Работают с разными категориями заёмщиков.",
                   "tags": ["working","freelance","good_credit"], "weight": 0.7},
    "beriberu":   {"name": "Бериберу",     "url": "https://vk.cc/d1TBkm",
                   "reason_0": "Простая анкета — минимум вопросов.",
                   "reason_bad": "Не заваливают проверками.",
                   "tags": ["freelance","no_job","bad_credit"], "weight": 0.65},
    "hurmacredit":{"name": "ХурмаКредит",  "url": "https://vk.cc/d1TzWz",
                   "reason_0": "Быстрое решение — для срочных случаев.",
                   "reason_bad": "Не требуют идеальной истории.",
                   "tags": ["freelance","student","good_credit"], "weight": 0.6},
    "davaka":     {"name": "Давака",       "url": "https://vk.cc/d1TEvz",
                   "reason_0": "Запасной вариант, который всегда под рукой.",
                   "reason_bad": "Если основные не подошли — этот точно сработает.",
                   "tags": ["student","no_job","bad_credit"], "weight": 0.55},
}

# Офферы для экрана «Займы под 0%»
ZERO_OFFERS = [
    ("🚀 Займер (0% до 30 000 ₽)",    "https://vk.cc/d1TuQm"),
    ("💳 Кредиска (0% до 30 000 ₽)",  "https://vk.cc/d1TwVC"),
    ("🏦 Webbankir (0% до 30 000 ₽)", "https://vk.cc/d1TDPS"),
    ("⚡ Турбозайм (0% до 30 000 ₽)", "https://vk.cc/d1TDw4"),
    ("🐰 BunnyMoney (0% до 9 000 ₽)", "https://vk.cc/d1TF5v"),
]

# ============================================================
#  ГИБКИЙ ПОДБОР ПО ТЕГАМ
# ============================================================
def get_offers_for_user(state: dict) -> list:
    status = state.get("status") or ""
    credit = state.get("credit") or ""
    amount = state.get("amount") or ""

    user_tags = []
    if status == "Студент":     user_tags.append("student")
    elif status == "Работаю":   user_tags.append("working")
    elif status == "Фриланс":   user_tags.append("freelance")
    elif status == "Без работы": user_tags.append("no_job")

    if credit == "Идеальная":         user_tags.append("good_credit")
    elif credit == "Были просрочки":  user_tags.append("bad_credit")
    elif credit == "Никогда не брал": user_tags.append("first_time")

    if amount == "50.000 – 100.000 ₽": user_tags.append("high_amount")
    elif amount == "до 15.000 ₽":       user_tags.append("low_amount")

    scored = []
    for key, offer in OFFERS.items():
        score = offer["weight"]
        for tag in offer["tags"]:
            if tag in user_tags: score += 1.0
        if credit == "Были просрочки" and "bad_credit" in offer["tags"]: score += 0.5
        if credit == "Никогда не брал" and "first_time" in offer["tags"]: score += 0.3
        if amount == "50.000 – 100.000 ₽" and "high_amount" in offer["tags"]: score += 0.4
        scored.append((score, key, offer))
    scored.sort(key=lambda x: x[0], reverse=True)

    result = []
    for score, key, offer in scored[:2]:
        rk = "reason_bad" if credit == "Были просрочки" else "reason_0"
        result.append({
            "name": offer["name"], "url": offer["url"],
            "reason": offer.get(rk, offer.get("reason_0", "")),
        })
    return result

# ============================================================
#  ХРАНИЛИЩЕ СОСТОЯНИЙ
# ============================================================
user_data = {}

def get_data(peer_id: int) -> dict:
    if peer_id not in user_data:
        user_data[peer_id] = {
            "step": None, "status": None, "credit": None,
            "amount": None, "phone": None, "name": None, "startedAt": None,
        }
    return user_data[peer_id]

# ============================================================
#  КЛАВИАТУРЫ
# ============================================================
def kb_start():
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("💸 Да, давай", payload={"cmd": "go"}), color=KeyboardButtonColor.POSITIVE)
    kb.row()
    kb.add(Text("🔥 Займы под 0%", payload={"cmd": "zero_loans"}), color=KeyboardButtonColor.SECONDARY)
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
    kb.row()
    kb.add(Text("🔥 Займы под 0%", payload={"cmd": "zero_loans"}), color=KeyboardButtonColor.SECONDARY)
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

def kb_big_ask():
    """Дверь в лоб: абсурдная анкета → откат к номеру."""
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("📱 Просто дам номер", payload={"cmd": "phone_start"}), color=KeyboardButtonColor.POSITIVE)
    kb.row()
    kb.add(Text("📄 Всё равно заполню анкету", payload={"cmd": "phone_start"}), color=KeyboardButtonColor.SECONDARY)
    return kb.get_json()

def kb_phone():
    kb = Keyboard(one_time=True, inline=False)
    kb.add(Text("📱 Отправить номер", payload={"cmd": "phone_hint"}), color=KeyboardButtonColor.PRIMARY)
    return kb.get_json()

def kb_main():
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("🔥 Займы под 0%", payload={"cmd": "zero_loans"}), color=KeyboardButtonColor.POSITIVE)
    kb.row()
    kb.add(Text("🏠 Начать заново", payload={"cmd": "restart"}), color=KeyboardButtonColor.SECONDARY)
    return kb.get_json()

def kb_zero_loans():
    kb = Keyboard(one_time=False, inline=False)
    for text, url in ZERO_OFFERS:
        kb.add(OpenLink(url, text), color=KeyboardButtonColor.PRIMARY)
        kb.row()
    kb.add(Text("🔙 В начало", payload={"cmd": "restart"}), color=KeyboardButtonColor.SECONDARY)
    return kb.get_json()

# ============================================================
#  ХЕЛПЕРЫ
# ============================================================
async def safe_get_name(message: Message) -> str:
    try:
        u = (await bot.api.users.get(user_ids=message.from_id))[0]
        return u.first_name or "друг"
    except Exception:
        return "друг"

def parse_payload(message: Message) -> str:
    p = getattr(message, "payload", None)
    if isinstance(p, dict):  return p.get("cmd") or ""
    if isinstance(p, str):
        try: return (json.loads(p) or {}).get("cmd") or ""
        except Exception: return ""
    return ""

def praise_for(status: str) -> str:
    return {
        "Студент":     "Студенты сейчас самые подкованные — многие МФО дают специальные условия.",
        "Работаю":     "С постоянным доходом тебе открыты почти все двери — это твой козырь.",
        "Фриланс":     "Фриланс — жёстко, но ты сам себе работодатель. Многие МФО это ценят.",
        "Без работы":  "Ничего страшного, это временно. Есть МФО, где одобряют и без 2-НДФЛ.",
    }.get(status, "")

def reflect_credit(credit: str) -> str:
    return {
        "Идеальная":       "Идеальная КИ — твой главный козырь, дадут лучшие условия.",
        "Были просрочки":  "С просрочками работают МФО с лояльным скорингом. Не переживай.",
        "Никогда не брал": "Чистая история — тоже плюс: увидят как нового и дадут 0%.",
    }.get(credit, "")

# ============================================================
#  ЭТАПЫ ВОРОНКИ
# ============================================================
async def send_welcome(message: Message, data: dict):
    data.update({"step": "status", "status": None, "credit": None,
                 "amount": None, "phone": None, "startedAt": datetime.now().isoformat()})
    await message.answer(
        "Супер ЗАЙМ 0% | MONEY BOT, привет.\n\n"
        "Если ты здесь — скорее всего, деньги нужны срочно: не хватает до зарплаты, "
        "банк отказал, или просто не хочется просить у знакомых.\n\n"
        "Я подбираю займы в МФО с лицензией ЦБ РФ. Одобрение — от 5 минут, деньги на карту. "
        "Без справок, без поручителей, без походов в офис.\n\n"
        "Три коротких вопроса — и я скажу, где тебе точно одобрят. Поехали?",
        keyboard=kb_start()
    )

async def step_status(message: Message, data: dict):
    data["step"] = "status"
    n = data["name"]
    await message.answer(
        f"{n}, первый вопрос — самый важный.\n\n"
        "Кто ты сейчас по статусу?\n\n"
        "Это не для проверки — это чтобы понять, куда тебе скорее всего одобрят. "
        "Студентам, фрилансерам и людям без официального дохода тоже дают, просто в других МФО.",
        keyboard=kb_status()
    )

async def step_credit(message: Message, data: dict):
    data["step"] = "credit"
    n = data["name"]
    await message.answer(
        f"Отлично, {n}. Идём дальше.\n\n"
        "Теперь про кредитную историю.\n\n"
        "Если были просрочки — это не приговор. Есть МФО, которые специально работают с такими клиентами. "
        "Просто у них чуть выше ставка, но одобрение приходит в тот же день.\n\n"
        "Как у тебя с КИ?",
        keyboard=kb_credit()
    )

async def step_amount(message: Message, data: dict):
    data["step"] = "amount"
    n = data["name"]
    await message.answer(
        f"{n}, понял. {reflect_credit(data['credit'])}\n\n"
        "Сколько нужно? Выбери диапазон — подберу МФО, где лимиты начинаются именно с таких сумм.\n\n"
        "Совет: бери ровно столько, сколько нужно, и на срок, который точно закроешь. "
        "Тогда переплата будет минимальной.",
        keyboard=kb_amount()
    )

async def step_confirm(message: Message, data: dict):
    data["step"] = "confirm"
    n = data["name"]
    # Рефлексивное слушание — пересказ всех ответов
    await message.answer(
        f"Итак, {n}, всё сходится:\n"
        f"• Статус: {data['status']}\n"
        f"• КИ: {data['credit']}\n"
        f"• Сумма: {data['amount']}\n\n"
        "Всё верно?",
        keyboard=kb_confirm()
    )

async def step_big_ask(message: Message, data: dict):
    """Дверь в лоб: абсурдная анкета → откат к номеру."""
    data["step"] = "big_ask"
    n = data["name"]
    await message.answer(
        f"{n}, для максимально точного подбора мне бы пригодилась полная анкета:\n\n"
        "• Паспорт (все страницы)\n"
        "• СНИЛС и ИНН\n"
        "• Справка 2-НДФЛ за полгода\n"
        "• Селфи с паспортом в руке\n"
        "• Выписка по карте за 3 месяца\n\n"
        "Но давай не будем так усложнять. Хватит просто номера телефона — "
        "этого достаточно для 90% случаев.",
        keyboard=kb_big_ask()
    )

async def step_phone(message: Message, data: dict):
    data["step"] = "phone"
    n = data["name"]
    await message.answer(
        f"{n}, отлично.\n\n"
        "Оставь номер телефона — пришлю подборку под тебя лично.\n\n"
        "🔒 По этому номеру мы не звоним без твоего согласия. Только чтобы отправить ссылку.\n\n"
        "Напиши в формате +7 900 123-45-67.",
        keyboard=kb_phone()
    )

async def step_final(message: Message, data: dict):
    n = data["name"]
    offers = get_offers_for_user(data)
    if not offers:
        await message.answer("Не удалось подобрать оффер. Попробуй /start заново.")
        return
    primary, backup = offers[0], (offers[1] if len(offers) > 1 else None)

    msg = (
        f"{n}, ты сделал 4 шага из 4 — красава. Вот твой вариант:\n\n"
        f"🏆 {primary['name']}\n"
        f"💡 {primary['reason']}\n"
        f"👉 {primary['url']}\n\n"
    )
    if backup:
        msg += f"🔄 Запасной вариант (если этот не подойдёт):\n👉 {backup['url']}\n\n"
    msg += (
        "Что делать прямо сейчас:\n"
        "1️⃣ Открой ссылку\n"
        "2️⃣ Заполни анкету (2–3 минуты)\n"
        "3️⃣ Дождись одобрения — обычно 5–15 минут\n"
        "4️⃣ Деньги упадут на карту в тот же день\n\n"
        "⚡ Ставки 0% для новых клиентов ограничены во времени — лучше сейчас.\n\n"
        "⚠️ Реклама. ПСК от 0% до 292% годовых. Оценивайте риски."
    )
    data["step"] = "done"
    await message.answer(msg, keyboard=kb_main())

async def step_zero_loans(message: Message, data: dict):
    n = data["name"]
    await message.answer(
        f"{n}, вот займы под 0% для новых клиентов.\n\n"
        "Это предложения, где первый займ можно взять без процентов — "
        "возвращаешь ровно ту сумму, которую взял.\n\n"
        "Как не переплатить:\n"
        "1️⃣ Бери только ту сумму, которую точно вернёшь.\n"
        "2️⃣ Верни в срок — обычно 7–30 дней. Просрочка обнуляет льготу.\n"
        "3️⃣ Проверь ПСК в договоре.\n"
        "4️⃣ Не подключай платные доп. услуги.\n\n"
        "👇 Выбирай МФО:",
        keyboard=kb_zero_loans()
    )

# ============================================================
#  ЕДИНЫЙ РОУТЕР
# ============================================================
@bot.on.message()
async def main_router(message: Message):
    peer_id = message.peer_id
    data = get_data(peer_id)
    if not data.get("name"):
        data["name"] = await safe_get_name(message)

    text = (message.text or "").strip()
    cmd = parse_payload(message)
    name = data["name"]

    # ---- /start ИЛИ ПЕРВОЕ СООБЩЕНИЕ → приветствие ----
    if not data.get("step") or text.lower().startswith("/start"):
        await send_welcome(message, data)
        return

    # ---- PAYLOAD-КОМАНДЫ ----
    if cmd == "go":
        await step_status(message, data); return

    if cmd in ("status_student","status_working","status_freelance","status_nojob"):
        data["status"] = {
            "status_student":"Студент","status_working":"Работаю",
            "status_freelance":"Фриланс","status_nojob":"Без работы"
        }[cmd]
        await message.answer(f"{name}, зафиксировал: {data['status']}. {praise_for(data['status'])}")
        await step_credit(message, data); return

    if cmd in ("credit_good","credit_bad","credit_none"):
        data["credit"] = {
            "credit_good":"Идеальная","credit_bad":"Были просрочки","credit_none":"Никогда не брал"
        }[cmd]
        await step_amount(message, data); return

    if cmd in ("amount_low","amount_mid","amount_high"):
        data["amount"] = {
            "amount_low":"до 15.000 ₽","amount_mid":"15.000 – 50.000 ₽",
            "amount_high":"50.000 – 100.000 ₽"
        }[cmd]
        await step_confirm(message, data); return

    if cmd == "confirm_yes":
        await step_big_ask(message, data); return

    if cmd == "confirm_edit":
        data.update({"status": None, "credit": None, "amount": None})
        await send_welcome(message, data); return

    if cmd in ("phone_start", "phone_hint"):
        await step_phone(message, data); return

    if cmd == "zero_loans":
        await step_zero_loans(message, data); return

    if cmd == "restart":
        await send_welcome(message, data); return

    # ---- ВВОД ТЕЛЕФОНА ----
    if data.get("step") == "phone":
        digits = re.sub(r"\D", "", text)
        if len(digits) >= 10:
            data["phone"] = text
            await step_final(message, data)
        else:
            await message.answer(f"{name}, формат немного другой. Скинь так: +7 900 123-45-67")
        return

    # ---- ТЕКСТ ВМЕСТО ТАПА НА ДРУГИХ ШАГАХ ----
    step = data.get("step")
    if step == "status":
        await message.answer(f"{name}, выбери, пожалуйста, кнопкой ниже 👇", keyboard=kb_status()); return
    if step == "credit":
        await message.answer(f"{name}, выбери, пожалуйста, кнопкой ниже 👇", keyboard=kb_credit()); return
    if step == "amount":
        await message.answer(f"{name}, выбери, пожалуйста, кнопкой ниже 👇", keyboard=kb_amount()); return
    if step == "confirm":
        await message.answer(f"{name}, подтверди, пожалуйста, кнопкой ниже 👇", keyboard=kb_confirm()); return
    if step == "big_ask":
        await message.answer(f"{name}, тапни кнопку ниже 👇", keyboard=kb_big_ask()); return

    # ---- FALLBACK ----
    await send_welcome(message, data)

# ============================================================
#  ЗАПУСК
# ============================================================
if __name__ == "__main__":
    bot.run_forever() vk1.a.AOyP3eRdxp8yz4R6iUbbTN6xkTkwVkxfBSzNYeycoGh9VGJLMTrg6mj1ndPWoF9Gbd7XEAcl7VIFTLvM9qa33LqPyy5R-5qjRNsca0Q-9naOTm9W_n437r7RM3LKrWtYvo1CVj9CS0_D6bGqstOvsUsbF_jxxSAXBF4IzXUP3MKjW_iiwJJEr6FqgHEo_pnrY_aEjclWJzPbQS_JhZKVJw"    # ← ЗАМЕНИ на свой токен
GROUP_ID    = 38935595

bot = Bot(token=GROUP_TOKEN)
bot.labeler.vbml_ignore_case = True

# ============================================================
#  БАЗА ОФФЕРОВ
# ============================================================
OFFERS = {
    "zaymigo":    {"name": "Займер",       "url": "https://vk.cc/d1TuQm",
                   "reason_0": "Первый займ под 0% — возвращаешь ровно столько, сколько взял.",
                   "reason_bad": "Дают даже с испорченной КИ — главное, без открытых просрочек.",
                   "tags": ["student","working","freelance","good_credit","first_time"], "weight": 0.9},
    "dobrozaym":  {"name": "ДоброЗайм",    "url": "https://vk.cc/d1TvN1",
                   "reason_0": "Лояльный скоринг — одобряют там, где банки отказали.",
                   "reason_bad": "Специально работают с просрочками — не отказывают автоматом.",
                   "tags": ["working","freelance","bad_credit","no_job"], "weight": 0.85},
    "krediska":   {"name": "Кредиска",     "url": "https://vk.cc/d1TwVC",
                   "reason_0": "0% на первый займ — для тех, кто берёт впервые.",
                   "reason_bad": "Гибкие условия для сложных случаев.",
                   "tags": ["student","first_time","good_credit"], "weight": 0.8},
    "webbankir":  {"name": "Webbankir",    "url": "https://vk.cc/d1TDPS",
                   "reason_0": "Стабильно одобряют студентам и без официального дохода.",
                   "reason_bad": "Лояльны к КИ — работают с просрочками до 90 дней.",
                   "tags": ["student","no_job","bad_credit","freelance"], "weight": 0.75},
    "turbozaym":  {"name": "Турбозайм",    "url": "https://vk.cc/d1TDw4",
                   "reason_0": "0% первые 7 дней — успеваешь вернуть без переплаты.",
                   "reason_bad": "Быстрое решение даже при плохой истории.",
                   "tags": ["freelance","working","good_credit","first_time"], "weight": 0.7},
    "bunnymoney": {"name": "BunnyMoney",   "url": "https://vk.cc/d1TF5v",
                   "reason_0": "Работает без 2-НДФЛ — для фрилансеров и самозанятых.",
                   "reason_bad": "Одобряют с минимальным пакетом документов.",
                   "tags": ["freelance","student","no_job","bad_credit"], "weight": 0.7},
    "cashmagnet": {"name": "Кэшмагнит",    "url": "https://vk.cc/d1TFpv",
                   "reason_0": "Сложные случаи — их профиль. Без работы, без КИ, без проблем.",
                   "reason_bad": "Берут тех, кого другие отвергли.",
                   "tags": ["no_job","bad_credit","first_time"], "weight": 0.65},
    "dengi_srazu":{"name": "Деньги Сразу", "url": "https://vk.cc/d1TC6W",
                   "reason_0": "Минимум бюрократии — одобрение за 5 минут.",
                   "reason_bad": "Не требуют справок и поручителей.",
                   "tags": ["working","no_job","bad_credit"], "weight": 0.75},
    "migcredit":  {"name": "МигКредит",    "url": "https://vk.cc/d1TCL1",
                   "reason_0": "Лимиты до 100 000 ₽ — под крупные суммы.",
                   "reason_bad": "Для тех, кому нужна сумма побольше.",
                   "tags": ["working","good_credit","high_amount"], "weight": 0.85},
    "bystrodengi":{"name": "Быстроденьги", "url": "https://vk.cc/d1TBzn",
                   "reason_0": "Классика рынка — стабильно одобряют.",
                   "reason_bad": "Работают с разными категориями заёмщиков.",
                   "tags": ["working","freelance","good_credit"], "weight": 0.7},
    "beriberu":   {"name": "Бериберу",     "url": "https://vk.cc/d1TBkm",
                   "reason_0": "Простая анкета — минимум вопросов.",
                   "reason_bad": "Не заваливают проверками.",
                   "tags": ["freelance","no_job","bad_credit"], "weight": 0.65},
    "hurmacredit":{"name": "ХурмаКредит",  "url": "https://vk.cc/d1TzWz",
                   "reason_0": "Быстрое решение — для срочных случаев.",
                   "reason_bad": "Не требуют идеальной истории.",
                   "tags": ["freelance","student","good_credit"], "weight": 0.6},
    "davaka":     {"name": "Давака",       "url": "https://vk.cc/d1TEvz",
                   "reason_0": "Запасной вариант, который всегда под рукой.",
                   "reason_bad": "Если основные не подошли — этот точно сработает.",
                   "tags": ["student","no_job","bad_credit"], "weight": 0.55},
}

# Офферы для экрана «Займы под 0%»
ZERO_OFFERS = [
    ("🚀 Займер (0% до 30 000 ₽)",    "https://vk.cc/d1TuQm"),
    ("💳 Кредиска (0% до 30 000 ₽)",  "https://vk.cc/d1TwVC"),
    ("🏦 Webbankir (0% до 30 000 ₽)", "https://vk.cc/d1TDPS"),
    ("⚡ Турбозайм (0% до 30 000 ₽)", "https://vk.cc/d1TDw4"),
    ("🐰 BunnyMoney (0% до 9 000 ₽)", "https://vk.cc/d1TF5v"),
]

# ============================================================
#  ГИБКИЙ ПОДБОР ПО ТЕГАМ
# ============================================================
def get_offers_for_user(state: dict) -> list:
    status = state.get("status") or ""
    credit = state.get("credit") or ""
    amount = state.get("amount") or ""

    user_tags = []
    if status == "Студент":     user_tags.append("student")
    elif status == "Работаю":   user_tags.append("working")
    elif status == "Фриланс":   user_tags.append("freelance")
    elif status == "Без работы": user_tags.append("no_job")

    if credit == "Идеальная":         user_tags.append("good_credit")
    elif credit == "Были просрочки":  user_tags.append("bad_credit")
    elif credit == "Никогда не брал": user_tags.append("first_time")

    if amount == "50.000 – 100.000 ₽": user_tags.append("high_amount")
    elif amount == "до 15.000 ₽":       user_tags.append("low_amount")

    scored = []
    for key, offer in OFFERS.items():
        score = offer["weight"]
        for tag in offer["tags"]:
            if tag in user_tags: score += 1.0
        if credit == "Были просрочки" and "bad_credit" in offer["tags"]: score += 0.5
        if credit == "Никогда не брал" and "first_time" in offer["tags"]: score += 0.3
        if amount == "50.000 – 100.000 ₽" and "high_amount" in offer["tags"]: score += 0.4
        scored.append((score, key, offer))
    scored.sort(key=lambda x: x[0], reverse=True)

    result = []
    for score, key, offer in scored[:2]:
        rk = "reason_bad" if credit == "Были просрочки" else "reason_0"
        result.append({
            "name": offer["name"], "url": offer["url"],
            "reason": offer.get(rk, offer.get("reason_0", "")),
        })
    return result

# ============================================================
#  ХРАНИЛИЩЕ СОСТОЯНИЙ
# ============================================================
user_data = {}

def get_data(peer_id: int) -> dict:
    if peer_id not in user_data:
        user_data[peer_id] = {
            "step": None, "status": None, "credit": None,
            "amount": None, "phone": None, "name": None, "startedAt": None,
        }
    return user_data[peer_id]

# ============================================================
#  КЛАВИАТУРЫ
# ============================================================
def kb_start():
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("💸 Да, давай", payload={"cmd": "go"}), color=KeyboardButtonColor.POSITIVE)
    kb.row()
    kb.add(Text("🔥 Займы под 0%", payload={"cmd": "zero_loans"}), color=KeyboardButtonColor.SECONDARY)
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
    kb.row()
    kb.add(Text("🔥 Займы под 0%", payload={"cmd": "zero_loans"}), color=KeyboardButtonColor.SECONDARY)
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

def kb_big_ask():
    """Дверь в лоб: абсурдная анкета → откат к номеру."""
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("📱 Просто дам номер", payload={"cmd": "phone_start"}), color=KeyboardButtonColor.POSITIVE)
    kb.row()
    kb.add(Text("📄 Всё равно заполню анкету", payload={"cmd": "phone_start"}), color=KeyboardButtonColor.SECONDARY)
    return kb.get_json()

def kb_phone():
    kb = Keyboard(one_time=True, inline=False)
    kb.add(Text("📱 Отправить номер", payload={"cmd": "phone_hint"}), color=KeyboardButtonColor.PRIMARY)
    return kb.get_json()

def kb_main():
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("🔥 Займы под 0%", payload={"cmd": "zero_loans"}), color=KeyboardButtonColor.POSITIVE)
    kb.row()
    kb.add(Text("🏠 Начать заново", payload={"cmd": "restart"}), color=KeyboardButtonColor.SECONDARY)
    return kb.get_json()

def kb_zero_loans():
    kb = Keyboard(one_time=False, inline=False)
    for text, url in ZERO_OFFERS:
        kb.add(OpenLink(url, text), color=KeyboardButtonColor.PRIMARY)
        kb.row()
    kb.add(Text("🔙 В начало", payload={"cmd": "restart"}), color=KeyboardButtonColor.SECONDARY)
    return kb.get_json()

# ============================================================
#  ХЕЛПЕРЫ
# ============================================================
async def safe_get_name(message: Message) -> str:
    try:
        u = (await bot.api.users.get(user_ids=message.from_id))[0]
        return u.first_name or "друг"
    except Exception:
        return "друг"

def parse_payload(message: Message) -> str:
    p = getattr(message, "payload", None)
    if isinstance(p, dict):  return p.get("cmd") or ""
    if isinstance(p, str):
        try: return (json.loads(p) or {}).get("cmd") or ""
        except Exception: return ""
    return ""

def praise_for(status: str) -> str:
    return {
        "Студент":     "Студенты сейчас самые подкованные — многие МФО дают специальные условия.",
        "Работаю":     "С постоянным доходом тебе открыты почти все двери — это твой козырь.",
        "Фриланс":     "Фриланс — жёстко, но ты сам себе работодатель. Многие МФО это ценят.",
        "Без работы":  "Ничего страшного, это временно. Есть МФО, где одобряют и без 2-НДФЛ.",
    }.get(status, "")

def reflect_credit(credit: str) -> str:
    return {
        "Идеальная":       "Идеальная КИ — твой главный козырь, дадут лучшие условия.",
        "Были просрочки":  "С просрочками работают МФО с лояльным скорингом. Не переживай.",
        "Никогда не брал": "Чистая история — тоже плюс: увидят как нового и дадут 0%.",
    }.get(credit, "")

# ============================================================
#  ЭТАПЫ ВОРОНКИ
# ============================================================
async def send_welcome(message: Message, data: dict):
    data.update({"step": "status", "status": None, "credit": None,
                 "amount": None, "phone": None, "startedAt": datetime.now().isoformat()})
    await message.answer(
        "Супер ЗАЙМ 0% | MONEY BOT, привет.\n\n"
        "Если ты здесь — скорее всего, деньги нужны срочно: не хватает до зарплаты, "
        "банк отказал, или просто не хочется просить у знакомых.\n\n"
        "Я подбираю займы в МФО с лицензией ЦБ РФ. Одобрение — от 5 минут, деньги на карту. "
        "Без справок, без поручителей, без походов в офис.\n\n"
        "Три коротких вопроса — и я скажу, где тебе точно одобрят. Поехали?",
        keyboard=kb_start()
    )

async def step_status(message: Message, data: dict):
    data["step"] = "status"
    n = data["name"]
    await message.answer(
        f"{n}, первый вопрос — самый важный.\n\n"
        "Кто ты сейчас по статусу?\n\n"
        "Это не для проверки — это чтобы понять, куда тебе скорее всего одобрят. "
        "Студентам, фрилансерам и людям без официального дохода тоже дают, просто в других МФО.",
        keyboard=kb_status()
    )

async def step_credit(message: Message, data: dict):
    data["step"] = "credit"
    n = data["name"]
    await message.answer(
        f"Отлично, {n}. Идём дальше.\n\n"
        "Теперь про кредитную историю.\n\n"
        "Если были просрочки — это не приговор. Есть МФО, которые специально работают с такими клиентами. "
        "Просто у них чуть выше ставка, но одобрение приходит в тот же день.\n\n"
        "Как у тебя с КИ?",
        keyboard=kb_credit()
    )

async def step_amount(message: Message, data: dict):
    data["step"] = "amount"
    n = data["name"]
    await message.answer(
        f"{n}, понял. {reflect_credit(data['credit'])}\n\n"
        "Сколько нужно? Выбери диапазон — подберу МФО, где лимиты начинаются именно с таких сумм.\n\n"
        "Совет: бери ровно столько, сколько нужно, и на срок, который точно закроешь. "
        "Тогда переплата будет минимальной.",
        keyboard=kb_amount()
    )

async def step_confirm(message: Message, data: dict):
    data["step"] = "confirm"
    n = data["name"]
    # Рефлексивное слушание — пересказ всех ответов
    await message.answer(
        f"Итак, {n}, всё сходится:\n"
        f"• Статус: {data['status']}\n"
        f"• КИ: {data['credit']}\n"
        f"• Сумма: {data['amount']}\n\n"
        "Всё верно?",
        keyboard=kb_confirm()
    )

async def step_big_ask(message: Message, data: dict):
    """Дверь в лоб: абсурдная анкета → откат к номеру."""
    data["step"] = "big_ask"
    n = data["name"]
    await message.answer(
        f"{n}, для максимально точного подбора мне бы пригодилась полная анкета:\n\n"
        "• Паспорт (все страницы)\n"
        "• СНИЛС и ИНН\n"
        "• Справка 2-НДФЛ за полгода\n"
        "• Селфи с паспортом в руке\n"
        "• Выписка по карте за 3 месяца\n\n"
        "Но давай не будем так усложнять. Хватит просто номера телефона — "
        "этого достаточно для 90% случаев.",
        keyboard=kb_big_ask()
    )

async def step_phone(message: Message, data: dict):
    data["step"] = "phone"
    n = data["name"]
    await message.answer(
        f"{n}, отлично.\n\n"
        "Оставь номер телефона — пришлю подборку под тебя лично.\n\n"
        "🔒 По этому номеру мы не звоним без твоего согласия. Только чтобы отправить ссылку.\n\n"
        "Напиши в формате +7 900 123-45-67.",
        keyboard=kb_phone()
    )

async def step_final(message: Message, data: dict):
    n = data["name"]
    offers = get_offers_for_user(data)
    if not offers:
        await message.answer("Не удалось подобрать оффер. Попробуй /start заново.")
        return
    primary, backup = offers[0], (offers[1] if len(offers) > 1 else None)

    msg = (
        f"{n}, ты сделал 4 шага из 4 — красава. Вот твой вариант:\n\n"
        f"🏆 {primary['name']}\n"
        f"💡 {primary['reason']}\n"
        f"👉 {primary['url']}\n\n"
    )
    if backup:
        msg += f"🔄 Запасной вариант (если этот не подойдёт):\n👉 {backup['url']}\n\n"
    msg += (
        "Что делать прямо сейчас:\n"
        "1️⃣ Открой ссылку\n"
        "2️⃣ Заполни анкету (2–3 минуты)\n"
        "3️⃣ Дождись одобрения — обычно 5–15 минут\n"
        "4️⃣ Деньги упадут на карту в тот же день\n\n"
        "⚡ Ставки 0% для новых клиентов ограничены во времени — лучше сейчас.\n\n"
        "⚠️ Реклама. ПСК от 0% до 292% годовых. Оценивайте риски."
    )
    data["step"] = "done"
    await message.answer(msg, keyboard=kb_main())

async def step_zero_loans(message: Message, data: dict):
    n = data["name"]
    await message.answer(
        f"{n}, вот займы под 0% для новых клиентов.\n\n"
        "Это предложения, где первый займ можно взять без процентов — "
        "возвращаешь ровно ту сумму, которую взял.\n\n"
        "Как не переплатить:\n"
        "1️⃣ Бери только ту сумму, которую точно вернёшь.\n"
        "2️⃣ Верни в срок — обычно 7–30 дней. Просрочка обнуляет льготу.\n"
        "3️⃣ Проверь ПСК в договоре.\n"
        "4️⃣ Не подключай платные доп. услуги.\n\n"
        "👇 Выбирай МФО:",
        keyboard=kb_zero_loans()
    )

# ============================================================
#  ЕДИНЫЙ РОУТЕР
# ============================================================
@bot.on.message()
async def main_router(message: Message):
    peer_id = message.peer_id
    data = get_data(peer_id)
    if not data.get("name"):
        data["name"] = await safe_get_name(message)

    text = (message.text or "").strip()
    cmd = parse_payload(message)
    name = data["name"]

    # ---- /start ИЛИ ПЕРВОЕ СООБЩЕНИЕ → приветствие ----
    if not data.get("step") or text.lower().startswith("/start"):
        await send_welcome(message, data)
        return

    # ---- PAYLOAD-КОМАНДЫ ----
    if cmd == "go":
        await step_status(message, data); return

    if cmd in ("status_student","status_working","status_freelance","status_nojob"):
        data["status"] = {
            "status_student":"Студент","status_working":"Работаю",
            "status_freelance":"Фриланс","status_nojob":"Без работы"
        }[cmd]
        await message.answer(f"{name}, зафиксировал: {data['status']}. {praise_for(data['status'])}")
        await step_credit(message, data); return

    if cmd in ("credit_good","credit_bad","credit_none"):
        data["credit"] = {
            "credit_good":"Идеальная","credit_bad":"Были просрочки","credit_none":"Никогда не брал"
        }[cmd]
        await step_amount(message, data); return

    if cmd in ("amount_low","amount_mid","amount_high"):
        data["amount"] = {
            "amount_low":"до 15.000 ₽","amount_mid":"15.000 – 50.000 ₽",
            "amount_high":"50.000 – 100.000 ₽"
        }[cmd]
        await step_confirm(message, data); return

    if cmd == "confirm_yes":
        await step_big_ask(message, data); return

    if cmd == "confirm_edit":
        data.update({"status": None, "credit": None, "amount": None})
        await send_welcome(message, data); return

    if cmd in ("phone_start", "phone_hint"):
        await step_phone(message, data); return

    if cmd == "zero_loans":
        await step_zero_loans(message, data); return

    if cmd == "restart":
        await send_welcome(message, data); return

    # ---- ВВОД ТЕЛЕФОНА ----
    if data.get("step") == "phone":
        digits = re.sub(r"\D", "", text)
        if len(digits) >= 10:
            data["phone"] = text
            await step_final(message, data)
        else:
            await message.answer(f"{name}, формат немного другой. Скинь так: +7 900 123-45-67")
        return

    # ---- ТЕКСТ ВМЕСТО ТАПА НА ДРУГИХ ШАГАХ ----
    step = data.get("step")
    if step == "status":
        await message.answer(f"{name}, выбери, пожалуйста, кнопкой ниже 👇", keyboard=kb_status()); return
    if step == "credit":
        await message.answer(f"{name}, выбери, пожалуйста, кнопкой ниже 👇", keyboard=kb_credit()); return
    if step == "amount":
        await message.answer(f"{name}, выбери, пожалуйста, кнопкой ниже 👇", keyboard=kb_amount()); return
    if step == "confirm":
        await message.answer(f"{name}, подтверди, пожалуйста, кнопкой ниже 👇", keyboard=kb_confirm()); return
    if step == "big_ask":
        await message.answer(f"{name}, тапни кнопку ниже 👇", keyboard=kb_big_ask()); return

    # ---- FALLBACK ----
    await send_welcome(message, data)

# ============================================================
#  ЗАПУСК
# ============================================================
if __name__ == "__main__":
    bot.run_forever()
