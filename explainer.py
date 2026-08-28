# مرشد الإعلال والإبدال التعليمي - استخراج الجذر والوزن
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

def init_analyzer():
    db = MorphologyDB.builtin_db()
    return Analyzer(db)

def get_word_details(analyzer, word):
    """استخراج الجذر والوزن الصرفي للكلمة"""
    analyses = analyzer.analyze(word)
    if not analyses:
        return "لم يتم العثور على تحليل صرفي."
    
    # اختيار التحليل الصرفي الأبرز
    top = analyses[0]
    return {
        "الكلمة": word,
        "الجذر": top.get('root', 'غير محدد'),
        "الوزن": top.get('pattern', 'غير محدد')
    }

if __name__ == "__main__":
    analyzer = init_analyzer()
    print("تم تحميل محرك التحليل الصرفي بنجاح!\n")
    
    # تجربة استخراج البيانات لكمات معتلة ومبدلة
    test_words = ["قال", "اصطبر", "يعد"]
    for word in test_words:
        info = get_word_details(analyzer, word)
        print(info)
