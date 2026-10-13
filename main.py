# ============================================================
#  VK BOT — СУПЕР ЗАЙМ 0% | MONEY BOT  v7.0
#  Фреймворк: vkbottle | Long Poll API
#  Без шага телефона. Результат сразу после суммы.
# ============================================================

import json
from datetime import datetime

from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink

# ================= НАСТРОЙКИ =================
GROUP_TOKEN = "vk1.a.ТВОЙ_ТОКЕН_СЮДА"    # ← ЗАМЕНИ на свой токен
GROUP_ID    = 38935595

bot = Bot(token=GROUP_TOKEN)
bot.labeler.vbml_ignore_case = True

# ============================================================
#  БАЗА ПАРТНЁРОВ (17 офферов)
# ============================================================
OFFERS = {
    "zaymigo":     {"name": "Займер",       "url": "https://vk.cc/d1TuQm",
                    "reason": "Первый продукт под 0% для новых клиентов."},
    "dobrozaym":   {"name": "Доброзайм",    "url": "https://vk.cc/d1TvN1",
                    "reason": "Лояльный скоринг и гибкие условия оформления."},
    "krediska":    {"name": "Кредиска",     "url": "https://vk.cc/d1TwVC",
                    "reason": "0% на первый продукт для новых клиентов."},
    "webbankir":   {"name": "Webbankir",    "url": "https://vk.cc/d1TDPS",
                    "reason": "Стабильно одобряют студентам и без официального дохода."},
    "turbozaym":   {"name": "Турбозайм",    "url": "https://vk.cc/d1TDw4",
                    "reason": "0% первые 7 дней — успеваешь закрыть без переплаты."},
    "bunnymoney":  {"name": "BunnyMoney",   "url": "https://vk.cc/d1TF5v",
                    "reason": "Работает без 2-НДФЛ — для фрилансеров и самозанятых."},
    "cashmagnet":  {"name": "Кэшмагнит",    "url": "https://vk.cc/d1TFpv",
                    "reason": "Специализируется на сложных случаях — без работы и без истории."},
    "dengi_srazu": {"name": "Деньги Сразу", "url": "https://vk.cc/d1TC6W",
                    "reason": "Минимум бюрократии — решение за 5 минут."},
    "migcredit":   {"name": "МигКредит",    "url": "https://vk.cc/d1TCL1",
                    "reason": "Лимиты до 100 000 ₽ — под крупные цели."},
    "bystrodengi": {"name": "Быстроденьги", "url": "https://vk.cc/d1TBzn",
                    "reason": "Классика рынка — стабильные одобрения."},
    "beriberu":    {"name": "Бериберу",     "url": "https://vk.cc/d1TBkm",
                    "reason": "Простая анкета — минимум вопросов."},
    "hurmacredit": {"name": "ХурмаКредит",  "url": "https://vk.cc/d1TzWz",
                    "reason": "Быстрое решение для срочных случаев."},
    "davaka":      {"name": "Давака",       "url": "https://vk.cc/d1TEvz",
                    "reason": "Запасной вариант, который всегда под рукой."},
    "snapcredit":  {"name": "Snapcredit",   "url": "https://vk.cc/d2SmVe",
                    "reason": "Мгновенное решение до 15 минут с переводом по СБП. Идеально, когда счёт идёт на минуты."},
    "denga":       {"name": "Деньга",       "url": "https://vk.cc/d2Snd9",
                    "reason": "Надёжный партнёр для крупных целей: лимиты до 200 000 ₽, долгие сроки и минимум бюрократии."},
    "smsfinance":  {"name": "СМС ФИНАНС",   "url": "https://vk.cc/d2SnMv",
                    "reason": "Лояльный скоринг и специальные программы для восстановления финансовой репутации."},
}

# Продукты под 0% — экран-витрина
ZERO_OFFERS = [
    ("🚀 Snapcredit (0% до 20 000 ₽)", "https://vk.cc/d2SmVe"),
    ("💳 Кредиска (0% до 30 000 ₽)",   "https://vk.cc/d1TwVC"),
    ("🏦 Webbankir (0% до 30 000 ₽)",  "https://vk.cc/d1TDPS"),
    ("⚡ Турбозайм (0% до 30 000 ₽)",  "https://vk.cc/d1TDw4"),
    ("🐰 BunnyMoney (0% до 9 000 ₽)",  "https://vk.cc/d1TF5v"),
]

# ============================================================
#  РОУТИНГ ПО ЦА — 4 сегмента, по ТЗ
# ============================================================
def get_offers_for_user(state: dict):
    s = state.get("status")
    c = state.get("credit")
    a = state.get("amount")

    good  = c in ("Идеальная", "Никогда не брал")
    bad   = c == "Были просрочки"
    small = a == "до 15.000 ₽"
    big   = a == "50.000 – 100.000 ₽"

    if s == "Студент":
        if good and small:
            return OFFERS["snapcredit"], OFFERS["zaymigo"]
        if good:
            return OFFERS["zaymigo"], OFFERS["krediska"]
        return OFFERS["smsfinance"], OFFERS["webbankir"]

    if s == "Работаю":
        if big:
            return OFFERS["denga"], OFFERS["migcredit"]
        if bad:
            return OFFERS["dobrozaym"], OFFERS["dengi_srazu"]
        return OFFERS["migcredit"], OFFERS["bystrodengi"]

    if s == "Фриланс":
        if bad:
            return OFFERS["smsfinance"], OFFERS["bunnymoney"]
        return OFFERS["snapcredit"], OFFERS["turbozaym"]

    if s == "Без работы":
        if bad:
            return OFFERS["cashmagnet"], OFFERS["smsfinance"]
        return OFFERS["dobrozaym"], OFFERS["dengi_srazu"]

    return OFFERS["zaymigo"], OFFERS["krediska"]

# ============================================================
#  РЕЙТИНГ ОДОБРЕНИЯ
# ============================================================
def calc_approval(state: dict) -> int:
    s = state.get("status")
    c = state.get("credit")
    if s == "Работаю" and c == "Идеальная":
        return 96
    if c == "Идеальная":
        base = 94
    elif c == "Были просрочки":
        base = 72
    else:
        base = 87
    if s == "Студент":
        base -= 5
    return base

# ============================================================
#  СРОЧНОСТЬ
# ============================================================
def hours_left_today() -> int:
    return max(1, 24 - datetime.now().hour)

# ============================================================
#  ХРАНИЛИЩЕ СОСТОЯНИЙ
# ============================================================
user_data = {}

def get_data(peer_id: int) -> dict:
    if peer_id not in user_data:
        user_data[peer_id] = {
            "step": None, "status": None, "credit": None,
            "amount": None, "name": None, "startedAt": None,
            "rating": None, "partner": None, "partner_url": None,
        }
    return user_data[peer_id]

# ============================================================
#  КЛАВИАТУРЫ
# ============================================================
def kb_start():
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("💸 Да, давай", payload={"cmd": "go"}), color=KeyboardButtonColor.POSITIVE)
    kb.row()
    kb.add(Text("🔥 Продукты под 0%", payload={"cmd": "zero_loans"}), color=KeyboardButtonColor.SECONDARY)
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
    kb.add(Text("🔥 Продукты под 0%", payload={"cmd": "zero_loans"}), color=KeyboardButtonColor.SECONDARY)
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

def kb_main():
    kb = Keyboard(one_time=False, inline=False)
    kb.add(Text("🏠 Пройти заново", payload={"cmd": "restart"}), color=KeyboardButtonColor.PRIMARY)
    return kb.get_json()

def kb_zero_loans():
    kb = Keyboard(one_time=False, inline=False)
    for label, url in ZERO_OFFERS:
        kb.add(OpenLink(url, label), color=KeyboardButtonColor.PRIMARY)
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
    if isinstance(p, dict):
        return p.get("cmd") or ""
    if isinstance(p, str):
        try:
            return (json.loads(p) or {}).get("cmd") or ""
        except Exception:
            return ""
    return ""

def praise_for(status: str) -> str:
    return {
        "Студент":     "Студенты сейчас самые подкованные — многие партнёры дают специальные условия.",
        "Работаю":     "С постоянным доходом тебе открыты почти все двери — это твой козырь.",
        "Фриланс":     "Фриланс — жёстко, но ты сам себе работодатель. Многие партнёры это ценят.",
        "Без работы":  "Ничего страшного, это временно. Есть партнёры, где одобряют и без 2-НДФЛ.",
    }.get(status, "")

def reflect_credit(credit: str) -> str:
    return {
        "Идеальная":       "Идеальная КИ — твой главный козырь, дадут лучшие условия.",
        "Были просрочки":  "С просрочками работают партнёры с лояльным скорингом. Не переживай.",
        "Никогда не брал": "Чистая история — тоже плюс: увидят как нового клиента и дадут 0%.",
    }.get(credit, "")

# ============================================================
#  ЭТАПЫ ВОРОНКИ
# ============================================================
async def send_welcome(message: Message, data: dict):
    data.update({
        "step": "status", "status": None, "credit": None,
        "amount": None, "startedAt": datetime.now().isoformat(),
        "rating": None, "partner": None, "partner_url": None,
    })
    await message.answer(
        "Супер ЗАЙМ 0% | MONEY BOT, привет.\n\n"
        "Если ты здесь — скорее всего, средства нужны срочно: не хватает до зарплаты, "
        "банк отказал, или просто не хочется просить у знакомых.\n\n"
        "Я подбираю финансовые решения у партнёров с лицензией ЦБ РФ. Одобрение — от 5 минут, "
        "средства на карту. Без справок, без поручителей, без походов в офис.\n\n"
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
        "Студентам, фрилансерам и людям без официального дохода тоже дают, просто у других партнёров.",
        keyboard=kb_status()
    )

async def step_credit(message: Message, data: dict):
    data["step"] = "credit"
    n = data["name"]
    await message.answer(
        f"Отлично, {n}. Идём дальше.\n\n"
        "Теперь про кредитную историю.\n\n"
        "Если были просрочки — это не приговор. Есть партнёры, которые специально работают "
        "с такими клиентами. Просто у них чуть выше ставка, но решение приходит в тот же день.\n\n"
        "Как у тебя с КИ?",
        keyboard=kb_credit()
    )

async def step_amount(message: Message, data: dict):
    data["step"] = "amount"
    n = data["name"]
    await message.answer(
        f"{n}, понял. {reflect_credit(data['credit'])}\n\n"
        "Какой лимит нужен? Выбери диапазон — подберу партнёра, где лимиты начинаются "
        "именно с таких сумм.\n\n"
        "Совет: бери ровно столько, сколько нужно, и на срок, который точно закроешь. "
        "Тогда переплата будет минимальной.",
        keyboard=kb_amount()
    )

async def step_final(message: Message, data: dict):
    n = data["name"]
    primary, backup = get_offers_for_user(data)
    rating = calc_approval(data)
    hours = hours_left_today()

    msg = (
        f"Анализ завершён, {n}!\n\n"
        f"📊 Рейтинг одобрения: {rating}%\n"
        f"На основе: статус «{data['status']}», КИ «{data['credit']}», "
        f"сумма «{data['amount']}».\n\n"
        f"🏆 Основной партнёр: {primary['name']}\n"
        f"💡 {primary['reason']}\n"
        f"👉 {primary['url']}\n\n"
        f"🔄 Запасной вариант: {backup['name']}\n"
        f"👉 {backup['url']}\n\n"
        f"⏰ Рекомендуем оформить в ближайшие {hours} ч.\n\n"
        f"💡 Заполняйте анкету точно как в паспорте.\n\n"
        f"⚠️ Реклама. ПСК от 0% до 292% годовых. Оценивайте свои финансовые возможности и риски."
    )

    data["step"] = "done"
    data["rating"] = rating
    data["partner"] = primary["name"]
    data["partner_url"] = primary["url"]

    await message.answer(msg, keyboard=kb_main())

async def step_zero_loans(message: Message, data: dict):
    n = data["name"]
    await message.answer(
        f"{n}, вот продукты под 0% для новых клиентов.\n\n"
        "Это предложения, где первый продукт можно оформить без процентов — "
        "возвращаешь ровно ту сумму, которую взял.\n\n"
        "Как не переплатить:\n"
        "1️⃣ Бери только тот лимит, который точно закроешь.\n"
        "2️⃣ Верни в срок — обычно 7–30 дней. Просрочка обнуляет льготу.\n"
        "3️⃣ Проверь ПСК в договоре.\n"
        "4️⃣ Не подключай платные доп. услуги.\n\n"
        "👇 Выбирай партнёра:",
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

    # ---- Приветствие при первом сообщении или /start ----
    if not data.get("step") or text.lower().startswith("/start"):
        await send_welcome(message, data)
        return

    # ---- PAYLOAD-КОМАНДЫ ----
    if cmd == "go":
        await step_status(message, data); return

    if cmd in ("status_student", "status_working", "status_freelance", "status_nojob"):
        data["status"] = {
            "status_student": "Студент", "status_working": "Работаю",
            "status_freelance": "Фриланс", "status_nojob": "Без работы"
        }[cmd]
        await message.answer(f"{name}, зафиксировал: {data['status']}. {praise_for(data['status'])}")
        await step_credit(message, data); return

    if cmd in ("credit_good", "credit_bad", "credit_none"):
        data["credit"] = {
            "credit_good": "Идеальная", "credit_bad": "Были просрочки",
            "credit_none": "Никогда не брал"
        }[cmd]
        await step_amount(message, data); return

    if cmd in ("amount_low", "amount_mid", "amount_high"):
        data["amount"] = {
            "amount_low": "до 15.000 ₽", "amount_mid": "15.000 – 50.000 ₽",
            "amount_high": "50.000 – 100.000 ₽"
        }[cmd]
        await step_final(message, data); return

    if cmd == "zero_loans":
        await step_zero_loans(message, data); return

    if cmd == "restart":
        await send_welcome(message, data); return

    # ---- ТЕКСТ ВМЕСТО ТАПА НА РАЗНЫХ ШАГАХ ----
    step = data.get("step")
    if step == "status":
        await message.answer(f"{name}, выбери, пожалуйста, кнопкой ниже 👇", keyboard=kb_status()); return
    if step == "credit":
        await message.answer(f"{name}, выбери, пожалуйста, кнопкой ниже 👇", keyboard=kb_credit()); return
    if step == "amount":
        await message.answer(f"{name}, выбери, пожалуйста, кнопкой ниже 👇", keyboard=kb_amount()); return

    # ---- FALLBACK ----
    await send_welcome(message, data)

# ============================================================
#  ЗАПУСК
# ============================================================
if __name__ == "__main__":
    bot.run_forever()
