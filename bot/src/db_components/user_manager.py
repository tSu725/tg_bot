import json
from pathlib import Path
from typing import Dict, Any, Optional


class UserManager:
    FILE_PATH = Path("users.json")

    def __init__(self):
        self.data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        """Загружает данные из файла или возвращает пустую структуру"""
        if not self.FILE_PATH.exists() or self.FILE_PATH.stat().st_size == 0:
            return {"users": []}

        try:
            with self.FILE_PATH.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict) or "users" not in data:
                    return {"users": []}
                return data
        except (json.JSONDecodeError, IOError):
            print("Ошибка чтения users.json, создаём пустую структуру")
            return {"users": []}

    def _save(self) -> None:
        """Сохраняет данные в файл"""
        try:
            with self.FILE_PATH.open("w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка записи в users.json: {e}")

    def get_user_index(self, user_id: int) -> Optional[int]:
        """Возвращает индекс пользователя в списке или None"""
        for i, user in enumerate(self.data["users"]):
            if user["id"] == user_id:
                return i
        return None

    def add_user(self, user_id: int) -> None:
        """Добавляет нового пользователя, если его ещё нет"""
        if self.get_user_index(user_id) is not None:
            return  # уже существует

        self.data["users"].append({
            "id": user_id,
            "answers": {}
        })
        self._save()

    def add_answer(self, user_id: int, question_id: int | str, answer: str) -> bool:
        """
        Добавляет/обновляет ответ пользователя на вопрос.
        Возвращает True если успешно, False если пользователя нет.
        """
        idx = self.get_user_index(user_id)
        if idx is None:
            return False

        # question_id приводим к строке, т.к. в JSON ключи — строки
        qid = str(question_id)
        self.data["users"][idx]["answers"][qid] = answer
        self._save()
        return True

    def get_answers(self, user_id: int) -> Optional[Dict[str, str]]:
        """Возвращает словарь ответов пользователя или None"""
        idx = self.get_user_index(user_id)
        if idx is None:
            return None
        return self.data["users"][idx]["answers"].copy()

    def clear_answers(self, user_id: int) -> bool:
        """Очищает все ответы пользователя"""
        idx = self.get_user_index(user_id)
        if idx is None:
            return False
        self.data["users"][idx]["answers"] = {}
        self._save()
        return True

    def remove_user(self, user_id: int) -> bool:
        """Удаляет пользователя полностью"""
        idx = self.get_user_index(user_id)
        if idx is None:
            return False
        del self.data["users"][idx]
        self._save()
        return True

    def get_all_users(self) -> list:
        """Возвращает список всех пользователей (только id)"""
        return [u["id"] for u in self.data["users"]]

    def __len__(self) -> int:
        return len(self.data["users"])