from charades_app.models import Category, Word
from charades_app.extensions import ma

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category

class WordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Word