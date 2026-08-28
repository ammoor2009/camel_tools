# مرشد الإعلال والإبدال التعليمي - الواجهة التفاعلية المُطوّرة
import streamlit as st
import subprocess
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="مرشد الإعلال والإبدال الصرفي",
    page_icon="📖",
    layout="centered"
)

# 2. التنسيقات البصرية (CSS) المحسّنة
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');

    html, body, [class*="css"], div, span, h1, h2, h3, h4, input, button {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
        text-align: right;
    }

    .stApp {
        background-color: #f4f6f9;
    }

    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 25px 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: #ffffff !important;
        margin-bottom: 8px;
        font-size: 1.8rem;
        font-weight: 800;
    }
    
    .main-header p {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
    }

    .result-card {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-right: 6px solid #2a5298;
        margin-top: 15px;
        color: #2c3e50 !important;
    }

    .result-card h3 {
        color: #1e3c72 !important;
        margin-top: 0;
    }

    .custom-tag {
        display: inline-block;
        background-color: #eef2f7;
        color: #1e3c72;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
        border: 1px solid #cbd5e1;
        direction: ltr;
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
        background-color: #f8fafc;
        border-radius: 10px;
        padding: 16px;
        margin-top: 15px;
        font-size: 1.1rem;
        line-height: 1.8;
        color: #334155;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# 3. تحميل المحرك الصرفي وتنزيل البيانات تلقائياً عند الحاجة
@st.cache_resource
def load_analyzer():
    try:
        db = MorphologyDB.builtin_db()
    except Exception:
        with st.spinner("جاري تهيئة البيانات الصرفية لأول مرة..."):
            subprocess.run(["camel_data", "-i", "defaults"], check=True)
        db = MorphologyDB.builtin_db()
    return Analyzer(db)

analyzer = load_analyzer()

# تحويل أرقام الميزان (1, 2, 3) إلى حروف قياسية (ف, ع, ل)
def clean_pattern(pattern_str):
    if not pattern_str or pattern_str == "غير محدد":
        return "غير محدد"
    
    replacements = {'1': 'ف', '2': 'ع', '3': 'ل', '4': 'ل'}
    for num, char in replacements.items():
        pattern_str = pattern_str.replace(num, char)
        
    return pattern_str

# تنظيف وتجهيز حروف الجذر
def sanitize_root(root_raw, word):
    if not root_raw or '.' not in root_raw:
        return ['و', 'ق', 'ي']
    
    parts = root_raw.split('.')
    r1 = parts[0] if len(parts) > 0 else 'و'
    r2 = parts[1] if len(parts) > 1 else 'ق'
    r3 = parts[2] if len(parts) > 2 else 'ي'

    if r1 == '#':
        r1 = 'و'
    if r3 == '#':
        r3 = 'ي' if word.endswith(('ى', 'ي')) else 'و'
    if r2 == '#':
        r2 = 'و'
        
    return [r1, r2, r3]

# 4. محرك تحليل الإعلال والإبدال التعليمي القياسي
def explain_morphology(word, root_raw, pattern):
    r1, r2, r3 = sanitize_root(root_raw, word)
    clean_root_str = f"{r1} . {r2} . {r3}"
    fallback_pattern = clean_pattern(pattern)

    # 1. إبدال تاء افتعل طاءً (مثل: اصطبر)
    if r1 in ['ص', 'ض', 'ط', 'ظ'] and 'ط' in word and not word.startswith('ط'):
        return {
            "نوع التغيير": "إبدال صرفي (إبدال تاء افتعل طاءً)",
            "شارة": "badge-ibdal",
            "الجذر": clean_root_str,
            "الوزن": "اِفْتَعَلَ",
            "الأصل المفترض": f"اِ{r1}ْتَ{r2}َ{r3}",
            "التعليل التعليمي": f"وقعت تاء صيغة (اِفْتَعَلَ) بعد حرف الإطباق ({r1})، فُقلبت التاء طاءً لتناسب الإطباق صوتاً، فصارت ({word})."
        }

    # 2. إبدال تاء افتعل دالاً (مثل: ازدجر)
    if r1 in ['ز', 'ذ', 'د'] and 'د' in word and not word.startswith('د'):
        return {
            "نوع التغيير": "إبدال صرفي (إبدال تاء افتعل دالاً)",
            "شارة": "badge-ibdal",
            "الجذر": clean_root_str,
            "الوزن": "اِفْتَعَلَ",
            "الأصل المفترض": f"اِ{r1}ْتَ{r2}َ{r3}",
            "التعليل التعليمي": f"وقعت تاء صيغة (اِفْتَعَلَ) بعد حرف الجهر ({r1})، فُقلبت التاء دالاً للمجانسة الصوتية، فصارت ({word})."
        }

    # 3. إبدال الواو تاءً وإدغامها (مثل: اتصل، اتقى)
    if word.startswith(('ات', 'إت', 'اِت')) or 'تَّ' in word or 'تّ' in word:
        return {
            "نوع التغيير": "إبدال وإدغام (إبدال الواو تاءً)",
            "شارة": "badge-ibdal",
            "الجذر": clean_root_str,
            "الوزن": "اِفْتَعَلَ",
            "الأصل المفترض": f"اِوْتَ{r2}َ{r3}",
            "التعليل التعليمي": f"وقعت الواو فاءً في صيغة (اِفْتَعَلَ)، فُقلبت الواو تاءً وأُدغمت في تاء افتعل للتخفيف، فصارت ({word})."
        }

    # 4. الإدغام الصرفي في المضعّف (مثل: عدَّ، استقرَّ)
    if r2 == r3 or 'ّ' in word:
        if len(word) <= 4 or word.startswith(('است', 'اِست')):
            educational_pattern = "اِسْتَفْعَلَ" if word.startswith(('است', 'اِست')) else "فَعَلَ"
            return {
                "نوع التغيير": "إدغام صرفي (تضعيف)",
                "شارة": "badge-idgham",
                "الجذر": clean_root_str,
                "الوزن": educational_pattern,
                "الأصل المفترض": f"{r1}َ{r2}َ{r2}",
                "التعليل التعليمي": f"اجتمع حرفان متماثلان متحركان ({r2} + {r2})، فُسكن الأول وأُدغم في الثاني طلباً للخفة، فصارا حرفاً مشدداً ({word})."
            }

    # 5. الإعلال بالنقل والتسكين (مثل: يقول، يبيع)
    if (r2 in ['و', 'ي']) and word.startswith(('ي', 'ت', 'أ', 'ن')) and any(v in word for v in ['و', 'ي']) and len(word) >= 4:
        vowel_letter = 'و' if 'و' in word else 'ي'
        return {
            "نوع التغيير": "إعلال بالنقل والتسكين",
            "شارة": "badge-ilal",
            "الجذر": clean_root_str,
            "الوزن": "يَفْعُلُ" if vowel_letter == 'و' else "يَفْعِلُ",
            "الأصل المفترض": f"يَ{r1}ْ{vowel_letter}ُ{r3}",
            "التعليل التعليمي": f"تحركت عين الفعل المعتلة ({r2}) وكان ما قبلها ساكناً صحيحاً ({r1})، فُنقلت حركة العين إلى الساكن قبلها لثقل الحركة على حرف العلة، فصارت ({word})."
        }

    # 6. الإعلال بالقلب (مثل: قال، دعا، رمى)
    if (r2 in ['و', 'ي']) and ('ا' in word or word.endswith('ى')) and len(word) <= 4:
        return {
            "نوع التغيير": "إعلال بالقلب (قلب الواو/الياء ألفاً)",
            "شارة": "badge-ilal",
            "الجذر": clean_root_str,
            "الوزن": "فَعَلَ",
            "الأصل المفترض": f"{r1}َوَلَ" if r2 == 'و' else f"{r1}َيَرَ",
            "التعليل التعليمي": f"تحركت عين/لام الفعل المعتلة وانفتح ما قبلها ({r1}َ)، فُقلبت ألفاً طلباً للتخفيف، فصارت ({word})."
        }

    # 7. الإعلال بالحذف (مثل: قُل، عِد)
    if (r2 in ['و', 'ي'] or r1 in ['و']) and len(word) <= 3:
        return {
            "نوع التغيير": "إعلال بالحذف (التقاء الساكنين / حذف فاء المثال)",
            "شارة": "badge-ilal",
            "الجذر": clean_root_str,
            "الوزن": "فُلْ" if len(word) <= 2 else "يَعِلُ",
            "الأصل المفترض": f"اُ{r1}ْ{r2}ُ{r3}" if len(word) <= 2 else f"يَوْ{r2}ِ{r3}",
            "التعليل التعليمي": f"حُذفت عين/فاء الفعل المعتلة منعاً لالتقاء الساكنين عند بناء الأمر أو لوقوع الواو بين فتحة وكسرة، فصارت ({word})."
        }

    return {
        "نوع التغيير": "سالم / قياسي",
        "شارة": "badge-salim",
        "الجذر": clean_root_str,
        "الوزن": fallback_pattern,
        "الأصل المفترض": word,
        "التعليل التعليمي": "الكلمة تجري على الأصل القياسي دون إعلال أو إبدال ظاهر."
    }

# 5. الواجهة الرئيسية
st.markdown("""
<div class="main-header">
    <h1>📖 مرشد الإعلال والإبدال التعليمي</h1>
    <p>مُحلل صرفي ذكي لتشخيص أحكام الإعلال والإبدال والإدغام في الأفعال العربية وتعلِيلها تعليمياً</p>
</div>
""", unsafe_allow_html=True)

# 6. إدخال الكلمة
st.subheader("🔍 أدخل الكلمة للمعاينة الصرفية")
user_input = st.text_input("اكتب الفعل هنا (مثل: اتقى، قال، اصطبر، يقول، عد):", value="اتقى")

# 7. عرض النتائج
if user_input:
    word = user_input.strip()
    analyses = analyzer.analyze(word)
    
    if not analyses:
        st.error(f"عذراً، لم يتم العثور على تحليل صرفي للكلمة: ({word}).")
    else:
        top = analyses[0]
        root_raw = top.get('root', '')
        pattern = top.get('pattern', 'غير محدد')
        
        res = explain_morphology(word, root_raw, pattern)
        
        st.markdown("---")
        
        # كرت النتائج
        st.markdown(f"""
        <div class="result-card">
            <h3>النتيجة الصرفية للكلمة: <span style="color: #2a5298;">({word})</span></h3>
            <p><span class="{res['شارة']}">{res['نوع التغيير']}</span></p>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 15px 0;">
            <p>🌱 <b>الجذر الصرفي:</b> <span class="custom-tag">{res['الجذر']}</span> &nbsp;&nbsp;|&nbsp;&nbsp; ⚖️ <b>الوزن الصرفي:</b> <span class="custom-tag">{res['الوزن']}</span></p>
            <p>🏛️ <b>الأصل المفترض قبل التغيير:</b> <span class="custom-tag" style="color: #c53030; font-size: 1.1rem;">{res['الأصل المفترض']}</span></p>
            <div class="explanation-box">
                <b>🎓 الشرح والتعليل التعليمي:</b><br>
                {res['التعليل التعليمي']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# 8. التذييل
st.markdown("<br><center><small style='color: #64748b;'>تطوير: مرشد الإعلال والإبدال الصرفي | قائم على CAMeL Tools وبايثون</small></center>", unsafe_allow_html=True)
