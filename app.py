from datetime import datetime
import json
import os
import zoneinfo
import requests
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. إعدادات الصفحة الرسمية والتوقيت الزمني للسعودية
# ==========================================
st.set_page_config(
    page_title="تقييم الأدوية المخدرة والمؤثرات العقلية | إدارة الخدمات الصيدلانية",
    page_icon="💊",
    layout="wide",
)

# ضبط توقيت المملكة العربية السعودية (توقيت الرياض)
saudi_tz = zoneinfo.ZoneInfo("Asia/Riyadh")
saudi_now = datetime.now(saudi_tz)

# رابط Google Apps Script الخاص بتقييم الأدوية المخدرة
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbZm08M6lDJVyWzVV7ENc9rHoXd_j2IzK-J_GxNOoqgvHmIvHDzjbNB4Q3RlADCySYd/exec"

# ==========================================
# 2. تنسيق الخطوط وإخفاء الشريط العلوي والسفلي والشارات بالكامل
# ==========================================
st.markdown(
    """
    <style>
        /* 1. إخفاء الشريط العلوي والمنيو والهيدر */
        header, footer, #MainMenu, 
        [data-testid="stHeader"], 
        [data-testid="stFooter"], 
        [data-testid="stToolbar"],
        [data-testid="stDecoration"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
        }

        /* 2. إخفاء الحاوية السفلية والشارات العائمة بالكامل */
        [data-testid="stBottom"],
        [data-testid="stBottomBlockContainer"],
        [data-testid="stStatusWidget"],
        .stAppDeployButton,
        div[class*="viewerBadge"],
        div[class*="viewerBadge_container"],
        div[class*="styles_viewerBadge"],
        div[class*="StyledAppViewerFooter"],
        div[class*="AppViewerFooter"],
        div[class*="stAppFooter"],
        a[href*="streamlit.io"],
        a[aria-label*="Streamlit"],
        div:has(> a[href*="streamlit.io"]),
        div:has(> [class*="viewerBadge"]) {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
            height: 0 !important;
            width: 0 !important;
        }

        /* 3. إخفاء تعليمات الإدخال الإنجليزية */
        div[data-testid="stInputInstructions"],
        [data-testid="InputInstructions"],
        small[data-testid="stWidgetInstructions"] {
            display: none !important;
        }

        /* 4. ضبط الخطوط والاتجاه من اليمين لليسار */
        html, body, [class*="css"], font, label, input, button, select, p, div, h1, h2, h3 {
            font-family: 'Calibri', 'Segoe UI', 'Arial', sans-serif !important;
            direction: rtl;
            text-align: right;
        }
        .stMetric { text-align: right; }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 3. عرض الترويسة الرئيسية
# ==========================================
header_files = [
    "header.PNG",
    "header.png",
    "HEADER.PNG",
    "header.jpg",
    "header.jpeg",
    "IMG_3602.PNG",
]
image_found = False
for img_file in header_files:
    if os.path.exists(img_file):
        st.image(img_file, use_container_width=True)
        image_found = True
        break

if not image_found:
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #0b192c 0%, #1e3e62 50%, #001427 100%);
            border: 2px solid #d4af37;
            border-radius: 16px;
            padding: 25px 30px;
            color: white;
            font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
            direction: rtl;
            text-align: right;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        ">
            <div style="border-bottom: 1px solid rgba(212, 175, 55, 0.4); padding-bottom: 12px; margin-bottom: 15px;">
                <span style="background: linear-gradient(90deg, #d4af37, #f3e5ab); color: #0b192c; font-size: 15px; font-weight: bold; padding: 4px 14px; border-radius: 6px; font-family: Calibri, sans-serif;">🏛️ التجمع الصحي الثاني</span>
                <div style="font-size: 22px; font-weight: bold; color: #ffffff; margin-top: 10px; font-family: Calibri, sans-serif;">إدارة الخدمات الصيدلانية - قسم الرقابة الدوائية</div>
            </div>
            <div style="margin-bottom: 15px;">
                <span style="font-size: 32px; font-weight: bold; color: #ffffff; font-family: Calibri, sans-serif;">تقييم الأدوية المخدرة والمؤثرات العقلية</span>
            </div>
            <div style="font-size: 16px; color: #cbd5e1; margin-bottom: 15px; font-family: Calibri, sans-serif;">
                النموذج الموحد لتدقيق السجلات، الخزائن، والامتثال للسياسات المنظمة للأدوية الخاضعة للرقابة.
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

st.write(
    "قم بتعبئة نموذج تقييم الأدوية المخدرة والمؤثرات العقلية للحصول على التقييم المباشر وتصدير التقرير المطبوع."
)
st.divider()

# ==========================================
# 4. البيانات الأساسية (التاريخ فقط)
# ==========================================
st.subheader("📌 البيانات الأساسية للزيارة")
c1, c2, c3 = st.columns(3)
with c1:
    center_name = st.text_input(
        "اسم المركز الصحي / المنشأة",
        value="",
        placeholder="أدخل اسم المركز الصحي",
    )
with c2:
    inspector_name = st.text_input(
        "اسم المفتش / المقيم",
        value="",
        placeholder="أدخل اسم المفتش الميداني",
    )
with c3:
    # التاريخ فقط - يمنع اختيار أي تاريخ سابق
    inspection_date = st.date_input(
        "تاريخ التقييم",
        value=saudi_now.date(),
        min_value=saudi_now.date(),
        format="YYYY/MM/DD",
    )

st.divider()

# ==========================================
# 5. بنود التقييم الـ 13 الخاصة بالأدوية المخدرة
# ==========================================
items_data = [
    (
        "1",
        "السياسات والصلاحيات",
        "وجود قائمة المعتمدين بكتابة الوصفات الطبية المخدرة والمؤثرات العقلية.",
    ),
    (
        "2",
        "السياسات والصلاحيات",
        "توفر قائمة بالمصرح لهم بدخول غرفة الأدوية وحمل مفتاح الخزنة.",
    ),
    (
        "3",
        "السياسات والصلاحيات",
        "توفر ونفاذ سياسات التعامل مع الأدوية المخدرة المحدثة والمعتمدة.",
    ),
    (
        "4",
        "إجراءات الحفظ والتخزين",
        "حفظ الأدوية المخدرة والمؤثرات العقلية داخل خزنة حديدية مغلقة ومثبتة.",
    ),
    (
        "5",
        "إجراءات الحفظ والتخزين",
        "حفظ مفتاح الخزنة بحوزة الصيدلي المسؤول المعتمد دائماً.",
    ),
    (
        "6",
        "إجراءات الحفظ والتخزين",
        "مطابقة الرصيد الفعلي في الخزنة مع السجلات ونظام رقيم.",
    ),
    (
        "7",
        "السجلات والتوثيق",
        "وجود سجل رسمي معتمد لمتابعة وحصر الأدوية المخدرة والمؤثرات العقلية.",
    ),
    (
        "8",
        "السجلات والتوثيق",
        "التوثيق الفوري والصحيح لكافة عمليات الصرف والاستلام والتسليم.",
    ),
    (
        "9",
        "السجلات والتوثيق",
        "اكتمال بيانات الوصفات الطبية الخاصة بالأدوية المخدرة والتوقيعات.",
    ),
    (
        "10",
        "الإتلاف والعهدة",
        "توفر ملف مخصص لمحاضر الإتلاف والفاقد والمكسور ومتابعة التعاميم.",
    ),
    (
        "11",
        "الإتلاف والعهدة",
        "التقييم الدوري والجرد الفعلي للعهدة وتوثيق محاضر الاستلام والتسليم.",
    ),
    (
        "12",
        "الإتلاف والعهدة",
        "التأكد من عدم وجود أدوية مخدرة منتهية الصلاحية أو تالفة دون اتخاذ"
        " الإجراء النظامي.",
    ),
    (
        "13",
        "الإتلاف والعهدة",
        "سلامة أقفال ومحاضر الفتح الخاصة بعربة الطوارئ أو الحقيبة الإسعافية.",
    ),
]

sections = {}
for num, sec, crit in items_data:
    sections.setdefault(sec, []).append((num, crit))

st.subheader("📋 نموذج تقييم الرقابة على الأدوية المخدرة (13 بنداً)")

responses = []

with st.form("narcotics_form"):
    for sec_name, items in sections.items():
        with st.expander(f"🔹 {sec_name} ({len(items)} بنود)", expanded=True):
            for num, crit in items:
                col_crit, col_status, col_note = st.columns([4, 3, 3])
                with col_crit:
                    st.markdown(f"**{num}.** {crit}")
                with col_status:
                    status = st.radio(
                        f"حالة البند {num}",
                        ["مطابق", "جزئي", "غير مطابق"],
                        index=None,
                        horizontal=True,
                        key=f"status_{num}",
                        label_visibility="collapsed",
                    )
                with col_note:
                    note = st.text_input(
                        f"ملاحظة البند {num}",
                        placeholder="ملاحظات التقييم (إن وجدت)",
                        key=f"note_{num}",
                        label_visibility="collapsed",
                    )
                responses.append({
                    "id": int(num),
                    "section": sec_name,
                    "criterion": crit,
                    "status": status,
                    "notes": note,
                })

    submit_btn = st.form_submit_button(
        "🚀 اعتماد التقييم وإصدار التقرير", use_container_width=True
    )

# ==========================================
# 6. معالجة النتائج وإصدار التقرير
# ==========================================
if submit_btn:
    total_score = 0.0
    matched_cnt = 0
    partial_cnt = 0
    unmatched_cnt = 0

    for r in responses:
        st_val = r["status"]
        if st_val == "مطابق":
            total_score += 1.0
            matched_cnt += 1
        elif st_val == "جزئي":
            total_score += 0.5
            partial_cnt += 1
        else:
            unmatched_cnt += 1

    compliance_rate = (total_score / len(responses)) * 100
    display_center = center_name if center_name.strip() else "غير محدد"
    display_inspector = (
        inspector_name if inspector_name.strip() else "غير محدد"
    )

    if GOOGLE_SCRIPT_URL:
        payload = {
            "center_name": display_center,
            "inspector_name": display_inspector,
            "inspection_date": str(inspection_date),
            "compliance_rate": f"{compliance_rate:.2f}",
            "matched_cnt": matched_cnt,
            "partial_cnt": partial_cnt,
            "unmatched_cnt": unmatched_cnt,
            "responses": responses,
        }
        try:
            headers = {"Content-Type": "application/json"}
            res = requests.post(
                GOOGLE_SCRIPT_URL,
                data=json.dumps(payload),
                headers=headers,
                timeout=30,
            )
            if res.status_code in [200, 302]:
                st.success("✅ تم إرسال وحفظ التقرير بنجاح!")
            else:
                st.warning("⚠️ تم حساب النتائج وتوليد التقرير محلياً.")
        except Exception:
            st.warning("⚠️ تم حساب النتائج وتوليد التقرير محلياً.")

    st.subheader("📊 ملخص نتائج التقييم")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🏥 المنشأة / المركز", display_center)
    m2.metric("👨‍⚕️ المفتش / المقيم", display_inspector)
    m3.metric("📅 تاريخ التقييم", inspection_date.strftime("%Y/%m/%d"))
    m4.metric("📈 نسبة الامتثال", f"{compliance_rate:.2f}%")

    c1, c2, c3 = st.columns(3)
    c1.success(f"✅ مطابق: {matched_cnt}")
    c2.warning(f"⚠️ جزئي: {partial_cnt}")
    c3.error(f"❌ غير مطابق / لم يحدد: {unmatched_cnt}")

    st.divider()

    st.subheader("🖨️ التقرير المطبوع (PDF)")

    html_report = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Calibri', Arial, sans-serif; padding: 20px; direction: rtl; text-align: right; }}
            .header {{ background-color: #0b192c; color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-right: 6px solid #d4af37; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: right; }}
            th {{ background-color: #f2f2f2; }}
            .warning {{ color: #d35400; font-weight: bold; }}
            .danger {{ color: #c0392b; font-weight: bold; }}
            .print-btn {{ background-color: #1e3e62; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; margin-bottom: 15px; }}
        </style>
    </head>
    <body>
        <button class="print-btn" onclick="window.print()">🖨️ اضغط هنا للطباعة أو الحفظ كـ PDF</button>
        <hr>
        <div class="header">
            <p style="font-size:14px; color:#f3e5ab; margin-bottom:5px;">🏛️ التجمع الصحي الثاني - إدارة الخدمات الصيدلانية</p>
            <h2>تقرير تقييم الأدوية المخدرة والمؤثرات العقلية</h2>
            <p><strong>اسم المركز:</strong> {display_center} | <strong>المقيم:</strong> {display_inspector} | <strong>تاريخ التقييم:</strong> {inspection_date.strftime('%Y/%m/%d')}</p>
            <p><strong>نسبة الامتثال الإجمالية:</strong> {compliance_rate:.2f}%</p>
        </div>
        
        <h3>📋 تفاصيل بنود التقييم والملاحظات (13 بنداً):</h3>
    """

    for sec_name, items in sections.items():
        html_report += f"<h4>🔹 {sec_name}</h4><table><tr><th>م</th><th>المعيار</th><th>الحالة</th><th>ملاحظات المقيم</th></tr>"
        sec_responses = [r for r in responses if r["section"] == sec_name]
        for it in sec_responses:
            st_text = it["status"] if it["status"] else "غير محدد"
            status_class = (
                "warning"
                if st_text == "جزئي"
                else (
                    "danger"
                    if st_text in ["غير مطابق", "غير محدد"]
                    else ""
                )
            )
            html_report += f"<tr><td>{it['id']}</td><td>{it['criterion']}</td><td class='{status_class}'>{st_text}</td><td>{it['notes']}</td></tr>"
        html_report += "</table>"

    html_report += "</body></html>"

    components.html(html_report, height=650, scrolling=True)

# ==========================================
# 7. تذييل الصفحة الرسمي
# ==========================================
st.markdown("---")
st.caption(
    "قسم الرقابة الدوائية - إدارة الخدمات الصيدلانية - تجمع الرياض الصحي"
    " الثاني"
)
