from sqlalchemy.orm import Session

from model.category import Category


class CategoryService:

    def __init__(self, session: Session):
        self.session = session
    
    def insert(self, category: dict) -> Category:
        category_loaded = Category(**category)
        self.session.add(category_loaded)
        self.session.commit()
        self.session.refresh(category_loaded)
        return category_loaded

    def get_by_name(self, name: str) -> Category:
        return self.session.query(
            Category
        ).filter(Category.name == name).first()