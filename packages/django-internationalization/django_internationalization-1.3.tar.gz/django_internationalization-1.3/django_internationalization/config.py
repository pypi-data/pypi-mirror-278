from django.utils.translation import gettext_lazy
import os


# This is a tuple that supposedly will not change
LIST_OF_COUNTRIES : tuple = (
    ('AF', 'Afghanistan'),
    ('AX', 'Åland Islands'),
    ('AL', 'Albania'),
    ('DZ', 'Algeria'),
    ('AS', 'American Samoa'),
    ('AD', 'Andorra'),
    ('AO', 'Angola'),
    ('AI', 'Anguilla'),
    ('AQ', 'Antarctica'),
    ('AG', 'Antigua and Barbuda'),
    ('AR', 'Argentina'),
    ('AM', 'Armenia'),
    ('AW', 'Aruba'),
    ('AU', 'Australia'),
    ('AT', 'Austria'),
    ('AZ', 'Azerbaijan'),
    ('BS', 'Bahamas'),
    ('BH', 'Bahrain'),
    ('BD', 'Bangladesh'),
    ('BB', 'Barbados'),
    ('BY', 'Belarus'),
    ('BE', 'Belgium'),
    ('BZ', 'Belize'),
    ('BJ', 'Benin'),
    ('BM', 'Bermuda'),
    ('BT', 'Bhutan'),
    ('BO', 'Bolivia'),
    ('BQ', 'Bonaire, Sint Eustatius and Saba'),
    ('BA', 'Bosnia and Herzegovina'),
    ('BW', 'Botswana'),
    ('BV', 'Bouvet Island'),
    ('BR', 'Brazil'),
    ('IO', 'British Indian Ocean Territory'),
    ('BN', 'Brunei Darussalam'),
    ('BG', 'Bulgaria'),
    ('BF', 'Burkina Faso'),
    ('BI', 'Burundi'),
    ('CV', 'Cabo Verde'),
    ('KH', 'Cambodia'),
    ('CM', 'Cameroon'),
    ('CA', 'Canada'),
    ('KY', 'Cayman Islands'),
    ('CF', 'Central African Republic'),
    ('TD', 'Chad'),
    ('CL', 'Chile'),
    ('CN', 'China'),
    ('CX', 'Christmas Island'),
    ('CC', 'Cocos (Keeling) Islands'),
    ('CO', 'Colombia'),
    ('KM', 'Comoros'),
    ('CG', 'Congo'),
    ('CD', 'Democratic Republic of the Congo'),
    ('CK', 'Cook Islands'),
    ('CR', 'Costa Rica'),
    ('CI', "Côte d'Ivoire"),
    ('HR', 'Croatia'),
    ('CU', 'Cuba'),
    ('CW', 'Curaçao'),
    ('CY', 'Cyprus'),
    ('CZ', 'Czechia'),
    ('DK', 'Denmark'),
    ('DJ', 'Djibouti'),
    ('DM', 'Dominica'),
    ('DO', 'Dominican Republic'),
    ('EC', 'Ecuador'),
    ('EG', 'Egypt'),
    ('SV', 'El Salvador'),
    ('GQ', 'Equatorial Guinea'),
    ('ER', 'Eritrea'),
    ('EE', 'Estonia'),
    ('SZ', 'Eswatini'),
    ('ET', 'Ethiopia'),
    ('FK', 'Falkland Islands (Malvinas)'),
    ('FO', 'Faroe Islands'),
    ('FJ', 'Fiji'),
    ('FI', 'Finland'),
    ('FR', 'France'),
    ('GF', 'French Guiana'),
    ('PF', 'French Polynesia'),
    ('TF', 'French Southern Territories'),
    ('GA', 'Gabon'),
    ('GM', 'Gambia'),
    ('GE', 'Georgia'),
    ('DE', 'Germany'),
    ('GH', 'Ghana'),
    ('GI', 'Gibraltar'),
    ('GR', 'Greece'),
    ('GL', 'Greenland'),
    ('GD', 'Grenada'),
    ('GP', 'Guadeloupe'),
    ('GU', 'Guam'),
    ('GT', 'Guatemala'),
    ('GG', 'Guernsey'),
    ('GN', 'Guinea'),
    ('GW', 'Guinea-Bissau'),
    ('GY', 'Guyana'),
    ('HT', 'Haiti'),
    ('HM', 'Heard Island and McDonald Islands'),
    ('VA', 'Holy See'),
    ('HN', 'Honduras'),
    ('HK', 'Hong Kong'),
    ('HU', 'Hungary'),
    ('IS', 'Iceland'),
    ('IN', 'India'),
    ('ID', 'Indonesia'),
    ('IR', 'Iran'),
    ('IQ', 'Iraq'),
    ('IE', 'Ireland'),
    ('IM', 'Isle of Man'),
    ('IT', 'Italy'),
    ('JM', 'Jamaica'),
    ('JP', 'Japan'),
    ('JE', 'Jersey'),
    ('JO', 'Jordan'),
    ('KZ', 'Kazakhstan'),
    ('KE', 'Kenya'),
    ('KI', 'Kiribati'),
    ('KP', 'North Korea'),
    ('KR', 'South Korea'),
    ('KW', 'Kuwait'),
    ('KG', 'Kyrgyzstan'),
    ('LA', "Lao People's Democratic Republic"),
    ('LV', 'Latvia'),
    ('LB', 'Lebanon'),
    ('LS', 'Lesotho'),
    ('LR', 'Liberia'),
    ('LY', 'Libya'),
    ('LI', 'Liechtenstein'),
    ('LT', 'Lithuania'),
    ('LU', 'Luxembourg'),
    ('MO', 'Macao'),
    ('MG', 'Madagascar'),
    ('MW', 'Malawi'),
    ('MY', 'Malaysia'),
    ('MV', 'Maldives'),
    ('ML', 'Mali'),
    ('MT', 'Malta'),
    ('MH', 'Marshall Islands'),
    ('MQ', 'Martinique'),
    ('MR', 'Mauritania'),
    ('MU', 'Mauritius'),
    ('YT', 'Mayotte'),
    ('MX', 'Mexico'),
    ('FM', 'Micronesia'),
    ('MD', 'Moldova'),
    ('MC', 'Monaco'),
    ('MN', 'Mongolia'),
    ('ME', 'Montenegro'),
    ('MS', 'Montserrat'),
    ('MA', 'Morocco'),
    ('MZ', 'Mozambique'),
    ('MM', 'Myanmar'),
    ('NA', 'Namibia'),
    ('NR', 'Nauru'),
    ('NP', 'Nepal'),
    ('NL', 'Netherlands'),
    ('NC', 'New Caledonia'),
    ('NZ', 'New Zealand'),
    ('NI', 'Nicaragua'),
    ('NE', 'Niger'),
    ('NG', 'Nigeria'),
    ('NU', 'Niue'),
    ('NF', 'Norfolk Island'),
    ('MK', 'North Macedonia'),
    ('MP', 'Northern Mariana Islands'),
    ('NO', 'Norway'),
    ('OM', 'Oman'),
    ('PK', 'Pakistan'),
    ('PW', 'Palau'),
    ('PS', 'Palestine, State of'),
    ('PA', 'Panama'),
    ('PG', 'Papua New Guinea'),
    ('PY', 'Paraguay'),
    ('PE', 'Peru'),
    ('PH', 'Philippines'),
    ('PN', 'Pitcairn'),
    ('PL', 'Poland'),
    ('PT', 'Portugal'),
    ('PR', 'Puerto Rico'),
    ('QA', 'Qatar'),
    ('RE', 'Réunion'),
    ('RO', 'Romania'),
    ('RU', 'Russia'),
    ('RW', 'Rwanda'),
    ('BL', 'Saint Barthélemy'),
    ('SH', 'Saint Helena, Ascension and Tristan da Cunha'),
    ('KN', 'Saint Kitts and Nevis'),
    ('LC', 'Saint Lucia'),
    ('MF', 'Saint Martin'),
    ('PM', 'Saint Pierre and Miquelon'),
    ('VC', 'Saint Vincent and the Grenadines'),
    ('WS', 'Samoa'),
    ('SM', 'San Marino'),
    ('ST', 'Sao Tome and Principe'),
    ('SA', 'Saudi Arabia'),
    ('SN', 'Senegal'),
    ('RS', 'Serbia'),
    ('SC', 'Seychelles'),
    ('SL', 'Sierra Leone'),
    ('SG', 'Singapore'),
    ('SX', 'Sint Maarten'),
    ('SK', 'Slovakia'),
    ('SI', 'Slovenia'),
    ('SB', 'Solomon Islands'),
    ('SO', 'Somalia'),
    ('ZA', 'South Africa'),
    ('GS', 'South Georgia and the South Sandwich Islands'),
    ('SS', 'South Sudan'),
    ('ES', 'Spain'),
    ('LK', 'Sri Lanka'),
    ('SD', 'Sudan'),
    ('SR', 'Suriname'),
    ('SJ', 'Svalbard and Jan Mayen'),
    ('SE', 'Sweden'),
    ('CH', 'Switzerland'),
    ('SY', 'Syria'),
    ('TW', 'Taiwan'),
    ('TJ', 'Tajikistan'),
    ('TZ', 'Tanzania'),
    ('TH', 'Thailand'),
    ('TL', 'Timor-Leste'),
    ('TG', 'Togo'),
    ('TK', 'Tokelau'),
    ('TO', 'Tonga'),
    ('TT', 'Trinidad and Tobago'),
    ('TN', 'Tunisia'),
    ('TR', 'Turkey'),
    ('TM', 'Turkmenistan'),
    ('TC', 'Turks and Caicos Islands'),
    ('TV', 'Tuvalu'),
    ('UG', 'Uganda'),
    ('UA', 'Ukraine'),
    ('AE', 'United Arab Emirates'),
    ('GB', 'United Kingdom'),
    ('UM', 'United States Minor Outlying Islands'),
    ('US', 'United States of America'),
    ('UY', 'Uruguay'),
    ('UZ', 'Uzbekistan'),
    ('VU', 'Vanuatu'),
    ('VE', 'Venezuela'),
    ('VN', 'Viet Nam'),
    ('VG', 'Virgin Islands (British)'),
    ('VI', 'Virgin Islands (U.S.)'),
    ('WF', 'Wallis and Futuna'),
    ('EH', 'Western Sahara'),
    ('YE', 'Yemen'),
    ('ZM', 'Zambia'),
    ('ZW', 'Zimbabwe'),
    # --------------------------------------
    ('DE-SN', 'Saxony'),
    ('ES-CT', 'Catalonia'),
    ('ES-GA', 'Galicia'),
    ('ES-PV', 'Basque Country'),
    ('GB-WLS', 'Wales'),
    ('ES-VC', 'Valencia'),
)

# Contains data for languages including the name in one language, the name in the local language, and the country code
LANGUAGE_DATA : dict = {
    "af": {"name": gettext_lazy("Afrikaans"), "name_local": "Afrikaans", "country": "ZA"},
    "ar": {"name": gettext_lazy("Arabic"), "name_local": "اَلْعَرَبِيَّةُ", "country": "DZ"},
    "ar-DZ": {"name": gettext_lazy("Algerian Arabic"), "name_local": "الدارجة الجزائرية", "country": "DZ"},
    "ast": {"name": gettext_lazy("Asturian"), "name_local": "asturianu", "country": "ES"},
    "az": {"name": gettext_lazy("Azerbaijani"), "name_local": "Azərbaycan", "country": "AZ"},
    "be": {"name": gettext_lazy("Belarusian"), "name_local": "беларуская", "country": "BY"},
    "bg": {"name": gettext_lazy("Bulgarian"), "name_local": "Български", "country": "BG"},
    "bn": {"name": gettext_lazy("Bengali"), "name_local": "বাংলা", "country": "BD"},
    "br": {"name": gettext_lazy("Breton"), "name_local": "brezhoneg", "country": "FR"},
    "bs": {"name": gettext_lazy("Bosnian"), "name_local": "bosanski", "country": "BA"},
    "ca": {"name": gettext_lazy("Catalan"), "name_local": "català", "country": "AD"},
    "ckb": {"name": gettext_lazy("Central Kurdish (Sorani)"), "name_local": "سۆرانی", "country": "IQ"},
    "cs": {"name": gettext_lazy("Czech"), "name_local": "čeština", "country": "CZ"},
    "cy": {"name": gettext_lazy("Welsh"), "name_local": "Cymraeg", "country": "GB-WLS"},
    "da": {"name": gettext_lazy("Danish"), "name_local": "dansk", "country": "DK"},
    "de": {"name": gettext_lazy("German"), "name_local": "Deutsch", "country": "DE"},
    "dsb": {"name": gettext_lazy("Lower Sorbian"), "name_local": "dolnoserbšćina", "country": "DE"},
    "el": {"name": gettext_lazy("Greek"), "name_local": "Ελληνικά", "country": "GR"},
    "en-US": {"name": gettext_lazy("English"), "name_local": "English", "country": "US"},
    "en-AU": {"name": gettext_lazy("Australian English"), "name_local": "English", "country": "AU"},
    "en-GB": {"name": gettext_lazy("British English"), "name_local": "English", "country": "GB"},
    "eo": {"name": gettext_lazy("Esperanto"), "name_local": "Lingvo Internacia", "country": None},
    "es": {"name": gettext_lazy("Spanish"), "name_local": "español", "country": "ES"},
    "es-AR": {"name": gettext_lazy("Argentinian Spanish"), "name_local": "español", "country": "AR"},
    "es-CO": {"name": gettext_lazy("Colombian Spanish"), "name_local": "español", "country": "CO"},
    "es-MX": {"name": gettext_lazy("Mexican Spanish"), "name_local": "español", "country": "MX"},
    "es-NI": {"name": gettext_lazy("Nicaraguan Spanish"), "name_local": "español", "country": "NI"},
    "es-VE": {"name": gettext_lazy("Venezuelan Spanish"), "name_local": "español", "country": "VE"},
    "et": {"name": gettext_lazy("Estonian"), "name_local": "eesti keel", "country": "EE"},
    "eu": {"name": gettext_lazy("Basque"), "name_local": "euskara", "country": "ES"},
    "fa": {"name": gettext_lazy("Persian"), "name_local": "فارسی", "country": "IR"},
    "fi": {"name": gettext_lazy("Finnish"), "name_local": "suomi", "country": "FI"},
    "fr": {"name": gettext_lazy("French"), "name_local": "français", "country": "FR"},
    "fy": {"name": gettext_lazy("Frisian"), "name_local": "Frysk", "country": "NL"},
    "ga": {"name": gettext_lazy("Irish"), "name_local": "Gaeilge", "country": "IE"},
    "gd": {"name": gettext_lazy("Scottish Gaelic"), "name_local": "Gàidhlig", "country": "GB"},
    "gl": {"name": gettext_lazy("Galician"), "name_local": "galego", "country": "ES"},
    "he": {"name": gettext_lazy("Hebrew"), "name_local": "עִבְֿרִית", "country": "IL"},
    "hi": {"name": gettext_lazy("Hindi"), "name_local": "हिन्दी", "country": "IN"},
    "hr": {"name": gettext_lazy("Croatian"), "name_local": "hrvatski", "country": "HR"},
    "hsb": {"name": gettext_lazy("Upper Sorbian"), "name_local": "hornjoserbšćina", "country": "DE-SN"},
    "hu": {"name": gettext_lazy("Hungarian"), "name_local": "magyar", "country": "HU"},
    "hy": {"name": gettext_lazy("Armenian"), "name_local": "հայերեն", "country": "AM"},
    "ia": {"name": gettext_lazy("Interlingua"), "name_local": "interlingua", "country": None},
    "id": {"name": gettext_lazy("Indonesian"), "name_local": "Bahasa Indonesia", "country": "ID"},
    "ig": {"name": gettext_lazy("Igbo"), "name_local": "Ìgbò", "country": "NG"},
    "io": {"name": gettext_lazy("Ido"), "name_local": "Ido", "country": "FI"},
    "is": {"name": gettext_lazy("Icelandic"), "name_local": "íslenska", "country": "IS"},
    "it": {"name": gettext_lazy("Italian"), "name_local": "italiano", "country": "IT"},
    "ja": {"name": gettext_lazy("Japanese"), "name_local": "日本語", "country": "JP"},
    "ka": {"name": gettext_lazy("Georgian"), "name_local": "ქართული", "country": "GE"},
    "kab": {"name": gettext_lazy("Kabyle"), "name_local": "ⵜⴰⵇⴱⴰⵢⵍⵉⵜ", "country": "DZ"},
    "kk": {"name": gettext_lazy("Kazakh"), "name_local": "қазақ", "country": "KZ"},
    "km": {"name": gettext_lazy("Khmer"), "name_local": "ខ្មែរ", "country": "KH"},
    "kn": {"name": gettext_lazy("Kannada"), "name_local": "ಕನ್ನಡ", "country": "IN"},
    "ko": {"name": gettext_lazy("Korean"), "name_local": "조선말", "country": "KP"}, 
    "ky": {"name": gettext_lazy("Kyrgyz"), "name_local": "Кыргыз", "country": "KG"},
    "lb": {"name": gettext_lazy("Luxembourgish"), "name_local": "Lëtzebuergesch", "country": "LU"},
    "lt": {"name": gettext_lazy("Lithuanian"), "name_local": "lietuvių", "country": "LT"},
    "lv": {"name": gettext_lazy("Latvian"), "name_local": "latviešu", "country": "LV"},
    "mk": {"name": gettext_lazy("Macedonian"), "name_local": "македонски", "country": "MK"},
    "ml": {"name": gettext_lazy("Malayalam"), "name_local": "മലയാളം", "country": "IN"},
    "mn": {"name": gettext_lazy("Mongolian"), "name_local": "монгол", "country": "MN"},
    "mr": {"name": gettext_lazy("Marathi"), "name_local": "मराठी", "country": "IN"},
    "ms": {"name": gettext_lazy("Malay"), "name_local": "Melayu", "country": "MY"},
    "my": {"name": gettext_lazy("Burmese"), "name_local": "မြန်မာ", "country": "MM"},
    "nb": {"name": gettext_lazy("Norwegian Bokmål"), "name_local": "bokmål", "country": "NO"},
    "ne": {"name": gettext_lazy("Nepali"), "name_local": "नेपाली", "country": "NP"},
    "nl": {"name": gettext_lazy("Dutch"), "name_local": "Nederlands", "country": "NL"},
    "nn": {"name": gettext_lazy("Norwegian Nynorsk"), "name_local": "nynorsk", "country": "NO"},
    "os": {"name": gettext_lazy("Ossetic"), "name_local": "ирон ӕвзаг", "country": "RU"},
    "pa": {"name": gettext_lazy("Punjabi"), "name_local": "ਪੰਜਾਬੀ", "country": "PK"},
    "pl": {"name": gettext_lazy("Polish"), "name_local": "polski", "country": "PL"},
    "pt": {"name": gettext_lazy("Portuguese"), "name_local": "português", "country": "PT"},
    "pt-BR": {"name": gettext_lazy("Brazilian Portuguese"), "name_local": "português", "country": "BR"},
    "ro": {"name": gettext_lazy("Romanian"), "name_local": "Română", "country": "RO"},
    "ru": {"name": gettext_lazy("Russian"), "name_local": "Русский", "country": "RU"},
    "sk": {"name": gettext_lazy("Slovak"), "name_local": "slovenský", "country": "SK"},
    "sl": {"name": gettext_lazy("Slovenian"), "name_local": "slovenščina", "country": "SI"},
    "sq": {"name": gettext_lazy("Albanian"), "name_local": "shqip", "country": "AL"},
    "sr": {"name": gettext_lazy("Serbian"), "name_local": "српски", "country": "RS"},
    "sr-LATN": {"name": gettext_lazy("Serbian Latin"), "name_local": "srpski", "country": "RS"},
    "sv": {"name": gettext_lazy("Swedish"), "name_local": "Svenska", "country": "SE"},
    "sw": {"name": gettext_lazy("Swahili"), "name_local": "Kiswahili", "country": "TZ"},
    "ta": {"name": gettext_lazy("Tamil"), "name_local": "தமிழ்", "country": "IN"},
    "te": {"name": gettext_lazy("Telugu"), "name_local": "తెలుగు", "country": "IN"},
    "tg": {"name": gettext_lazy("Tajik"), "name_local": "Тоҷикӣ", "country": "TJ"},
    "th": {"name": gettext_lazy("Thai"), "name_local": "แบบไทย", "country": "TH"},
    "tk": {"name": gettext_lazy("Turkmen"), "name_local": "türkmençe", "country": "TM"},
    "tr": {"name": gettext_lazy("Turkish"), "name_local": "Türkçe", "country": "TR"},
    "tt": {"name": gettext_lazy("Tatar"), "name_local": "татар", "country": "RU"},
    "udm": {"name": gettext_lazy("Udmurt"), "name_local": "Удмурт", "country": "RU"},
    "ug": {"name": gettext_lazy("Uyghur"), "name_local": "ئۇيغۇر", "country": "CN"},
    "uk": {"name": gettext_lazy("Ukrainian"), "name_local": "українська", "country": "UA"},
    "ur": {"name": gettext_lazy("Urdu"), "name_local": "اردو", "country": "PK"},
    "uz": {"name": gettext_lazy("Uzbek"), "name_local": "Oʻzbekcha", "country": "UZ"},
    "vi": {"name": gettext_lazy("Vietnamese"), "name_local": "Tiếng Việt", "country": "VN"},
    "zh-HANS": {"name": gettext_lazy("Simplified Chinese"), "name_local": "汉字", "country": "CN"},
    "zh-HANT": {"name": gettext_lazy("Traditional Chinese"), "name_local": "漢字", "country": "CN"},
    
}

# Tuple of tuples containing language locale and name
LANGUAGES : tuple = tuple((key, value['name']) for key, value in LANGUAGE_DATA.items())
LANGUAGES_LOCAL : tuple = tuple((key, value['name_local']) for key, value in LANGUAGE_DATA.items())

LANGUAGE_CODE : str = 'en-US'

APP_TRANSLATION_PATH : str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'translations')

APP_LOCALE_PATH : str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locale')

SYSTEM_TRANSLATION_TAGS : list = ['system', 'django-admin', 'admin-panel']

# To be added
LANGUAGES_TO_BE_ADDED = ( 
    ("fa_AF", "فارسی"), # Persian (Afghanistan)
    ("ps_AF", "پښتو"), # Pashto (Afghanistan)
    ("sq", "shqip"), # Albanian (Albania)
    ("ar_DZ", "العربيّة"), # Arabic (Algeria)
    ("ber_DZ", "تَمَزِيغت"), # Berber (Algeria)
    ("ca", "català"), # Catalan (Andorra)
    ("pt_AO", "português"), # Portuguese (Angola)
    ("en_AG", "English"), # English (Antigua and Barbuda)
    ("es_AR", "Español"), # Spanish (Argentina)
    ("hy", "հայերէն"), # Armenian (Armenia)
    ("en_AU", "English"), # English (Australia)
    ("de_AT", "Deutsch"), # German (Austria)
    ("az", "Azərbaycanca"), # Azerbaijani (Azerbaijan)
    ("en_BS", "English"), # English (Bahamas)
    ("ar_BH", "العربيّة"), # Arabic (Bahrain)
    ("bn_BD", "বাংলা"), # Bengali (Bangladesh)
    ("en_BB", "English"), # English (Barbados)
    ("be", "Беларуская"), # Belarusian (Belarus)
    ("ru_BY", "русский"), # Russian (Belarus)
    ("nl_BE", "Nederlands"), # Dutch (Belgium)
    ("fr_BE", "Français"), # French (Belgium)
    ("de_BE", "Deutsch"), # German (Belgium)
    ("en_BZ", "English"), # English (Belize)
    ("fr_BJ", "Français"), # French (Benin)
    ("dz", "རྫོང་ཁ་"), # Dzongkha (Bhutan)
    ("es_BO", "castellano"), # Castilian (Bolivia)
    ("aro", "Araona"), # Araona (Bolivia)
    ("cav", "Cavineña"), # Cavineña (Bolivia)
    ("cyb", "Kayuvava"), # Cayubaba (Bolivia)
    ("cao", "Chokobo_Pakawara"), # Chácobo (Bolivia)
    ("qu", "Kechua"), # Quechua (Bolivia)
    ("gn_BO", "avañe'ẽ"), # Guaraní (Bolivia)
    ("bs", "bosanski"), # Bosnian (Bosnia and Herzegovina)
    ("hr_BA", "hrvatski"), # Croatian (Bosnia and Herzegovina)
    ("sr_BA", "српски"), # Serbian (Bosnia and Herzegovina)
    ("en_BW", "English"), # English (Botswana)
    ("pt_BR", "português"), # Portuguese (Brazil)
    ("ms_BN", "بهاس ملايو"), # Malay (Brunei)
    ("bg", "български"), # Bulgarian (Bulgaria)
    ("fr_BF", "Français"), # French (Burkina Faso)
    ("fr_BI", "Français"), # French (Burundi)
    ("rn", "Ikirundi"), # Kirundi (Burundi)
    ("en_BI", "English"), # English (Burundi)
    ("km", "ភាសាខ្មែរ"), # Khmer (Cambodia)
    ("en_CM", "English"), # English (Cameroon)
    ("fr_CM", "Français"), # French (Cameroon)
    ("en_CA", "English"), # English (Canada)
    ("fr_CA", "Français"), # French (Canada)
    ("pt_CV", "português"), # Portuguese (Cape Verde)
    ("fr_CF", "Français"), # French (Central African Republic)
    ("sg", "sängö"), # Sango (Central African Republic)
    ("ar_TD", "العربيّة"), # Arabic (Chad)
    ("fr_TD", "Français"), # French (Chad)
    ("es_CL", "Español"), # Spanish (Chile)
    ("zh", "汉语"), # Chinese (China)
    ("en_CX", "English"), # English (Christmas Island)
    ("cmn_CX", "官话"), # Mandarin (Christmas Island)
    ("ms_CX", "بهاس ملايو"), # Malay (Christmas Island)
    ("en_CC", "English"), # English (Cocos Islands)
    ("coa", "Basa Pulu Cocos"), # Cocos Malay (Cocos Islands)
    ("es_CO", "Español"), # Spanish (Colombia)
    ("ar_KM", "العربيّة"), # Arabic (Comoros)
    ("zdj", "شِكُمُرِ"), # Comorian (Comoros)
    ("wni", "شِكُمُرِ"), # Comorian (Comoros)
    ("swb", "شِكُمُرِ"), # Comorian (Comoros)
    ("wlc", "شِكُمُرِ"), # Comorian (Comoros)
    ("fr_KM", "Français"), # French (Comoros)
    ("fr_CD", "Français"), # French (Democratic Republic of the Congo)
    ("fr_CG", "Français"), # French (Republic of the Congo)
    ("en_CK", "English"), # English (Cook Islands)
    ("mi_CK", "Māori"), # Maori (Cook Islands)
    ("es_CR", "Español"), # Spanish (Costa Rica)
    ("hr", "hrvatski"), # Croatian (Croatia)
    ("es_CU", "Español"), # Spanish (Cuba)
    ("el_CY", "Ελληνικά"), # Greek (Cyprus)
    ("tr_CY", "Türkçe"), # Turkish (Cyprus)
    ("cs", "česky"), # Czech (Czech Republic)
    ("sk_CZ", "slovenčina"), # Slovak (Czech Republic)
    ("da", "dansk"), # Danish (Denmark)
    ("ar_DJ", "العربيّة"), # Arabic (Djibouti)
    ("fr_DJ", "Français"), # French (Djibouti)
    ("en_DM", "English"), # English (Dominica)
    ("es_DO", "Español"), # Spanish (Dominican Republic)
    ("pt_TL", "português"), # Portuguese (East Timor)
    ("tet_TL", "Tetun"), # Tetum (East Timor)
    ("es_EC", "Español"), # Spanish (Ecuador)
    ("ar_EG", "العربيّة"), # Arabic (Egypt)
    ("es_SV", "Español"), # Spanish (El Salvador)
    ("fr_GQ", "Français"), # French (Equatorial Guinea)
    ("pt_GQ", "português"), # Portuguese (Equatorial Guinea)
    ("es_GQ", "Español"), # Spanish (Equatorial Guinea)
    ("ti_ER", "ትግርኛ"), # Tigrinya (Eritrea)
    ("et", "eesti"), # Estonian (Estonia)
    ("en_SZ", "English"), # English (Eswatini)
    ("ss_SZ", "siSwati"), # Swazi (Eswatini)
    ("aa_ET", "Qafar af"), # Afar (Ethiopia)
    ("am", "አማርኛ"), # Amharic (Ethiopia)
    ("om_ET", "Oromoo"), # Oromo (Ethiopia)
    ("so_ET", "اَف سٝومالِ"), # Somali (Ethiopia)
    ("ti_ET", "ትግርኛ"), # Tigrinya (Ethiopia)
    ("en_FJ", "English"), # English (Fiji)
    ("fj", "Vosa Vaka_Viti"), # Fijian (Fiji)
    ("hif", "फ़िजी हिंदी"), # Fiji Hindi (Fiji)
    ("fi", "suomi"), # Finnish (Finland)
    ("sv_FI", "Svenska"), # Swedish (Finland)
    ("fr", "Français"), # French (France)
    ("fr_GA", "Français"), # French (Gabon)
    ("en_GM", "English"), # English (Gambia)
    ("ka", "ქართული ენა"), # Georgian (Georgia)
    ("de", "Deutsch"), # German (Germany)
    ("en_GH", "English"), # English (Ghana)
    ("el", "Ελληνικά"), # Greek (Greece)
    ("en_GD", "English"), # English (Grenada)
    ("es_GT", "Español"), # Spanish (Guatemala)
    ("fr_GN", "Français"), # French (Guinea)
    ("pt_GW", "português"), # Portuguese (Guinea_Bissau)
    ("en_GY", "English"), # English (Guyana)
    ("fr_HT", "Français"), # French (Haiti)
    #("#", "/"), # Creole (Haiti)
    ("es_HN", "Español"), # Spanish (Honduras)
    ("hu", "magyar nyelv"), # Hungarian (Hungary)
    ("is", "Íslenska"), # Icelandic (Iceland)
    ("hi", "हिन्दी"), # Hindi (India)
    ("en_IN", "English"), # English (India)
    ("id", "Indonesia"), # Indonesian (Indonesia)
    ("fa_IR", "فارسی"), # Persian (Iran)
    ("ar_IQ", "العربيّة"), # Arabic (Iraq)
    ("ckb", "کوردی"), # Kurdish (Iraq)
    ("ga", "Gaeilge"), # Irish (Ireland)
    ("en_IE", "English"), # English (Ireland)
    ("he_IL", "עִבְֿרִית"), # Hebrew (Israel)
    ("it", "Italiano"), # Italian (Italy)
    ("fr_CI", "Français"), # French (Ivory Coast)
    ("en_JM", "English"), # English (Jamaica)
    ("ja", "日本語"), # Japanese (Japan)
    ("ar_JO", "العربيّة"), # Arabic (Jordan)
    ("kk", "قازاقشا"), # Kazakh (Kazakhstan)
    ("ru_KZ", "русский"), # Russian (Kazakhstan)
    ("en_KE", "English"), # English (Kenya)
    ("sw_KE", "كِسوَحِيلِ"), # Swahili (Kenya)
    ("en_KI", "English"), # English (Kiribati)
    ("gil", "Kiribati"), # Gilbertese (Kiribati)
    ("ko_KP", "조선말"), # Korean (North Korea)
    ("ko_KR", "한국어"), # Korean (South Korea)
    #("sq_", "shqip"), # Albanian (Kosovo)
    #("#", "српски"), # Serbian (Kosovo)
    ("ar_KW", "العربيّة"), # Arabic (Kuwait)
    ("ky", "قىرعىز تىلى"), # Kyrgyz (Kyrgyzstan)
    ("ru_KG", "русский"), # Russian (Kyrgyzstan)
    ("lo", "ພາສາລາວ"), # Lao (Laos)
    ("lv", "Lettish"), # Latvian (Latvia)
    ("ar_LB", "العربيّة"), # Arabic (Lebanon)
    ("st_LS", "Sesotho"), # Sotho (Lesotho)
    ("en_LS", "English"), # English (Lesotho)
    ("en_LR", "English"), # English (Liberia)
    ("ar_LY", "العربيّة"), # Arabic (Libya)
    ("de_LI", "Deutsch"), # German (Liechtenstein)
    ("lt", "lietuvių"), # Lithuanian (Lithuania)
    ("fr_LU", "Français"), # French (Luxembourg)
    ("de_LU", "Deutsch"), # German (Luxembourg)
    ("lb", "Lëtzebuergesch"), # Luxembourgish (Luxembourg)
    ("fr_MG", "Français"), # French (Madagascar)
    ("mg", "مَلَغَسِ"), # Malagasy (Madagascar)
    ("en_MW", "English"), # English (Malawi)
    ("ny_MW", "Chichewa"), # Chichewa (Malawi)
    ("ms", "بهاس ملايو"), # Malay (Malaysia)
    ("dv", "ދިވެހި"), # Dhivehi (Maldives)
    ("bm", "ߓߡߊߣߊ߲ߞߊ߲"), # Bambara (Mali)
    ("bbo", "Bobo"), # Bobo (Mali)
    ("boz", "Bozo"), # Bozo (Mali)
    ("mey", "حسانية"), # Hassaniya (Mali)
    ("kao", "Xaasongaxango"), # Kassonke (Mali)
    ("mku", "ߡߊ߬ߣߌ߲߬ߞߊ߬ߞߊ߲"), # Maninke (Mali)
    ("myk", "Mamara"), # Minyanka (Mali)
    ("snk", "سࣷونِکَنْخَنّࣹ"), # Soninke (Mali)
    ("taq", "Tafaghist"), # Tamasheq (Mali)
    ("mt", "Malti"), # Maltese (Malta)
    ("en_MT", "English"), # English (Malta)
    ("en_MH", "English"), # English (Marshall Islands)
    ("mh", "Kajin M̧ajel‌̧"), # Marshallese (Marshall Islands)
    ("ar_MR", "العربيّة"), # Arabic (Mauritania)
    ("en_MU", "English"), # English (Mauritius)
    ("mfe", "morisien"), # Morisien (Mauritius)
    ("es_MX", "Español"), # Spanish (Mexico)
    ("en_FM", "English"), # English (Micronesia)
    ("ro_MD", "românește"), # Romanian (Moldova)
    ("fr_MC", "Français"), # French (Monaco)
    ("mn", "ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ"), # Mongolian (Mongolia)
    ("cnr", "црногорски"), # Montenegrin (Montenegro)
    ("ar_MA", "العربيّة"), # Arabic (Morocco)
    ("ber_MA", "تَمَزِيغت"), # Berber (Morocco)
    ("pt_MZ", "português"), # Portuguese (Mozambique)
    ("my_MM", "မြန်မာဘာသာ"), # Burmese (Myanmar)
    ("en_NA", "English"), # English (Namibia)
    ("en_NR", "English"), # English (Nauru)
    ("na", "Naoero"), # Nauruan (Nauru)
    ("ne", "नेपाली"), # Nepali (Nepal)
    ("nl", "Nederlands"), # Dutch (Netherlands)
    ("en_NZ", "English"), # English (New Zealand)
    ("mi_NZ", "Māori"), # Maori (New Zealand)
    ("es_NI", "Español"), # Spanish (Nicaragua)
    ("fr_NE", "Français"), # French (Niger)
    ("en_NG", "English"), # English (Nigeria)
    ("en_NU", "English"), # English (Niue)
    ("niu", "ko e vagahau Niuē"), # Niuean (Niue)
    ("en_NF", "English"), # English (Norfolk Island)
    ("pih", "Norf'k"), # Norfuk (Norfolk Island)
    ("mk", "македонски"), # Macedonian (North Macedonia)
    ("sq_MK", "shqip"), # Albanian (North Macedonia)
    ("no", "norsk"), # Norwegian (Norway)
    ("ar_OM", "العربيّة"), # Arabic (Oman)
    ("ur_PK", "اُردُو"), # Urdu (Pakistan)
    ("en_PK", "English"), # English (Pakistan)
    ("en_PW", "English"), # English (Palau)
    ("pau", "a tekoi er a Belau"), # Palauan (Palau)
    ("ar_PS", "العربيّة"), # Arabic (Palestine)
    ("es_PA", "Español"), # Spanish (Panama)
    ("en_PG", "English"), # English (Papua New Guinea)
    #("/", "/"), # Hiri Motu (Papua New Guinea)
    ("tpi", "Tok Pisin"), # Tok Pisin (Papua New Guinea)
    ("es_PY", "Español"), # Spanish (Paraguay)
    ("gn_PY", "avañe'ẽ"), # Guaraní (Paraguay)
    ("es_PE", "Español"), # Spanish (Peru)
    ("fil", "Tagalog"), # Filipino (Philippines)
    ("en_PH", "English"), # English (Philippines)
    ("pl", "polski"), # Polish (Poland)
    ("pt", "português"), # Portuguese (Portugal)
    ("ar_QA", "العربيّة"), # Arabic (Qatar)
    ("ro", "românește"), # Romanian (Romania)
    ("ru", "русский"), # Russian (Russia)
    ("en_RW", "English"), # English (Rwanda)
    ("fr_RW", "Français"), # French (Rwanda)
    ("rw", "Ikinyarwanda"), # Kinyarwanda (Rwanda)
    ("sw_RW", "كِسوَحِيلِ"), # Swahili (Rwanda)
    ("ar_EH", "العربيّة"), # Arabic (Sahrawi Arab Democratic Republic)
    ("es_EH", "Español"), # Spanish (Sahrawi Arab Democratic Republic)
    ("en_KN", "English"), # English (Saint Kitts and Nevis)
    ("en_LC", "English"), # English (Saint Lucia)
    ("en_VC", "English"), # English (Saint Vincent and the Grenadines)
    ("en_WS", "English"), # English (Samoa)
    ("sm", "Gagana faʻa Sāmoa"), # Samoan (Samoa)
    ("it_SM", "Italiano"), # Italian (San Marino)
    ("pt_ST", "português"), # Portuguese (São Tomé and Príncipe)
    ("ar_SA", "العربيّة"), # Arabic (Saudi Arabia)
    ("fr_SN", "Français"), # French (Senegal)
    ("sr", "српски"), # Serbian (Serbia)
    ("en_SC", "English"), # English (Seychelles)
    ("fr_SC", "Français"), # French (Seychelles)
    #("/", "/"), # Seychellois Creole (Seychelles)
    ("en_SL", "English"), # English (Sierra Leone)
    ("en_SG", "English"), # English (Singapore)
    ("ms_SG", "بهاس ملايو"), # Malay (Singapore)
    ("cmn_SG", "官话"), # Mandarin Chinese (Singapore)
    ("ta_SG", "தமிழ்"), # Tamil (Singapore)
    ("sk", "slovenčina"), # Slovak (Slovakia)
    ("sl", "slovenščina"), # Slovene (Slovenia)
    ("en_SB", "English"), # English (Solomon Islands)
    ("so", "اَف سٝومالِ"), # Somali (Somalia)
    ("ar_SO", "العربيّة"), # Arabic (Somalia)
    ("af", "Afrikaans"), # Afrikaans (South Africa)
    ("en_ZA", "English"), # English (South Africa)
    ("nr_ZA", "isiNdebele"), # Southern Ndebele (South Africa)
    ("st_ZA", "Sesotho"), # Sotho (South Africa)
    ("ss_ZA", "siSwati"), # Swazi (South Africa)
    ("ts_ZA", "Xitsonga"), # Tsonga (South Africa)
    ("tn_ZA", "Setswana"), # Tswana (South Africa)
    ("ve_ZA", "Tshivenḓa"), # Venda (South Africa)
    ("xh_ZA", "isiXhosa"), # Xhosa (South Africa)
    ("zu", "isiZulu"), # Zulu (South Africa)
    #("#", "/"), # Ossetian (South Ossetia)
    #("ru_", "русский"), # Russian (South Ossetia)
    ("en_SS", "English"), # English (South Sudan)
    ("es_ES", "Español"), # Spanish (Spain)
    ("si", "සිංහල"), # Sinhala (Sri Lanka)
    ("ta_LK", "தமிழ்"), # Tamil (Sri Lanka)
    ("ar_SD", "العربيّة"), # Arabic (Sudan)
    ("en_SS", "English"), # English (Sudan)
    ("nl_SR", "Nederlands"), # Dutch (Suriname)
    ("sv", "Svenska"), # Swedish (Sweden)
    ("fr_CH", "Français"), # French (Switzerland)
    ("de_CH", "Deutsch"), # German (Switzerland)
    ("it_CH", "Italiano"), # Italian (Switzerland)
    ("rm", "romontsch"), # Romansh (Switzerland)
    ("ar_SY", "العربيّة"), # Arabic (Syria)
    ("cmn_TW", "官话"), # Mandarin (Taiwan)
    ("tg", "Тоҷикӣ"), # Tajik (Tajikistan)
    ("sw_TZ", "كِسوَحِيلِ"), # Swahili (Tanzania)
    ("en_TZ", "English"), # English (Tanzania)
    ("th", "ภาษาไทย"), # Thai (Thailand)
    ("fr_TG", "Français"), # French (Togo)
    ("en_TK", "English"), # English (Tokelau)
    ("tkl", "Tokelau"), # Tokelauan (Tokelau)
    ("en_TO", "English"), # English (Tonga)
    ("to", "lea faka_Tonga"), # Tongan (Tonga)
    #("#", "/"), # Moldovan (Transnistria)
    #("ru_", "русский"), # Russian (Transnistria)
    #("#", "/"), # Ukrainian (Transnistria)
    ("en_TT", "English"), # English (Trinidad and Tobago)
    ("ar_TN", "العربيّة"), # Arabic (Tunisia)
    ("tr", "Türkçe"), # Turkish (Turkey)
    ("tk", "تۆرکمنچه"), # Turkmek (Turkmenistan)
    ("tvl", "Tuuvalu"), # Tuvaluan (Tuvalu)
    ("en_TV", "English"), # English (Tuvalu)
    ("en_UG", "English"), # English (Uganda)
    ("sw_UG", "كِسوَحِيلِ"), # Swahili (Uganda)
    ("uk", "українська"), # Ukrainian (Ukraine)
    ("ar_AE", "العربيّة"), # Arabic (United Arab Emirates)
    ("en_GB", "English"), # English (United Kingdom)
    ("en_US", "English"), # English (United States)
    ("es_UY", "Español"), # Spanish (Uruguay)
    ("uz", "اۉزبېکچه"), # Uzbek (Uzbekistan)
    ("en_VU", "English"), # English (Vanuatu)
    ("fr_VU", "Français"), # French (Vanuatu)
    #("#", "/"), # Bislama (Vanuatu)
    ("es_VE", "Español"), # Spanish (Venezuela)
    ("vi", "tiếng Việt"), # Vietnamese (Vietnam)
    ("ar_YE", "العربيّة"), # Arabic (Yemen)
    ("en_ZM", "English"), # English (Zambia)
    ("ny", "Chichewa"), # Chewa (Zimbabwe)
    #("#", "/"), # Chibarwe (Zimbabwe)
    ("en_ZW", "English"), # English (Zimbabwe)
    ("kck", "Ikalanga"), # Kalanga (Zimbabwe)
    ("nmq", "Nanzva"), # Nambya (Zimbabwe)
    ("nd_ZW", "isiNdebele"), # Northern Ndebele (Zimbabwe)
    ("ts_ZW", "Xitsonga"), # Shangani (Zimbabwe)
    ("sn_ZW", "chiShona"), # Shona (Zimbabwe)
    ("st_ZW", "Sesotho"), # Sotho (Zimbabwe)
    ("to_ZW", "lea faka-Tonga"), # Tonga (Zimbabwe)
    ("tn_ZW", "Setswana"), # Tswana (Zimbabwe)
    ("ve_ZW", "Tshivenḓa"), # Venda (Zimbabwe)
    ("xh_ZW", "isiXhosa"), # Xhosa (Zimbabwe)
    ("cy", "Cymraeg"), # Welsh (Britain)
    # ----------------------------------------------
    # Widely spoken languages
    # ----------------------------------------------
    ("it_AL", "Italiano"), # Italian (Albania)
    ("fr_DZ", "Français"), # French (Algeria)
    #("#", "/"), # Creole (Antigua and Barbuda)
    ("ru_AM", "русский"), # Russian (Armenia)
    ("en_AT", "English"), # English (Austria)
    ("ru_AZ", "русский"), # Russian (Azerbaijan)
    ("en_BE", "English"), # English (Belgium)
    ("bzj", "Creole"), # Kriol (Belize)
    ("es_BZ", "Español"), # Spanish (Belize)
    ("sw_BI", "كِسوَحِيلِ"), # Swahili (Burundi)
    ("en_HR", "English"), # English (Croatia)
    ("en_CY", "English"), # English (Cyprus)
    ("en_DK", "English"), # English (Denmark)
    ("en_EG", "English"), # English (Egypt)
    ("ar_ER", "العربيّة"), # Arabic (Eritrea)
    ("it_ER", "Italiano"), # Italian (Eritrea)
    ("ru_EE", "русский"), # Russian (Estonia)
    ("en_FI", "English"), # English (Finland)
    #("#", "/"), # Occitan (France)
    ("ru_GE", "русский"), # Russian (Georgia)
    ("en_DE", "English"), # English (Germany)
    ("ff", "فولا"), # Fula
    #("#", "/"), # Maninka (Guinea)
    ("sus", "Sosoxui"), # Susu (Guinea)
    #("#", "/"), # Guyanese Creole (Guyana)
    ("bn_IN", "বাংলা"), # Bengali (India)
    ("mr", "मराठी"), # Marathi (India)
    ("te", "తెలుగు"), # Telugu (India)
    ("ta_IN", "தமிழ்"), # Tamil (India)
    ("gu_IN", "ગુજરાતી"), # Gujarati (India)
    ("ur_IN", "اُردُو"), # Urdu (India)
    ("kn", "ಕನ್ನಡ"), # Kannada (India)
    ("or", "ଓଡ଼ିଆ"), # Odia (India)
    ("ms", "بهاس ملايو"), # Malayalam (India)
    ("pa_IN", "ਪੰਜਾਬੀ"), # Punjabi (India)
    ("ms", "بهاس ملايو"), # Malay (Indonesia)
    #("#", "/"), # Javanese (Indonesia)
    #("#", "/"), # Sundanese (Indonesia)
    #("#", "/"), # Madurese (Indonesia)
    #("#", "/"), # Minangkabau (Indonesia)
    ("ru_IL", "русский"), # Russian (Israel)
    ("en_IL", "English"), # English (Israel)
    ("ru_LV", "русский"), # Russian (Latvia)
    ("en_LB", "English"), # English (Lebanon)
    ("fr_LB", "Français"), # French (Lebanon)
    ("pl_LT", "polski"), # Polish (Lithuania)
    ("ru_LT", "русский"), # Russian (Lithuania)
    ("en_LU", "English"), # English (Luxembourg)
    ("pt_LU", "português"), # Portuguese (Luxembourg)
    ("cmn_MY", "官话"), # Mandarin Chinese (Malaysia)
    ("yue_MY", "廣東話"), # Cantonese (Malaysia)
    ("ta_MY", "தமிழ்"), # Tamil (Malaysia)
    ("en_MY", "English"), # English (Malaysia)
    ("en_MV", "English"), # English (Maldives)
    ("fr_MR", "Français"), # French (Mauritania)
    #("#", "munegascu"), # Monégasque (Monaco)
    ("en_MM", "English"), # English (Myanmar)
    ("en_NL", "English"), # English (Netherlands)
    ("ha", "هَرْشٜىٰن هَوْسَا"), # Hausa (Nigeria)
    ("en_NO", "English"), # English (Norway)
    ("pa_PK", "پنجابی"), # Punjabi (Pakistan)
    ("bal", "بلۏچی"), # Balochi (Pakistan)
    ("sd_PK", "سِنڌِي"), # Sindhi (Pakistan)
    ("sd_IN", "सिन्धी"), # Sindhi (India)
    ("ps_PK", "پښتو"), # Pashto (Pakistan)
    ("skr", "سرائیکی"), # Saraiki (Pakistan)
    ("en_PS", "English"), # English (Palestine)
    ("he_PS", "עִבְֿרִית"), # Hebrew (Palestine)
    ("en_PL", "English"), # English (Poland)
    ("en_PT", "English"), # English (Portugal)
    ("fil_SA", "Tagalog"), # Filipino (Saudi Arabia)
    ("bn_SA", "বাংলা"), # Bengali (Saudi Arabia)
    ("en_LK", "English"), # English (Sri Lanka)
    ("ru_TJ", "русский"), # Russian (Tajikistan)
    ("my_TH", "မြန်မာဘာသာ"), # Burmese (Thailand)
    #("#", "/"), # Creole (Trinidad and Tobago)
    ("ru_TM", "русский"), # Russian (Turkmenistan)
    ("en_AE", "English"), # English (United Arab Emirates)
    ("es_US", "Español"), # Spanish (United States)
    ("ru_UZ", "русский"), # Russian (Uzbekistan)

    # Other Django languages ------------------------------------------------

)




