# مرشد الإعلال والإبدال التعليمي - محرك القواعد الصرفية
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

def init_analyzer():
    db = MorphologyDB.builtin_db()
    return Analyzer(db)

def explain_morphology(word, root, pattern):
    """تحليل الشواهد الصرفية وتطبيق قواعد الإعلال والإبدال"""
    if not root or '.' not in root:
        return {
            "نوع التغيير": "غير محدد",
            "التعليل التعليمي": "كلمة جامدة أو لا تنطبق عليها قواعد الأفعال المشتقة القياسية."
        }

    roots = root.split('.')
    r1 = roots[0] if len(roots) > 0 else ''
    r2 = roots[1] if len(roots) > 1 else ''
    r3 = roots[2] if len(roots) > 2 else ''

    # 1. قاعدة إبدال تاء (افتعل) طاءً بعد حروف الإطباق (ص، ض، ط، ظ)
    if r1 in ['ص', 'ض', 'ط', 'ظ'] and 'ط' in word:
        return {
            "نوع التغيير": "إبدال صرفي (إبدال تاء افتعل طاءً)",
            "الأصل المفترض": f"اِ{r1}ْتَ{r2}َ{r3}",
            "التعليل التعليمي": f"وقعت تاء (اِفْتَعَلَ) بعد حرف الإطباق ({r1})، فـُقُلبت التاء طاءً لتناسب الإطباق صوتاً، فصارت ({word})."
        }

    # 2. قاعدة الإعلال بالقلب (تحرك الواو أو الياء وانفتاح ما قبلهما)
    if r2 in ['و', 'ي'] and 'ا' in word:
        return {
            "نوع التغيير": "إعلال بالقلب (قلب الواو/الياء ألفاً)",
            "الأصل المفترض": f"{r1}َ{r2}َ{r3}",
            "التعليل التعليمي": f"تحركت العين ({r2}) وانفتح ما قبلها ({r1}َ)، فـُقُلبت ألفاً، فصارت ({word})."
        }

    # 3. قاعدة الإعلال بالحذف (حذف فاء المثال الواوي في المضارع)
    if r1 == 'و' and word.startswith(('ي', 'ت', 'أ', 'ن')) and 'و' not in word:
        return {
            "نوع التغيير": "إعلال بالحذف (حذف فاء الفعل الواوي)",
            "الأصل المفترض": f"يَوْ{r2}ِ{r3}",
            "التعليل التعليمي": f"وقعت الواو (فاء الفعل) بين فتحة وكسرة لازمة في الفعل المضارع المكسور العين، فُحذفت، فصارت ({word})."
        }

    return {
        "نوع التغيير": "سالم / قياسي",
        "الأصل المفترض": word,
        "التعليل التعليمي": "الكلمة تجري على الأصل القياسي دون إعلال أو إبدال ظاهر."
    }

def analyze_word(analyzer, word):
    analyses = analyzer.analyze(word)
    if not analyses:
        return {"الكلمة": word, "خطأ": "لم يتم العثور على تحليل صرفي."}
    
    top = analyses[0]
    root = top.get('root', '')
    pattern = top.get('pattern', '')
    explanation = explain_morphology(word, root, pattern)

    return {
        "الكلمة المستعملة": word,
        "الجذر الصرفي": root,
        "الوزن": pattern,
        **explanation
    }

if __name__ == "__main__":
    analyzer = init_analyzer()
    print("=== مرشد الإعلال والإبدال التعليمي ===\n")
    
    # قائمة تجريبية تنوع بين الإعلال والإبدال والأفعال السالمة
    test_words = ["اصطبر", "قال", "يعد", "كتب"]
    for word in test_words:
        res = analyze_word(analyzer, word)
        print(f"الكلمة: {res['الكلمة المستعملة']}")
        print(f"الجذر: {res['الجذر الصرفي']} | الوزن: {res['الوزن']}")
        print(f"نوع التغيير: {res['نوع التغيير']}")
        print(f"الشرح: {res['التعليل التعليمي']}")
        print("-" * 55)
