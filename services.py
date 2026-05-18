from uuid import uuid4

from database import get_conn


# ----------------
# 房間系統
# ----------------


def create_room(room_name):
    token = uuid4().hex[:8]

    with get_conn() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT OR IGNORE INTO rooms(room_name, room_token) VALUES (?, ?)",
            (room_name, token),
        )


    return token



def get_room(room_name):
    with get_conn() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM rooms WHERE room_name = ?",
            (room_name,),
        )

        return cursor.fetchone()



# ----------------
# 成員系統
# ----------------


def add_member(room_name, name, nickname):
    member_id = uuid4().hex

    with get_conn() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO members(id, room_name, name, nickname)
            VALUES (?, ?, ?, ?)
            """,
            (member_id, room_name, name, nickname),
        )

    return member_id




def get_members(room_name):
    with get_conn() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM members WHERE room_name = ?",
            (room_name,),
        )

        return cursor.fetchall()


# ----------------
# 時間系統
# ----------------


def save_availability(member_id, slots):
    with get_conn() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM availability WHERE member_id = ?",
            (member_id,),
        )

        for slot in slots:
            cursor.execute(
                "INSERT INTO availability(member_id, slot) VALUES (?, ?)",
                (member_id, slot),
            )




def get_availability(member_id):
    with get_conn() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT slot FROM availability WHERE member_id = ?",
            (member_id,),
        )

        return [row["slot"] for row in cursor.fetchall()]


# ----------------
# 規範系統
# ----------------


def add_norm(room_name, content):
    norm_id = uuid4().hex

    with get_conn() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO norms(id, room_name, content)
            VALUES (?, ?, ?)
            """,
            (norm_id, room_name, content),
        )




def get_norms(room_name):
    with get_conn() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM norms WHERE room_name = ?",
            (room_name,),
        )

        return cursor.fetchall()