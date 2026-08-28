# مرشد الإعلال والإبدال التعليمي - النواة الأولى
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

def init_analyzer():
    """تحميل قاعدة بيانات CAMeL Tools"""
    db = MorphologyDB.builtin_db()
    return Analyzer(db)

if __name__ == "__main__":
    analyzer = init_analyzer()
    print("تم تحميل محرك التحليل الصرفي بنجاح!")
