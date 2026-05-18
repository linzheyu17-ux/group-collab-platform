from datetime import date, timedelta


# ----------------
# 討論時間安排
# ----------------

st.divider()
st.subheader("🗓️ 討論時間安排")

slots = half_hour_slots()

start_day = st.date_input("起始日期", value=date.today())

days = [start_day + timedelta(days=i) for i in range(5)]


selected_member = st.selectbox(
    "選擇填寫成員",
    members,
    format_func=lambda x: x["nickname"] or x["name"],
)


selected_slots = []

for d in days:
    st.markdown(f"### {d.strftime('%m/%d')}")

    cols = st.columns(4)

    for idx, slot in enumerate(slots):
        slot_key = f"{d.isoformat()} {slot}"

        checked = cols[idx % 4].checkbox(
            slot,
            key=f"{selected_member['id']}_{slot_key}",
        )

        if checked:
            selected_slots.append(slot_key)


if st.button("💾 儲存時間"):
    save_availability(selected_member["id"], selected_slots)

    st.success("時間已儲存")


# ----------------
# 合作規範系統
# ----------------

st.divider()
st.subheader("⚖️ 合作規範")

with st.form("norm_form"):
    norm_text = st.text_area(
        "匿名合作規範",
        placeholder="例如：訊息應於 12 小時內回覆",
    )

    norm_submit = st.form_submit_button("送出")

    if norm_submit:
        if norm_text.strip():
            add_norm(current_room, norm_text)
            st.success("規範已送出")
            st.rerun()


norms = get_norms(current_room)

for norm in norms:
    st.container(border=True)
    st.write(norm["content"])