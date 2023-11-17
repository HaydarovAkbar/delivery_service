class MessageText:
    settings = {
        'uz': "<b>Sozlamalar menyusiga xush kelibsiz</b>",
        'ru': "<b>Добро пожаловать в меню настроек</b>",
        'en': "Welcome to the settings menu",
    }
    change_language = {
        'uz': "<b>Tilni o'zgartirish</b>",
        'ru': "<b>Изменить язык</b>",
        'en': "Change language",
    }
    successfuly_changed_language = {
        'uz': "<b>Til muvaffaqiyatli o'zgartirildi</b>",
        'ru': "<b>Язык успешно изменен</b>",
        'en': "Language changed successfully",
    }
    change_phone_number = {
        'uz': "<b>Telefon raqamini o'zgartirish</b>",
        'ru': "<b>Изменить номер телефона</b>",
        'en': "Change phone number",
    }
    successfuly_changed_phone_number = {
        'uz': "<b>Telefon raqami muvaffaqiyatli o'zgartirildi</b>",
        'ru': "<b>Номер телефона успешно изменен</b>",
        'en': "Phone number changed successfully",
    }
    order_not_found = {
        'uz': "<b>Sizda buyurtma yo'q</b>",
        'ru': "<b>У вас нет заказа</b>",
        'en': "<b>You don't have an order</b>",
    }
    order_created = {
        'uz': "<b>Buyurtma qabul qilindi</b>",
        'ru': "<b>Заказ принят</b>",
        'en': "<b>Order accepted</b>",
    }

    order_history = {
        'uz': "<code>🗂 Buyurtmalaringiz tarixi:</code>",
        'ru': "<code>🗂 История ваших заказов:</code>",
        'en': "<code>🗂 History of your orders:</code>",
    }
    main = {
        'uz': "<b>Tilni tanlang!</b>",
        'ru': "<b>Выберите язык!</b>",
        'en': "<b>Choose language!</b>",
    }
    phone_number = {
        'uz': "<b>Telefon raqamingizni yuboring</b>",
        'ru': "<b>Отправьте свой номер телефона</b>",
        'en': "<b>Send your phone number</b>",
    }

    phone_number_error = {
        'uz': "<b>Siz xato ko'rinishda yubordingiz</b> \n\n<code>Menga +998901234567 shaklida yuboring</code>",
        'ru': "<b>Вы отправили неправильно</b> \n\n<code>Отправьте мне в форме +998901234567</code>",
        'en': "<b>You sent it wrong</b> \n\n<code>Send me in the form +998901234567</code>",
    }

    get_location = {
        'uz': "<b>📍 Geolokatsiyani yuboring yoki yetkazib berish manzilini tanlang</b>",
        'ru': "<b>📍 Отправьте геолокацию или выберите адрес доставки</b>",
        'en': "<b>📍 Send a geolocation or select a delivery address</b>",
    }

    not_found_location = {
        'uz': "<b>Sizda geolokatsiya bo'sh</b>",
        'ru': "<b>У вас нет геолокации</b>",
        'en': "<b>You don't have a geolocation</b>",
    }
    base = {
        'uz': "<code>Botdan foydalanishingiz mumkin</code>",
        'ru': "<code>Вы можете использовать бота</code>",
        'en': "<code>You can use the bot</code>",
    }

    get_link = {
        'uz': "<b>Link jo'natishing va \n\nInstagram\nYoutube\nTiktok\n\nIjtimoiy tarmoqlaridan video yuklashingiz mumkin!!!</b>",
        'ru': "<b>Вы можете отправить ссылку и загрузить видео из социальных сетей\n\nInstagram\nYoutube\nTiktok</b>",
        'en': "<b>You can send a link and upload a video from social networks\n\nInstagram\nYoutube\nTiktok</b>",
    }

    get_feedback = {
        'uz': "<b>Fikringizni jo'nating</b>",
        'ru': "<b>Отправьте свой комментарий</b>",
        'en': "<b>Send us your feedback</b>",

    }

    get_stats = {
        'uz': "<b>Statistika</b>",
        'ru': "<b>Статистика</b>",
        'en': "<b>Statistics</b>",
    }

    feedback_sent = {
        "uz": "<b>Fikringiz jo'natildi\nBiz uni ko'rib chiqamiz va tez orada javob qaytaramiz</b>",
        'ru': "<b>Ваш комментарий отправлен\nМы рассмотрим его и свяжемся с вами в ближайшее время.</b>",
        'en': "<b>Your comment has been submitted\nWe will review it and get back to you shortly</b>",
    }

    youtube = {
        'uz': "<b>yuborilmoqda ...</b>",
        'ru': "<b>отправляется ...</b>",
        'en': "<b>sending ...</b>",
    }

    down_error = {
        'uz':
            """
    👻 Afsuski, havolangizni qayta ishlay olmayman:
            <code>&LINK&</code>
            
    Bu oqim, pleylist yoki qo‘llab-quvvatlanmaydigan saytga havola ekanligini tekshiring. Qo'llab-quvvatlanadigan xizmatlarning to'liq ro'yxati - /help.
            
    Menga havola bering 👌""",
        'ru':
            """
    👻 К сожалению, я не могу обработать ваш запрос:
            <code>&LINK&</code>
            
    Проверьте, является ли это потоком, плейлистом или неподдерживаемым сайтом. Полный список поддерживаемых сервисов - /help.
    
    Пришлите мне ссылку 👌""",
        'en':
            """
    👻 Unfortunately, I can't process your request:
            <code>&LINK&</code>
            
    Check if it's a stream, playlist, or unsupported site. Full list of supported services - /help.
    
    Send me a link 👌""",
    }
    help = {
        'uz': """
    @Gozilla_bot siz shunga o'xshagan botga ega bo'lishni xoxlaysizmi?
    
    @khaydarov_akbar ⬅️ bizga aloqaga chiqing
    
    ✅ Cheklovingiz: cheklovlar yo'q!
    """,
        'ru': """
    Хотите иметь бота, похожего на @Gozilla_bot?
    
    @khaydarov_akbar ⬅️ свяжитесь с нами
    
    ✅ Ваш чек: чеки отсутствуют!
    """,
        'en': """
    Do you want to have a bot like @Gozilla_bot?
    
    @khaydarov_akbar ⬅️ contact us
    
    ✅ Your check: no checks!
    """,
    }

    add_to_channel = {
        'uz': "Botdan foydalanish uchun avval kanallarimizga a'zo bo'ling",
        'ru': "Прежде чем использовать бота, подпишитесь на наши каналы",
        'en': "Before using the bot, subscribe to our channels",
    }

    is_admin = {
        'uz': "<b>Xush kelibsiz Admin</b>",
        'ru': "<b>Добро пожаловать Админ</b>",
        'en': "<b>Welcome Admin</b>",
    }

    search_user = {
        'uz': "Foydalanuvchini izlash uchun ismini kiriting",
        'ru': "Введите имя пользователя, чтобы найти его",
        'en': "Enter the username to find the user",
    }
    not_found_user = {
        'uz': "Foydalanuvchi topilmadi",
        'ru': "Пользователь не найден",
        'en': "User not found",
    }

    enter_channel_title = {
        'uz': "Kanal nomini kiriting",
        'ru': "Введите название канала",
        'en': "Enter the channel name",
    }

    enter_channel_url = {
        'uz': "Kanal havolasini kiriting",
        'ru': "Введите ссылку на канал",
        'en': "Enter the channel link",
    }

    enter_channel_id = {
        'uz': "Kanal ID sini kiriting",
        'ru': "Введите ID канала",
        'en': "Enter the channel ID",
    }

    succesfuly_added = {
        'uz': "Kanal muvaffaqiyatli qo'shildi 👌  \n\n<b>Bot kanaldan foydalanishi uchun botni avval kanalga a'zo qilish kerak buni unitmang!!!</b>",
        'ru': "Канал успешно добавлен 👌  \n\n<b>Чтобы бот мог использовать канал, сначала подпишитесь на канал!</b>",
        'en': "Channel added successfully 👌  \n\n<b>To use the bot, first subscribe to the channel!</b>",
    }

    channel_deleted = {
        'uz': "Kanal muvaffaqiyatli o'chirildi 👌",
        'ru': "Канал успешно удален 👌",
        'en': "Channel deleted successfully 👌",
    }

    add_category = {
        'uz': "Kategoriya nomini kiriting [uz] va [ru]\n\nMasalan: Lavash * Лаваш",
        'ru': "Введите название категории [uz] и [ru]\n\nНапример: Lavash * Лаваш",
        'en': "Enter the category name [uz] and [ru]\n\nFor example: Lavash * Лаваш",
    }

    add_category_image_uz = {
        'uz': "Kategoriya rasmini yuboring [uz]",
        'ru': "Отправьте изображение категории [uz]",
        'en': "Send category image [uz]",
    }

    add_category_image_ru = {
        'uz': "Kategoriya rasmini yuboring [ru]",
        'ru': "Отправьте изображение категории [ru]",
        'en': "Send category image [ru]",
    }

    add_product_name = {
        'uz': "Mahsulot nomini kiriting [uz] va [ru]\n\nMasalan: Lavash sirli * Лаваш сырный",
        'ru': "Введите название продукта [uz] и [ru]\n\nНапример: Lavash sirli * Лаваш сырный",
        'en': "Enter the product name [uz] and [ru]\n\nFor example: Lavash sirli * Лаваш сырный",
    }

    add_product_content = {
        'uz': "Mahsulot tarkibini kiriting [uz] va [ru]\n\nMasalan: Lavash sirli * Лаваш сырный",
        'ru': "Введите состав продукта [uz] и [ru]\n\nНапример: Lavash sirli * Лаваш сырный",
        'en': "Enter the product content [uz] and [ru]\n\nFor example: Lavash sirli * Лаваш сырный",
    }

    add_product_price = {
        'uz': "Mahsulot narxini kiriting",
        'ru': "Введите цену продукта",
        'en': "Enter the product price",
    }
    add_product_discount = {
        'uz': "Mahsulot chegirmadagi narxini kiriting",
        'ru': "Введите цену продукта со скидкой",
        'en': "Enter the discounted product price",
    }
    add_product_photo = {
        'uz': "Mahsulot rasmini yuboring",
        'ru': "Отправьте фото продукта",
        'en': "Send a photo of the product",
    }
    add_product_category = {
        'uz': "Mahsulot kategoriyasini tanlang",
        'ru': "Выберите категорию продукта",
        'en': "Select a product category",
    }
    product_devided_size = {
        'uz': "Mahsulot o'lchamiga ko'ra bo'linadimi ?",
        'ru': "Разделен ли продукт по размеру?",
        'en': "Is the product divided by size?",
    }

    product_size_name = {
        'uz': "Mahsulot o'lchamini nomini kiriting [uz] va [ru]\n\nMasalan: mini lavash * мини лаваш",
        'ru': "Введите название размера продукта [uz] и [ru]\n\nНапример: mini lavash * мини лаваш",
        'en': "Enter the product size name [uz] and [ru]\n\nFor example: mini lavash * мини лаваш",
    }

    product_size_price = {
        'uz': "Mahsulot o'lchamini narxini kiriting",
        'ru': "Введите цену размера продукта",
        'en': "Enter the product size price",
    }
    succesfuly_added_product = {
        'uz': "Mahsulot muvaffaqiyatli qo'shildi 👌",
        'ru': "Продукт успешно добавлен 👌",
        'en': "Product added successfully 👌",
    }

    add_again = {
        'uz': "Chiqib ketish uchun Orqaga tugmasini bosing",
        'ru': "Нажмите кнопку Назад, чтобы выйти",
        'en': "Press the Back button to exit",
    }
    add_admin_with_chat_id = {
        'uz': "Admin chat id sini kiriting",
        'ru': "Введите chat id админа",
        'en': "Enter the admin chat id",
    }

    add_supplier_with_chat_id = {
        'uz': "Kuryer chat id sini kiriting",
        'ru': "Введите chat id курьера",
        'en': "Enter the courier chat id",
    }
    add_supplier_name = {
        'uz': "Kuryer ismini kiriting",
        'ru': "Введите имя курьера",
        'en': "Enter the courier name",
    }

    add_supplier_phone = {
        'uz': "Kuryer telefon raqamini kiriting",
        'ru': "Введите номер телефона курьера",
        'en': "Enter the courier phone number",
    }

    send_adversting = {
        'uz': "Reklama xabarini yuboring",
        'ru': "Отправьте рекламное сообщение",
        'en': "Send an advertising message",
    }

    orders = {
        'uz': "Tugatilmagan buyurtmalar",
        'ru': "Незавершенные заказы",
        'en': "Unfinished orders",
    }

    get_only_location = {
        'uz': "Geolokatsiyani yuboring",
        'ru': "Отправьте геолокацию",
        'en': "Send a geolocation",
    }

    confirmation = {
        'uz': "Laktsiyangizni tasdiqlaysizmi ?",
        'ru': "Вы подтверждаете свой выбор ?",
        'en': "Do you confirm your choice ?",
    }

    choose_menu = {
        'uz': "Menyudan tanlang",
        'ru': "Выберите из меню",
        'en': "Choose from the menu",
    }

    choose_location = {
        'uz': "Geolokatsiyadan tanlang",
        'ru': "Выберите из геолокации",
        'en': "Choose from geolocation",
    }
    adress_has_been_found = {
        "uz": "Manzilingiz aniqlandi",
        "ru": "Ваш адрес найден",
        "en": "Your address has been found"
    }

    sell_product_count = {
        'uz': "Sonini tanlang",
        'ru': "Выберите количество",
        'en': "Choose the quantity",
    }
    change_code = {
        'uz': "mahsulot soni {} ga o'zgartirildi",
        'ru': "количество продукта изменено на {}",
        'en': "product quantity changed to {}",
    }
    cart_empty = {
        'uz': "Savatcha bo'sh",
        'ru': "Корзина пуста",
        'en': "Cart is empty",
    }

    notification_admins = {
        'uz': "<b>Yangi buyurtma kelib tushdi</b>",
        'ru': "<b>Поступил новый заказ</b>",
        'en': "<b>A new order has arrived</b>",
    }

    all_supplier = {
        'uz': "Barcha kuryerlar",
        'ru': "Все курьеры",
        'en': "All couriers",
    }
    added_to_cart = {
        'uz': "Savatga qo'shildi",
        'ru': "Добавлено в корзину",
        'en': "Added to cart",
    }

    order_completed = {
        'uz': "Buyurtmangiz: {}",
        'ru': "Ваш заказ: {}",
        'en': "Your order: {}",
    }

    order_status_to_admins = {
        'uz': "Buyurtma holati: \n\n№{}\n{}\n{}",
        'ru': "Статус заказа: \n\n№{}\n{}\n{}",
        'en': "Order status: \n\n№{}\n{}\n{}",
    }


class KeyboardText:
    languages = {
        'uz': '🇺🇿 O\'zbekcha',
        'ru': '🇷🇺 Русский',
    }
    base = {
        'uz': ["Menyu 🍽", "Savatcha 🛒", "Buyurtmalar tarixi 🗑", "Fikr bildirish ✍️", "Sozlamalar ⚙️"],
        'ru': ["Меню 🍽", "Корзина 🛒", "История заказов 🗑", "Оставить отзыв ✍️", "Настройки ⚙️"],
    }
    send = {
        "uz": "Yuborish 📤",
        "ru": "Отправить 📤",
        "en": "Send 📤",
    }
    back = {
        'uz': "⬅️ Orqaga",
        "ru": "⬅️ Назад",
        "en": "⬅️ Back"
    }

    yt_file_types = {
        '720p': '📹 720 - MP4',
        # '480p': '📹 480 - MP4',
        '360p': '📹 360 - 3GP',
        'audio': '🎵 MP3',
    }

    channel = {
        'uz': 'Tekshirish ♻️',
        'ru': 'Проверить ♻️',
        'en': 'Check ♻️', }

    channel_set = {
        'uz': ["Kanal qo'shish", "⬅️ Orqaga"],
        'ru': ["Добавить канал", "⬅️ Назад"],
        'en': ["Add channel", "⬅️ Back"],
    }

    admin = {
        'uz': ["Kanal qo'shish", "Kanal sozlamalari", "Foydalanuvchilar", "Kategoriya yaratish", "Kategoriya o'chirish",
               "Mahsulot qo'shish", "Mahsulot o'chirsh", "Admin qo'shish", "Admin o'chirish", "Kuryer qo'shish",
               "Kuryer o'chirish", "Menejer qo'shish", "Menejer o'chirish", "Reklama", "Tugatilmagan Zakaslar",
               "Tugatilgan Zakaslar", "Rasmni IDsini olish"],
        'ru': ["Добавить канал", "Настройки канала", "Пользователи", "Создать категорию", "Удалить категорию",
               "Добавить продукт", "Удалить продукт", "Добавить админа", "Удалить админа", "Добавить курьера",
               "Удалить курьера", "Добавить менеджера", "Удалить менеджера", "Реклама", "Незавершенные заказы",
               "Завершенные заказы", "Получить ID фото"],
    }

    manager = {
        'uz': ["Zakaslar Statistikasi", "Foydalanuvchilar Statistikasi", "Kunlik hisobot olish"],
        'ru': ["Статистика заказов", "Статистика пользователей", "Получить ежедневный отчет"],
    }

    get_location = {
        'uz': ["📍 Mening manzillarim", "🗺 Manzilni tanlash", "⬅️ Orqaga"],
        'ru': ["📍 Мои адреса", "🗺 Выбрать адрес", "⬅️ Назад"],
        'en': ["📍 My addresses", "🗺 Select address", "⬅️ Back"],
    }

    confirmation = {
        'uz': ["Ha ✅", "⬅️ Orqaga"],
        'ru': ["Да ✅", "⬅️ Назад"],
        'en': ["Yes ✅", "⬅️ Back"],
    }

    product_back = {
        'uz': ["⬅️ Orqaga", "↪️ Asosiy menyuga", "🛒 Savatga qo'shish", "🛒 Savatga o'tish"],
        'ru': ["⬅️ Назад", "↪️ В главное меню", "🛒 Добавить в корзину", "🛒 Перейти в корзину"],
        'en': ["⬅️ Back", "↪️ Main menu", "🛒 Add to cart", "🛒 Go to cart"],
    }
    yes_no = {
        'uz': ["Ha ✅", "Yo'q ❌"],
        'ru': ["Да ✅", "Нет ❌"],
        'en': ["Yes ✅", "No ❌"],
    }

    cart = {
        'uz': ["⬅️ Orqaga ", "📤 Buyurtma berish", "🛒 Savatni tozalash"],
        'ru': ["⬅️ Назад", "📤 Оформить заказ", "🛒 Очистить корзину"],
        'en': ["⬅️ Back", "📤 Checkout", "🛒 Clear cart"],
    }

    settings = {
        'uz': ["🇺🇿 Tilni o'zgartirish 🔄", "☎️ Telefon nomerni o'zgartirish 🔄", "⬅️ Orqaga"],
        'ru': ["🇷🇺 Изменить язык 🔄", "☎️ Изменить номер телефона 🔄", "⬅️ Назад"],
        'en': ["🇺🇿 Change language 🔄", "☎️ Change phone number 🔄", "⬅️ Back"],
    }

    supplier = {
        'uz': ["Tugallanmagan zakaslar", "Tugallangan zakaslarim"],
        'ru': ["Незавершенные заказы", "Мои завершенные заказы"],
        'en': ["Unfinished orders", "My finished orders"],
    }

    supplier_order = {
        'uz': ["⏳ Jaryonda", "🏎 Yetkazyapman", "✅ Yakunlandi", "❌ Qaytarildi", "⬅️ Orqaga"],
        'ru': ["⏳ В процессе", "🏎 Доставляю", "✅ Завершен", "❌ Возвращен", "⬅️ Назад"],
        'en': ["⏳ In process", "🏎 Delivering", "✅ Finished", "❌ Returned", "⬅️ Back"],
    }


class MenejerText:
    main = {
        'uz': "<b>Admin panelga xush kelibsiz!!!</b>",
        'ru': "<b>Добро пожаловать в панель администратора!!!</b>",
        'en': "<b>Welcome to the admin panel!!!</b>",
    }

    not_found_finished_order = {
        'uz': "<b>Tugatilgan yoki qaytarilgan buyurtmalar topilmadi</b>",
        'ru': "<b>Завершенные или возвращенные заказы не найдены</b>",
        'en': "<b>Finished or returned orders not found</b>",
    }


class SupplierText:
    main = {
        'uz': "<b>Kuryer panelga xush kelibsiz!!!</b>",
        'ru': "<b>Добро пожаловать в панель курьера!!!</b>",
        'en': "<b>Welcome to the courier panel!!!</b>",
    }

    not_found_finished_order = {
        'uz': "<b>Sizda tugatilgan buyurtmalar topilmadi</b>",
        'ru': "<b>У вас нет завершенных заказов</b>",
        'en': "<b>You don't have finished orders</b>",
    }

    no_order = {
        'uz': "<b>Sizda buyurtma yo'q</b>",
        'ru': "<b>У вас нет заказа</b>",
        'en': "<b>You don't have an order</b>",
    }
    one_order_code = {
        'uz': "<b>Bajarilayotgan buyurtma raqamini kiriting !!!\n\nLakatsiyasi va statuslarini o'zgartirish imkoniyati mavjud bo'ladi</b>",
        'ru': "<b>Введите номер заказа, который выполняется !!!\n\nВы можете изменить его местоположение и статус</b>",
        'en': "<b>Enter the order number that is being executed !!!\n\nYou can change its location and status</b>",
    }

    error_order_id = {
        'uz': "<b>Bunday buyurtma xato kiritidi !!!\n\n Faqat ramalardan iborat bo'lishi kerak!!!</b>",
        'ru': "<b>Такой заказ введен неправильно !!!\n\n Должен состоять только из цифр!!!</b>",
        'en': "<b>Such an order is entered incorrectly !!!\n\n Must consist only of numbers!!!</b>",
    }

    order_status = {
        'uz': "<b>Buyurtma statusini o'zgartirildi</b>",
        'ru': "<b>Статус заказа изменен</b>",
        'en': "<b>Order status changed</b>",
    }

    error_order_status = {
        'uz': "<b>Buyurtma statusini o'zgartirishda xatolik !!!</b>",
        'ru': "<b>Ошибка при изменении статуса заказа !!!</b>",
        'en': "<b>Error changing order status !!!</b>",
    }

    order_completed = {
        'uz': "Buyurtmangiz: {}",
        'ru': "Ваш заказ: {}",
        'en': "Your order: {}",
    }
    order_status_to_admins = {
        'uz': "🛍 Buyurtma holati: \n\nNomeri: №{}\nYetkazib beruvchi: {}\nStatusi: {}",
        'ru': "🛍 Статус заказа: \n\nНомер: №{}\nДоставщик: {}\nСтатус: {}",
        'en': "🛍 Order status: \n\nNumber: №{}\nCourier: {}\nStatus: {}",
    }