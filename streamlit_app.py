import sqlite3
from datetime import date, timedelta, datetime

import streamlit as st

DB_PATH = "gesthotel.db"

st.set_page_config(
    page_title="GestHotel Pro",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at 5% 5%, rgba(255, 77, 109, .18), transparent 28%),
                radial-gradient(circle at 95% 8%, rgba(0, 210, 255, .16), transparent 26%),
                radial-gradient(circle at 80% 92%, rgba(124, 58, 237, .16), transparent 28%);
        }

        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 3rem;
            max-width: 1500px;
        }

        .hero {
            padding: 24px 28px;
            border-radius: 24px;
            margin: 4px 0 18px 0;
            color: white;
            background: linear-gradient(120deg, #ff4d6d 0%, #7c3aed 48%, #00b4d8 100%);
            box-shadow: 0 18px 46px rgba(124, 58, 237, .24);
        }

        .hero h1 {
            margin: 0;
            font-size: 2.25rem;
            line-height: 1.05;
        }

        .hero p {
            margin: 8px 0 0 0;
            font-size: 1rem;
            opacity: .94;
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

        .product-card {
            min-height: 150px;
            border-radius: 22px;
            padding: 18px;
            margin-bottom: 12px;
            color: white;
            background: linear-gradient(145deg, #ff6b6b 0%, #f59e0b 45%, #7c3aed 100%);
            box-shadow: 0 12px 28px rgba(124,58,237,.18);
        }

        .product-card .emoji {font-size: 2.2rem;}
        .product-card .name {font-size: 1.15rem; font-weight: 850; margin-top: 5px;}
        .product-card .price {font-size: 1.05rem; font-weight: 800; margin-top: 8px;}
        .product-card .stock {font-size: .86rem; opacity: .92; margin-top: 4px;}

        .bar-banner {
            padding: 18px 22px;
            border-radius: 20px;
            margin: 4px 0 16px 0;
            color: white;
            background: linear-gradient(110deg, #06b6d4, #10b981, #f59e0b);
            box-shadow: 0 12px 30px rgba(6,182,212,.18);
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
            background: linear-gradient(90deg, #ff4d6d, #7c3aed, #00b4d8);
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
                maintenance INTEGER NOT NULL DEFAULT 0
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

        if con.execute("SELECT COUNT(*) FROM bar_products").fetchone()[0] == 0:
            con.executemany(
                """
                INSERT INTO bar_products(name, category, emoji, price, stock)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    ("Coca-Cola 50 cl", "Sodas", "🥤", 6000, 24),
                    ("Limonade 50 cl", "Sodas", "🍋", 5000, 18),
                    ("Eau minérale 1 L", "Eaux", "💧", 3000, 30),
                    ("Bière 65 cl", "Bières", "🍺", 8000, 20),
                    ("Jus naturel mangue", "Jus naturels", "🥭", 7000, 12),
                    ("Jus naturel ananas", "Jus naturels", "🍍", 7000, 12),
                ],
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


def room_view():
    data = []
    for room in rows("SELECT * FROM rooms ORDER BY name"):
        data.append(
            {
                "Chambre": room["name"],
                "Tarif / nuit": format_ar(room["nightly_rate"]),
                "Statut": room_status(room["id"], room["maintenance"]),
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


init_db()

if "bar_cart" not in st.session_state:
    st.session_state.bar_cart = []

st.markdown(
    """
    <div class="hero">
        <h1>🏨 GestHotel Pro</h1>
        <p>Réservations • chambres • clients • check-in / check-out • bar • paiements • dépenses</p>
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
                        st.success("✅ Check-out enregistré.")
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
            <h2 style="margin:0;color:white;-webkit-text-fill-color:white;">🍹 Le Bar de GestHotel</h2>
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

    st.markdown("### 🥤 Carte des boissons")
    products = rows(
        """
        SELECT id, name, category, emoji, price, stock
        FROM bar_products
        WHERE active = 1
        ORDER BY category, name
        """
    )

    product_columns = st.columns(3)
    for index, product in enumerate(products):
        with product_columns[index % 3]:
            stock_text = (
                "🔴 Stock faible"
                if int(product["stock"]) <= 5
                else f'📦 Stock : {product["stock"]}'
            )
            st.markdown(
                f"""
                <div class="product-card">
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
        product for product in products if int(product["stock"]) > 0
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
