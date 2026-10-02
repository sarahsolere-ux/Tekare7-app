import sqlite3
from datetime import date, timedelta

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

        if con.execute("SELECT COUNT(*) FROM rooms").fetchone()[0] == 0:
            con.executemany(
                "INSERT INTO rooms(name, nightly_rate) VALUES (?, ?)",
                [
                    ("Chambre 101", 150000),
                    ("Chambre 102", 120000),
                    ("Chambre 103", 180000),
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


init_db()

st.markdown(
    """
    <div class="hero">
        <h1>🏨 GestHotel Pro</h1>
        <p>Réservations • chambres • clients • check-in / check-out • paiements • dépenses</p>
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
    tab_payments,
    tab_expenses,
) = st.tabs(
    [
        "📊 Tableau de bord",
        "🛏️ Chambres",
        "📅 Réservations",
        "🗓️ Planning",
        "👥 Clients",
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
        SELECT r.id, r.client, r.arrival, r.departure, r.checked_in, r.checked_out,
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
