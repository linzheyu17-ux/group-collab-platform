from datetime import date, timedelta
import streamlit as st

# 1. 補上模擬的函數與資料（實際開發時請替換為你的資料庫邏輯）
def half_hour_slots():
    """生成時間區段範例"""
    return ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00"]

# 模擬成員資料
members = [
    {"id": 1, "name": "張小明", "nickname": "小明"},
    {"id": 2, "name": "李小華", "nickname": None},
    {"id": 3, "name": "王大同", "nickname": "大同"},
]

current_room = "room_123" # 模擬當前房間 ID

# 模擬資料庫儲存與讀取
def save_availability(member_id, slots):
    st.info(f"模擬儲存：成員 {member_id} 選擇了 {len(slots)} 個時段")

def add_norm(room_id, text):
    if "mock_norms" not in st.session_state:
        st.session_state.mock_norms = []
    st.session_state.mock_norms.append({"content": text})

def get_norms(room_id):
    if "mock_norms" not in st.session_state:
        st.session_state.mock_norms = [{"content": "預設規範：請保持禮貌"}]
    return st.session_state.mock_norms


# ---------------------------------------------------------
# 以下為你原本的程式碼（部分細節因應邏輯與排版有微調）
# ---------------------------------------------------------

# ----------------
# 討論時間安排
# ----------------
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
        
        # 使用 cols[idx % 4] 來分配格子
        with cols[idx % 4]:
            checked = st.checkbox(
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

# 顯示規範
norms = get_norms(current_room)
for norm in norms:
    # 修正原本 st.container(border=True) 內沒有寫入內容的問題
    with st.container(border=True):
        st.write(norm["content"])