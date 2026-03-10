import streamlit as st
from PIL import Image
import io
from services.file_service import FileService
from services.ai_service import AIService

st.set_page_config(page_title="Snap-N-Snack", layout="centered")


def compress_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    img = img.convert("RGB")
    img.thumbnail((800, 800))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return buf.getvalue()


st.markdown("<h1 style='text-align: center;'>🍳 Snap-N-Snack</h1>", unsafe_allow_html=True)
st.write("---")

context = FileService.get_all_recipes_text()

st.subheader("מה נבשל היום?")
ingredients_input = st.text_area("הקלידי מצרכים (אופציונלי):", placeholder="למשל: תפוחים, קמח...")

col1, col2 = st.columns(2)
with col1:
    camera_photo = st.camera_input("📸 צילום מצרכים")
with col2:
    uploaded_photo = st.file_uploader("🖼️ העלאת תמונה", type=["jpg", "jpeg", "png"])

image_bytes = None
if camera_photo:
    image_bytes = camera_photo.getvalue()
elif uploaded_photo:
    image_bytes = uploaded_photo.getvalue()

if st.button("מצא לי מתכון! 🔍"):
    if not ingredients_input and not image_bytes:
        st.warning("תני לי כיוון - טקסט או תמונה")
    else:
        if image_bytes:
            image_bytes = compress_image(image_bytes)

        with st.status("השף בודק בחוברת...") as status:
            result = AIService.find_match(ingredients_input, context, image_bytes)

            if result and "error" not in result:
                if result.get("is_found"):
                    status.update(label="מצאתי שילוב מנצח!", state="complete")
                    st.balloons()
                    st.success(f"זיהיתי בתמונה: {', '.join(result.get('identified_ingredients', []))}")
                    st.markdown(f"## {result['title']}")
                    st.caption(f"📍 מקור: {result['source']}")

                    c1, c2 = st.columns(2)
                    with c1:
                        st.subheader("🛒 מצרכים")
                        for ing in result['ingredients']: st.write(f"- {ing}")
                    with c2:
                        st.subheader("👨‍🍳 הוראות הכנה")
                        for idx, step in enumerate(result['instructions'], 1): st.write(f"{idx}. {step}")
                else:
                    status.update(label="לא נמצא מתכון בחוברת", state="error")
                    st.warning("זיהיתי את המצרכים, אבל הם לא מופיעים בחוברת שלך.")
                    if result.get("identified_ingredients"):
                        st.info(f"ראיתי בתמונה: {', '.join(result['identified_ingredients'])}")
            else:
                status.update(label="שגיאה בתקשורת", state="error")
                st.error(f"שגיאה: {result.get('error') if result else 'תקשורת נכשלה'}")