# مرشد الإعلال والإبدال التعليمي - الواجهة التفاعلية
import streamlit as st
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

# 1. إعدادات الصفحة الرئيسية
st.set_page_config(
    page_title="مرشد الإعلال والإبدال الصرفي",
    page_icon="📖",
    layout="centered"
)

# 2. إضافة التنسيقات البصرية (CSS) لدعم اللغة العربية وتجميل الواجهة
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');

    html, body, [class*="css"], div, span, h1, h2, h3, h4, input, button {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
        text-align: right;
    }

    .stApp {
        background-color: #f8f9fa;
    }

    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 30px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: #ffffff !important;
        margin-bottom: 8px;
        font-weight: 800;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }

    .result-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border-right: 6px solid #2a5298;
        margin-top: 15px;
    }

    .badge-ibdal {
        background-color: #e3f2fd;
        color: #0d47a1;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
    }

    .badge-ilal {
        background-color: #fff3e0;
        color: #e65100;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
    }

    .badge-idgham {
        background-color: #f3e5f5;
        color: #4a148c;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
    }

    .badge-salim {
        background-color: #e8f5e9;
        color: #1b5e20;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
    }

    .explanation-box {
        background-color: #f1f3f4;
        border-radius: 10px;
        padding: 18px;
        margin-top: 15px;
        font-size: 1.15rem;
        line-height: 1.8;
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# 3. تحميل المحرك الصرفي وتخزينه في الذاكرة لتسريع الأداء
@st.cache_resource
def load_analyzer():
    db = MorphologyDB.builtin_db()
    return Analyzer(db)

analyzer = load_analyzer()

# 4. محرك تحليل الإعلال والإبدال
def explain_morphology(word, root, pattern):
    if not root or '.' not in root:
        return {
            "نوع التغيير": "غير محدد",
            "شارة": "badge-salim",
            "الأصل المفترض": word,
            "التعليل التعليمي": "كلمة جامدة أو لا تنطبق عليها قواعد الأفعال المشتقة القياسية."
        }

    roots = root.split('.')
    r1 = roots[0] if len(roots) > 0 else ''
    r2 = roots[1] if len(roots) > 1 else ''
    r3 = roots[2] if len(roots) > 2 else ''

    # 1. إبدال تاء افتعل طاءً
    if r1 in ['ص', 'ض', 'ط', 'ظ'] and 'ط' in word and not word.startswith('ط'):
        return {
            "نوع التغيير": "إبدال صرفي (إبدال تاء افتعل طاءً)",
            "شارة": "badge-ibdal",
            "الأصل المفترض": f"اِ{r1}ْتَ{r2}َ{r3}",
            "التعليل التعليمي": f"وقعت تاء صيغة (اِفْتَعَلَ) بعد حرف الإطباق ({r1})، فُقلبت التاء طاءً لتناسب الإطباق صوتاً، فصارت ({word})."
        }

    # 2. إبدال تاء افتعل دالاً
    if r1 in ['ز', 'ذ', 'د'] and 'د' in word and not word.startswith('د'):
        return {
            "نوع التغيير": "إبدال صرفي (إبدال تاء افتعل دالاً)",
            "شارة": "badge-ibdal",
            "الأصل المفترض": f"اِ{r1}ْتَ{r2}َ{r3}",
            "التعليل التعليمي": f"وقعت تاء صيغة (اِفْتَعَلَ) بعد حرف الجهر ({r1})، فُقلبت التاء دالاً للمجانسة الصوتية، فصارت ({word})."
        }

    # 3. إبدال الواو تاءً وإدغامها
    if word.startswith(('ات', 'إت', 'اِت')) or (r1 in ['و', 'ي', '#'] and ('تَّ' in word or 'تّ' in word or word.startswith('ات'))):
        return {
            "نوع التغيير": "إبدال وإدغام (إبدال الواو تاءً)",
            "شارة": "badge-ibdal",
            "الأصل المفترض": f"اِوْتَ{r2}َ{r3}",
            "التعليل التعليمي": f"وقعت الواو فاءً في صيغة (اِفْتَعَلَ)، فُقلبت الواو تاءً وأُدغمت في تاء افتعل للتخفيف، فصارت ({word})."
        }

    # 4. الإدغام الصرفي في المضعّف
    if r2 == r3 or (r2 != '' and r3 in ['#', r2]) or 'ّ' in word:
        if len(word) <= 4 or word.startswith(('است', 'اِست')):
            return {
                "نوع التغيير": "إدغام صرفي (تضعيف)",
                "شارة": "badge-idgham",
                "الأصل المفترض": f"{r1}َ{r2}َ{r2}",
                "التعليل التعليمي": f"اجتمع حرفان متماثلان متحركان ({r2} + {r2})، فُسكن الأول وأُدغم في الثاني طلباً للخفة، فصارا حرفاً مشدداً ({word})."
            }

    # 5. الإعلال بالنقل والتسكين
    if (r2 in ['و', 'ي', '#']) and word.startswith(('ي', 'ت', 'أ', 'ن')) and any(v in word for v in ['و', 'ي']) and len(word) >= 4:
        vowel_letter = 'و' if 'و' in word else 'ي'
        return {
            "نوع التغيير": "إعلال بالنقل والتسكين",
            "شارة": "badge-ilal",
            "الأصل المفترض": f"يَ{r1}ْ{vowel_letter}ُ{r3}",
            "التعليل التعليمي": f"تحركت عين الفعل المعتلة ({r2}) وكان ما قبلها ساكناً صحيحاً ({r1})، فُنقلت حركة العين إلى الساكن قبلها لثقل الحركة على حرف العلة، فصارت ({word})."
        }

    # 6. الإعلال بالقلب
    if (r2 in ['و', 'ي', '#']) and ('ا' in word or word.endswith('ى')) and len(word) <= 4:
        return {
            "نوع التغيير": "إعلال بالقلب (قلب الواو/الياء ألفاً)",
            "شارة": "badge-ilal",
            "الأصل المفترض": f"{r1}َوَلَ",
            "التعليل التعليمي": f"تحركت عين/لام الفعل المعتلة وانفتح ما قبلها ({r1}َ)، فُقلبت ألفاً طلباً للتخفيف، فصارت ({word})."
        }

    # 7. الإعلال بالحذف
    if (r2 in ['و', 'ي', '#'] or r1 in ['و', '#']) and len(word) <= 3:
        return {
            "نوع التغيير": "إعلال بالحذف (التقاء الساكنين / حذف فاء المثال)",
            "شارة": "badge-ilal",
            "الأصل المفترض": f"اُ{r1}ْ{('و' if r2 in ['و','#'] else 'ي')}ُ{r3}" if len(word) <= 2 else f"يَوْ{r2}ِ{r3}",
            "التعليل التعليمي": f"حُذفت عين/فاء الفعل المعتلة منعاً لالتقاء الساكنين عند بناء الأمر أو لوقوع الواو بين فتحة وكسرة، فصارت ({word})."
        }

    return {
        "نوع التغيير": "سالم / قياسي",
        "شارة": "badge-salim",
        "الأصل المفترض": word,
        "التعليل التعليمي": "الكلمة تجري على الأصل القياسي دون إعلال أو إبدال ظاهر."
    }

# 5. الترويسة الرئيسية
st.markdown("""
<div class="main-header">
    <h1>📖 مرشد الإعلال والإبدال التعليمي</h1>
    <p>مُحلل صرفي ذكي لتشخيص أحكام الإعلال والإبدال والإدغام في الأفعال العربية وتعلِيلها تعليمياً</p>
</div>
""", unsafe_allow_html=True)

# 6. أدوات إدخال الكلمة
st.subheader("🔍 أدخل الكلمة للمعاينة الصرفية")
col1, col2 = st.columns([3, 1])

with col1:
    user_input = st.text_input("اكتب الفعل هنا (مشكولاً أو غير مشكول):", value="اصطبر", label_visibility="collapsed")

with col2:
    analyze_btn = st.button("تحليل الكلمة", use_container_width=True, type="primary")

# أزرار شواهد سريعة للتجربة
st.caption("💡 شواهد تجريبية سريعة:")
q_cols = st.columns(6)
examples = ["اصطبر", "ازدحم", "اتصل", "قال", "يقول", "عد"]

for idx, ex in enumerate(examples):
    if q_cols[idx].button(ex, use_container_width=True):
        user_input = ex

# 7. تنفيذ التحليل وعرض النتائج
if user_input:
    word = user_input.strip()
    analyses = analyzer.analyze(word)
    
    if not analyses:
        st.error(f"عذراً، لم يتم العثور على تحليل صرفي للكلمة: ({word}). تأكد من كتابتها بصورة صحيحة.")
    else:
        top = analyses[0]
        root = top.get('root', 'غير محدد')
        pattern = top.get('pattern', 'غير محدد')
        res = explain_morphology(word, root, pattern)
        
        st.markdown("---")
        
        # تفاصيل النتيجة الصرفية
        st.markdown(f"""
        <div class="result-card">
            <h3>النتيجة الصرفية للكلمة: <span style="color: #2a5298;">({word})</span></h3>
            <p><span class="{res['شارة']}">{res['نوع التغيير']}</span></p>
            <hr>
            <p><b>🌱 الجذر الصرفي:</b> <code>{root}</code> &nbsp;&nbsp;|&nbsp;&nbsp; <b>⚖️ الوزن الصرفي:</b> <code>{pattern}</code></p>
            <p><b>🏛️ الأصل المفترض قبل التغيير:</b> <code style="font-size: 1.1rem; color: #d32f2f;">{res['الأصل المفترض']}</code></p>
            <div class="explanation-box">
                <b>🎓 الشرح والتعليل التعليمي:</b><br>
                {res['التعليل التعليمي']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# 8. التذييل والمعلومات
st.markdown("---")
st.markdown("<center><small>تطوير: مرشد الإعلال والإبدال الصرفي | قائم على CAMeL Tools وبايثون</small></center>", unsafe_allow_html=True)
