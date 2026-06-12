# Design Document

## Overview

این سند طراحی، رویکرد فنی برای آماده‌سازی پروژه‌ی «سامانه‌ی مدیریت ریزشبکه‌ی برق DC و انرژی خورشیدی» برای ارائه‌ی دانشگاهی را شرح می‌دهد. هدف، بهبود کیفیت کد، اطمینان از کارکرد سرتاسری، غنی‌سازی داده‌ی نمایشی، پاک‌سازی کد و فایل‌های اضافی، و مستندسازی روشن است.

پروژه شامل:
- **بک‌اند**: FastAPI + MongoDB (pymongo) + Redis، ساختار ماژولار (`auth`, `solar_panel`, `battery`, `device`, `apartment`, `block`, `power_record`, `pricing`, `order`, `shop`, `profile`, `admins`).
- **فرانت‌اند**: Nuxt 3 (Vue) + Tailwind.
- **اجرا**: Docker Compose.

رویکرد کلی: تغییرات **کم‌ریسک و افزایشی** انجام می‌شوند. ابتدا بررسی و سلامت‌سنجی، سپس پاک‌سازی محتاطانه (با اطمینان از عدم وابستگی)، سپس غنی‌سازی داده، و در نهایت تأیید سرتاسری و مستندسازی. هیچ تغییر معماری بزرگی انجام نمی‌شود تا ریسک خراب‌شدن قبل از ارائه حداقل بماند.

## Architecture

### وضعیت فعلی (As-Is)

```
docker-compose.yml
├── university-project (back, FastAPI :8002)
├── redis (:6389)
├── university-project-db (MongoDB :27020)
├── mongo-compass (mongo-express :8082)
└── university-project-front (Nuxt :80)
```

- اتصال دیتابیس در `src/db/db.py` و دوباره در `src/main.py` (تکراری).
- راه‌اندازی اولیه از طریق `GET /startup` و توابع ماژول‌سطح در `main.py`.
- داده‌ی نمایشی از طریق `src/seed_data.py` (با اجرای دستی `python -m src.seed_data <email>`).

### مشکلات شناسایی‌شده

| مورد | محل | اقدام |
|------|------|-------|
| ماژول مرده با SQLAlchemy، ثبت‌نشده در main | `src/power_source/` | حذف |
| ارجاع بی‌استفاده به دیتابیس gpt | `.env`, `.env.example`, `docker-compose.yml` (`gpt-db-data`, `DATABASE_URL_GPT`) | حذف |
| کد دیباگ | `main.py` (`"asdasdsad"`)، `db.py` (`"wqwdqwd"`)، `auth/services.py`, `order/services.py` و سایر `print` ها | حذف |
| باگ منطقی فصل | `power_record/services.py` تابع `get_season` (پاییز → "summer") | اصلاح |
| حجم زیاد کد کامنت‌شده | `order/services.py` (صدها خط)، `db.py` | پاک‌سازی |
| فایل لاگ داخل مخزن | `back/university.log` | حذف + gitignore |
| اتصال DB تکراری | `main.py` کلاینت Mongo جدا می‌سازد | استفاده از `db.db` مشترک |
| `.env` واقعی با کلیدهای حساس | ریشه‌ی مخزن | خارج‌کردن از git + gitignore |
| کلیدهای واقعی در `.env.example` | `.env.example` | جایگزینی با placeholder |

### وضعیت هدف (To-Be)

ساختار تمیز، بدون ماژول مرده، بدون کد دیباگ، با اسکریپت seed قوی‌تر و idempotent، مستندات به‌روز، و `.env` خارج از مخزن. رفتار کارکردی برنامه تغییر نمی‌کند مگر اصلاح باگ‌های روشن.

## Components and Interfaces

### ۱. مؤلفه‌ی پاک‌سازی کد (Code Cleanup)

**مسئولیت:** حذف کد مرده، فایل‌های اضافی و کدهای دیباگ بدون آسیب به رفتار فعال.

**اقدامات:**
- حذف پوشه‌ی `src/power_source/` پس از تأیید عدم import در هر جای فعال (با grep).
- حذف عبارت‌های `print` دیباگ از `main.py`, `db.py`, `auth/services.py`, `order/services.py`, `power_record/services.py` و سایر فایل‌ها. (لاگ‌های واقعی با `logger` حفظ می‌شوند.)
- حذف بلوک بزرگ کد کامنت‌شده در `order/services.py` و `db.py`.
- حذف فایل `back/university.log` و افزودن الگوهای لاگ به `.gitignore`.
- یکپارچه‌سازی اتصال DB: `main.py` به‌جای ساخت کلاینت جدید، از `src.db.db` استفاده کند (با حفظ سازگاری توابع startup).

**ملاحظه‌ی ایمنی:** پیش از هر حذف، با `grep_search` تأیید می‌شود که هیچ ماژول فعالی import نمی‌کند. حذف‌ها فایل‌به‌فایل و قابل‌بازگشت‌اند (git).

### ۲. مؤلفه‌ی اصلاح باگ‌های روشن (Targeted Fixes)

**مسئولیت:** اصلاح باگ‌های منطقی واضح که می‌توانند در نمایش مشکل ایجاد کنند.

**اقدامات:**
- اصلاح `get_season` در `power_record/services.py`: ماه‌های ۹ تا ۱۱ باید "fall" برگردانند نه "summer".
- بررسی `service_add_power_records` برای دسترسی امن به `device` (در صورت `None` نبودن دستگاه) تا خطای زمان اجرا رخ ندهد.

**دامنه:** فقط باگ‌های روشن و کم‌ریسک. بازنویسی منطق محاسبات انرژی در دامنه‌ی این spec نیست.

### ۳. مؤلفه‌ی غنی‌سازی داده‌ی نمایشی (Enhanced Seed)

**مسئولیت:** ارتقای `src/seed_data.py` برای تولید داده‌ی فراوان، متنوع و idempotent که همه‌ی صفحات را پر می‌کند.

**رابط:** اجرای `python -m src.seed_data [email]` داخل کانتینر بک‌اند.

**طراحی داده:**

```
کاربر نمایشی (demo user)
├── پروفایل کامل (نام، تصویر)
├── بلوک + آپارتمان (area معتبر: 100)
├── دستگاه‌ها (۶+ دستگاه با نام فارسی، AC/DC، kind)
├── پنل خورشیدی + باتری (مقادیر واقع‌نما)
├── رکوردهای مصرف برق
│   └── ≥ ۹۰ روز، چند session روزانه، چند دستگاه → نمودارهای پر
├── قیمت‌گذاری (هر ۴ فصل)
├── فروشگاه
│   ├── دسته‌بندی‌ها (≥ ۴ دسته)
│   └── محصولات (≥ ۸ محصول متنوع، فعال/غیرفعال)
└── سفارش‌ها (چند سفارش نمونه با وضعیت/تاریخ متفاوت)
```

**اصول:**
- **Idempotency**: هر بخش پیش از درج، وجود را بررسی می‌کند یا داده‌ی قبلی خود را پاک و بازسازی می‌کند (مانند رویکرد فعلی برای devices/power_records).
- **سازگاری نوع**: `user_id` در `power_records` به‌صورت `ObjectId` ذخیره شود (مطابق aggregationها).
- **افزایش حجم**: بازه‌ی روزها از ۶۰ به ۹۰+ و تنوع دستگاه‌ها/محصولات بیشتر شود.
- **حساب نمایشی**: ساخت کاربر نمایشی با رمز مشخص اگر وجود ندارد (برای ورود ساده در ارائه)، با ثبت در مستندات.

### ۴. مؤلفه‌ی امنیت و پیکربندی محیطی

**مسئولیت:** خارج‌کردن اطلاعات حساس از مخزن.

**اقدامات:**
- افزودن `.env` و فایل‌های لاگ به `.gitignore`.
- خارج‌کردن `.env` از ردگیری git با `git rm --cached .env` (فایل روی دیسک باقی می‌ماند تا اجرا نشکند).
- بازنویسی `.env.example` با placeholderها (بدون کلید واقعی SMTP، زرین‌پال، S3، SECRET_KEY).
- حذف ارجاعات `DATABASE_URL_GPT` و `gpt-db-data`.

**ملاحظه:** رمزهای پیش‌فرض MongoDB (admin/admin) برای محیط توسعه باقی می‌مانند و در مستندات به‌عنوان «فقط توسعه» علامت‌گذاری می‌شوند. این یک سرویس محلی است؛ تغییر آن ریسک شکستن اجرا را دارد و خارج از نیاز ارائه است.

### ۵. مؤلفه‌ی سلامت‌سنجی و تأیید (Verification)

**مسئولیت:** اطمینان از اینکه پس از تغییرات، همه‌چیز بالا می‌آید و کار می‌کند.

**روش:**
- **Import check بک‌اند**: اجرای `python -c "import src.main"` داخل محیط بک‌اند برای کشف خطای import.
- **بالا آوردن پشته**: `docker compose up --build` و بررسی سالم بودن سرویس‌ها.
- **Smoke test endpointها**: فراخوانی `/startup`, `/docs`, و چند endpoint کلیدی (لیست محصولات، لیست دسته‌بندی).
- **اجرای seed** و تأیید درج داده.
- **بررسی فرانت**: build شدن و باز شدن صفحات اصلی.

اگر دسترسی به Docker در محیط اجرا میسر نباشد، حداقل بررسی‌های static (import، syntax) و بازبینی کد انجام و در گزارش ذکر می‌شود.

### ۶. مؤلفه‌ی مستندسازی

**مسئولیت:** به‌روزرسانی README و افزودن راهنمای ارائه.

**اقدامات:**
- اصلاح بخش ساختار پروژه پس از حذف `power_source`.
- افزودن دستور seed و اطلاعات حساب نمایشی.
- برجسته‌کردن امکانات کلیدی برای دمو.
- ذکر نکات امنیتی (env، رمزهای توسعه).

## Data Models

داده‌ها در MongoDB و schema-less هستند. کالکشن‌های کلیدی و فیلدهای مورد استفاده‌ی seed:

| کالکشن | فیلدهای کلیدی |
|--------|----------------|
| `users` | `_id`, `email`, `password` (hash), `permissions[]`, `devices[]` |
| `profiles` | `user_id`, `photo`, (نام در صورت نیاز) |
| `permissions` | `name`, `description` |
| `apartments` | `apartment_no`, `admin_id`, `block_no` |
| `blocks` | `user_id`, `apartment_id`, `unit`, `area` |
| `device` | `name`, `size`, `kind`, `AC_power_consumption`, `DC_power_consumption` |
| `solar_panels` | `user_id`, `fee` |
| `battery` | `user_id`, `solar_panel_id`, `saved_energy`, `sold_energy`, `status`, `email`, `fee`, `created_at` |
| `power_records` | `user_id` (ObjectId), `device_name`, `start_time`, `end_time`, `consumption` |
| `pricing` | `season_name`, `start_time`, `end_time`, `peak_*`, `general_price`, `peak_price`, `day_light` |
| `categories` | `name.{fa,en}` |
| `products` | `slug`, `name.{fa,en}`, `description.{fa,en}`, `price`, `logo`, `photo`, `background`, `isActivate`, `category_id` |
| `orders` | `user_id`, `battery_id`, `seller_id`, `amount`, `fee`, `created_at` |
| `carts` | `user_id`, اقلام |

**نکته‌ی سازگاری:** فیلد `created_at` در `orders` توسط `service_get_order_buy_user` با `.strftime` فرمت می‌شود، پس باید `datetime` ذخیره شود نه رشته. در seed سفارش‌ها از `datetime` استفاده می‌شود تا با کوئری‌های خروجی سازگار بماند.

## Error Handling

- **حذف ایمن**: هر حذف ماژول/فایل با grep قبلی محافظت می‌شود؛ در صورت یافتن وابستگی، حذف انجام نمی‌شود و گزارش می‌شود.
- **Seed مقاوم**: اسکریپت seed در صورت نبود کاربر، پیام روشن می‌دهد؛ بخش‌ها idempotent‌اند تا اجرای مکرر خراب نکند.
- **عدم تغییر رفتار خروجی**: پاک‌سازی `print`ها نباید مقدار بازگشتی توابع را تغییر دهد.
- **بازگشت‌پذیری**: همه‌ی تغییرات در git قابل بازگشت‌اند؛ تغییرات پرریسک (مانند خارج‌کردن `.env`) فایل را روی دیسک حفظ می‌کنند.

## Correctness Properties

این ویژگی‌ها باید پس از همه‌ی تغییرات همواره برقرار باشند:

### Property 1: حفظ رفتار import
`import src.main` بدون خطا اجرا می‌شود و همه‌ی روترهای فعلی همچنان ثبت می‌شوند.

**Validates: Requirements 1.1, 1.4**

### Property 2: پایداری حذف
حذف هر فایل/ماژول نباید هیچ import فعالی را بشکند؛ پس از حذف، بررسی import دوباره موفق است.

**Validates: Requirements 4.1, 4.6**

### Property 3: Idempotency داده
اجرای چندباره‌ی seed منجر به داده‌ی تکراری یا خراب نمی‌شود و تعداد رکوردهای کلیدی پایدار می‌ماند.

**Validates: Requirements 3.6**

### Property 4: سازگاری نوع user_id
همه‌ی `power_records` تولیدشده `user_id` از نوع `ObjectId` دارند تا با aggregationهای نمودار مطابق باشند.

**Validates: Requirements 3.2, 7.3**

### Property 5: سازگاری نوع created_at سفارش
`orders.created_at` به‌صورت `datetime` ذخیره می‌شود تا `.strftime` در خروجی نشکند.

**Validates: Requirements 3.7**

### Property 6: عدم تغییر مقدار بازگشتی
حذف `print`ها مقدار بازگشتی هیچ تابعی را تغییر نمی‌دهد.

**Validates: Requirements 4.3**

### Property 7: عدم نشت راز
پس از تغییرات، هیچ کلید واقعی در فایل‌های ردگیری‌شده‌ی git باقی نمی‌ماند.

**Validates: Requirements 5.1, 5.2**

## Testing Strategy

از آنجا که پروژه تست خودکار ندارد و هدف، آماده‌سازی نمایش است، استراتژی بر **سلامت‌سنجی و smoke test** متمرکز است:

1. **Static checks**: تأیید import شدن `src.main` و عدم خطای syntax پس از پاک‌سازی.
2. **Seed verification**: اجرای seed و شمارش رکوردهای درج‌شده در کالکشن‌های کلیدی.
3. **Endpoint smoke tests**: فراخوانی endpointهای عمومی (محصولات، دسته‌بندی) و startup.
4. **بررسی دستی فرانت**: build و باز شدن صفحات اصلی بدون خطای مسدودکننده.
5. **تأیید end-to-end**: ورود کاربر نمایشی، مشاهده‌ی داشبورد/نمودار/فروشگاه با داده‌ی seed.

نتیجه‌ی هر مرحله گزارش می‌شود؛ اگر محیط Docker در دسترس نباشد، محدودیت صریحاً ذکر می‌شود.
