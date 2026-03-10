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
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            headers = {'Content-Type': 'application/json'}

            # פרומפט שדורש זיהוי מלא ודיוק מקסימלי
            prompt_text = f"""
            אתה שף מנתח תמונות. בצע את השלבים הבאים בסדר הזה:

            1. זיהוי ויזואלי מלא: זהה את כל המצרכים בתמונה בפירוט (למשל: עגבניות במדף, פלפל ירוק, ביצים, בירה, יוגורט). אל תתעלם מירקות!
            2. סריקת חוברת: עבור על טקסט החוברת המצורף כאן:
            ---
            {recipes_context[:15000]}
            ---
            3. התאמה: האם יש בחוברת מתכון שמשתמש במצרכים שזיהית? 
            - אם כן: החזר את פרטי המתכון.
            - אם לא: החזר false בשדה is_found.

            חשוב: אל תמציא קשרים. אם ראית עגבניות ואין מתכון עגבניות, רשום שראית עגבניות אבל אל תציע מתכון לא קשור.

            החזר JSON בלבד בעברית:
            {{
                "is_found": true/false,
                "identified_ingredients": ["רשימת כל מה שראית בתמונה בפירוט"],
                "title": "שם המתכון מהחוברת",
                "ingredients": ["מצרכים"],
                "instructions": ["הוראות"],
                "source": "שם הקובץ"
            }}
            """

            parts = [{"text": prompt_text}]
            if image_data:
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                parts.append({"inline_data": {"mime_type": "image/jpeg", "data": image_base64}})

            payload = {"contents": [{"parts": parts}]}
            # verify=False עוזר לעקוף בעיות חיבור בנטפרי/סינון
            response = requests.post(url, headers=headers, json=payload, verify=False, timeout=30)

            if response.status_code == 200:
                text_response = response.json()['candidates'][0]['content']['parts'][0]['text']
                match = re.search(r'\{.*\}', text_response, re.DOTALL)
                if match:
                    return json.loads(match.group())
                return {"error": "Format error"}
            return {"error": f"Status {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}