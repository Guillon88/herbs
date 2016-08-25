#coding: utf-8

codes = {"Австралия": "AU",
"Австрия": "AT",
"Азербайджан": "AZ",
"Аландские острова": "AX",
"Албания": "AL",
"Алжир": "DZ",
"Виргинские Острова (США)": "VI",
"Американское Самоа": "AS",
"Ангилья": "AI",
"Ангола": "AO",
"Андорра": "AD",
"Антарктида": "AQ",
"Антигуа и Барбуда": "AG",
"Аргентина": "AR",
"Армения": "AM",
"Аруба": "AW",
"Афганистан": "AF",
"Багамы": "BS",
"Бангладеш": "BD",
"Барбадос": "BB",
"Бахрейн": "BH",
"Белиз": "BZ",
"Белоруссия": "BY",
"Бельгия": "BE",
"Бенин": "BJ",
"Бермуды": "BM",
"Болгария": "BG",
"Боливия": "BO",
"Бонэйр.  Синт-Эстатиус и Саба": "BQ",
"Босния и Герцеговина": "BA",
"Ботсвана": "BW",
"Бразилия": "BR",
"Британская территория в Индийском океане": "IO",
"Виргинские Острова (Великобритания)": "VG",
"Бруней": "BN",
"Буркина-Фасо": "BF",
"Бурунди": "BI",
"Бутан": "BT",
"Вануату": "VU",
"Ватикан": "VA",
"Великобритания": "GB",
"Венгрия": "HU",
"Венесуэла": "VE",
"Внешние малые острова (США)": "UM",
"Восточный Тимор": "TL",
"Вьетнам": "VN",
"Габон": "GA",
"Гаити": "HT",
"Гайана": "GY",
"Гамбия": "GM",
"Гана": "GH",
"Гваделупа": "GP",
"Гватемала": "GT",
"Гвиана": "GF",
"Гвинея": "GN",
"Гвинея-Бисау": "GW",
"Германия": "DE",
"Гернси": "GG",
"Гибралтар": "GI",
"Гондурас": "HN",
"Гонконг": "HK",
"Гренада": "GD",
"Гренландия": "GL",
"Греция": "GR",
"Грузия": "GE",
"Гуам": "GU",
"Дания": "DK",
"Джерси": "JE",
"Джибути": "DJ",
"Доминика": "DM",
"Доминиканская Республика": "DO",
"Демократическая Республика Конго": "CD",
"Европейский союз": "EU",
"Египет": "EG",
"Замбия": "ZM",
"САДР": "EH",
"Зимбабве": "ZW",
"Израиль": "IL",
"Индия": "IN",
"Индонезия": "ID",
"Иордания": "JO",
"Ирак": "IQ",
"Иран": "IR",
"Ирландия": "IE",
"Исландия": "IS",
"Испания": "ES",
"Италия": "IT",
"Йемен": "YE",
"Кабо-Верде": "CV",
"Казахстан": "KZ",
"Острова Кайман": "KY",
"Камбоджа": "KH",
"Камерун": "CM",
"Канада": "CA",
"Катар": "QA",
"Кения": "KE",
"Кипр": "CY",
"Киргизия": "KG",
"Кирибати": "KI",
"Китайская Республика": "TW",
"КНДР (Корейская Народно-Демократическая Республика)": "KP",
"КНР (Китайская Народная Республика)": "CN",
"Кокосовые острова": "CC",
"Колумбия": "CO",
"Коморы": "KM",
"Коста-Рика": "CR",
"Кот-д’Ивуар": "CI",
"Куба": "CU",
"Кувейт": "KW",
"Кюрасао": "CW",
"Лаос": "LA",
"Латвия": "LV",
"Лесото": "LS",
"Либерия": "LR",
"Ливан": "LB",
"Ливия": "LY",
"Литва": "LT",
"Лихтенштейн": "LI",
"Люксембург": "LU",
"Маврикий": "MU",
"Мавритания": "MR",
"Мадагаскар": "MG",
"Майотта": "YT",
"Макао": "MO",
"Македония": "MK",
"Малави": "MW",
"Малайзия": "MY",
"Мали": "ML",
"Мальдивы": "MV",
"Мальта": "MT",
"Марокко": "MA",
"Мартиника": "MQ",
"Маршалловы Острова": "MH",
"Мексика": "MX",
"Микронезия": "FM",
"Мозамбик": "MZ",
"Молдавия": "MD",
"Монако": "MC",
"Монголия": "MN",
"Монтсеррат": "MS",
"Мьянма": "MM",
"Намибия": "nan",
"Науру": "NR",
"Непал": "NP",
"Нигер": "NE",
"Нигерия": "NG",
"Нидерланды": "NL",
"Никарагуа": "NI",
"Ниуэ": "NU",
"Новая Зеландия": "NZ",
"Новая Каледония": "NC",
"Норвегия": "NO",
"ОАЭ": "AE",
"Оман": "OM",
"Остров Буве": "BV",
"Остров Мэн": "IM",
"Острова Кука": "CK",
"Остров Норфолк": "NF",
"Остров Рождества": "CX",
"Острова Питкэрн": "PN",
"Острова Святой Елены.  Вознесения и Тристан-да-Кунья": "SH",
"Пакистан": "PK",
"Палау": "PW",
"Государство Палестина": "PS",
"Панама": "PA",
"Папуа — Новая Гвинея": "PG",
"Парагвай": "PY",
"Перу": "PE",
"Польша": "PL",
"Португалия": "PT",
"Пуэрто-Рико": "PR",
"Республика Конго": "CG",
"Республика Корея": "KR",
"Реюньон": "RE",
"Россия": "RU",
"Руанда": "RW",
"Румыния": "RO",
"Сальвадор": "SV",
"Самоа": "WS",
"Сан-Марино": "SM",
"Сан-Томе и Принсипи": "ST",
"Саудовская Аравия": "SA",
"Свазиленд": "SZ",
"Северные Марианские Острова": "MP",
"Сейшельские Острова": "SC",
"Сен-Бартелеми": "BL",
"Сен-Мартен": "MF",
"Сен-Пьер и Микелон": "PM",
"Сенегал": "SN",
"Сент-Винсент и Гренадины": "VC",
"Сент-Китс и Невис": "KN",
"Сент-Люсия": "LC",
"Сербия": "RS",
"Сингапур": "SG",
"Синт-Мартен": "SX",
"Сирия": "SY",
"Словакия": "SK",
"Словения": "SI",
"Соломоновы Острова": "SB",
"Сомали": "SO",
"Судан": "SD",
"СССР (до сентября 1992 года)": "SU",
"Суринам": "SR",
"США": "US",
"Сьерра-Леоне": "SL",
"Таджикистан": "TJ",
"Таиланд": "TH",
"Танзания": "TZ",
"Тёркс и Кайкос": "TC",
"Того": "TG",
"Токелау": "TK",
"Тонга": "TO",
"Тринидад и Тобаго": "TT",
"Тувалу": "TV",
"Тунис": "TN",
"Туркмения": "TM",
"Турция": "TR",
"Уганда": "UG",
"Узбекистан": "UZ",
"Украина": "UA",
"Уоллис и Футуна": "WF",
"Уругвай": "UY",
"Фареры": "FO",
"Фиджи": "FJ",
"Филиппины": "PH",
"Финляндия": "FI",
"Фолклендские острова": "FK",
"Франция": "FR",
"Французская Полинезия": "PF",
"Французские Южные и Антарктические Территории": "TF",
"Херд и Макдональд": "HM",
"Хорватия": "HR",
"ЦАР": "CF",
"Чад": "TD",
"Черногория": "ME",
"Чехия": "CZ",
"Чили": "CL",
"Швейцария": "CH",
"Швеция": "SE",
"Шпицберген и Ян-Майен": "SJ",
"Шри-Ланка": "LK",
"Эквадор": "EC",
"Экваториальная Гвинея": "GQ",
"Эритрея": "ER",
"Эстония": "EE",
"Эфиопия": "ET",
"ЮАР": "ZA",
"Южная Георгия и Южные Сандвичевы Острова": "GS",
"Южный Судан": "SS",
"Ямайка": "JM",
"Япония": "JP",
}