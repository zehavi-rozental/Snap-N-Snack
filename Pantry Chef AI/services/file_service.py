import os


class FileService:
    @staticmethod
    def get_all_recipes_text():
        # שימוש בשם התיקייה כפי שמופיע אצלך בפרויקט
        recipes_path = os.path.join(os.getcwd(), "recipes")

        if not os.path.exists(recipes_path):
            return "שגיאה: תיקיית recipes לא נמצאה."

        combined_text = ""
        for filename in os.listdir(recipes_path):
            if filename.endswith(".txt"):
                try:
                    with open(os.path.join(recipes_path, filename), "r", encoding="utf-8") as f:
                        combined_text += f"\n--- מקור: {filename} ---\n{f.read()}\n"
                except:
                    continue
        return combined_text