import streamlit as st
import json
import requests
import re
import base64


class AIService:
    @staticmethod
    def find_match(ingredients, recipes_context, image_data=None):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            # שימוש במודל 2.5 Flash כפי שביקשת
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

            headers = {'Content-Type': 'application/json'}

            # פרומפט "חריף" לזיהוי תמונה בלבד וסריקה עמוקה של החוברת
            prompt_text = f"""
            משימה: מצא מתכון שוקולד מהחוברת על סמך ראייה בלבד!

            1. ניתוח ויזואלי: זהה כל פריט בתמונה. אם זה שוקולד מריר של ורד הגליל (או כל מותג אחר), שים לב לזה!
            2. סריקה טקסטואלית: עבור על כל חוברת המתכונים מטה. אל תפספס אף מתכון שמכיל את המצרכים שזיהית.
            3. התאמה: אם זיהית שוקולד בתמונה, חובה למצוא מתכון שוקולד מהחוברת.

            טקסט החוברת:
            ---
            {recipes_context[:15000]}
            ---

            מצרכים נוספים מהמשתמש: {ingredients if ingredients else "הסתמך על התמונה בלבד"}

            החזר JSON בלבד (בעברית):
            {{
                "identified_ingredients": ["רשימת המצרכים שזיהית בתמונה"],
                "title": "שם המתכון המדויק מהחוברת",
                "ingredients": ["מצרכים"],
                "instructions": ["הוראות"],
                "source": "שם הקובץ"
            }}

            אם לא נמצאה התאמה, החזר: {{"title": "לא נמצאה התאמה", "identified_ingredients": ["מה שראית"]}}
            """

            parts = [{"text": prompt_text}]
            if image_data:
                # הפיכת התמונה ל-Base64
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                parts.append({
                    "inline_data": {
                        "mime_type": "image/png",
                        "data": image_base64
                    }
                })

            payload = {"contents": [{"parts": parts}]}

            # שליחת הבקשה עם timeout וביטול אימות SSL לנטפרי
            response = requests.post(url, headers=headers, json=payload, verify=False, timeout=30)

            if response.status_code == 200:
                result_json = response.json()
                text_response = result_json['candidates'][0]['content']['parts'][0]['text']
                match = re.search(r'\{.*\}', text_response, re.DOTALL)
                if match:
                    return json.loads(match.group())
                return {"error": "התשובה לא חזרה בפורמט JSON"}
            elif response.status_code == 429:
                return {"error": "Quota Exceeded: הגעת למכסה היומית (20 בקשות). נסי שוב מחר ב-10:00 או החליפי פרויקט."}
            else:
                return {"error": f"Status {response.status_code}: {response.text}"}

        except Exception as e:
            return {"error": str(e)}