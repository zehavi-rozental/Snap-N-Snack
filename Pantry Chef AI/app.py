import streamlit as st
from services.file_service import FileService
from services.ai_service import AIService

st.set_page_config(page_title="Snap-N-Snack", layout="centered")

st.markdown("<h1 style='text-align: center;'>🍳 Snap-N-Snack</h1>", unsafe_allow_html=True)
st.write("---")

context = FileService.get_all_recipes_text()

# יצירת הקלט - טקסט ותמונה זמינים תמיד במקביל
st.subheader("מה נבשל היום?")
ingredients_input = st.text_area("הקלידי מצרכים (אופציונלי):", placeholder="למשל: שוקולד, קמח...")

col1, col2 = st.columns(2)
with col1:
    camera_photo = st.camera_input("📸 צילום מצרכים")
with col2:
    # כאן היה התיקון: file_uploader במקום file_upload
    uploaded_photo = st.file_uploader("🖼️ העלאת תמונה מהגלריה", type=["jpg", "jpeg", "png"])

# איסוף נתוני התמונה
image_bytes = None
if camera_photo:
    image_bytes = camera_photo.getvalue()
elif uploaded_photo:
    image_bytes = uploaded_photo.getvalue()

if st.button("מצא לי מתכון! 🔍"):
    if not ingredients_input and not image_bytes:
        st.warning("בבקשה תני לי כיוון - טקסט או תמונה (או שניהם!)")
    else:
        with st.status("השף משלב בין המצרכים לחוברת המתכונים...") as status:
            # שליחה משולבת ל-AI
            result = AIService.find_match(ingredients_input, context, image_bytes)

            if result and "error" not in result:
                status.update(label="מצאתי שילוב מנצח!", state="complete")
                st.balloons()

                st.markdown(f"## {result['title']}")
                st.caption(f"📍 מקור: {result['source']}")

                c1, c2 = st.columns(2)
                with c1:
                    st.subheader("🛒 מצרכים")
                    for ing in result['ingredients']:
                        st.write(f"- {ing}")
                with c2:
                    st.subheader("👨‍🍳 הוראות הכנה")
                    for idx, step in enumerate(result['instructions'], 1):
                        st.write(f"{idx}. {step}")
            else:
                status.update(label="משהו השתבש", state="error")
                st.error(f"שגיאה: {result.get('error') if result else 'תקשורת נכשלה'}")