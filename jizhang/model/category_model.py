from model.db import Database

class CategoryModel:
    def __init__(self):
        self.db = Database()

    def add_category(self, user_id, name, type_, description=None):
        if not name:
            return False, "分类名称不能为空"
        
        if type_ not in ('income', 'expense'):
            return False, "分类类型无效"

        existing = self.db.query_one(
            "SELECT id FROM categories WHERE user_id = ? AND name = ? AND type = ?",
            (user_id, name, type_)
        )
        if existing:
            return False, "该分类已存在"

        self.db.execute(
            "INSERT INTO categories (user_id, name, type, description) VALUES (?, ?, ?, ?)",
            (user_id, name, type_, description)
        )
        return True, "添加成功"

    def update_category(self, category_id, user_id, name, description=None):
        if not name:
            return False, "分类名称不能为空"

        existing = self.db.query_one(
            "SELECT id FROM categories WHERE id = ? AND user_id = ?",
            (category_id, user_id)
        )
        if not existing:
            return False, "分类不存在或无权限"

        same_name = self.db.query_one(
            "SELECT id FROM categories WHERE user_id = ? AND name = ? AND id != ?",
            (user_id, name, category_id)
        )
        if same_name:
            return False, "该分类名称已存在"

        self.db.execute(
            "UPDATE categories SET name = ?, description = ? WHERE id = ? AND user_id = ?",
            (name, description, category_id, user_id)
        )
        return True, "更新成功"

    def delete_category(self, category_id, user_id):
        existing = self.db.query_one(
            "SELECT id FROM categories WHERE id = ? AND user_id = ?",
            (category_id, user_id)
        )
        if not existing:
            return False, "分类不存在或无权限"

        self.db.execute(
            "DELETE FROM categories WHERE id = ? AND user_id = ?",
            (category_id, user_id)
        )
        return True, "删除成功"

    def get_categories(self, user_id, type_=None, keyword=None):
        query = "SELECT id, name, type, description FROM categories WHERE user_id = ?"
        params = [user_id]

        if type_:
            query += " AND type = ?"
            params.append(type_)
        
        if keyword:
            query += " AND name LIKE ?"
            params.append(f"%{keyword}%")
        
        query += " ORDER BY type, name"
        
        return self.db.query(query, params)

    def get_category_by_id(self, category_id, user_id):
        return self.db.query_one(
            "SELECT id, name, type, description FROM categories WHERE id = ? AND user_id = ?",
            (category_id, user_id)
        )