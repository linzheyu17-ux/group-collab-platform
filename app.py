from datetime import date, timedelta
import streamlit as st
from database import init_db
from services import create_room, get_room, add_member, get_members, save_availability, get_availability, add_norm, get_norms
from utils import half_hour_slots

st.set_page_config(
    page_title="小組協作平台",
    page_icon="🤝",
    layout="wide"
)

init_db()


st.title("🤝 小組協作平台")
st.caption("多人同步討論時間安排與合作規範系統")


# ----------------
# 房間系統
# ----------------

st.sidebar.header("🚪 房間系統")

room_name = st.sidebar.text_input("房間名稱")

if st.sidebar.button("建立 / 進入房間"):
    if room_name:
        room = get_room(room_name)

        if room is None:
            token = create_room(room_name)
            st.sidebar.success(f"建立成功 Token: {token}")

        st.session_state.room_name = room_name



if "room_name" not in st.session_state:
    st.info("請先建立或加入房間")
    st.stop()


current_room = st.session_state.room_name

st.success(f"目前房間：{current_room}")



# ----------------
# 成員系統
# ----------------

st.subheader("👤 成員加入")

with st.form("member_form"):
    name = st.text_input("姓名")
    nickname = st.text_input("暱稱")

    submitted = st.form_submit_button("加入")

    if submitted:
        if name:
            add_member(current_room, name, nickname)
            st.success("加入成功")
            st.rerun()



members = get_members(current_room)

st.write(f"目前成員數：{len(members)}")

for member in members:
    display_name = member["nickname"] or member["name"]
    st.write(f"👤 {display_name}")



# ----------------
# 討論時間安排
# ----------------

st.divider()
st.subheader("🗓️ 討論時間安排")

slots = half_hour_slots()

start_day = st.date_input("起始日期", value=date.today())

days = [start_day + timedelta(days=i) for i in range(5)]

# 💡 1. 確保 members 是一個標準的 Python dict 列表，排除 sqlite3.Row 或特殊物件的干擾
clean_members = []
for m in members:
    if m is not None:
        # 如果 m 本身就是 dict，轉成標準 dict；如果是 sqlite3.Row，dict(m) 可以完美轉換
        clean_members.append(dict(m))

# 💡 2. 在 selectbox 中使用轉換後的 clean_members
if clean_members:
    selected_member = st.selectbox(
        "選擇填寫成員",
        clean_members,
        format_func=lambda x: x.get("nickname") or x.get("name") or "未命名成員",
    )
else:
    st.warning("目前沒有成員資料。")
    selected_member = None

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
