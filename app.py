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
    page_title="تقرير تقييم الأدوية المخدرة والمؤثرات العقلية | إدارة الخدمات الصيدلانية",
    page_icon="💊",
    layout="wide",
)

# ضبط توقيت المملكة العربية السعودية (توقيت الرياض)
saudi_tz = zoneinfo.ZoneInfo("Asia/Riyadh")
saudi_now = datetime.now(saudi_tz)

# الرابط الجديد الصحيح الخاص بك
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbywnfQOufl2YE4dQQ0ddOlm6iQXiEjE3J_4roFoCXRxyki0MPpMaBbT5q8NNEZMrUFLHg/exec"

# ==========================================
# 2. تنسيق الخطوط وإخفاء الشريط العلوي والسفلي والشارات بالكامل
# ==========================================
st.markdown(
    """
    <style>
        /* 1. إخفاء الشريط العلوي والمنيو والهيدر والفوتر */
        header, footer, #MainMenu, 
        [data-testid="stHeader"], 
        [data-testid="stFooter"], 
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        [data-testid="stBottom"],
        [data-testid="stBottomBlockContainer"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
        }

        /* 2. إخفاء الشارات العائمة (Hosted with Streamlit) */
        div[class*="viewerBadge"],
        div[class*="viewerBadge_container"],
        div[class*="styles_viewerBadge"],
        div[class*="StyledAppViewerFooter"],
        div[class*="AppViewerFooter"],
        div[class*="stAppFooter"],
        .stAppDeployButton,
        .stAppFooter,
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

        /* 3. إخفاء العناصر العائمة أسفل الشاشة على الجوال */
        div[style*="position: fixed"][style*="bottom"],
        div[style*="position: fixed"][style*="bottom: 0px"],
        div[style*="position: fixed"][style*="bottom: 0"],
        div[style*="bottom: 0px"],
        div[style*="bottom: 0"] {
            display: none !important;
            visibility: hidden !important;
        }

        /* 4. إخفاء تعليمات الإدخال الإنجليزية */
        div[data-testid="stInputInstructions"],
        [data-testid="InputInstructions"],
        small[data-testid="stWidgetInstructions"] {
            display: none !important;
        }

        /* 5. ضبط الخطوط والاتجاه من اليمين لليسار */
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
                <div style="font-size: 22px; font-weight: bold; color: #ffffff; margin-top: 10px; font-family: Calibri, sans-serif;">إدارة الخدمات الصيدلانية لمراكز الرعاية الصحية الأولية</div>
            </div>
            <div style="margin-bottom: 15px;">
                <span style="font-size: 34px; font-weight: bold; color: #ffffff; font-family: Calibri, sans-serif;">تقرير تقييم الأدوية المخدرة والمؤثرات العقلية</span>
            </div>
            <div style="font-size: 16px; color: #cbd5e1; margin-bottom: 15px; font-family: Calibri, sans-serif;">
                المنصة الرقمية الموحدة لتقييم ومتابعة عهد الأدوية المخدرة والرقابة الصيدلانية المباشرة.
            </div>
            <div>
                <span style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.25); color: white; padding: 5px 14px; border-radius: 8px; font-size: 14px; font-family: Calibri, sans-serif; margin-left: 8px;">📊 تقييم امتثال فوري</span>
                <span style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.25); color: white; padding: 5px 14px; border-radius: 8px; font-size: 14px; font-family: Calibri, sans-serif;">🖨️ تقارير PDF مباشرة</span>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

st.write(
    "قم بتعبئة النموذج الميداني أدناه للحصول على التقييم الفوري وتوليد تقرير PDF مطبوع مباشرة دون الحاجة للتعامل مع الإكسل."
)
st.divider()

# ==========================================
# 4. البيانات الأساسية للزيارة التفتيشية
# ==========================================
st.subheader("📌 البيانات الأساسية للزيارة التفتيشية")
c1, c2, c3 = st.columns(3)
with c1:
    center_name = st.text_input(
        "اسم المركز الصحي", value="", placeholder="أدخل اسم المركز الصحي"
    )
with c2:
    inspector_name = st.text_input(
        "اسم المفتش / المُقيم",
        value="",
        placeholder="أدخل اسم المفتش أو المُقيم",
    )
with c3:
    inspection_date = st.date_input(
        "تاريخ التفتيش",
        value=saudi_now.date(),
        min_value=saudi_now.date(),
        format="YYYY/MM/DD",
    )

st.divider()

# ==========================================
# 5. بنود التقييم التفتيشية الـ 15
# ==========================================
items_data = [
    ("1", "محور الخزنة والسياسات العامة", "توفر سياسات صيدلانية محدثة ومعتمدة للأدوية المخدرة والمؤثرات العقلية."),
    ("2", "محور الخزنة والسياسات العامة", "وجود قائمة المصرح لهم بكتابة الوصفات الطبية المخدرة."),
    ("3", "محور الخزنة والسياسات العامة", "وجود قائمة للمصرح لهم بحمل مفتاح خزنة الأدوية المخدرة."),
    ("4", "محور الخزنة والسياسات العامة", "توفر خزنة مخصصة ومحكمة الإغلاق للأدوية المخدرة."),
    ("5", "محور الخزنة والسياسات العامة", "حفظ مفتاح الخزنة مع مسؤول غرفة الادوية دائما."),
    ("6", "محور الخزنة والسياسات العامة", "مطابقة الرصيد الفعلي في الخزنة مع السجلات."),
    ("7", "محور السجلات والمتابعة والجرد", "التشييك على قائمة المتابعه اليومي."),
    ("8", "محور السجلات والمتابعة والجرد", "توفر وصفات الادوية المخدره وتوفيرها عند الحاجه."),
    ("9", "محور السجلات والمتابعة والجرد", "توفر وتوثيق سجلات صرف واستلام الأدوية المخدرة ."),
    ("10", "محور السجلات والمتابعة والجرد", "توفر ملف مخصص لإتلاف الأدوية المخدرة وتوثيق تعاميم السحب ومحاضر الإتلاف."),
    ("11", "محور السجلات والمتابعة والجرد", "توفر المدور والجرد."),
    ("12", "محور السجلات والمتابعة والجرد", "توفر وتوثيق المؤشرات للأدوية المخدرة ورصد الأخطاء الدوائية."),
    ("13", "محور السجلات والمتابعة والجرد", "الاحتفاظ بالوصفات و السجلات حسب السياسات و الانظمة ( الوصفات 3 سنوات ، السجلات 5 سنوات )."),
    ("14", "محور اللجان والتوثيق الميداني", "توفر أعضاء لجان الصرف والوصف."),
    ("15", "محور اللجان والتوثيق الميداني", "توفر محاضر اجتماع اللجنة والتوثيق بعد عمليات الصرف."),
]

sections = {}
for num, sec, crit in items_data:
    sections.setdefault(sec, []).append((num, crit))

st.subheader("📋 نموذج تقييم بنود الأدوية المخدرة")

responses = []

for sec_name, items in sections.items():
    with st.expander(f"🔹 {sec_name} ({len(items)} بند)", expanded=True):
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
                    placeholder="ملاحظات المفتش / المُقيم",
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

st.markdown("<br>", unsafe_allow_html=True)
general_notes = st.text_area(
    "الملاحظات إن وجدت",
    placeholder="أدخل أي ملاحظات عامة أو توصيات ختامية هنا...",
    height=100,
    key="general_notes_input",
)

st.markdown("<br>", unsafe_allow_html=True)
submit_btn = st.button("🚀 اعتماد التقييم وإصدار التقرير", use_container_width=True)

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
    display_inspector = (inspector_name if inspector_name.strip() else "غير محدد")
    
    current_saudi_time = datetime.now(saudi_tz)
    formatted_time_str = current_saudi_time.strftime("%I:%M %p")

    payload = {
        "center_name": display_center,
        "inspector_name": display_inspector,
        "inspection_date": str(inspection_date),
        "inspection_time": formatted_time_str,
        "compliance_rate": f"{compliance_rate:.2f}",
        "matched_cnt": matched_cnt,
        "partial_cnt": partial_cnt,
        "unmatched_cnt": unmatched_cnt,
        "general_notes": general_notes,
        "responses": responses,
    }

    if GOOGLE_SCRIPT_URL:
        try:
            res = requests.post(
                GOOGLE_SCRIPT_URL,
                json=payload,
                timeout=30,
            )

            if res.ok:
                try:
                    result = res.json()
                except ValueError:
                    result = {}

                if result.get("status") == "success":
                    st.success("✅ تم حفظ التقرير في Google Drive بنجاح")

                    report_url = result.get("url")
                    if report_url:
                        st.markdown(
                            f"[📄 فتح التقرير في Google Drive]({report_url})"
                        )

                elif result.get("status") == "error":
                    st.error(
                        f"❌ خطأ من Apps Script: "
                        f"{result.get('message', 'خطأ غير معروف')}"
                    )

                else:
                    st.success("✅ تم إرسال التقرير إلى Google Apps Script بنجاح")

            else:
                st.error(f"❌ خطأ HTTP: {res.status_code}")

        except Exception as error:
            st.error(f"❌ تعذر الاتصال بخادم التقارير: {error}")
            
    st.subheader("📊 ملخص نتائج التقييم")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🏥 المركز الصحي", display_center)
    m2.metric("👨‍⚕️ المفتش / المُقيم", display_inspector)
    m3.metric("📅 تاريخ ووقت التفتيش", f"{inspection_date.strftime('%Y/%m/%d')} ({formatted_time_str})")
    m4.metric("📈 نسبة الامتثال الإجمالية", f"{compliance_rate:.2f}%")

    c1, c2, c3 = st.columns(3)
    c1.success(f"✅ مطابق: {matched_cnt}")
    c2.warning(f"⚠️ جزئي: {partial_cnt}")
    c3.error(f"❌ غير مطابق: {unmatched_cnt}")

    st.divider()

    st.subheader("🖨️ التقرير المطبوع (PDF)")
    
    display_notes_html = f"<div style='background:#f8fafc; border-right:4px solid #1e3e62; padding:10px; margin-top:15px; border-radius:4px;'><strong>📝 الملاحظات العامة:</strong><br>{general_notes}</div>" if general_notes.strip() else ""

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
            <p style="font-size:14px; color:#f3e5ab; margin-bottom:5px;">🏛️ التجمع الصحي الثاني - إدارة الخدمات الصيدلانية لمراكز الرعاية الصحية الأولية</p>
            <h2>تقرير تقييم الأدوية المخدرة والمؤثرات العقلية</h2>
            <p><strong>اسم المركز:</strong> {display_center} | <strong>المفتش / المُقيم:</strong> {display_inspector} | <strong>التاريخ والوقت:</strong> {inspection_date.strftime('%Y/%m/%d')} - {formatted_time_str}</p>
            <p><strong>نسبة الامتثال الإجمالية:</strong> {compliance_rate:.2f}%</p>
        </div>
        {display_notes_html}
        <h3>📋 تفاصيل بنود التفتيش والملاحظات:</h3>
    """

    for sec_name, items in sections.items():
        html_report += f"<h4>🔹 {sec_name}</h4><table><tr><th>م</th><th>المعيار</th><th>الحالة</th><th>ملاحظات المفتش / المُقيم</th></tr>"
        sec_responses = [r for r in responses if r["section"] == sec_name]
        for it in sec_responses:
            st_text = it["status"] if it["status"] else "غير محدد"
            status_class = "warning" if st_text == "جزئي" else ("danger" if st_text in ["غير مطابق", "غير محدد"] else "")
            html_report += f"<tr><td>{it['id']}</td><td>{it['criterion']}</td><td class='{status_class}'>{st_text}</td><td>{it['notes']}</td></tr>"
        html_report += "</table>"
    html_report += "</body></html>"

    components.html(html_report, height=700, scrolling=True)

# ==========================================
# 7. تذييل الصفحة الرسمي
# ==========================================
st.markdown("---")
st.caption("إدارة الخدمات الصيدلانية - تجمع الرياض الصحي الثاني")
