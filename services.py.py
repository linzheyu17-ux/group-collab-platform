from uuid import uuid4
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