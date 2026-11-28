"""Giao diện Streamlit cho bản chạy thử Class Pulse."""
import streamlit as st

from ui_service import display_lesson_names, generate_card

st.set_page_config(page_title="Class Pulse", page_icon="✦", layout="wide")

st.markdown("""
<style>
    .block-container { max-width: 1440px; padding-top: 6rem; padding-bottom: 3rem; }
    h1, h2, h3 { letter-spacing: -0.025em; }
    .brand { font-size: 1rem; font-weight: 800; letter-spacing: 0.12em; }
    .eyebrow { font-size: 0.9rem; font-weight: 700; letter-spacing: 0.08em; }
    .subtle { opacity: 0.8; font-size: 1rem; line-height: 1.6; }
    .draft { display: inline-block; border: 1px solid currentColor;
             border-radius: 20px; padding: 0.3rem 0.8rem; font-size: 0.9rem; font-weight: 700; }
    div[data-testid="stVerticalBlockBorderWrapper"] > div { border-radius: 16px; }
    div.stButton > button, div.stFormSubmitButton > button { border-radius: 10px; min-height: 2.8rem; }
</style>
""", unsafe_allow_html=True)


def display_card(output):
    output = display_lesson_names(output)
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("THẺ ĐIỂM NGHẼN"):
            st.subheader(line)
        elif line.startswith(("A. ", "B. ", "C. ", "D. ")):
            st.markdown("#### " + line)
        elif line.startswith(("Lưu ý:", "(Đã bỏ")):
            st.warning(line)
        elif line.startswith("Giới hạn:"):
            st.info(line)
        elif line.startswith("["):
            st.markdown("**" + line.replace("*", "\\*") + "**")
        else:
            st.write(line)


st.markdown('<span class="brand">✦ CLASS PULSE</span>', unsafe_allow_html=True)
st.markdown('<p class="subtle">Không gian chuẩn bị bài dành cho giảng viên</p>', unsafe_allow_html=True)
st.divider()

left, right = st.columns([0.9, 1.6], gap="large")
with left:
    st.markdown('<p class="eyebrow">NẮM BẮT NHỊP LỚP</p>', unsafe_allow_html=True)
    st.title("Lớp mình đang vướng ở đâu?")
    st.markdown("Nhìn nhanh tín hiệu pre-class để chuẩn bị cho buổi học tiếp theo.")
    with st.form("question_form"):
        question = st.text_area("Câu hỏi của bạn", key="question", height=120,
                                placeholder="Ví dụ: Ngày 5 lớp vướng gì?")
        submitted = st.form_submit_button("Tạo thẻ điểm nghẽn", type="primary", use_container_width=True)
    st.caption("Dữ liệu tổng hợp · Không xếp hạng học viên")
    st.caption("Gợi ý là bản nháp; giảng viên duyệt trước khi sử dụng.")

if submitted:
    if not question.strip():
        st.session_state.card_error = "Hãy nhập ngày học hoặc mã câu ôn."
    else:
        # Không giữ kết quả cũ dưới lỗi của lượt mới.
        st.session_state.card = None
        st.session_state.card_error = None
        with st.spinner("Đang tổng hợp dữ liệu và chờ AI. Việc này có thể mất một lúc…"):
            try:
                st.session_state.card = generate_card(question.strip())
            except Exception as exc:
                st.session_state.card_error = "Không tạo được thẻ: %s" % exc

with right:
    with st.container(border=True):
        st.markdown('<p class="eyebrow">BẢNG TỔNG HỢP</p>', unsafe_allow_html=True)
        st.header("Thẻ điểm nghẽn")
        st.markdown('<span class="draft">BẢN NHÁP · GIẢNG VIÊN DUYỆT</span>', unsafe_allow_html=True)
        st.divider()
        if st.session_state.get("card_error"):
            st.error(st.session_state.card_error)
            st.caption("Nếu gặp HTTP 429 hoặc 503, hãy chờ rồi thử lại hoặc kiểm tra hạn mức API.")
        elif st.session_state.get("card"):
            output, summary = st.session_state.card
            display_card(output)
            st.divider()
            models = ", ".join(summary["models"]) or "không gọi model"
            st.caption("Model: %s · Token vào: %d · Token ra: %d" %
                       (models, summary["tokens_in"], summary["tokens_out"]))
        else:
            st.subheader("Một góc nhìn rõ hơn về lớp học")
            st.write("Nhập ngày học hoặc mã câu ôn để tạo thẻ tổng hợp.")
            st.markdown("""
**Tín hiệu từ dữ liệu**  
Xem câu ôn cần chú ý và các phần bài có dấu hiệu vướng.

**Gợi ý từ AI**  
Nhận gợi ý chuẩn bị bài, kèm giới hạn của dữ liệu.

**Giảng viên quyết định**  
Mọi nội dung đều là bản nháp, không tự gửi cho học viên.
""")
