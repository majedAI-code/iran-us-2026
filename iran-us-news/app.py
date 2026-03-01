import streamlit as st
import feedparser
from datetime import datetime
import socket

# إعدادات الصفحة
st.set_page_config(page_title="إحاطة | رصد وتحليل", page_icon="📡", layout="centered")

# إضافة CSS مخصص
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #1a1d24; }
    .header-box { background-color: #14161b; padding: 20px; border-bottom: 3px solid #e11d48; text-align: center; margin-bottom: 20px; border-radius: 0 0 10px 10px; }
    .news-card { background-color: #21252d; border: 1px solid #2d333f; padding: 20px; border-radius: 12px; margin-bottom: 12px; }
    .source-tag { color: #3b82f6; font-size: 12px; font-weight: bold; margin-bottom: 8px; }
    .news-title { color: #ffffff !important; font-size: 18px; font-weight: bold; text-decoration: none; line-height: 1.5; }
    .news-meta { color: #94a3b8; font-size: 11px; margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px; }
    </style>
    <div class="header-box">
        <h1 style="color: white; margin:0;">إحاطة</h1>
        <p style="color: #10b981; font-size: 12px; margin-top:5px;">● جاري جلب احدث الاخبار ..</p>
    </div>
""", unsafe_allow_html=True)

SOURCES = [
    {"name": "الجزيرة", "url": "https://www.aljazeera.net/xml/rss/all.xml"},
    {"name": "العربية", "url": "https://www.alarabiya.net/ar/tools/rss.xml"},
    {"name": "سكاي نيوز", "url": "https://www.skynewsarabia.com/web/rss"},
    {"name": "BBC News", "url": "https://feeds.bbci.co.uk/news/world/rss.xml"},
    {"name": "Reuters", "url": "https://www.reutersagency.com/feed/?best-topics=political-general&format=xml"}
]

def fetch_news():
    all_entries = []
    # إضافة User-Agent لتجنب الحظر من المصادر العربية
    feedparser.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    for src in SOURCES:
        try:
            # تعيين وقت مهلة (Timeout) لضمان عدم تعليق التطبيق
            socket.setdefaulttimeout(10)
            feed = feedparser.parse(src['url'])
            for entry in feed.entries:
                dt = datetime.now()
                if hasattr(entry, 'published_parsed'):
                    dt = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed'):
                    dt = datetime(*entry.updated_parsed[:6])
                
                all_entries.append({
                    "title": entry.title,
                    "link": entry.link,
                    "source": src['name'],
                    "date": dt
                })
        except Exception as e:
            continue
    
    return sorted(all_entries, key=lambda x: x['date'], reverse=True)

news_data = fetch_news()

if not news_data:
    st.warning("تعذر جلب الأخبار حالياً، يرجى المحاولة مرة أخرى.")
else:
    for item in news_data[:40]:
        st.markdown(f"""
            <div class="news-card">
                <div class="source-tag">{item['source']}</div>
                <a href="{item['link']}" target="_blank" class="news-title">{item['title']}</a>
                <div class="news-meta">
                    🕒 {item['date'].strftime('%I:%M %p')} | 📅 {item['date'].strftime('%Y-%m-%d')}
                </div>
            </div>
        """, unsafe_allow_html=True)

if st.button("🔄 تحديث يدوي للرصد"):
    st.rerun()