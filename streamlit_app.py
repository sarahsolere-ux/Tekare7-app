import sqlite3
from datetime import date, timedelta, datetime

import streamlit as st

DB_PATH = "gesthotel.db"

HOTEL_NAME = "Hôtel Palmeria"
HOTEL_TAGLINE = "Nature • Confort • Authenticité"
HOTEL_SUBTITLE = "Un séjour authentique au cœur de Madagascar"

HOTEL_HERO_IMAGE = "https://www.fortynine.co.jp/upimg/ho24476116190.jpg"

ROOM_IMAGES = [
    "https://www.hilton.com/im/en/DPSDHLX/22546376/146979375-desahay-50-o.jpg?ch=2812&cw=5000&gravity=NorthWest&impolicy=crop&rh=675&rw=1200&xposition=0&yposition=0",
    "https://photos.hotelbeds.com/giata/bigger/09/094335/094335a_hb_ro_001.jpg",
    "data:image/jpeg;base64,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",
]

BAR_IMAGES = {
    "Coca-Cola 50 cl": "https://ocdn.eu/pulscms-transforms/1/R3mk9kpTURBXy9hNDhiMDExYzQwZDU4NDgwZTRjNGJlNzMwZmFhNjYxMC5qcGeRkwLNAcIA3gABoTAB",
    "Limonade 50 cl": "https://amfood.ch/1127-large_default/lemonsoda-24200ml-6-er-pack.jpg",
    "Eau minérale 1 L": "data:image/jpeg;base64,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",
    "Bière 65 cl": "https://www.saveursupreme.com/572-large_default/pivo-thb-z-madagaskaru-54.jpg",
    "Jus naturel mangue": "data:image/jpeg;base64,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",
    "Jus naturel ananas": "data:image/jpeg;base64,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",
}

st.set_page_config(
    page_title="Hôtel Palmeria",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at 5% 5%, rgba(76, 116, 86, .15), transparent 28%),
                radial-gradient(circle at 95% 8%, rgba(205, 163, 103, .15), transparent 26%),
                radial-gradient(circle at 80% 92%, rgba(22, 119, 117, .12), transparent 28%);
        }

        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 3rem;
            max-width: 1500px;
        }

        .hero {
            position: relative;
            min-height: 265px;
            padding: 26px 30px;
            border-radius: 24px;
            margin: 4px 0 18px 0;
            color: white;
            overflow: hidden;
            background:
                linear-gradient(90deg, rgba(20,44,34,.88) 0%, rgba(20,44,34,.55) 46%, rgba(20,44,34,.16) 100%),
                url("https://www.fortynine.co.jp/upimg/ho24476116190.jpg") center 58% / cover no-repeat;
            box-shadow: 0 18px 46px rgba(51, 65, 47, .22);
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
        }

        .wood-logo {
            display: inline-block;
            width: fit-content;
            max-width: 520px;
            padding: 14px 20px;
            border-radius: 10px;
            color: #1f2d24;
            background:
                linear-gradient(rgba(224,190,140,.93), rgba(192,151,102,.93));
            border: 1px solid rgba(83,58,32,.35);
            box-shadow: 0 8px 22px rgba(0,0,0,.22);
            text-shadow: 0 1px 0 rgba(255,255,255,.35);
        }

        .wood-logo .brand {
            font-family: Georgia, "Times New Roman", serif;
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: .06em;
            line-height: 1;
        }

        .wood-logo .tagline {
            margin-top: 7px;
            font-size: .9rem;
            letter-spacing: .12em;
            text-transform: uppercase;
        }

        .hero-subtitle {
            margin-top: 14px;
            font-size: 1.02rem;
            font-weight: 600;
            text-shadow: 0 2px 8px rgba(0,0,0,.55);
        }

        [data-testid="stMetric"] {
            border: 1px solid rgba(255,255,255,.16);
            border-radius: 18px;
            padding: 15px 16px;
            background: linear-gradient(135deg, rgba(124,58,237,.20), rgba(0,180,216,.12));
            box-shadow: 0 8px 22px rgba(0,0,0,.08);
        }

        [data-testid="stMetricLabel"] {font-weight: 700;}
        [data-testid="stMetricValue"] {font-weight: 800;}

        div[data-testid="stForm"] {
            border: 1px solid rgba(255, 77, 109, .35);
            border-radius: 20px;
            padding: 20px;
            background: linear-gradient(145deg, rgba(255,77,109,.08), rgba(124,58,237,.08));
        }

        div[data-baseweb="tab-list"] {
            gap: 8px;
            flex-wrap: wrap;
        }

        div[data-baseweb="tab-list"] button {
            border-radius: 999px;
            padding-left: 14px;
            padding-right: 14px;
            border: 1px solid rgba(255,255,255,.12);
            font-weight: 700;
        }

        div[data-baseweb="tab-list"] button:nth-child(1) {background: rgba(124,58,237,.18);}
        div[data-baseweb="tab-list"] button:nth-child(2) {background: rgba(0,180,216,.18);}
        div[data-baseweb="tab-list"] button:nth-child(3) {background: rgba(255,183,3,.18);}
        div[data-baseweb="tab-list"] button:nth-child(4) {background: rgba(16,185,129,.18);}
        div[data-baseweb="tab-list"] button:nth-child(5) {background: rgba(236,72,153,.18);}
        div[data-baseweb="tab-list"] button:nth-child(6) {background: rgba(59,130,246,.18);}
        div[data-baseweb="tab-list"] button:nth-child(7) {background: rgba(249,115,22,.18);}
        div[data-baseweb="tab-list"] button:nth-child(8) {background: rgba(6,182,212,.20);}
        div[data-baseweb="tab-list"] button:nth-child(9) {background: rgba(14,165,233,.20);}

        .invoice-card {
            border-radius: 24px;
            padding: 22px;
            margin: 8px 0 18px 0;
            background: linear-gradient(145deg, rgba(14,165,233,.14), rgba(124,58,237,.12), rgba(16,185,129,.10));
            border: 1px solid rgba(14,165,233,.28);
            box-shadow: 0 14px 34px rgba(14,165,233,.12);
        }

        .invoice-card .invoice-title {
            font-size: 1.35rem;
            font-weight: 900;
            margin-bottom: 6px;
        }

        .invoice-card .invoice-meta {
            opacity: .82;
            line-height: 1.7;
        }

        .room-photo-card {
            border-radius: 20px;
            overflow: hidden;
            margin-bottom: 12px;
            border: 1px solid rgba(40,90,70,.14);
            background: rgba(255,255,255,.72);
            box-shadow: 0 10px 28px rgba(36, 70, 55, .10);
        }

        .room-photo-card img {
            width: 100%;
            height: 180px;
            object-fit: cover;
            display: block;
        }

        .room-photo-card .body {
            padding: 12px 14px 14px 14px;
        }

        .room-photo-card .title {
            font-weight: 850;
            font-size: 1.02rem;
        }

        .product-card {
            min-height: 238px;
            border-radius: 22px;
            padding: 18px;
            margin-bottom: 12px;
            color: white;
            background: linear-gradient(145deg, #ff6b6b 0%, #f59e0b 45%, #7c3aed 100%);
            box-shadow: 0 12px 28px rgba(124,58,237,.18);
        }

        .product-card img {
            width: 100%;
            height: 125px;
            object-fit: cover;
            border-radius: 14px;
            margin-bottom: 10px;
            background: white;
        }

        .product-card .emoji {font-size: 1.6rem;}
        .product-card .name {font-size: 1.05rem; font-weight: 850; margin-top: 5px;}
        .product-card .price {font-size: 1rem; font-weight: 800; margin-top: 7px;}
        .product-card .stock {font-size: .84rem; opacity: .92; margin-top: 4px;}

        .bar-banner {
            min-height: 150px;
            padding: 22px 24px;
            border-radius: 20px;
            margin: 4px 0 16px 0;
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            background:
                linear-gradient(90deg, rgba(23,55,40,.86), rgba(23,55,40,.40)),
                url("https://www.fortynine.co.jp/upimg/ho24476116190.jpg") center 55% / cover no-repeat;
            box-shadow: 0 12px 30px rgba(49,92,70,.22);
            text-shadow: 0 2px 8px rgba(0,0,0,.45);
        }

        .invoice-preview {
            border-radius: 20px;
            padding: 22px;
            margin: 12px 0 18px 0;
            background: #fffdf8;
            border: 1px solid rgba(115,86,52,.18);
            box-shadow: 0 12px 28px rgba(80,60,35,.08);
        }

        .invoice-preview .invoice-brand {
            font-family: Georgia, "Times New Roman", serif;
            font-size: 1.4rem;
            font-weight: 900;
            color: #315c46;
            letter-spacing: .06em;
        }

        .invoice-preview table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 14px;
            font-size: .92rem;
        }

        .invoice-preview th,
        .invoice-preview td {
            padding: 9px 8px;
            border-bottom: 1px solid rgba(80,60,35,.10);
            text-align: left;
        }

        .invoice-preview .total-row {
            font-weight: 900;
            font-size: 1.02rem;
        }

        div.stButton > button,
        div[data-testid="stFormSubmitButton"] > button {
            border: none;
            border-radius: 12px;
            font-weight: 800;
            background: linear-gradient(90deg, #ff4d6d, #7c3aed);
            color: white;
            box-shadow: 0 8px 20px rgba(124,58,237,.22);
        }

        div.stButton > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {
            filter: brightness(1.08);
            color: white;
        }

        h2, h3 {
            background: linear-gradient(90deg, #315c46, #167775, #b78245);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 850 !important;
        }

        [data-testid="stDataFrame"] {
            border: 1px solid rgba(0,180,216,.25);
            border-radius: 16px;
            overflow: hidden;
        }

        .legend {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin: 6px 0 14px 0;
        }

        .legend span {
            padding: 6px 11px;
            border-radius: 999px;
            font-weight: 700;
            font-size: .88rem;
        }

        .green {background: rgba(16,185,129,.18);}
        .orange {background: rgba(245,158,11,.20);}
        .purple {background: rgba(124,58,237,.20);}
        .blue {background: rgba(59,130,246,.18);}
        .red {background: rgba(239,68,68,.18);}

        /* Palmeria Mobile Manager */
        .mobile-shell {
            max-width: 620px;
            margin: 0 auto;
            padding-bottom: 92px;
        }

        .mobile-topbar {
            padding: 18px 18px 16px;
            border-radius: 22px;
            margin-bottom: 14px;
            color: white;
            background:
                linear-gradient(135deg, rgba(34,83,57,.96), rgba(22,119,117,.90)),
                url("https://www.fortynine.co.jp/upimg/ho24476116190.jpg") center / cover no-repeat;
            box-shadow: 0 14px 32px rgba(36,73,55,.22);
        }

        .mobile-topbar .brand {
            font-family: Georgia, "Times New Roman", serif;
            font-size: 1.55rem;
            font-weight: 900;
            letter-spacing: .04em;
        }

        .mobile-topbar .date {
            margin-top: 6px;
            opacity: .92;
            font-size: .92rem;
        }

        .mobile-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px;
            margin: 10px 0 14px;
        }

        .mobile-stat {
            padding: 14px;
            border-radius: 18px;
            border: 1px solid rgba(49,92,70,.12);
            background: rgba(255,255,255,.82);
            box-shadow: 0 8px 22px rgba(40,60,45,.07);
        }

        .mobile-stat .label {
            font-size: .78rem;
            color: #617066;
            font-weight: 700;
        }

        .mobile-stat .value {
            margin-top: 3px;
            font-size: 1.18rem;
            color: #234b38;
            font-weight: 900;
        }

        .mobile-section-title {
            margin: 18px 0 8px;
            font-size: 1.03rem;
            font-weight: 900;
            color: #315c46;
        }

        .mobile-row-card {
            padding: 12px 14px;
            margin: 8px 0;
            border-radius: 16px;
            background: rgba(255,255,255,.88);
            border: 1px solid rgba(22,119,117,.13);
            box-shadow: 0 6px 18px rgba(40,60,45,.06);
        }

        .mobile-row-card .title {
            font-weight: 900;
            color: #25372d;
        }

        .mobile-row-card .meta {
            margin-top: 3px;
            font-size: .87rem;
            color: #69766e;
        }

        .mobile-room {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: center;
        }

        .mobile-room .room-name {
            font-weight: 900;
            color: #25372d;
        }

        .mobile-room .guest {
            font-size: .84rem;
            color: #6b756f;
            margin-top: 3px;
        }

        .mobile-badge {
            white-space: nowrap;
            padding: 6px 9px;
            border-radius: 999px;
            font-size: .76rem;
            font-weight: 800;
            background: rgba(49,92,70,.10);
        }

        @media (max-width: 700px) {
            .block-container {
                padding: .75rem .75rem 5rem .75rem;
            }

            .hero {
                min-height: 190px;
                padding: 18px;
            }

            .wood-logo .brand {
                font-size: 1.35rem;
            }

            .mobile-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            [data-testid="stHorizontalBlock"] {
                gap: .55rem;
            }

            div[data-testid="stDataFrame"] {
                font-size: .82rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def db():
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    with db() as con:
        con.executescript(
            """
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                nightly_rate INTEGER NOT NULL DEFAULT 0,
                maintenance INTEGER NOT NULL DEFAULT 0,
                room_type TEXT NOT NULL DEFAULT 'Double',
                capacity_adults INTEGER NOT NULL DEFAULT 2,
                capacity_children INTEGER NOT NULL DEFAULT 0,
                bed_type TEXT NOT NULL DEFAULT 'Lit double',
                floor TEXT NOT NULL DEFAULT 'RDC',
                view_type TEXT NOT NULL DEFAULT 'Jardin',
                amenities TEXT NOT NULL DEFAULT 'Wi-Fi|Douche|TV',
                housekeeping_status TEXT NOT NULL DEFAULT 'Prête',
                notes TEXT NOT NULL DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL,
                client TEXT NOT NULL,
                phone TEXT DEFAULT '',
                arrival TEXT NOT NULL,
                departure TEXT NOT NULL,
                nightly_rate INTEGER NOT NULL,
                total INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'Confirmée',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(room_id) REFERENCES rooms(id)
            );

            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reservation_id INTEGER NOT NULL,
                payment_date TEXT NOT NULL,
                amount INTEGER NOT NULL,
                method TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(reservation_id) REFERENCES reservations(id)
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT DEFAULT '',
                amount INTEGER NOT NULL,
                payment_method TEXT NOT NULL DEFAULT 'Espèces',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS bar_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                emoji TEXT NOT NULL DEFAULT '🥤',
                price INTEGER NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                active INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS bar_sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket TEXT NOT NULL,
                sale_date TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price INTEGER NOT NULL,
                total INTEGER NOT NULL,
                payment_method TEXT NOT NULL,
                room_id INTEGER,
                client TEXT DEFAULT '',
                paid INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(product_id) REFERENCES bar_products(id),
                FOREIGN KEY(room_id) REFERENCES rooms(id)
            );

            CREATE TABLE IF NOT EXISTS guest_extras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reservation_id INTEGER NOT NULL,
                service_date TEXT NOT NULL,
                label TEXT NOT NULL,
                description TEXT DEFAULT '',
                amount INTEGER NOT NULL,
                paid INTEGER NOT NULL DEFAULT 0,
                payment_method TEXT DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(reservation_id) REFERENCES reservations(id)
            );
            """
        )

        room_columns = {
            item[1] for item in con.execute("PRAGMA table_info(rooms)").fetchall()
        }
        room_migrations = {
            "room_type": "TEXT NOT NULL DEFAULT 'Double'",
            "capacity_adults": "INTEGER NOT NULL DEFAULT 2",
            "capacity_children": "INTEGER NOT NULL DEFAULT 0",
            "bed_type": "TEXT NOT NULL DEFAULT 'Lit double'",
            "floor": "TEXT NOT NULL DEFAULT 'RDC'",
            "view_type": "TEXT NOT NULL DEFAULT 'Jardin'",
            "amenities": "TEXT NOT NULL DEFAULT 'Wi-Fi|Douche|TV'",
            "housekeeping_status": "TEXT NOT NULL DEFAULT 'Prête'",
            "notes": "TEXT NOT NULL DEFAULT ''",
        }
        for column_name, column_definition in room_migrations.items():
            if column_name not in room_columns:
                con.execute(
                    f"ALTER TABLE rooms ADD COLUMN {column_name} {column_definition}"
                )

        reservation_columns = {
            item[1] for item in con.execute("PRAGMA table_info(reservations)").fetchall()
        }
        if "checked_in" not in reservation_columns:
            con.execute(
                "ALTER TABLE reservations ADD COLUMN checked_in INTEGER NOT NULL DEFAULT 0"
            )
        if "checked_out" not in reservation_columns:
            con.execute(
                "ALTER TABLE reservations ADD COLUMN checked_out INTEGER NOT NULL DEFAULT 0"
            )
        if "checkin_at" not in reservation_columns:
            con.execute(
                "ALTER TABLE reservations ADD COLUMN checkin_at TEXT DEFAULT ''"
            )
        if "checkout_at" not in reservation_columns:
            con.execute(
                "ALTER TABLE reservations ADD COLUMN checkout_at TEXT DEFAULT ''"
            )
        if "invoice_closed" not in reservation_columns:
            con.execute(
                "ALTER TABLE reservations ADD COLUMN invoice_closed INTEGER NOT NULL DEFAULT 0"
            )
        if "invoice_number" not in reservation_columns:
            con.execute(
                "ALTER TABLE reservations ADD COLUMN invoice_number TEXT DEFAULT ''"
            )
        if "invoice_closed_at" not in reservation_columns:
            con.execute(
                "ALTER TABLE reservations ADD COLUMN invoice_closed_at TEXT DEFAULT ''"
            )

        bar_columns = {
            item[1] for item in con.execute("PRAGMA table_info(bar_sales)").fetchall()
        }
        if "reservation_id" not in bar_columns:
            con.execute(
                "ALTER TABLE bar_sales ADD COLUMN reservation_id INTEGER"
            )

        if con.execute("SELECT COUNT(*) FROM rooms").fetchone()[0] == 0:
            con.executemany(
                "INSERT INTO rooms(name, nightly_rate) VALUES (?, ?)",
                [
                    ("Chambre 101", 150000),
                    ("Chambre 102", 120000),
                    ("Chambre 103", 180000),
                ],
            )

        # Fiches chambres de démonstration, sans écraser les réglages déjà personnalisés.
        room_demo_profiles = [
            (
                "Chambre 101", "Double Deluxe", 2, 0, "Queen Size",
                "RDC", "Jardin tropical",
                "Wi-Fi|Climatisation|TV|Douche|Minibar|Coffre-fort|Terrasse"
            ),
            (
                "Chambre 102", "Double Confort", 2, 1, "Lit double",
                "1er étage", "Cour tropicale",
                "Wi-Fi|Ventilateur|TV|Douche|Bureau"
            ),
            (
                "Chambre 103", "Suite Familiale", 3, 1, "King + canapé-lit",
                "1er étage", "Jardin",
                "Wi-Fi|Climatisation|TV|Douche|Minibar|Coffre-fort|Balcon|Bouilloire"
            ),
        ]
        for (
            room_name, room_type, adults, children, bed_type, floor,
            view_type, amenities
        ) in room_demo_profiles:
            con.execute(
                """
                UPDATE rooms
                SET room_type = CASE WHEN room_type = 'Double' THEN ? ELSE room_type END,
                    capacity_adults = CASE WHEN capacity_adults = 2 THEN ? ELSE capacity_adults END,
                    capacity_children = CASE WHEN capacity_children = 0 THEN ? ELSE capacity_children END,
                    bed_type = CASE WHEN bed_type = 'Lit double' THEN ? ELSE bed_type END,
                    floor = CASE WHEN floor = 'RDC' THEN ? ELSE floor END,
                    view_type = CASE WHEN view_type = 'Jardin' THEN ? ELSE view_type END,
                    amenities = CASE WHEN amenities = 'Wi-Fi|Douche|TV' THEN ? ELSE amenities END
                WHERE name = ?
                """,
                (
                    room_type, adults, children, bed_type, floor,
                    view_type, amenities, room_name
                ),
            )

        # Carte complète d'un bar d'hôtel. INSERT OR IGNORE permet d'ajouter
        # les nouveaux produits aux bases déjà existantes sans écraser les prix
        # ou stocks personnalisés par l'hôtel.
        default_bar_products = [
            # Eaux
            ("Eau minérale 33 cl", "Eaux", "💧", 2000, 24),
            ("Eau minérale 50 cl", "Eaux", "💧", 2500, 30),
            ("Eau minérale 1 L", "Eaux", "💧", 3000, 30),
            ("Eau pétillante 50 cl", "Eaux", "🫧", 5000, 16),
            ("Eau pétillante 1 L", "Eaux", "🫧", 7000, 12),

            # Sodas et boissons fraîches
            ("Coca-Cola 33 cl", "Sodas", "🥤", 5000, 24),
            ("Coca-Cola 50 cl", "Sodas", "🥤", 6000, 24),
            ("Coca-Cola Zéro 33 cl", "Sodas", "🥤", 5500, 18),
            ("Fanta Orange 33 cl", "Sodas", "🍊", 5000, 18),
            ("Sprite 33 cl", "Sodas", "🥤", 5000, 18),
            ("Limonade 50 cl", "Sodas", "🍋", 5000, 18),
            ("Tonic 25 cl", "Sodas", "🫧", 6000, 14),
            ("Ginger Ale 25 cl", "Sodas", "🫚", 6000, 12),
            ("Thé glacé pêche 33 cl", "Sodas", "🍑", 6000, 14),

            # Jus naturels
            ("Jus naturel mangue", "Jus naturels", "🥭", 7000, 12),
            ("Jus naturel ananas", "Jus naturels", "🍍", 7000, 12),
            ("Jus naturel orange", "Jus naturels", "🍊", 7000, 12),
            ("Jus naturel citron", "Jus naturels", "🍋", 7000, 12),
            ("Jus naturel passion", "Jus naturels", "🌿", 8000, 10),
            ("Jus naturel goyave", "Jus naturels", "🍹", 8000, 10),
            ("Jus naturel papaye", "Jus naturels", "🍹", 7000, 10),
            ("Jus naturel pastèque", "Jus naturels", "🍉", 7000, 10),

            # Jus en bouteille
            ("Jus orange bouteille 25 cl", "Jus bouteille", "🧃", 5000, 18),
            ("Jus pomme bouteille 25 cl", "Jus bouteille", "🧃", 5000, 16),
            ("Jus ananas bouteille 25 cl", "Jus bouteille", "🧃", 5000, 16),
            ("Jus multifruits 25 cl", "Jus bouteille", "🧃", 5500, 16),
            ("Jus tomate 25 cl", "Jus bouteille", "🍅", 5500, 10),

            # Boissons chaudes
            ("Espresso", "Boissons chaudes", "☕", 4000, 40),
            ("Double espresso", "Boissons chaudes", "☕", 6000, 30),
            ("Café allongé", "Boissons chaudes", "☕", 4500, 30),
            ("Café au lait", "Boissons chaudes", "🥛", 6000, 25),
            ("Cappuccino", "Boissons chaudes", "☕", 7000, 25),
            ("Thé noir", "Boissons chaudes", "🫖", 4000, 30),
            ("Thé vert", "Boissons chaudes", "🍵", 4500, 25),
            ("Infusion", "Boissons chaudes", "🌿", 4500, 20),
            ("Chocolat chaud", "Boissons chaudes", "🍫", 6500, 20),

            # Bières et cidres
            ("Bière 65 cl", "Bières", "🍺", 8000, 20),
            ("Bière blonde 33 cl", "Bières", "🍺", 6000, 24),
            ("Bière locale 33 cl", "Bières", "🍺", 5500, 24),
            ("Bière sans alcool 33 cl", "Bières", "🍺", 6500, 12),
            ("Bière brune 33 cl", "Bières", "🍺", 7000, 12),
            ("Panaché 33 cl", "Bières", "🍺", 5500, 14),
            ("Cidre 33 cl", "Bières", "🍎", 8000, 10),

            # Vins
            ("Verre de vin rouge", "Vins", "🍷", 12000, 20),
            ("Verre de vin blanc", "Vins", "🥂", 12000, 20),
            ("Verre de vin rosé", "Vins", "🍷", 12000, 20),
            ("Bouteille vin rouge", "Vins", "🍷", 55000, 8),
            ("Bouteille vin blanc", "Vins", "🥂", 55000, 8),
            ("Bouteille vin rosé", "Vins", "🍷", 55000, 8),
            ("Coupe de vin pétillant", "Vins", "🥂", 15000, 16),
            ("Bouteille vin pétillant", "Vins", "🍾", 75000, 6),

            # Spiritueux
            ("Rhum local 4 cl", "Spiritueux", "🥃", 10000, 18),
            ("Rhum arrangé 4 cl", "Spiritueux", "🥃", 12000, 16),
            ("Whisky 4 cl", "Spiritueux", "🥃", 15000, 15),
            ("Gin 4 cl", "Spiritueux", "🍸", 14000, 12),
            ("Vodka 4 cl", "Spiritueux", "🍸", 14000, 12),
            ("Tequila 4 cl", "Spiritueux", "🥃", 14000, 10),
            ("Cognac 4 cl", "Spiritueux", "🥃", 18000, 8),
            ("Liqueur 4 cl", "Spiritueux", "🍸", 12000, 10),

            # Cocktails
            ("Mojito", "Cocktails", "🍸", 18000, 20),
            ("Piña Colada", "Cocktails", "🍍", 20000, 20),
            ("Planteur tropical", "Cocktails", "🍹", 18000, 20),
            ("Punch maison", "Cocktails", "🍹", 16000, 20),
            ("Gin Tonic", "Cocktails", "🍸", 18000, 20),
            ("Vodka Orange", "Cocktails", "🍊", 17000, 20),
            ("Cuba Libre", "Cocktails", "🥃", 18000, 20),
            ("Spritz", "Cocktails", "🍹", 22000, 16),
            ("Virgin Mojito", "Cocktails sans alcool", "🌿", 12000, 20),
            ("Cocktail fruits tropicaux", "Cocktails sans alcool", "🍹", 12000, 20),

            # Snacks et petite restauration
            ("Cacahuètes grillées", "Snacks", "🥜", 5000, 24),
            ("Noix de cajou", "Snacks", "🥜", 8000, 18),
            ("Chips", "Snacks", "🥔", 5000, 24),
            ("Olives", "Snacks", "🫒", 7000, 14),
            ("Sambos x4", "Snacks", "🥟", 8000, 20),
            ("Mini sandwich", "Snacks", "🥪", 12000, 15),
            ("Croque-monsieur", "Snacks", "🥪", 16000, 12),
            ("Assiette de fruits", "Snacks", "🍉", 15000, 12),
            ("Assiette de fromages", "Snacks", "🧀", 22000, 8),
        ]

        con.executemany(
            """
            INSERT OR IGNORE INTO bar_products(name, category, emoji, price, stock)
            VALUES (?, ?, ?, ?, ?)
            """,
            default_bar_products,
        )

        # Démonstration : deux vrais scénarios clients visibles dans le prototype.
        today_demo = date.today()
        demo_clients = [
            {
                "client": "Ranaivo Andry",
                "phone": "034 12 345 67",
                "room": "Chambre 101",
                "nights": 2,
                "payment": 150000,
                "method": "MVola",
            },
            {
                "client": "Vololona M.",
                "phone": "032 98 765 43",
                "room": "Chambre 102",
                "nights": 1,
                "payment": 60000,
                "method": "Espèces",
            },
        ]

        for demo in demo_clients:
            existing_demo = con.execute(
                """
                SELECT id FROM reservations
                WHERE client = ? AND phone = ?
                LIMIT 1
                """,
                (demo["client"], demo["phone"]),
            ).fetchone()

            if existing_demo:
                continue

            room = con.execute(
                "SELECT id, nightly_rate FROM rooms WHERE name = ?",
                (demo["room"],),
            ).fetchone()

            if not room:
                continue

            arrival_demo = today_demo.isoformat()
            departure_demo = (
                today_demo + timedelta(days=demo["nights"])
            ).isoformat()
            lodging_total = int(room["nightly_rate"]) * demo["nights"]

            cursor = con.execute(
                """
                INSERT INTO reservations(
                    room_id, client, phone, arrival, departure,
                    nightly_rate, total, status, checked_in, checkin_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, 'Confirmée', 1, CURRENT_TIMESTAMP)
                """,
                (
                    room["id"],
                    demo["client"],
                    demo["phone"],
                    arrival_demo,
                    departure_demo,
                    int(room["nightly_rate"]),
                    lodging_total,
                ),
            )
            reservation_id = cursor.lastrowid

            con.execute(
                """
                INSERT INTO payments(
                    reservation_id, payment_date, amount, method
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    reservation_id,
                    today_demo.isoformat(),
                    min(demo["payment"], lodging_total),
                    demo["method"],
                ),
            )

            if demo["client"] == "Ranaivo Andry":
                con.execute(
                    """
                    INSERT INTO guest_extras(
                        reservation_id, service_date, label, description, amount
                    )
                    VALUES (?, ?, 'Petit-déjeuner', 'Petit-déjeuner tropical', 20000)
                    """,
                    (reservation_id, today_demo.isoformat()),
                )

                coca = con.execute(
                    """
                    SELECT id, price, stock FROM bar_products
                    WHERE name = 'Coca-Cola 50 cl'
                    """
                ).fetchone()
                if coca and int(coca["stock"]) >= 2:
                    con.execute(
                        """
                        INSERT INTO bar_sales(
                            ticket, sale_date, product_id, quantity, unit_price,
                            total, payment_method, room_id, client, paid, reservation_id
                        )
                        VALUES (
                            'DEMO-R101', ?, ?, 2, ?, ?,
                            'Ajouter à la chambre', ?, ?, 0, ?
                        )
                        """,
                        (
                            today_demo.isoformat(),
                            coca["id"],
                            int(coca["price"]),
                            int(coca["price"]) * 2,
                            room["id"],
                            demo["client"],
                            reservation_id,
                        ),
                    )
                    con.execute(
                        "UPDATE bar_products SET stock = stock - 2 WHERE id = ?",
                        (coca["id"],),
                    )

        con.commit()


def rows(query, params=()):
    with db() as con:
        return [dict(r) for r in con.execute(query, params).fetchall()]


def one(query, params=()):
    with db() as con:
        r = con.execute(query, params).fetchone()
        return dict(r) if r else None


def run(query, params=()):
    with db() as con:
        con.execute(query, params)
        con.commit()


def format_ar(value):
    return f"{int(value or 0):,} Ar".replace(",", " ")


def room_status(room_id, maintenance):
    if maintenance:
        return "🛠️ Maintenance"

    room = one(
        "SELECT housekeeping_status FROM rooms WHERE id = ?",
        (room_id,),
    )
    housekeeping = (
        room["housekeeping_status"]
        if room and room.get("housekeeping_status")
        else "Prête"
    )
    if housekeeping == "À nettoyer":
        return "🧹 À nettoyer"
    if housekeeping == "En nettoyage":
        return "🧽 En nettoyage"
    if housekeeping == "Hors service":
        return "🚫 Hors service"

    today = date.today().isoformat()

    current = one(
        """
        SELECT 1 FROM reservations
        WHERE room_id = ?
          AND status != 'Annulée'
          AND checked_out = 0
          AND (
              (checked_in = 1)
              OR (arrival <= ? AND departure > ?)
          )
        LIMIT 1
        """,
        (room_id, today, today),
    )
    if current:
        return "🔴 Occupée"

    future = one(
        """
        SELECT 1 FROM reservations
        WHERE room_id = ?
          AND status != 'Annulée'
          AND checked_out = 0
          AND arrival > ?
        LIMIT 1
        """,
        (room_id, today),
    )
    if future:
        return "🟠 Réservée"

    return "🟢 Libre"


def current_room_stay(room_id):
    today = date.today().isoformat()
    return one(
        """
        SELECT r.id, r.client, r.arrival, r.departure, r.total,
               r.checked_in, r.phone
        FROM reservations r
        WHERE r.room_id = ?
          AND r.status != 'Annulée'
          AND r.checked_out = 0
          AND (r.checked_in = 1 OR (r.arrival <= ? AND r.departure > ?))
        ORDER BY r.checked_in DESC, r.arrival
        LIMIT 1
        """,
        (room_id, today, today),
    )


def next_room_booking(room_id):
    today = date.today().isoformat()
    return one(
        """
        SELECT id, client, arrival, departure
        FROM reservations
        WHERE room_id = ?
          AND status != 'Annulée'
          AND checked_out = 0
          AND arrival > ?
        ORDER BY arrival
        LIMIT 1
        """,
        (room_id, today),
    )


def room_view():
    data = []
    for room in rows("SELECT * FROM rooms ORDER BY name"):
        current = current_room_stay(room["id"])
        upcoming = next_room_booking(room["id"])
        capacity = f'{room["capacity_adults"]} ad.'
        if int(room["capacity_children"] or 0) > 0:
            capacity += f' + {room["capacity_children"]} enf.'
        data.append(
            {
                "Chambre": room["name"],
                "Type": room["room_type"],
                "Capacité": capacity,
                "Lit": room["bed_type"],
                "Étage": room["floor"],
                "Vue": room["view_type"],
                "Tarif / nuit": format_ar(room["nightly_rate"]),
                "Statut": room_status(room["id"], room["maintenance"]),
                "Client actuel": current["client"] if current else "-",
                "Prochaine arrivée": upcoming["arrival"] if upcoming else "-",
                "Ménage": room["housekeeping_status"],
            }
        )
    return data

def reservation_conflict(room_id, arrival, departure):
    return one(
        """
        SELECT 1 FROM reservations
        WHERE room_id = ?
          AND status != 'Annulée'
          AND checked_out = 0
          AND arrival < ?
          AND departure > ?
        LIMIT 1
        """,
        (room_id, departure.isoformat(), arrival.isoformat()),
    ) is not None


def paid_for(reservation_id):
    result = one(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM payments WHERE reservation_id = ?",
        (reservation_id,),
    )
    return int(result["total"] if result else 0)


def reservation_view():
    result = []
    data = rows(
        """
        SELECT r.*, rm.name AS room_name
        FROM reservations r
        JOIN rooms rm ON rm.id = r.room_id
        ORDER BY r.arrival DESC, r.id DESC
        """
    )
    for item in data:
        paid = paid_for(item["id"])
        remaining = max(int(item["total"]) - paid, 0)

        if item["status"] == "Annulée":
            payment_status = "⚪ Annulée"
        elif paid == 0:
            payment_status = "🔴 Non payé"
        elif remaining > 0:
            payment_status = "🟠 Partiel"
        else:
            payment_status = "🟢 Payé"

        nights = (
            date.fromisoformat(item["departure"])
            - date.fromisoformat(item["arrival"])
        ).days

        if item.get("checked_out"):
            stay_status = "🔵 Check-out fait"
        elif item.get("checked_in"):
            stay_status = "🟣 En séjour"
        elif date.fromisoformat(item["arrival"]) > date.today():
            stay_status = "🟠 À venir"
        elif date.fromisoformat(item["departure"]) <= date.today():
            stay_status = "🔴 À clôturer"
        else:
            stay_status = "🟡 Arrivée attendue"

        result.append(
            {
                "ID": f'R{item["id"]:03d}',
                "Séjour": stay_status,
                "Chambre": item["room_name"],
                "Client": item["client"],
                "Téléphone": item["phone"] or "-",
                "Arrivée": item["arrival"],
                "Départ": item["departure"],
                "Nuits": nights,
                "Total": format_ar(item["total"]),
                "Payé": format_ar(paid),
                "Reste": format_ar(remaining),
                "Paiement": payment_status,
                "Statut": item["status"],
            }
        )
    return result


def payable_reservations():
    result = []
    for item in rows(
        """
        SELECT r.*, rm.name AS room_name
        FROM reservations r
        JOIN rooms rm ON rm.id = r.room_id
        WHERE r.status != 'Annulée'
        ORDER BY r.id DESC
        """
    ):
        paid = paid_for(item["id"])
        remaining = max(int(item["total"]) - paid, 0)
        if remaining > 0:
            item["remaining"] = remaining
            result.append(item)
    return result


def revenue_totals():
    payments = rows("SELECT payment_date, amount FROM payments")
    today = date.today()
    start_week = today - timedelta(days=today.weekday())
    start_month = today.replace(day=1)

    day_total = 0
    week_total = 0
    month_total = 0
    all_total = 0

    for payment in payments:
        pdate = date.fromisoformat(payment["payment_date"])
        amount = int(payment["amount"])
        all_total += amount
        if pdate == today:
            day_total += amount
        if pdate >= start_week:
            week_total += amount
        if pdate >= start_month:
            month_total += amount

    return day_total, week_total, month_total, all_total


def expense_totals():
    expenses = rows("SELECT expense_date, amount FROM expenses")
    today = date.today()
    start_week = today - timedelta(days=today.weekday())
    start_month = today.replace(day=1)

    day_total = 0
    week_total = 0
    month_total = 0
    all_total = 0

    for expense in expenses:
        edate = date.fromisoformat(expense["expense_date"])
        amount = int(expense["amount"])
        all_total += amount
        if edate == today:
            day_total += amount
        if edate >= start_week:
            week_total += amount
        if edate >= start_month:
            month_total += amount

    return day_total, week_total, month_total, all_total


def outstanding_total():
    total = 0
    for item in rows("SELECT id, total, status FROM reservations"):
        if item["status"] == "Annulée":
            continue
        total += max(int(item["total"]) - paid_for(item["id"]), 0)

    pending_bar = one(
        "SELECT COALESCE(SUM(total), 0) AS total FROM bar_sales WHERE paid = 0"
    )
    pending_extras = one(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM guest_extras WHERE paid = 0"
    )

    total += int(pending_bar["total"] if pending_bar else 0)
    total += int(pending_extras["total"] if pending_extras else 0)
    return total


def today_movements():
    today = date.today().isoformat()

    arrivals = rows(
        """
        SELECT r.id, r.client, r.phone, rm.name AS room_name
        FROM reservations r
        JOIN rooms rm ON rm.id = r.room_id
        WHERE r.arrival = ? AND r.status != 'Annulée' AND r.checked_in = 0
        ORDER BY rm.name
        """,
        (today,),
    )

    departures = rows(
        """
        SELECT r.id, r.client, r.phone, rm.name AS room_name
        FROM reservations r
        JOIN rooms rm ON rm.id = r.room_id
        WHERE r.departure = ? AND r.status != 'Annulée' AND r.checked_out = 0
        ORDER BY rm.name
        """,
        (today,),
    )

    return arrivals, departures


def planning_view(start_date, days):
    room_list = rows("SELECT * FROM rooms ORDER BY name")
    reservations = rows(
        """
        SELECT id, room_id, client, arrival, departure, status, checked_in, checked_out
        FROM reservations
        WHERE status != 'Annulée'
        ORDER BY arrival
        """
    )

    result = []
    for room in room_list:
        line = {"Chambre": room["name"]}
        for offset in range(days):
            current_day = start_date + timedelta(days=offset)
            label = current_day.strftime("%d/%m")
            cell = "🟢 Libre"

            if room["maintenance"]:
                cell = "🛠️ Maintenance"
            else:
                for reservation in reservations:
                    if reservation["room_id"] != room["id"]:
                        continue
                    if reservation["checked_out"]:
                        continue

                    arrival = date.fromisoformat(reservation["arrival"])
                    departure = date.fromisoformat(reservation["departure"])

                    if arrival <= current_day < departure:
                        if reservation["checked_in"]:
                            cell = f'🟣 {reservation["client"]}'
                        else:
                            cell = f'🟠 {reservation["client"]}'
                        break

            line[label] = cell
        result.append(line)

    return result


def client_summary():
    data = rows(
        """
        SELECT r.*, rm.name AS room_name
        FROM reservations r
        JOIN rooms rm ON rm.id = r.room_id
        WHERE r.status != 'Annulée'
        ORDER BY r.departure DESC
        """
    )

    clients = {}
    for item in data:
        key = (item["client"].strip(), (item["phone"] or "").strip())
        paid = paid_for(item["id"])

        if key not in clients:
            clients[key] = {
                "Client": key[0],
                "Téléphone": key[1] or "-",
                "Séjours": 0,
                "Total réservé": 0,
                "Total payé": 0,
                "Reste": 0,
                "Dernier départ": item["departure"],
            }

        clients[key]["Séjours"] += 1
        clients[key]["Total réservé"] += int(item["total"])
        clients[key]["Total payé"] += paid
        clients[key]["Reste"] += max(int(item["total"]) - paid, 0)

        if item["departure"] > clients[key]["Dernier départ"]:
            clients[key]["Dernier départ"] = item["departure"]

    result = []
    for client in clients.values():
        result.append(
            {
                "Client": client["Client"],
                "Téléphone": client["Téléphone"],
                "Séjours": client["Séjours"],
                "Total réservé": format_ar(client["Total réservé"]),
                "Total payé": format_ar(client["Total payé"]),
                "Reste": format_ar(client["Reste"]),
                "Dernier départ": client["Dernier départ"],
            }
        )

    return sorted(result, key=lambda item: item["Dernier départ"], reverse=True)


def bar_totals():
    sales = rows(
        "SELECT sale_date, total, paid FROM bar_sales"
    )
    today = date.today()
    start_month = today.replace(day=1)

    today_total = 0
    month_total = 0
    all_total = 0
    pending_total = 0

    for sale in sales:
        amount = int(sale["total"])
        sale_day = date.fromisoformat(sale["sale_date"])
        if sale["paid"]:
            all_total += amount
            if sale_day == today:
                today_total += amount
            if sale_day >= start_month:
                month_total += amount
        else:
            pending_total += amount

    return today_total, month_total, all_total, pending_total


def active_guest_for_room(room_id):
    today = date.today().isoformat()
    guest = one(
        """
        SELECT client
        FROM reservations
        WHERE room_id = ?
          AND status != 'Annulée'
          AND checked_out = 0
          AND (
              checked_in = 1
              OR (arrival <= ? AND departure > ?)
          )
        ORDER BY checked_in DESC, arrival
        LIMIT 1
        """,
        (room_id, today, today),
    )
    return guest["client"] if guest else ""


def active_reservation_for_room(room_id):
    today = date.today().isoformat()
    reservation = one(
        """
        SELECT id, client
        FROM reservations
        WHERE room_id = ?
          AND status != 'Annulée'
          AND checked_out = 0
          AND (
              checked_in = 1
              OR (arrival <= ? AND departure >= ?)
          )
        ORDER BY checked_in DESC, arrival
        LIMIT 1
        """,
        (room_id, today, today),
    )
    return reservation


def reservation_invoice(reservation_id):
    reservation = one(
        """
        SELECT r.*, rm.name AS room_name
        FROM reservations r
        JOIN rooms rm ON rm.id = r.room_id
        WHERE r.id = ?
        """,
        (reservation_id,),
    )

    if not reservation:
        return None

    lodging_total = int(reservation["total"])
    lodging_paid = paid_for(reservation_id)

    bar_items = rows(
        """
        SELECT
            bs.id,
            bs.ticket,
            bs.sale_date,
            bp.name AS product_name,
            bs.quantity,
            bs.unit_price,
            bs.total,
            bs.paid,
            bs.payment_method
        FROM bar_sales bs
        JOIN bar_products bp ON bp.id = bs.product_id
        WHERE
            bs.reservation_id = ?
            OR (
                bs.reservation_id IS NULL
                AND bs.room_id = ?
                AND bs.sale_date >= ?
                AND bs.sale_date <= ?
            )
        ORDER BY bs.sale_date, bs.id
        """,
        (
            reservation_id,
            reservation["room_id"],
            reservation["arrival"],
            reservation["departure"],
        ),
    )

    extras = rows(
        """
        SELECT id, service_date, label, description, amount, paid, payment_method
        FROM guest_extras
        WHERE reservation_id = ?
        ORDER BY service_date, id
        """,
        (reservation_id,),
    )

    bar_total = sum(int(item["total"]) for item in bar_items)
    bar_paid = sum(int(item["total"]) for item in bar_items if item["paid"])
    extras_total = sum(int(item["amount"]) for item in extras)
    extras_paid = sum(int(item["amount"]) for item in extras if item["paid"])

    grand_total = lodging_total + bar_total + extras_total
    paid_total = lodging_paid + bar_paid + extras_paid
    remaining = max(grand_total - paid_total, 0)

    return {
        "reservation": reservation,
        "lodging_total": lodging_total,
        "lodging_paid": lodging_paid,
        "bar_items": bar_items,
        "bar_total": bar_total,
        "bar_paid": bar_paid,
        "extras": extras,
        "extras_total": extras_total,
        "extras_paid": extras_paid,
        "grand_total": grand_total,
        "paid_total": paid_total,
        "remaining": remaining,
    }


def close_reservation_invoice(reservation_id, payment_method):
    invoice = reservation_invoice(reservation_id)
    if not invoice:
        raise ValueError("Séjour introuvable.")

    reservation = invoice["reservation"]
    invoice_number = (
        reservation["invoice_number"]
        or f'FAC-{date.today().year}-{reservation_id:04d}'
    )

    lodging_due = max(
        invoice["lodging_total"] - invoice["lodging_paid"],
        0,
    )

    with db() as con:
        if lodging_due > 0:
            con.execute(
                """
                INSERT INTO payments(
                    reservation_id, payment_date, amount, method
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    reservation_id,
                    date.today().isoformat(),
                    lodging_due,
                    payment_method,
                ),
            )

        con.execute(
            """
            UPDATE bar_sales
            SET paid = 1, payment_method = ?
            WHERE paid = 0
              AND (
                  reservation_id = ?
                  OR (
                      reservation_id IS NULL
                      AND room_id = ?
                      AND sale_date >= ?
                      AND sale_date <= ?
                  )
              )
            """,
            (
                payment_method,
                reservation_id,
                reservation["room_id"],
                reservation["arrival"],
                reservation["departure"],
            ),
        )

        con.execute(
            """
            UPDATE guest_extras
            SET paid = 1, payment_method = ?
            WHERE reservation_id = ? AND paid = 0
            """,
            (payment_method, reservation_id),
        )

        con.execute(
            """
            UPDATE reservations
            SET
                checked_out = 1,
                checkout_at = CASE
                    WHEN checkout_at = '' OR checkout_at IS NULL
                    THEN CURRENT_TIMESTAMP
                    ELSE checkout_at
                END,
                invoice_closed = 1,
                invoice_number = ?,
                invoice_closed_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (invoice_number, reservation_id),
        )

        con.execute(
            """
            UPDATE rooms
            SET housekeeping_status = 'À nettoyer'
            WHERE id = ?
            """,
            (reservation["room_id"],),
        )

        con.commit()

    return invoice_number


def save_bar_ticket(cart, payment_method, room_id=None, client=""):
    ticket = f'BAR-{datetime.now().strftime("%Y%m%d-%H%M%S-%f")}'
    paid = 0 if payment_method == "Ajouter à la chambre" else 1
    linked_reservation = active_reservation_for_room(room_id) if room_id else None
    reservation_id = linked_reservation["id"] if linked_reservation else None

    with db() as con:
        for line in cart:
            product = con.execute(
                "SELECT id, name, price, stock FROM bar_products WHERE id = ?",
                (line["product_id"],),
            ).fetchone()

            if not product:
                raise ValueError("Un produit du panier n’existe plus.")

            if int(product["stock"]) < int(line["quantity"]):
                raise ValueError(
                    f'Stock insuffisant pour {product["name"]}.'
                )

            quantity = int(line["quantity"])
            unit_price = int(product["price"])
            total = quantity * unit_price

            con.execute(
                """
                INSERT INTO bar_sales(
                    ticket, sale_date, product_id, quantity, unit_price, total,
                    payment_method, room_id, client, paid, reservation_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ticket,
                    date.today().isoformat(),
                    product["id"],
                    quantity,
                    unit_price,
                    total,
                    payment_method,
                    room_id,
                    client.strip(),
                    paid,
                    reservation_id,
                ),
            )

            con.execute(
                "UPDATE bar_products SET stock = stock - ? WHERE id = ?",
                (quantity, product["id"]),
            )

        con.commit()

    return ticket


def render_mobile_manager():
    today = date.today()
    room_data = rows("SELECT * FROM rooms ORDER BY name")
    statuses = [
        room_status(room["id"], room["maintenance"])
        for room in room_data
    ]

    occupied_count = statuses.count("🔴 Occupée")
    free_count = statuses.count("🟢 Libre")
    reserved_count = statuses.count("🟠 Réservée")
    day_total, _, month_total, _ = revenue_totals()
    expense_day, _, expense_month, _ = expense_totals()
    outstanding = outstanding_total()
    arrivals, departures = today_movements()

    st.markdown('<div class="mobile-shell">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="mobile-topbar">
            <div class="brand">🌴 PALMERIA MANAGER</div>
            <div class="date">{today.strftime("%d/%m/%Y")} · Vue gérant</div>
        </div>
        <div class="mobile-grid">
            <div class="mobile-stat">
                <div class="label">🏨 Occupées</div>
                <div class="value">{occupied_count}/{len(room_data)}</div>
            </div>
            <div class="mobile-stat">
                <div class="label">🟢 Libres</div>
                <div class="value">{free_count}</div>
            </div>
            <div class="mobile-stat">
                <div class="label">💰 Aujourd’hui</div>
                <div class="value">{format_ar(day_total)}</div>
            </div>
            <div class="mobile-stat">
                <div class="label">⏳ À encaisser</div>
                <div class="value">{format_ar(outstanding)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="mobile-section-title">⚡ Actions rapides</div>', unsafe_allow_html=True)
    quick_reservation, quick_payment = st.tabs(["➕ Réservation", "💳 Paiement"])

    with quick_reservation:
        available_rooms = rows(
            """
            SELECT id, name, nightly_rate
            FROM rooms
            WHERE maintenance = 0
            ORDER BY name
            """
        )
        if available_rooms:
            mobile_room_labels = {
                f'{room["name"]} — {format_ar(room["nightly_rate"])}': room
                for room in available_rooms
            }
            mobile_room_label = st.selectbox(
                "Chambre",
                list(mobile_room_labels.keys()),
                key="mobile_reservation_room",
            )
            selected_room = mobile_room_labels[mobile_room_label]

            with st.form("mobile_new_reservation", clear_on_submit=True):
                client = st.text_input("Nom du client", key="mobile_client")
                phone = st.text_input("Téléphone", key="mobile_phone")
                arrival = st.date_input(
                    "Arrivée",
                    value=today,
                    key="mobile_arrival",
                )
                departure = st.date_input(
                    "Départ",
                    value=today + timedelta(days=1),
                    key="mobile_departure",
                )
                save_mobile_reservation = st.form_submit_button(
                    "✅ Enregistrer",
                    type="primary",
                    use_container_width=True,
                )

            if save_mobile_reservation:
                clean_client = client.strip()
                if not clean_client:
                    st.error("Saisissez le nom du client.")
                elif departure <= arrival:
                    st.error("La date de départ doit être après l’arrivée.")
                elif reservation_conflict(selected_room["id"], arrival, departure):
                    st.error("Cette chambre est déjà réservée sur ces dates.")
                else:
                    nights = (departure - arrival).days
                    total = nights * int(selected_room["nightly_rate"])
                    run(
                        """
                        INSERT INTO reservations(
                            room_id, client, phone, arrival, departure,
                            nightly_rate, total, status
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, 'Confirmée')
                        """,
                        (
                            selected_room["id"],
                            clean_client,
                            phone.strip(),
                            arrival.isoformat(),
                            departure.isoformat(),
                            int(selected_room["nightly_rate"]),
                            total,
                        ),
                    )
                    st.success(f"✅ Réservation enregistrée · {format_ar(total)}")
                    st.rerun()
        else:
            st.info("Aucune chambre disponible.")

    with quick_payment:
        mobile_stays = rows(
            """
            SELECT r.id, r.client, r.total, rm.name AS room_name
            FROM reservations r
            JOIN rooms rm ON rm.id = r.room_id
            WHERE r.status != 'Annulée' AND r.checked_out = 0
            ORDER BY r.arrival, r.id
            """
        )
        if mobile_stays:
            stay_labels = {
                f'R{item["id"]:03d} · {item["client"]} · {item["room_name"]}': item
                for item in mobile_stays
            }
            stay_label = st.selectbox(
                "Séjour",
                list(stay_labels.keys()),
                key="mobile_payment_stay",
            )
            selected_stay = stay_labels[stay_label]
            already_paid = paid_for(selected_stay["id"])
            remaining = max(int(selected_stay["total"]) - already_paid, 0)
            st.caption(f"Reste hébergement : {format_ar(remaining)}")

            with st.form("mobile_payment_form", clear_on_submit=True):
                amount = st.number_input(
                    "Montant (Ar)",
                    min_value=0,
                    value=int(remaining),
                    step=5000,
                )
                method = st.selectbox(
                    "Mode de paiement",
                    ["Espèces", "MVola", "Orange Money", "Airtel Money", "Carte bancaire"],
                )
                save_mobile_payment = st.form_submit_button(
                    "💳 Enregistrer le paiement",
                    type="primary",
                    use_container_width=True,
                )

            if save_mobile_payment:
                if amount <= 0:
                    st.error("Saisissez un montant supérieur à 0.")
                else:
                    run(
                        """
                        INSERT INTO payments(reservation_id, payment_date, amount, method)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            selected_stay["id"],
                            today.isoformat(),
                            int(amount),
                            method,
                        ),
                    )
                    st.success("✅ Paiement enregistré.")
                    st.rerun()
        else:
            st.info("Aucun séjour à encaisser.")

    st.markdown('<div class="mobile-section-title">📍 Aujourd’hui</div>', unsafe_allow_html=True)
    if arrivals:
        for item in arrivals:
            st.markdown(
                f"""
                <div class="mobile-row-card">
                    <div class="title">🟢 Arrivée · {item["room_name"]}</div>
                    <div class="meta">{item["client"]} · {item["phone"] or "Téléphone non renseigné"}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.caption("Aucune arrivée aujourd’hui.")

    if departures:
        for item in departures:
            st.markdown(
                f"""
                <div class="mobile-row-card">
                    <div class="title">🔵 Départ · {item["room_name"]}</div>
                    <div class="meta">{item["client"]} · {item["phone"] or "Téléphone non renseigné"}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.caption("Aucun départ aujourd’hui.")

    st.markdown('<div class="mobile-section-title">🛏️ Chambres</div>', unsafe_allow_html=True)
    for room in room_data:
        status = room_status(room["id"], room["maintenance"])
        guest = active_guest_for_room(room["id"])
        guest_line = guest if guest else "Aucun client en chambre"
        st.markdown(
            f"""
            <div class="mobile-row-card mobile-room">
                <div>
                    <div class="room-name">{room["name"]}</div>
                    <div class="guest">{guest_line}</div>
                </div>
                <div class="mobile-badge">{status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="mobile-section-title">📊 Résumé financier</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="mobile-grid">
            <div class="mobile-stat">
                <div class="label">Encaissements mois</div>
                <div class="value">{format_ar(month_total)}</div>
            </div>
            <div class="mobile-stat">
                <div class="label">Dépenses mois</div>
                <div class="value">{format_ar(expense_month)}</div>
            </div>
            <div class="mobile-stat">
                <div class="label">Résultat mois</div>
                <div class="value">{format_ar(month_total - expense_month)}</div>
            </div>
            <div class="mobile-stat">
                <div class="label">Réservées</div>
                <div class="value">{reserved_count}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Palmeria Mobile Manager · mêmes données que la réception")
    st.markdown("</div>", unsafe_allow_html=True)


init_db()

if "bar_cart" not in st.session_state:
    st.session_state.bar_cart = []

mobile_mode = str(st.query_params.get("mobile", "0")).lower() in {"1", "true", "yes"}
if mobile_mode:
    render_mobile_manager()
    st.stop()

st.markdown(
    f"""
    <div class="hero">
        <div class="wood-logo">
            <div class="brand">🌴 HÔTEL PALMERIA</div>
            <div class="tagline">{HOTEL_TAGLINE}</div>
        </div>
        <div class="hero-subtitle">{HOTEL_SUBTITLE}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

(
    tab_dashboard,
    tab_rooms,
    tab_reservations,
    tab_planning,
    tab_clients,
    tab_bar,
    tab_invoice,
    tab_payments,
    tab_expenses,
) = st.tabs(
    [
        "📊 Tableau de bord",
        "🛏️ Chambres",
        "📅 Réservations",
        "🗓️ Planning",
        "👥 Clients",
        "🍹 Bar",
        "📄 Facture",
        "💰 Paiements",
        "🧾 Dépenses",
    ]
)

with tab_dashboard:
    st.markdown("### Bienvenue à l’Hôtel Palmeria")
    st.caption("Gestion quotidienne de l’hôtel — chambres, clients, bar et facturation")

    room_data = rows("SELECT * FROM rooms ORDER BY name")
    statuses = [
        room_status(room["id"], room["maintenance"])
        for room in room_data
    ]

    occupied_count = statuses.count("🔴 Occupée")
    occupancy_rate = round((occupied_count / len(room_data)) * 100) if room_data else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("🏨 Chambres", len(room_data))
    c2.metric("🟢 Libres", statuses.count("🟢 Libre"))
    c3.metric("🔴 Occupées", occupied_count)
    c4.metric("🟠 Réservées", statuses.count("🟠 Réservée"))
    c5.metric("📈 Occupation", f"{occupancy_rate} %")

    st.markdown("---")
    st.subheader("💰 Finances")
    day_total, week_total, month_total, all_total = revenue_totals()
    expense_day, expense_week, expense_month, expense_all = expense_totals()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Encaissements aujourd’hui", format_ar(day_total))
    c2.metric("Encaissements ce mois", format_ar(month_total))
    c3.metric("Dépenses ce mois", format_ar(expense_month))
    c4.metric("Résultat ce mois", format_ar(month_total - expense_month))

    c1, c2, c3 = st.columns(3)
    c1.metric("Total encaissé", format_ar(all_total))
    c2.metric("Total dépenses", format_ar(expense_all))
    c3.metric("⏳ Reste à encaisser", format_ar(outstanding_total()))

    bar_today, bar_month, bar_all, bar_pending = bar_totals()
    c1, c2, c3 = st.columns(3)
    c1.metric("🍹 Bar aujourd’hui", format_ar(bar_today))
    c2.metric("🍹 Bar ce mois", format_ar(bar_month))
    c3.metric("🧾 Notes bar en chambre", format_ar(bar_pending))

    st.markdown("---")
    st.subheader("📍 Aujourd’hui")
    arrivals, departures = today_movements()
    left_today, right_today = st.columns(2)

    with left_today:
        st.markdown("#### 🟢 Arrivées")
        if arrivals:
            st.dataframe(
                [
                    {
                        "Réservation": f'R{item["id"]:03d}',
                        "Chambre": item["room_name"],
                        "Client": item["client"],
                        "Téléphone": item["phone"] or "-",
                    }
                    for item in arrivals
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("Aucune arrivée aujourd’hui.")

    with right_today:
        st.markdown("#### 🔵 Départs")
        if departures:
            st.dataframe(
                [
                    {
                        "Réservation": f'R{item["id"]:03d}',
                        "Chambre": item["room_name"],
                        "Client": item["client"],
                        "Téléphone": item["phone"] or "-",
                    }
                    for item in departures
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("Aucun départ aujourd’hui.")

    st.markdown("---")
    st.subheader("🛏️ État des chambres")
    st.dataframe(room_view(), use_container_width=True, hide_index=True)

with tab_rooms:
    st.subheader("🛏️ Gestion des chambres")

    room_cards = rows("SELECT * FROM rooms ORDER BY name")
    if room_cards:
        photo_cols = st.columns(min(3, len(room_cards)))
        for index, room in enumerate(room_cards[:3]):
            with photo_cols[index]:
                image_url = ROOM_IMAGES[index % len(ROOM_IMAGES)]
                status = room_status(room["id"], room["maintenance"])
                current = current_room_stay(room["id"])
                upcoming = next_room_booking(room["id"])
                amenities = [
                    item for item in (room["amenities"] or "").split("|") if item
                ]
                amenities_preview = " · ".join(amenities[:5]) or "Équipements à renseigner"
                guest_line = (
                    f'👤 {current["client"]} · départ {current["departure"]}'
                    if current
                    else "👤 Aucun client en chambre"
                )
                next_line = (
                    f'📅 Prochaine arrivée : {upcoming["arrival"]} · {upcoming["client"]}'
                    if upcoming
                    else "📅 Aucune arrivée à venir"
                )
                st.markdown(
                    f"""
                    <div class="room-photo-card">
                        <img src="{image_url}" alt="{room["name"]}">
                        <div class="body">
                            <div class="title">{room["name"]} · {room["room_type"]}</div>
                            <div>{status} · 🧹 {room["housekeeping_status"]}</div>
                            <div style="margin-top:5px;">🛏️ {room["bed_type"]} · 👥 {room["capacity_adults"]} adulte(s) + {room["capacity_children"]} enfant(s)</div>
                            <div>🏢 {room["floor"]} · 👀 {room["view_type"]}</div>
                            <div style="margin-top:5px;">{guest_line}</div>
                            <div>{next_line}</div>
                            <div style="margin-top:5px;font-size:.86rem;">✨ {amenities_preview}</div>
                            <div style="margin-top:7px;"><b>{format_ar(room["nightly_rate"])}</b> / nuit</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.dataframe(room_view(), use_container_width=True, hide_index=True)

    st.markdown("---")
    left, right = st.columns(2)

    with left:
        st.markdown("#### ➕ Ajouter une chambre")
        with st.form("add_room", clear_on_submit=True):
            room_name = st.text_input(
                "Nom / numéro de chambre",
                placeholder="Ex. Chambre 104",
            )
            nightly_rate = st.number_input(
                "Tarif par nuit (Ar)",
                min_value=0,
                value=100000,
                step=5000,
            )
            add_room = st.form_submit_button(
                "Ajouter la chambre",
                type="primary",
                use_container_width=True,
            )

        if add_room:
            clean_name = room_name.strip()
            if not clean_name:
                st.error("Veuillez saisir un nom de chambre.")
            elif one(
                "SELECT id FROM rooms WHERE lower(name) = lower(?)",
                (clean_name,),
            ):
                st.warning("Cette chambre existe déjà.")
            else:
                run(
                    "INSERT INTO rooms(name, nightly_rate) VALUES (?, ?)",
                    (clean_name, int(nightly_rate)),
                )
                st.success(f"✅ {clean_name} ajoutée.")
                st.rerun()

    with right:
        st.markdown("#### 🛠️ Maintenance")
        room_options = rows(
            "SELECT id, name, maintenance FROM rooms ORDER BY name"
        )
        if room_options:
            labels = {
                f'{room["name"]}{" — maintenance" if room["maintenance"] else ""}': room
                for room in room_options
            }
            selected_label = st.selectbox(
                "Chambre",
                list(labels.keys()),
                key="maintenance_room",
            )
            selected_room = labels[selected_label]

            if selected_room["maintenance"]:
                if st.button("✅ Remettre disponible", use_container_width=True):
                    run(
                        "UPDATE rooms SET maintenance = 0 WHERE id = ?",
                        (selected_room["id"],),
                    )
                    st.rerun()
            else:
                if st.button("🛠️ Mettre en maintenance", use_container_width=True):
                    run(
                        "UPDATE rooms SET maintenance = 1 WHERE id = ?",
                        (selected_room["id"],),
                    )
                    st.rerun()

    st.markdown("---")
    st.markdown("#### 🧹 État ménage & disponibilité")
    housekeeping_rooms = rows("SELECT * FROM rooms ORDER BY name")
    if housekeeping_rooms:
        housekeeping_labels = {room["name"]: room for room in housekeeping_rooms}
        housekeeping_label = st.selectbox(
            "Chambre à mettre à jour",
            list(housekeeping_labels.keys()),
            key="housekeeping_room_select",
        )
        housekeeping_room = housekeeping_labels[housekeeping_label]
        housekeeping_choices = ["Prête", "À nettoyer", "En nettoyage", "Hors service"]
        current_housekeeping = (
            housekeeping_room["housekeeping_status"]
            if housekeeping_room["housekeeping_status"] in housekeeping_choices
            else "Prête"
        )
        housekeeping_status = st.selectbox(
            "État de la chambre",
            housekeeping_choices,
            index=housekeeping_choices.index(current_housekeeping),
            key="housekeeping_status_select",
        )
        if st.button(
            "💾 Mettre à jour l’état",
            use_container_width=True,
            key="save_housekeeping_status",
        ):
            run(
                "UPDATE rooms SET housekeeping_status = ? WHERE id = ?",
                (housekeeping_status, housekeeping_room["id"]),
            )
            st.success("✅ État de la chambre mis à jour.")
            st.rerun()

    st.markdown("---")
    st.markdown("#### 🛏️ Fiche détaillée de la chambre")
    detail_rooms = rows("SELECT * FROM rooms ORDER BY name")
    if detail_rooms:
        detail_labels = {room["name"]: room for room in detail_rooms}
        detail_label = st.selectbox(
            "Chambre à personnaliser",
            list(detail_labels.keys()),
            key="room_details_select",
        )
        detail_room = detail_labels[detail_label]

        room_type_options = [
            "Simple", "Double", "Double Confort", "Double Deluxe",
            "Twin", "Triple", "Familiale", "Suite", "Suite Familiale"
        ]
        bed_options = [
            "Lit simple", "Lit double", "Queen Size", "King Size",
            "2 lits simples", "King + canapé-lit", "Lits superposés"
        ]
        amenity_options = [
            "Wi-Fi", "Climatisation", "Ventilateur", "TV", "Douche",
            "Baignoire", "Minibar", "Coffre-fort", "Balcon", "Terrasse",
            "Bureau", "Bouilloire", "Réfrigérateur", "Sèche-cheveux",
            "Lit bébé", "Accessible PMR"
        ]
        current_amenities = [
            item for item in (detail_room["amenities"] or "").split("|") if item
        ]

        with st.form("room_details_form"):
            c1, c2 = st.columns(2)
            with c1:
                room_type = st.selectbox(
                    "Type",
                    room_type_options,
                    index=room_type_options.index(detail_room["room_type"])
                    if detail_room["room_type"] in room_type_options else 1,
                )
                adults = st.number_input(
                    "Capacité adultes",
                    min_value=1,
                    max_value=10,
                    value=int(detail_room["capacity_adults"]),
                    step=1,
                )
                bed_type = st.selectbox(
                    "Type de lit",
                    bed_options,
                    index=bed_options.index(detail_room["bed_type"])
                    if detail_room["bed_type"] in bed_options else 1,
                )
                floor = st.text_input(
                    "Étage / emplacement",
                    value=detail_room["floor"],
                )
            with c2:
                children = st.number_input(
                    "Capacité enfants",
                    min_value=0,
                    max_value=10,
                    value=int(detail_room["capacity_children"]),
                    step=1,
                )
                view_type = st.text_input(
                    "Vue",
                    value=detail_room["view_type"],
                )
                notes = st.text_area(
                    "Notes internes",
                    value=detail_room["notes"] or "",
                    placeholder="Ex. lit bébé demandé, ampoule à changer…",
                )

            amenities = st.multiselect(
                "Équipements",
                amenity_options,
                default=[a for a in current_amenities if a in amenity_options],
            )
            save_room_details = st.form_submit_button(
                "💾 Enregistrer la fiche chambre",
                type="primary",
                use_container_width=True,
            )

        if save_room_details:
            run(
                """
                UPDATE rooms
                SET room_type = ?, capacity_adults = ?, capacity_children = ?,
                    bed_type = ?, floor = ?, view_type = ?, amenities = ?, notes = ?
                WHERE id = ?
                """,
                (
                    room_type, int(adults), int(children), bed_type,
                    floor.strip(), view_type.strip(), "|".join(amenities),
                    notes.strip(), detail_room["id"],
                ),
            )
            st.success("✅ Fiche chambre enregistrée.")
            st.rerun()

    st.markdown("---")
    st.markdown("#### ✏️ Modifier le tarif d’une chambre")
    editable_rooms = rows("SELECT id, name, nightly_rate FROM rooms ORDER BY name")
    if editable_rooms:
        edit_labels = {room["name"]: room for room in editable_rooms}
        edit_label = st.selectbox(
            "Chambre à modifier",
            list(edit_labels.keys()),
            key="edit_room_rate",
        )
        edit_room = edit_labels[edit_label]
        with st.form("edit_room_rate_form"):
            new_rate = st.number_input(
                "Nouveau tarif / nuit (Ar)",
                min_value=0,
                value=int(edit_room["nightly_rate"]),
                step=5000,
            )
            save_rate = st.form_submit_button(
                "💾 Enregistrer le tarif",
                use_container_width=True,
            )
        if save_rate:
            run(
                "UPDATE rooms SET nightly_rate = ? WHERE id = ?",
                (int(new_rate), edit_room["id"]),
            )
            st.success("✅ Tarif mis à jour.")
            st.rerun()

with tab_reservations:
    st.subheader("📅 Nouvelle réservation")

    available_rooms = rows(
        """
        SELECT id, name, nightly_rate
        FROM rooms
        WHERE maintenance = 0
        ORDER BY name
        """
    )

    if not available_rooms:
        st.warning("Aucune chambre disponible : toutes sont en maintenance.")
    else:
        room_labels = {
            f'{room["name"]} — {format_ar(room["nightly_rate"])} / nuit': room
            for room in available_rooms
        }
        selected_room_label = st.selectbox(
            "Chambre",
            list(room_labels.keys()),
            key="reservation_room",
        )
        selected_room = room_labels[selected_room_label]

        with st.form("new_reservation", clear_on_submit=True):
            client = st.text_input("Nom du client")
            phone = st.text_input("Téléphone")

            c1, c2 = st.columns(2)
            with c1:
                arrival = st.date_input("Date d’arrivée", value=date.today())
            with c2:
                departure = st.date_input(
                    "Date de départ",
                    value=date.today() + timedelta(days=1),
                )

            nightly_rate = st.number_input(
                "Prix par nuit (Ar)",
                min_value=0,
                value=int(selected_room["nightly_rate"]),
                step=5000,
            )
            status = st.selectbox("Statut", ["Confirmée", "En attente"])
            save_reservation = st.form_submit_button(
                "✅ Enregistrer la réservation",
                type="primary",
                use_container_width=True,
            )

        if save_reservation:
            clean_client = client.strip()
            if not clean_client:
                st.error("Veuillez saisir le nom du client.")
            elif departure <= arrival:
                st.error("La date de départ doit être après la date d’arrivée.")
            elif reservation_conflict(selected_room["id"], arrival, departure):
                st.error(
                    "❌ Cette chambre est déjà réservée sur tout ou partie de ces dates."
                )
            else:
                nights = (departure - arrival).days
                total = nights * int(nightly_rate)
                run(
                    """
                    INSERT INTO reservations(
                        room_id, client, phone, arrival, departure,
                        nightly_rate, total, status
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        selected_room["id"],
                        clean_client,
                        phone.strip(),
                        arrival.isoformat(),
                        departure.isoformat(),
                        int(nightly_rate),
                        int(total),
                        status,
                    ),
                )
                st.success(
                    f"✅ Réservation enregistrée : {nights} nuit(s), total {format_ar(total)}."
                )
                st.rerun()

    st.markdown("---")
    st.subheader("📋 Réservations")

    search_col, filter_col = st.columns([2, 1])
    with search_col:
        reservation_search = st.text_input(
            "🔎 Rechercher un client, téléphone ou chambre",
            key="reservation_search",
            placeholder="Ex. Rakoto, 034..., Chambre 102",
        )
    with filter_col:
        reservation_filter = st.selectbox(
            "Filtre séjour",
            ["Tous", "En séjour", "À venir", "Check-out fait", "À clôturer"],
            key="reservation_filter",
        )

    reservation_data = reservation_view()
    filtered_reservations = reservation_data

    if reservation_search.strip():
        needle = reservation_search.strip().lower()
        filtered_reservations = [
            item
            for item in filtered_reservations
            if needle in item["Client"].lower()
            or needle in item["Téléphone"].lower()
            or needle in item["Chambre"].lower()
            or needle in item["ID"].lower()
        ]

    if reservation_filter != "Tous":
        filtered_reservations = [
            item
            for item in filtered_reservations
            if reservation_filter.lower() in item["Séjour"].lower()
        ]

    if filtered_reservations:
        st.dataframe(
            filtered_reservations,
            use_container_width=True,
            hide_index=True,
        )
    elif reservation_data:
        st.warning("Aucune réservation ne correspond à votre recherche.")
    else:
        st.info("Aucune réservation enregistrée.")

    st.markdown("---")
    st.subheader("🚪 Check-in / Check-out")
    operation_rows = rows(
        """
        SELECT r.id, r.room_id, r.client, r.arrival, r.departure, r.checked_in, r.checked_out,
               rm.name AS room_name
        FROM reservations r
        JOIN rooms rm ON rm.id = r.room_id
        WHERE r.status != 'Annulée' AND r.checked_out = 0
        ORDER BY r.arrival, r.id
        """
    )

    if operation_rows:
        operation_labels = {
            (
                f'R{item["id"]:03d} — {item["client"]} — {item["room_name"]} '
                f'({item["arrival"]} → {item["departure"]})'
            ): item
            for item in operation_rows
        }
        operation_label = st.selectbox(
            "Sélectionner le séjour",
            list(operation_labels.keys()),
            key="stay_operation",
        )
        stay = operation_labels[operation_label]

        left_action, right_action = st.columns(2)

        with left_action:
            if not stay["checked_in"]:
                if st.button(
                    "🟣 Faire le check-in",
                    use_container_width=True,
                    key="checkin_button",
                ):
                    run(
                        """
                        UPDATE reservations
                        SET checked_in = 1, checkin_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                        """,
                        (stay["id"],),
                    )
                    st.success("✅ Check-in enregistré.")
                    st.rerun()
            else:
                st.success("🟣 Client déjà en séjour.")

        with right_action:
            if stay["checked_in"]:
                if st.button(
                    "🔵 Faire le check-out",
                    use_container_width=True,
                    key="checkout_button",
                ):
                    pending_bar = one(
                        """
                        SELECT COALESCE(SUM(total), 0) AS total
                        FROM bar_sales
                        WHERE room_id = ? AND paid = 0
                        """,
                        (stay["room_id"],),
                    )
                    pending_amount = int(pending_bar["total"] if pending_bar else 0)

                    if pending_amount > 0:
                        st.error(
                            f"🍹 Note bar à régler avant le départ : {format_ar(pending_amount)}"
                        )
                    else:
                        run(
                            """
                            UPDATE reservations
                            SET checked_out = 1, checkout_at = CURRENT_TIMESTAMP
                            WHERE id = ?
                            """,
                            (stay["id"],),
                        )
                        run(
                            """
                            UPDATE rooms
                            SET housekeeping_status = 'À nettoyer'
                            WHERE id = ?
                            """,
                            (stay["room_id"],),
                        )
                        st.success("✅ Check-out enregistré. Chambre passée en 🧹 À nettoyer.")
                        st.rerun()
            else:
                st.info("Le check-in doit être fait avant le check-out.")
    else:
        st.info("Aucun séjour actif à traiter.")

    cancellable = rows(
        """
        SELECT r.id, r.client, rm.name AS room_name
        FROM reservations r
        JOIN rooms rm ON rm.id = r.room_id
        WHERE r.status != 'Annulée' AND r.checked_in = 0 AND r.checked_out = 0
        ORDER BY r.id DESC
        """
    )
    if cancellable:
        with st.expander("🚫 Annuler une réservation"):
            cancel_labels = {
                f'R{item["id"]:03d} — {item["client"]} — {item["room_name"]}': item["id"]
                for item in cancellable
            }
            cancel_label = st.selectbox(
                "Réservation à annuler",
                list(cancel_labels.keys()),
                key="cancel_reservation",
            )
            if st.button("🚫 Confirmer l’annulation", key="cancel_button"):
                run(
                    "UPDATE reservations SET status = 'Annulée' WHERE id = ?",
                    (cancel_labels[cancel_label],),
                )
                st.success("Réservation annulée.")
                st.rerun()


with tab_planning:
    st.subheader("🗓️ Planning visuel des chambres")
    st.markdown(
        """
        <div class="legend">
            <span class="green">🟢 Libre</span>
            <span class="orange">🟠 Réservée</span>
            <span class="purple">🟣 En séjour</span>
            <span class="red">🛠️ Maintenance</span>
            <span class="orange">🧹 À nettoyer</span>
            <span class="blue">🧽 En nettoyage</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([2, 1])
    with c1:
        planning_start = st.date_input(
            "Début du planning",
            value=date.today(),
            key="planning_start",
        )
    with c2:
        planning_days = st.selectbox(
            "Période",
            [7, 14, 21],
            index=1,
            format_func=lambda value: f"{value} jours",
            key="planning_days",
        )

    st.dataframe(
        planning_view(planning_start, planning_days),
        use_container_width=True,
        hide_index=True,
        height=320,
    )
    st.caption(
        "🟣 = client présent • 🟠 = réservation à venir • 🟢 = chambre libre"
    )


with tab_clients:
    st.subheader("👥 Fichier clients")
    clients = client_summary()

    if clients:
        c1, c2, c3 = st.columns(3)
        c1.metric("👥 Clients", len(clients))
        c2.metric(
            "🔁 Clients revenus",
            sum(1 for item in clients if item["Séjours"] > 1),
        )
        c3.metric(
            "🏨 Séjours enregistrés",
            sum(item["Séjours"] for item in clients),
        )

        client_search = st.text_input(
            "🔎 Rechercher un client",
            placeholder="Nom ou téléphone",
            key="client_search",
        )

        filtered_clients = clients
        if client_search.strip():
            needle = client_search.strip().lower()
            filtered_clients = [
                item
                for item in clients
                if needle in item["Client"].lower()
                or needle in item["Téléphone"].lower()
            ]

        st.dataframe(
            filtered_clients,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("#### 📚 Historique d’un client")
        client_labels = {
            f'{item["Client"]} — {item["Téléphone"]}': item
            for item in clients
        }
        client_label = st.selectbox(
            "Client",
            list(client_labels.keys()),
            key="client_history_select",
        )
        selected_client = client_labels[client_label]

        client_history = rows(
            """
            SELECT r.id, r.arrival, r.departure, r.total, r.status,
                   r.checked_in, r.checked_out, rm.name AS room_name
            FROM reservations r
            JOIN rooms rm ON rm.id = r.room_id
            WHERE r.client = ? AND COALESCE(r.phone, '') = ?
            ORDER BY r.arrival DESC
            """,
            (
                selected_client["Client"],
                "" if selected_client["Téléphone"] == "-" else selected_client["Téléphone"],
            ),
        )

        history_display = []
        for item in client_history:
            paid = paid_for(item["id"])
            history_display.append(
                {
                    "Réservation": f'R{item["id"]:03d}',
                    "Chambre": item["room_name"],
                    "Arrivée": item["arrival"],
                    "Départ": item["departure"],
                    "Total": format_ar(item["total"]),
                    "Payé": format_ar(paid),
                    "Reste": format_ar(max(int(item["total"]) - paid, 0)),
                    "Statut": (
                        "🔵 Terminé"
                        if item["checked_out"]
                        else "🟣 En séjour"
                        if item["checked_in"]
                        else item["status"]
                    ),
                }
            )

        st.dataframe(
            history_display,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Aucun client enregistré pour le moment.")


with tab_bar:
    st.markdown(
        """
        <div class="bar-banner">
            <h2 style="margin:0;color:white;-webkit-text-fill-color:white;">🍹 Le Bar Palmeria</h2>
            <p style="margin:6px 0 0 0;">Commandes comptoir • consommation en chambre • stock • encaissements</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    bar_today, bar_month, bar_all, bar_pending = bar_totals()
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("💵 Aujourd’hui", format_ar(bar_today))
    b2.metric("📅 Ce mois", format_ar(bar_month))
    b3.metric("🏆 Total encaissé", format_ar(bar_all))
    b4.metric("🧾 À régler en chambre", format_ar(bar_pending))

    st.markdown("### 🍹 Carte complète du bar")
    all_products = rows(
        """
        SELECT id, name, category, emoji, price, stock
        FROM bar_products
        WHERE active = 1
        ORDER BY category, name
        """
    )

    categories = sorted({product["category"] for product in all_products})
    category_filter = st.selectbox(
        "📂 Catégorie",
        ["Tous les produits"] + categories,
        key="bar_category_filter",
    )
    product_search = st.text_input(
        "🔎 Rechercher un produit",
        placeholder="Ex. mojito, café, jus, chips…",
        key="bar_product_search",
    )

    products = all_products
    if category_filter != "Tous les produits":
        products = [
            product for product in products
            if product["category"] == category_filter
        ]
    if product_search.strip():
        needle = product_search.strip().lower()
        products = [
            product for product in products
            if needle in product["name"].lower()
            or needle in product["category"].lower()
        ]

    st.caption(
        f"🍽️ {len(all_products)} produits enregistrés • "
        f"{len(categories)} catégories • prix et stocks modifiables"
    )

    product_columns = st.columns(3)
    for index, product in enumerate(products):
        with product_columns[index % 3]:
            stock_text = (
                "🔴 Stock faible"
                if int(product["stock"]) <= 5
                else f'📦 Stock : {product["stock"]}'
            )
            product_image = BAR_IMAGES.get(product["name"], "")
            image_html = (
                f'<img src="{product_image}" alt="{product["name"]}">'
                if product_image
                else ""
            )
            st.markdown(
                f"""
                <div class="product-card">
                    {image_html}
                    <div class="emoji">{product["emoji"]}</div>
                    <div class="name">{product["name"]}</div>
                    <div>{product["category"]}</div>
                    <div class="price">{format_ar(product["price"])}</div>
                    <div class="stock">{stock_text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.subheader("🛒 Nouvelle commande")

    available_products = [
        product for product in all_products if int(product["stock"]) > 0
    ]

    if available_products:
        product_labels = {
            f'{item["emoji"]} {item["name"]} — {format_ar(item["price"])} — stock {item["stock"]}': item
            for item in available_products
        }

        c1, c2 = st.columns([3, 1])
        with c1:
            selected_product_label = st.selectbox(
                "Boisson",
                list(product_labels.keys()),
                key="bar_product_select",
            )
            selected_product = product_labels[selected_product_label]
        with c2:
            bar_quantity = st.number_input(
                "Quantité",
                min_value=1,
                max_value=max(1, int(selected_product["stock"])),
                value=1,
                step=1,
                key="bar_quantity",
            )

        if st.button("➕ Ajouter au panier", key="bar_add_cart"):
            existing = next(
                (
                    item
                    for item in st.session_state.bar_cart
                    if item["product_id"] == selected_product["id"]
                ),
                None,
            )

            if existing:
                new_quantity = existing["quantity"] + int(bar_quantity)
                if new_quantity > int(selected_product["stock"]):
                    st.warning("Quantité supérieure au stock disponible.")
                else:
                    existing["quantity"] = new_quantity
            else:
                st.session_state.bar_cart.append(
                    {
                        "product_id": selected_product["id"],
                        "name": selected_product["name"],
                        "emoji": selected_product["emoji"],
                        "price": int(selected_product["price"]),
                        "quantity": int(bar_quantity),
                    }
                )
            st.rerun()
    else:
        st.warning("Aucune boisson en stock.")

    if st.session_state.bar_cart:
        st.markdown("#### 🧺 Panier")
        cart_display = []
        cart_total = 0

        for item in st.session_state.bar_cart:
            subtotal = int(item["price"]) * int(item["quantity"])
            cart_total += subtotal
            cart_display.append(
                {
                    "Produit": f'{item["emoji"]} {item["name"]}',
                    "Qté": item["quantity"],
                    "Prix": format_ar(item["price"]),
                    "Sous-total": format_ar(subtotal),
                }
            )

        st.dataframe(
            cart_display,
            use_container_width=True,
            hide_index=True,
        )
        st.metric("🧾 Total de la commande", format_ar(cart_total))

        if st.button("🗑️ Vider le panier", key="bar_clear_cart"):
            st.session_state.bar_cart = []
            st.rerun()

        st.markdown("#### 💳 Encaisser / mettre sur la chambre")
        destination = st.radio(
            "Destination",
            ["Comptoir", "Chambre"],
            horizontal=True,
            key="bar_destination",
        )

        room_id = None
        guest_name = ""

        if destination == "Chambre":
            occupied_rooms = [
                room
                for room in rows("SELECT id, name, maintenance FROM rooms ORDER BY name")
                if room_status(room["id"], room["maintenance"]) == "🔴 Occupée"
            ]

            if occupied_rooms:
                room_labels = {
                    room["name"]: room for room in occupied_rooms
                }
                selected_room_name = st.selectbox(
                    "Chambre",
                    list(room_labels.keys()),
                    key="bar_room_select",
                )
                room_id = room_labels[selected_room_name]["id"]
                guest_name = active_guest_for_room(room_id)
                if guest_name:
                    st.info(f"👤 Client : **{guest_name}**")
            else:
                st.warning("Aucune chambre occupée actuellement.")

        payment_options = [
            "Espèces",
            "MVola",
            "Orange Money",
            "Airtel Money",
            "Carte bancaire",
        ]
        if destination == "Chambre":
            payment_options.append("Ajouter à la chambre")

        bar_payment_method = st.selectbox(
            "Mode de règlement",
            payment_options,
            key="bar_payment_method",
        )

        manual_client = st.text_input(
            "Nom du client (facultatif)",
            value=guest_name,
            key="bar_client_name",
        )

        if st.button(
            "✅ Valider la commande",
            type="primary",
            use_container_width=True,
            key="bar_validate_order",
        ):
            if destination == "Chambre" and room_id is None:
                st.error("Sélectionnez une chambre occupée.")
            elif bar_payment_method == "Ajouter à la chambre" and room_id is None:
                st.error("Une note de chambre doit être liée à une chambre.")
            else:
                try:
                    ticket = save_bar_ticket(
                        st.session_state.bar_cart,
                        bar_payment_method,
                        room_id,
                        manual_client,
                    )
                    st.session_state.bar_cart = []
                    st.success(f"✅ Commande {ticket} enregistrée.")
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))
    else:
        st.info("Ajoutez une boisson au panier pour créer une commande.")

    st.markdown("---")
    st.subheader("🧾 Notes bar en attente")
    pending_tickets = rows(
        """
        SELECT
            bs.ticket,
            bs.sale_date,
            rm.name AS room_name,
            MAX(bs.client) AS client,
            SUM(bs.total) AS total
        FROM bar_sales bs
        LEFT JOIN rooms rm ON rm.id = bs.room_id
        WHERE bs.paid = 0
        GROUP BY bs.ticket, bs.sale_date, rm.name
        ORDER BY MAX(bs.id) DESC
        """
    )

    if pending_tickets:
        st.dataframe(
            [
                {
                    "Ticket": item["ticket"],
                    "Date": item["sale_date"],
                    "Chambre": item["room_name"] or "-",
                    "Client": item["client"] or "-",
                    "À régler": format_ar(item["total"]),
                }
                for item in pending_tickets
            ],
            use_container_width=True,
            hide_index=True,
        )

        pending_labels = {
            f'{item["ticket"]} — {item["room_name"] or "Sans chambre"} — {format_ar(item["total"])}': item
            for item in pending_tickets
        }
        pending_label = st.selectbox(
            "Note à régler",
            list(pending_labels.keys()),
            key="bar_pending_select",
        )
        pending = pending_labels[pending_label]

        settle_method = st.selectbox(
            "Paiement de la note",
            ["Espèces", "MVola", "Orange Money", "Airtel Money", "Carte bancaire"],
            key="bar_settle_method",
        )

        if st.button("💰 Régler la note bar", key="bar_settle_button"):
            with db() as con:
                con.execute(
                    """
                    UPDATE bar_sales
                    SET paid = 1, payment_method = ?
                    WHERE ticket = ?
                    """,
                    (settle_method, pending["ticket"]),
                )
                con.commit()
            st.success("✅ Note bar réglée.")
            st.rerun()
    else:
        st.success("✅ Aucune note bar en attente.")

    st.markdown("---")
    st.subheader("📦 Stock du bar")
    stock_rows = rows(
        """
        SELECT id, emoji, name, category, price, stock
        FROM bar_products
        WHERE active = 1
        ORDER BY category, name
        """
    )
    st.dataframe(
        [
            {
                "Produit": f'{item["emoji"]} {item["name"]}',
                "Catégorie": item["category"],
                "Prix": format_ar(item["price"]),
                "Stock": item["stock"],
                "Alerte": "🔴 Faible" if int(item["stock"]) <= 5 else "🟢 OK",
            }
            for item in stock_rows
        ],
        use_container_width=True,
        hide_index=True,
    )

    with st.expander("➕ Réapprovisionner le stock"):
        stock_labels = {
            f'{item["emoji"]} {item["name"]}': item
            for item in stock_rows
        }
        stock_label = st.selectbox(
            "Produit",
            list(stock_labels.keys()),
            key="bar_stock_product",
        )
        stock_product = stock_labels[stock_label]
        added_stock = st.number_input(
            "Quantité reçue",
            min_value=1,
            value=6,
            step=1,
            key="bar_stock_qty",
        )
        if st.button("📦 Ajouter au stock", key="bar_stock_add"):
            run(
                "UPDATE bar_products SET stock = stock + ? WHERE id = ?",
                (int(added_stock), stock_product["id"]),
            )
            st.success("✅ Stock mis à jour.")
            st.rerun()

    st.markdown("---")
    st.subheader("📒 Historique des commandes")
    bar_history = rows(
        """
        SELECT
            bs.ticket,
            bs.sale_date,
            rm.name AS room_name,
            MAX(bs.client) AS client,
            MAX(bs.payment_method) AS payment_method,
            MIN(bs.paid) AS paid,
            SUM(bs.total) AS total
        FROM bar_sales bs
        LEFT JOIN rooms rm ON rm.id = bs.room_id
        GROUP BY bs.ticket, bs.sale_date, rm.name
        ORDER BY MAX(bs.id) DESC
        LIMIT 50
        """
    )

    if bar_history:
        st.dataframe(
            [
                {
                    "Ticket": item["ticket"],
                    "Date": item["sale_date"],
                    "Destination": item["room_name"] or "Comptoir",
                    "Client": item["client"] or "-",
                    "Total": format_ar(item["total"]),
                    "Règlement": item["payment_method"],
                    "Statut": "🟢 Payé" if item["paid"] else "🟠 À régler",
                }
                for item in bar_history
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Aucune commande enregistrée.")


with tab_invoice:
    st.subheader("📄 Facture client & clôture du séjour")
    st.caption(
        "Une seule fiche regroupe l’hébergement, le bar, les extras, les paiements et le solde final."
    )

    invoice_stays = rows(
        """
        SELECT
            r.id,
            r.client,
            r.phone,
            r.arrival,
            r.departure,
            r.checked_in,
            r.checked_out,
            r.invoice_closed,
            r.invoice_number,
            rm.name AS room_name
        FROM reservations r
        JOIN rooms rm ON rm.id = r.room_id
        WHERE r.status != 'Annulée'
        ORDER BY r.invoice_closed ASC, r.departure DESC, r.id DESC
        """
    )

    if not invoice_stays:
        st.info("Aucun séjour disponible pour la facturation.")
    else:
        invoice_labels = {
            (
                f'{"✅ " if item["invoice_closed"] else "🟣 "}'
                f'R{item["id"]:03d} — {item["client"]} — {item["room_name"]} '
                f'({item["arrival"]} → {item["departure"]})'
            ): item
            for item in invoice_stays
        }

        invoice_label = st.selectbox(
            "Séjour / client",
            list(invoice_labels.keys()),
            key="invoice_stay_select",
        )
        invoice_stay = invoice_labels[invoice_label]
        invoice = reservation_invoice(invoice_stay["id"])

        if invoice:
            r = invoice["reservation"]
            nights = (
                date.fromisoformat(r["departure"])
                - date.fromisoformat(r["arrival"])
            ).days
            invoice_number = (
                r["invoice_number"]
                or f'PROV-{date.today().year}-{r["id"]:04d}'
            )

            st.markdown(
                f"""
                <div class="invoice-card">
                    <div style="font-family:Georgia,serif;font-size:1.05rem;font-weight:900;letter-spacing:.08em;margin-bottom:8px;">🌴 HÔTEL PALMERIA</div>
                    <div style="opacity:.72;font-size:.86rem;margin-bottom:12px;">{HOTEL_TAGLINE}</div>
                    <div class="invoice-title">🧾 {invoice_number}</div>
                    <div class="invoice-meta">
                        <b>Client :</b> {r["client"]}<br>
                        <b>Téléphone :</b> {r["phone"] or "-"}<br>
                        <b>Chambre :</b> {r["room_name"]}<br>
                        <b>Séjour :</b> {r["arrival"]} → {r["departure"]} • {nights} nuit(s)<br>
                        <b>Statut :</b> {"✅ Facture clôturée" if r["invoice_closed"] else "🟣 Facture ouverte"}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            m1, m2, m3 = st.columns(3)
            m1.metric("🧾 Total facture", format_ar(invoice["grand_total"]))
            m2.metric("✅ Déjà réglé", format_ar(invoice["paid_total"]))
            m3.metric("💳 Reste à payer", format_ar(invoice["remaining"]))

            preview_rows = [
                (
                    f"{nights} nuit(s) — {r['room_name']}",
                    "Hébergement",
                    invoice["lodging_total"],
                )
            ]
            preview_rows.extend(
                [
                    (
                        f"{item['quantity']} × {item['product_name']}",
                        "Bar",
                        int(item["total"]),
                    )
                    for item in invoice["bar_items"]
                ]
            )
            preview_rows.extend(
                [
                    (
                        item["label"],
                        item["description"] or "Extra",
                        int(item["amount"]),
                    )
                    for item in invoice["extras"]
                ]
            )

            preview_html_rows = "".join(
                [
                    (
                        "<tr>"
                        f"<td>{label}</td>"
                        f"<td>{detail}</td>"
                        f"<td>{format_ar(amount)}</td>"
                        "</tr>"
                    )
                    for label, detail, amount in preview_rows
                ]
            )

            st.markdown("### 👁️ Aperçu facture client")
            st.markdown(
                f"""
                <div class="invoice-preview">
                    <div class="invoice-brand">🌴 HÔTEL PALMERIA</div>
                    <div style="margin-top:4px;color:#6f6252;">{HOTEL_TAGLINE}</div>
                    <div style="margin-top:14px;"><b>{invoice_number}</b></div>
                    <div style="margin-top:8px;">
                        Client : <b>{r["client"]}</b> • Chambre : <b>{r["room_name"]}</b><br>
                        Séjour : {r["arrival"]} → {r["departure"]}
                    </div>
                    <table>
                        <thead>
                            <tr><th>Désignation</th><th>Détail</th><th>Montant</th></tr>
                        </thead>
                        <tbody>
                            {preview_html_rows}
                            <tr class="total-row">
                                <td colspan="2">TOTAL</td>
                                <td>{format_ar(invoice["grand_total"])}</td>
                            </tr>
                            <tr>
                                <td colspan="2">Déjà réglé</td>
                                <td>{format_ar(invoice["paid_total"])}</td>
                            </tr>
                            <tr class="total-row">
                                <td colspan="2">RESTE À PAYER</td>
                                <td>{format_ar(invoice["remaining"])}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("#### 🛏️ Hébergement")
            st.dataframe(
                [
                    {
                        "Prestation": f'{nights} nuit(s) — {r["room_name"]}',
                        "Prix / nuit": format_ar(r["nightly_rate"]),
                        "Total": format_ar(invoice["lodging_total"]),
                        "Déjà payé": format_ar(invoice["lodging_paid"]),
                        "Reste": format_ar(
                            max(
                                invoice["lodging_total"] - invoice["lodging_paid"],
                                0,
                            )
                        ),
                    }
                ],
                use_container_width=True,
                hide_index=True,
            )

            st.markdown("#### 🍹 Bar")
            if invoice["bar_items"]:
                st.dataframe(
                    [
                        {
                            "Date": item["sale_date"],
                            "Produit": item["product_name"],
                            "Qté": item["quantity"],
                            "Prix": format_ar(item["unit_price"]),
                            "Total": format_ar(item["total"]),
                            "Statut": "🟢 Payé" if item["paid"] else "🟠 Sur la chambre",
                        }
                        for item in invoice["bar_items"]
                    ],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("Aucune consommation bar sur ce séjour.")

            st.markdown("#### ✨ Autres extras")
            if invoice["extras"]:
                st.dataframe(
                    [
                        {
                            "Date": item["service_date"],
                            "Extra": item["label"],
                            "Description": item["description"] or "-",
                            "Montant": format_ar(item["amount"]),
                            "Statut": "🟢 Payé" if item["paid"] else "🟠 À régler",
                        }
                        for item in invoice["extras"]
                    ],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("Aucun extra ajouté.")

            if not r["invoice_closed"]:
                with st.expander("➕ Ajouter un extra à la facture"):
                    with st.form("invoice_extra_form", clear_on_submit=True):
                        extra_date = st.date_input(
                            "Date",
                            value=date.today(),
                            key="invoice_extra_date",
                        )
                        extra_label = st.selectbox(
                            "Type d’extra",
                            [
                                "Petit-déjeuner",
                                "Blanchisserie",
                                "Transfert / transport",
                                "Repas",
                                "Room service",
                                "Autre",
                            ],
                        )
                        extra_description = st.text_input(
                            "Description",
                            placeholder="Ex. Transfert aéroport",
                        )
                        extra_amount = st.number_input(
                            "Montant (Ar)",
                            min_value=0,
                            step=5000,
                        )
                        save_extra = st.form_submit_button(
                            "➕ Ajouter à la facture",
                            type="primary",
                            use_container_width=True,
                        )

                    if save_extra:
                        if extra_amount <= 0:
                            st.error("Le montant doit être supérieur à 0.")
                        else:
                            run(
                                """
                                INSERT INTO guest_extras(
                                    reservation_id,
                                    service_date,
                                    label,
                                    description,
                                    amount
                                )
                                VALUES (?, ?, ?, ?, ?)
                                """,
                                (
                                    r["id"],
                                    extra_date.isoformat(),
                                    extra_label,
                                    extra_description.strip(),
                                    int(extra_amount),
                                ),
                            )
                            st.success("✅ Extra ajouté à la facture.")
                            st.rerun()

                st.markdown("---")
                st.markdown("### ✅ Clôturer le séjour")

                if invoice["remaining"] > 0:
                    st.warning(
                        f'Reste à régler avant clôture : **{format_ar(invoice["remaining"])}**'
                    )
                    final_payment_method = st.selectbox(
                        "Mode de règlement final",
                        [
                            "Espèces",
                            "MVola",
                            "Orange Money",
                            "Airtel Money",
                            "Carte bancaire",
                            "Virement",
                        ],
                        key="invoice_final_payment",
                    )
                else:
                    st.success("La facture est entièrement réglée.")
                    final_payment_method = "Déjà réglé"

                confirm_close = st.checkbox(
                    "Je confirme la clôture du séjour et de la facture.",
                    key="invoice_close_confirm",
                )

                if st.button(
                    "🔒 Clôturer le séjour",
                    type="primary",
                    use_container_width=True,
                    disabled=not confirm_close,
                    key="invoice_close_button",
                ):
                    try:
                        closed_number = close_reservation_invoice(
                            r["id"],
                            final_payment_method,
                        )
                        st.success(
                            f"✅ Séjour clôturé. Facture {closed_number} finalisée."
                        )
                        st.rerun()
                    except ValueError as exc:
                        st.error(str(exc))
            else:
                st.success(
                    f'✅ Séjour clôturé — facture {r["invoice_number"] or invoice_number}'
                )

            st.markdown("---")
            st.markdown("#### 💳 Paiements hébergement")
            stay_payments = rows(
                """
                SELECT payment_date, amount, method
                FROM payments
                WHERE reservation_id = ?
                ORDER BY payment_date, id
                """,
                (r["id"],),
            )
            if stay_payments:
                st.dataframe(
                    [
                        {
                            "Date": item["payment_date"],
                            "Montant": format_ar(item["amount"]),
                            "Mode": item["method"],
                        }
                        for item in stay_payments
                    ],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("Aucun paiement hébergement enregistré.")


with tab_payments:
    st.subheader("💰 Enregistrer un paiement")
    payable = payable_reservations()

    if not payable:
        st.info("Aucun paiement en attente.")
    else:
        payment_labels = {
            (
                f'R{item["id"]:03d} — {item["client"]} — {item["room_name"]}'
                f' — reste {format_ar(item["remaining"])}'
            ): item
            for item in payable
        }
        payment_label = st.selectbox(
            "Réservation",
            list(payment_labels.keys()),
            key="payment_reservation",
        )
        selected = payment_labels[payment_label]

        st.info(f'Reste à payer : **{format_ar(selected["remaining"])}**')

        with st.form("new_payment", clear_on_submit=True):
            amount = st.number_input(
                "Montant encaissé (Ar)",
                min_value=0,
                max_value=int(selected["remaining"]),
                value=int(selected["remaining"]),
                step=5000,
            )
            method = st.selectbox(
                "Mode de paiement",
                [
                    "Espèces",
                    "MVola",
                    "Orange Money",
                    "Airtel Money",
                    "Carte bancaire",
                    "Virement",
                    "Autre",
                ],
            )
            payment_date = st.date_input(
                "Date du paiement",
                value=date.today(),
            )
            save_payment = st.form_submit_button(
                "💰 Enregistrer le paiement",
                type="primary",
                use_container_width=True,
            )

        if save_payment:
            if amount <= 0:
                st.error("Le montant doit être supérieur à 0.")
            else:
                run(
                    """
                    INSERT INTO payments(
                        reservation_id, payment_date, amount, method
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        selected["id"],
                        payment_date.isoformat(),
                        int(amount),
                        method,
                    ),
                )
                st.success("✅ Paiement enregistré.")
                st.rerun()

    st.markdown("---")
    st.subheader("📒 Historique des paiements")
    history = rows(
        """
        SELECT
            p.payment_date AS payment_date,
            p.reservation_id AS reservation_id,
            r.client AS client,
            p.amount AS amount,
            p.method AS method
        FROM payments p
        JOIN reservations r ON r.id = p.reservation_id
        ORDER BY p.payment_date DESC, p.id DESC
        """
    )

    display_history = [
        {
            "Date": item["payment_date"],
            "Réservation": f'R{item["reservation_id"]:03d}',
            "Client": item["client"],
            "Montant": format_ar(item["amount"]),
            "Mode": item["method"],
        }
        for item in history
    ]

    if display_history:
        st.dataframe(
            display_history,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Aucun paiement enregistré.")


with tab_expenses:
    st.subheader("🧾 Dépenses de l’établissement")

    with st.form("new_expense", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            expense_date = st.date_input(
                "Date",
                value=date.today(),
                key="expense_date",
            )
            category = st.selectbox(
                "Catégorie",
                [
                    "Personnel",
                    "Électricité / eau",
                    "Internet / téléphone",
                    "Entretien / ménage",
                    "Réparations",
                    "Fournitures",
                    "Achats",
                    "Transport",
                    "Taxes / frais",
                    "Autre",
                ],
            )
        with c2:
            expense_amount = st.number_input(
                "Montant (Ar)",
                min_value=0,
                step=5000,
            )
            expense_method = st.selectbox(
                "Mode de paiement",
                [
                    "Espèces",
                    "MVola",
                    "Orange Money",
                    "Airtel Money",
                    "Carte bancaire",
                    "Virement",
                    "Autre",
                ],
                key="expense_method",
            )

        expense_description = st.text_input(
            "Description",
            placeholder="Ex. Achat produits de ménage",
        )

        save_expense = st.form_submit_button(
            "➕ Enregistrer la dépense",
            type="primary",
            use_container_width=True,
        )

    if save_expense:
        if expense_amount <= 0:
            st.error("Le montant doit être supérieur à 0.")
        else:
            run(
                """
                INSERT INTO expenses(
                    expense_date, category, description, amount, payment_method
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    expense_date.isoformat(),
                    category,
                    expense_description.strip(),
                    int(expense_amount),
                    expense_method,
                ),
            )
            st.success("✅ Dépense enregistrée.")
            st.rerun()

    st.markdown("---")

    exp_day, exp_week, exp_month, exp_all = expense_totals()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Aujourd’hui", format_ar(exp_day))
    c2.metric("Cette semaine", format_ar(exp_week))
    c3.metric("Ce mois", format_ar(exp_month))
    c4.metric("Total", format_ar(exp_all))

    st.markdown("#### 📒 Historique des dépenses")
    expense_history = rows(
        """
        SELECT expense_date, category, description, amount, payment_method
        FROM expenses
        ORDER BY expense_date DESC, id DESC
        """
    )

    if expense_history:
        st.dataframe(
            [
                {
                    "Date": item["expense_date"],
                    "Catégorie": item["category"],
                    "Description": item["description"] or "-",
                    "Montant": format_ar(item["amount"]),
                    "Paiement": item["payment_method"],
                }
                for item in expense_history
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Aucune dépense enregistrée.")
