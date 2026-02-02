import json
from pathlib import Path
from typing import List, Dict, Optional, Any


class FormManager:
    FILE_PATH = Path("survey.json")  # файл, где хранится анкета
    def __init__(self):
        self.data: Dict[str, Any] = self._load()
        self._next_id = self._get_next_id()

    def _refresh(self):
        self.data = self._load()
        self._next_id = self._get_next_id()

    def _load(self) -> Dict[str, Any]:
        """Загружает данные из JSON-файла или возвращает пустую структуру"""
        if not self.FILE_PATH.exists() or self.FILE_PATH.stat().st_size == 0:
            return {"questions": []}
        try:
            with self.FILE_PATH.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict) or "questions" not in data:
                    return {"questions": []}
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка чтения survey.json: {e}. Создаём пустую анкету.")
            return {"questions": []}

    def _save(self) -> None:
        try:
            with self.FILE_PATH.open("w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка записи в survey.json: {e}")

    def _get_next_id(self) -> int:
        if not self.data["questions"]:
            return 1
        max_id = max(q["id"] for q in self.data["questions"])
        return max_id + 1

    def create(self) -> None:
        if self.FILE_PATH.exists():
            return
        self.data = {"questions": []}
        self._save()

    def add_question(self, text: str, question_type: str = "text") -> int:
        new_question = {
            "id": self._next_id,
            "text": text.strip(),
            "type": question_type.strip()
        }
        self.data["questions"].append(new_question)
        self._next_id += 1
        self._save()
        return new_question["id"]

    def get_question_by_id(self, question_id: int) -> Optional[Dict[str, Any]]:
        self._refresh()
        for q in self.data["questions"]:
            if q["id"] == question_id:
                return q
        return None

    def edit_question(self, question_id: int, new_text: Optional[str] = None, new_type: Optional[str] = None) -> bool:
        self._refresh()
        question = self.get_question_by_id(question_id)
        if not question:
            print(f"Вопрос с id {question_id} не найден.")
            return False
        if new_text is not None:
            question["text"] = new_text.strip()
        if new_type is not None:
            question["type"] = new_type.strip()
        self._save()
        return True

    def delete_question(self, question_id: int) -> bool:
        self._refresh()
        original_count = len(self.data["questions"])
        self.data["questions"] = [q for q in self.data["questions"] if q["id"] != question_id]
        if len(self.data["questions"]) == original_count:
            return False
        for i, question in enumerate(self.data["questions"], start=1):
            question["id"] = i
        self._next_id = len(self.data["questions"]) + 1 if self.data["questions"] else 1
        self._save()
        return True

    def get_form_for_admin(self) -> str:
        self._refresh()
        if not self.data.get('questions'):
            return "Анкета пуста"
        lines = [f"#{q['id']} {q['text']} ({q['type']})" for q in self.data['questions']]
        return '\n'.join(lines)

    def clear(self) -> None:
        self.data["questions"] = []
        self._next_id = 1
        self._save()


    def __len__(self) -> int:
        return len(self.data['questions'])



