# 🍳 Pantry Chef AI

אפליקציית Streamlit חכמה שמזהה מצרכים מתמונה או טקסט ומציעה מתכונים מתוך חוברות PDF של מתכונים קיימים.

## תכונות

- **זיהוי מצרכים**: העלה תמונה או הזן טקסט עם רשימת מצרכים.
- **חיפוש מתכונים**: מצא מתכונים מתאימים מתוך חוברות PDF שהעלית.
- **ממשק בעברית**: ממשק משתמש נקי וידידותי בעברית.
- **שימוש ב-Gemini AI**: לזיהוי מצרכים וחיפוש מתכונים מדויק.

## התקנה

1. שכפל את הריפו:
   ```bash
   git clone https://github.com/yourusername/pantry-chef-ai.git
   cd pantry-chef-ai
   ```

2. התקן את התלויות:
   ```bash
   pip install -r requirements.txt
   ```

3. הוסף את המפתח שלך ל-`.streamlit/secrets.toml`:
   ```
   GEMINI_API_KEY = "your_api_key_here"
   ```

4. הצב את חוברות ה-PDF בתיקיית `cookbooks/`.

## שימוש

הרץ את האפליקציה:
```bash
streamlit run app.py
```

- **טאב צילום מצלמה**: צלם תמונה של המצרכים.
- **טאב הזנת טקסט**: הזן רשימת מצרכים.

האפליקציה תזהה את המצרכים ותציע מתכונים מתאימים מהחוברות.

## מבנה הפרויקט

```
pantry-chef-ai/
├── app.py                 # האפליקציה הראשית
├── requirements.txt       # תלויות Python
├── .streamlit/
│   └── secrets.toml       # מפתחות סודיים
├── services/
│   ├── ai_service.py      # שירות AI לזיהוי וחיפוש
│   └── pdf_service.py     # שירות לטעינת וניתוח PDFs
├── cookbooks/             # תיקייה לחוברות PDF
├── .gitignore             # קבצים להתעלמות
└── README.md              # קובץ זה
```

## דרישות

- Python 3.8+
- מפתח API מ-Google AI Studio (Gemini)

## תרומה

תרומות מוזמנות! אנא פתח issue או pull request.

## רישיון

MIT License
