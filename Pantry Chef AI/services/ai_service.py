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

            # פרומפט משופר שמתמקד בזיהוי ויזואלי עוצמתי
            prompt_text = f"""
            תפקיד: שף מומחה לזיהוי מצרכים מתמונות.

            הוראות עבודה:
            1. ניתוח תמונה: אם צורפה תמונה, זהה את כל המצרכים שבה ברמת דיוק גבוהה (למשל: "שוקולד מריר", "חמאה", "ריבת חלב").
            2. הצלבה עם החוברת: חפש בטקסט החוברת מטה מתכון שמשתמש במצרכים שזיהית בתמונה (או במצרכים שנכתבו בטקסט).
            3. עדיפות: אם זיהית שוקולד בתמונה, תן עדיפות למתכוני שוקולד מהחוברת.

            טקסט החוברת:
            ---
            {recipes_context[:12000]}
            ---

            מצרכים בטקסט (אם יש): {ingredients if ingredients else "הסתמך על התמונה בלבד"}

            החזר אך ורק JSON תקין בעברית:
            {{
                "title": "שם המנה המדויק מהחוברת",
                "ingredients": ["רשימת המצרכים מהמתכון בחוברת"],
                "instructions": ["הוראות ההכנה מהחוברת"],
                "source": "שם קובץ המקור"
            }}

            אם לא מצאת שום מתכון שמתאים למצרכים שבתמונה, החזר JSON עם title: "לא נמצאה התאמה".
            """

            parts = [{"text": prompt_text}]

            if image_data:
                # שימוש ב-mime_type גמיש (תומך ב-JPG ו-PNG)
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_base64
                    }
                })

            payload = {"contents": [{"parts": parts}]}

            # verify=False לטובת משתמשי נטפרי
            response = requests.post(url, headers=headers, json=payload, verify=False, timeout=30)

            if response.status_code == 200:
                result_json = response.json()
                text_response = result_json['candidates'][0]['content']['parts'][0]['text']
                match = re.search(r'\{.*\}', text_response, re.DOTALL)
                if match:
                    return json.loads(match.group())
                return {"error": "הצלחנו להתחבר, אך התשובה לא במבנה הנכון"}
            elif response.status_code == 429:
                return {"error": "חרגת ממכסת הבקשות של Gemini 2.5 (20 ליום). נסי שוב בעוד דקה."}
            else:
                return {"error": f"שגיאה {response.status_code}: {response.text}"}

        except Exception as e:
            return {"error": str(e)}