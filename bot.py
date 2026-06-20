import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import (
    BOT_TOKEN, CARD_NUMBER_1, CARD_OWNER_1,
    CARD_NUMBER_2, CARD_OWNER_2, ADMIN_USERNAME, WELCOME_MESSAGE
)

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════
#                     داده‌های محصولات
# ══════════════════════════════════════════════════════

BOOKS = [
    {
        "id": "book_1",
        "name": "کد گشایی حکمت (جلد ۱ و ۲)",
        "emoji": "📗",
        "description": (
            "💎 کتاب کد گشایی حکمت جلد یک و دو 💎\n\n"
            "﴿هم هردو جلد رو به زبون ساده‌تر نوشتیم و هم رمزگشایی کردیم برای اولین بار﴾"
        ),
        "price": "۱,۲۹۰",
        "images": ["images/book_1.jpg"]
    },
    {
        "id": "book_2",
        "name": "کتاب حکمت – جلد اول",
        "emoji": "📕",
        "description": (
            "از جذاب‌ترین و پر آگاهی‌ترین کتاب مجموعه 📕\n\n"
            "👀 فعال‌سازی چشم سوم\n"
            "🧘‍♀️ پاکسازی حرفه‌ای چاکراها\n"
            "✍🏼 رازهای خودشناسی عمیق\n"
            "🗣️ نمادشناسی مخفی\n"
            "🌌 کدهای انرژی کیهان\n"
            "🌀 اتصال به آگاهی برتر\n"
            "☸️ اتر و سرّ وجود\n"
            "🛑 اسرار زمین\n"
            "☯️ راز اعداد و نومرولوژی\n"
            "🐍 راز صعود روح و کندالینی"
        ),
        "price": "۱,۳۹۰",
        "images": ["images/book_2.jpg", "images/book_2b.jpg"]
    },
    {
        "id": "book_3",
        "name": "کتاب حکمت – جلد دوم",
        "emoji": "📘",
        "description": (
            "بخشی از سرفصل‌های کامل جلد دوم حکمت 📜❤️‍🔥\n\n"
            "💠 ۴ علامت ثابت و ۴ انجیل – رازهای نمادین\n"
            "💠 زوروبلاک و فرشتگان\n"
            "💠 اخترشناسی و بدن انسان\n"
            "💠 مذکر و مؤنث الهی\n"
            "💠 ۷ سیاره قابل مشاهده\n"
            "💠 ساعت آسمان\n"
            "💠 سمبولیسم مدل هلیوسنتریک\n"
            "💠 قدرت کلمات – کدهای زبانی و فرکانسی\n"
            "💠 آزاد کردن ذهن – شکستن قالب‌ها\n\n"
            "📖 ۲۹۸ صفحه سایز A4\n"
            "⚠️ جلد دوم رو برای هر کسی توصیه نمیکنم ∞"
        ),
        "price": "۱,۴۹۰",
        "images": ["images/book_3.jpg", "images/book_3b.jpg"]
    },
    {
        "id": "book_4",
        "name": "راهنمای سلامت انسان",
        "emoji": "🌿",
        "description": (
            "🌏 موضوعی که نباید بدونید ولی در کتاب راهنمای سلامت انسان نوشته شده\n\n"
            "هم بیماری و هم دارو برات فروخته میشه و تو دائماً درگیر بیماری‌ها میشی "
            "مخصوصاً وقتی که میدونی هم غذا و هم هوا سمی هستش\n\n"
            "پس بهترین راه حل آگاهیه❗️"
        ),
        "price": "۹۳۰",
        "images": ["images/book_4.jpg"]
    },
    {
        "id": "book_5",
        "name": "راهنمای عملی باز کردن چشم سوم",
        "emoji": "👁️",
        "description": (
            "کتاب کامل «راهنمای عملی باز کردن چشم سوم»\n\n"
            "این کتاب فقط یه توضیح تئوری نیست! واقعاً تمرین داره، قدم به قدمه.\n\n"
            "🔹 چطور پینال رو فعال‌تر کنی\n"
            "🔹 چطور نویزهای ذهنی رو خاموش کنی\n"
            "🔹 چطور شهودت قوی‌تر بشه\n"
            "🔹 چطور تمرکز و خواب عمیق‌تر داشته باشی\n"
            "🔹 تکنیک‌هایی که سال‌ها مخفی بودن\n\n"
            "➕ پاکسازی انسداد چاکراها\n"
            "➕ رمزگشایی بخشی از کتاب حکمت\n"
            "➕ بهترین مراقبه‌ها برای پاکسازی چاکراها\n"
            "➕ رسیدن به بالاترین حد فرکانسیک\n"
            "➕ کتاب کمیاب درباره غده پینه‌آل\n"
            "➕ توضیح کلی درباره سیستم ماتریکس\n"
            "➕ پشتیبانی ۲۴ساعته و رایگان مادام‌العمر"
        ),
        "price": "۷۹۰",
        "images": ["images/book_5.jpg", "images/book_5b.jpg"]
    },
    {
        "id": "book_6",
        "name": "راز اعداد",
        "emoji": "🔢",
        "description": (
            "✅ این کتاب مطابق با اعداد به بخش‌های مختلف تقسیم شده و آنه شیمل "
            "به توضیح در رابطه با هر عدد پرداخته و به طور کامل آن‌ها را بررسی کرده.\n\n"
            "برای درک بهتر، تصاویری نیز در نظر گرفته شده تا افراد بهتر بتوانند "
            "با دنیای اعداد ارتباط برقرار کنند.\n\n"
            "📖 تعداد صفحات: ۵۵۰"
        ),
        "price": "۱,۴۹۰",
        "images": ["images/book_6.jpg"]
    },
    {
        "id": "book_7",
        "name": "کلید سلیمان",
        "emoji": "🔑",
        "description": (
            "🔴 راز سیجیل‌ها\n"
            "🔴 ناگفته‌های حضرت سلیمان\n"
            "🔴 اسرار باستانی فلسطین و سرزمین‌های مقدس\n"
            "🔴 چاکرای زمین\n"
            "🔴 ناگفته‌های ماسون‌ها"
        ),
        "price": "۱,۰۹۹",
        "images": ["images/book_7a.jpg", "images/book_7b.jpg"]
    },
    {
        "id": "book_8",
        "name": "بیداری قلیایی",
        "emoji": "💚",
        "description": (
            "کتاب بیداری قلیایی\n\n"
            "سرفصل‌هاش به شدت جذاب و کاربردی هستن\n"
            "میتونه توی سلامتی خودت و اطرافیانت خیلی مهم باشه 😇✨\n\n"
            "در قرنی که ما زندگی می‌کنیم برای پاکسازی بدنمون بهترین متدها رو داره ♾💎"
        ),
        "price": "۱,۳۳۰",
        "images": ["images/book_8a.jpg", "images/book_8b.jpg", "images/book_8c.jpg",
                   "images/book_8d.jpg", "images/book_8e.jpg"]
    },
]

BRACELETS = [
    {
        "id": "bracelet_1",
        "name": "دستبند متافیزیکی هفت چاکرا",
        "emoji": "📿",
        "description": (
            "💢 دستبند متافیزیکی هفت چاکرا (انرژتیک)\n\n"
            "♾ تمامی دونه‌ها بر اساس علم اعداد کنار هم قرار گرفته ۳۶۷۷۹❗️\n\n"
            "با دونه‌های رودراکشا که مخصوص پاکسازی هستن\n"
            "(بین سنگ‌ها حدید به کار رفته)"
        ),
        "price": "۹۸۰",
        "images": ["images/bracelet_1a.jpg", "images/bracelet_1b.jpg", "images/bracelet_1c.jpg"]
    }
]

SHIPPING_IMAGES = [
    "images/shipping_1.jpg",
    "images/shipping_2.jpg",
    "images/shipping_3.jpg",
    "images/shipping_4.jpg",
]

LIBRARY_DESC = (
    "📖 کتابخانه مخفی\n"
    "━━━━━━━━━━━━━━━━━━━━\n\n"
    "‼️ لیست کتاب‌های خاص کتابخانه مخفی ‼️\n\n"
    "1️⃣ کد کیهانی\n"
    "2️⃣ ارتعاش اعداد\n"
    "3️⃣ مفاهیم ارتعاشی اعداد\n"
    "4️⃣ ذکرهای خاص عارفان\n"
    "5️⃣ راز کندالینی\n"
    "6️⃣ حکمت ۱\n"
    "7️⃣ حکمت ۲\n"
    "8️⃣ راهنمای سلامت انسان\n"
    "9️⃣ باز کردن چشم سوم 🔥\n"
    "🔟 کلید گمشده سلیمان 🔥\n"
    "1️⃣1️⃣ گنجینه اسرار 🔥\n"
    "1️⃣2️⃣ عجایب مخلوقات\n"
    "1️⃣3️⃣ اسرار ماوراء\n"
    "1️⃣4️⃣ راز نمادها\n"
    "1️⃣5️⃣ مرجان جادو ❗️🔒\n"
    "1️⃣6️⃣ بیداری قلیایی ❤️‍🔥\n"
    "1️⃣7️⃣ کدهای کیهانی ♾\n"
    "1️⃣8️⃣ کندالینی و چاکراها\n"
    "1️⃣9️⃣ اسرار ماتریکس 🔥\n"
    "و....\n\n"
    "🔮 هر هفته کتاب‌های خاصی رو آپلود می‌کنیم\n\n"
    "🔸 همه کتاب‌ها به صورت ترجمه شده و بدون سانسور آپلود شدن 🔸\n\n"
    "فرکانس‌های موجود:\n"
    "🔴 خود شفادهی\n"
    "🟠 پاکسازی هفت چاکرا\n"
    "🟣 بالا بردن فرکانس\n"
    "🔵 جذب ثروت 💴\n"
    "و....\n\n"
    "⏰ تا آخر هفته ۳۰٪ تخفیف برای ده نفر اول 👇🏼\n\n"
    "💰 بهای اصلی: ۹۵۰ تومان\n"
    "✅ با تخفیف: ۸۳۳ تومان 🫵🏼"
)

LIBRARY_PAYMENT = (
    "💎 طریقه عضویت در کتابخانه مخفی\n"
    "━━━━━━━━━━━━━━━━━━━━\n\n"
    "💰 بهای اصلی: ۹۵۰ تومان\n"
    "✅ با تخفیف: ۸۳۳ تومان\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "💳 شماره کارت‌ها:\n\n"
    f"  {CARD_NUMBER_1}\n"
    f"  به نام: {CARD_OWNER_1}\n\n"
    f"  {CARD_NUMBER_2}\n"
    f"  به نام: {CARD_OWNER_2}\n"
    "━━━━━━━━━━━━━━━━━━━━\n\n"
    "پس از واریز مبلغ، روی دکمه «✅ پرداخت کردم» بزنید."
)

# ══════════════════════════════════════════════════════
#                     توابع کمکی
# ══════════════════════════════════════════════════════

def find_product(product_id: str):
    for item in BOOKS:
        if item["id"] == product_id:
            return item
    for item in BRACELETS:
        if item["id"] == product_id:
            return item
    return None

def payment_text(product):
    return (
        f"💳 اطلاعات پرداخت\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📦 محصول: {product['emoji']} {product['name']}\n"
        f"💰 مبلغ: {product['price']} تومان\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💳 شماره کارت‌ها:\n\n"
        f"  {CARD_NUMBER_1}\n"
        f"  به نام: {CARD_OWNER_1}\n\n"
        f"  {CARD_NUMBER_2}\n"
        f"  به نام: {CARD_OWNER_2}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"پس از واریز، روی «✅ پرداخت کردم» بزنید."
    )

def admin_text(product_name: str):
    return (
        f"✅ ممنون از خرید شما!\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📦 محصول: {product_name}\n\n"
        f"لطفاً تصویر فیش واریزی را برای ادمین ارسال کنید:\n\n"
        f"👤 {ADMIN_USERNAME}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"پس از تأیید پرداخت، سفارش شما پردازش خواهد شد 🙏"
    )

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 کتاب‌ها", callback_data="cat_books")],
        [InlineKeyboardButton("📿 دستبندها", callback_data="cat_bracelets")],
        [InlineKeyboardButton("📦 ارسالی‌ها", callback_data="cat_shipping")],
        [InlineKeyboardButton("📖 کتابخانه مخفی", callback_data="cat_library")],
    ])

async def cleanup_photos(context, chat_id):
    for msg_id in context.user_data.get("photos", []):
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception:
            pass
    context.user_data["photos"] = []

async def send_photos(context, chat_id, images):
    msg_ids = []
    valid = [p for p in images if os.path.exists(p)]
    if not valid:
        return msg_ids
    if len(valid) == 1:
        with open(valid[0], "rb") as f:
            msg = await context.bot.send_photo(chat_id=chat_id, photo=f)
        msg_ids.append(msg.message_id)
    else:
        handles = [open(p, "rb") for p in valid[:10]]
        media = [InputMediaPhoto(media=h) for h in handles]
        try:
            msgs = await context.bot.send_media_group(chat_id=chat_id, media=media)
            msg_ids.extend([m.message_id for m in msgs])
        finally:
            for h in handles:
                h.close()
    return msg_ids

# ══════════════════════════════════════════════════════
#                     هندلرها
# ══════════════════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cleanup_photos(context, update.effective_chat.id)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=main_keyboard())


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = query.message.chat_id

    # ── بازگشت به خانه ──────────────────────────────
    if data == "home":
        await cleanup_photos(context, chat_id)
        await query.edit_message_text(WELCOME_MESSAGE, reply_markup=main_keyboard())

    # ── دسته‌بندی کتاب‌ها ───────────────────────────
    elif data == "cat_books":
        await cleanup_photos(context, chat_id)
        keyboard = [
            [InlineKeyboardButton(f"{b['emoji']} {b['name']}", callback_data=f"p_{b['id']}")]
            for b in BOOKS
        ]
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="home")])
        await query.edit_message_text("📚 کتاب‌ها\n\n👇 یکی از کتاب‌ها را انتخاب کنید:",
                                      reply_markup=InlineKeyboardMarkup(keyboard))

    # ── دسته‌بندی دستبندها ──────────────────────────
    elif data == "cat_bracelets":
        await cleanup_photos(context, chat_id)
        keyboard = [
            [InlineKeyboardButton(f"{b['emoji']} {b['name']}", callback_data=f"p_{b['id']}")]
            for b in BRACELETS
        ]
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="home")])
        await query.edit_message_text("📿 دستبندها\n\n👇 یکی را انتخاب کنید:",
                                      reply_markup=InlineKeyboardMarkup(keyboard))

    # ── ارسالی‌ها ────────────────────────────────────
    elif data == "cat_shipping":
        await cleanup_photos(context, chat_id)
        await query.edit_message_text("📦 در حال بارگذاری تصاویر ارسالی‌ها...")
        ids = await send_photos(context, chat_id, SHIPPING_IMAGES)
        context.user_data["photos"] = ids
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="home")]])
        await query.edit_message_text("📦 ارسالی‌ها\n\nنمونه‌ای از سفارش‌های ارسال‌شده 👆",
                                      reply_markup=keyboard)

    # ── کتابخانه مخفی ───────────────────────────────
    elif data == "cat_library":
        await cleanup_photos(context, chat_id)
        await query.edit_message_text("📖 در حال بارگذاری...")

        # ارسال عکس لیست کتاب‌ها
        ids = []
        if os.path.exists("images/library_books.jpg"):
            ids += await send_photos(context, chat_id, ["images/library_books.jpg"])

        # ارسال ویدیو معرفی
        if os.path.exists("images/library_intro.mov"):
            try:
                with open("images/library_intro.mov", "rb") as vf:
                    vmsg = await context.bot.send_video(chat_id=chat_id, video=vf)
                ids.append(vmsg.message_id)
            except Exception as e:
                logger.warning(f"Video send failed: {e}")

        context.user_data["photos"] = ids

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📋 طریقه عضویت در کتابخانه مخفی", callback_data="lib_how")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="home")],
        ])
        await query.edit_message_text(LIBRARY_DESC, reply_markup=keyboard)

    # ── طریقه عضویت کتابخانه ────────────────────────
    elif data == "lib_how":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ پرداخت کردم", callback_data="lib_paid")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="cat_library")],
        ])
        await query.edit_message_text(LIBRARY_PAYMENT, reply_markup=keyboard)

    # ── پرداخت کتابخانه انجام شد ────────────────────
    elif data == "lib_paid":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 بازگشت به خانه", callback_data="home")]
        ])
        text = (
            "✅ ممنون از اعتماد شما!\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "لطفاً تصویر فیش واریزی را برای ادمین ارسال کنید:\n\n"
            f"👤 {ADMIN_USERNAME}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "پس از تأیید، لینک کتابخانه مخفی برای شما ارسال می‌شود 🔮"
        )
        await query.edit_message_text(text, reply_markup=keyboard)

    # ── نمایش جزئیات محصول ──────────────────────────
    elif data.startswith("p_"):
        product_id = data[2:]
        product = find_product(product_id)
        if not product:
            return

        await cleanup_photos(context, chat_id)
        await query.edit_message_text("⏳ در حال بارگذاری...")

        ids = await send_photos(context, chat_id, product["images"])
        context.user_data["photos"] = ids

        # تعیین دکمه بازگشت
        if product_id.startswith("book_"):
            back_cb = "cat_books"
        else:
            back_cb = "cat_bracelets"

        text = (
            f"{product['emoji']}  {product['name']}\n"
            f"{'─' * 28}\n\n"
            f"{product['description']}\n\n"
            f"{'─' * 28}\n"
            f"💰 قیمت:  {product['price']} تومان"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 خرید", callback_data=f"buy_{product_id}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data=back_cb)],
        ])
        await query.edit_message_text(text, reply_markup=keyboard)

    # ── خرید – نمایش شماره کارت ─────────────────────
    elif data.startswith("buy_"):
        product_id = data[4:]
        product = find_product(product_id)
        if not product:
            return

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ پرداخت کردم", callback_data=f"paid_{product_id}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data=f"p_{product_id}")],
        ])
        await query.edit_message_text(payment_text(product), reply_markup=keyboard)

    # ── پرداخت انجام شد – نمایش آیدی ادمین ─────────
    elif data.startswith("paid_"):
        product_id = data[5:]
        product = find_product(product_id)
        name = product["name"] if product else "محصول"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 بازگشت به خانه", callback_data="home")]
        ])
        await query.edit_message_text(admin_text(name), reply_markup=keyboard)


# ══════════════════════════════════════════════════════
#                     اجرای ربات
# ══════════════════════════════════════════════════════

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("✅ ربات فروشگاه شروع به کار کرد...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
