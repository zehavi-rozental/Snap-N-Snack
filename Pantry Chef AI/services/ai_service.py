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

            # שימוש בנתיב המדויק למודל 2.5 כפי שהופיע בניסוי שהצליח
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

            headers = {'Content-Type': 'application/json'}

            # בניית הפרומפט למקרה משולב
            prompt_text = f"""
            מצא מתכון מתאים מהטקסט הבא:
            ---
            {recipes_context[:8000]}
            ---
            מצרכים שהמשתמש ציין בטקסט: {ingredients if ingredients else "לא צוינו"}
            {", ומצורפת תמונה של מצרכים נוספים - זהה אותם ושלב הכל יחד." if image_data else ""}

            החזר אך ורק JSON תקין בעברית:
            {{
                "title": "שם המנה",
                "ingredients": [".."],
                "instructions": [".."],
                "source": "שם הקובץ"
            }}
            """

            # בניית רשימת ה-Parts (טקסט ותמונה)
            parts = [{"text": prompt_text}]

            if image_data:
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_base64
                    }
                })

            payload = {"contents": [{"parts": parts}]}

            # עקיפת SSL עבור נטפרי
            response = requests.post(url, headers=headers, json=payload, verify=False)

            if response.status_code == 200:
                result_json = response.json()
                text_response = result_json['candidates'][0]['content']['parts'][0]['text']

                # חילוץ ה-JSON מתוך הטקסט
                match = re.search(r'\{.*\}', text_response, re.DOTALL)
                if match:
                    return json.loads(match.group())
                return {"error": "הצלחנו להתחבר, אבל התשובה לא הייתה בפורמט JSON תקין"}
            else:
                return {"error": f"Status {response.status_code}: {response.text}"}

        except Exception as e:
            return {"error": str(e)}