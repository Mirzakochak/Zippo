import base64
import requests

# ۳ منبع معتبر و پرسرعت گیت‌هاب
SOURCE_SUBS = [
    "https://raw.githubusercontent.com/Danialsamadi/v2go/main/AllConfigsSub.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity.txt",
    "https://raw.githubusercontent.com/sevcator/5ubscrpt10n/main/protocols/vl.txt"
]

# تعداد دقیق کانفیگ دریافتی از هر منبع
CONFIGS_PER_SOURCE = 100

def fix_base64_padding(b64_string):
    """رفع مشکل پدینگ ساب‌لینک‌ها برای جلوگیری از کرش پایتون"""
    padding = len(b64_string) % 4
    if padding != 0:
        b64_string += '=' * (4 - padding)
    return b64_string

def fetch_and_decode(url):
    """دریافت ساب‌لینک و استخراج کانفیگ‌های vless و vmess"""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        text_content = response.text.strip()
        
        # تشخیص خودکار فرمت محتوا (متن خام یا Base64)
        if text_content.startswith(("vmess://", "vless://", "trojan://")):
            raw_text = text_content
        else:
            b64_text = fix_base64_padding(text_content)
            raw_text = base64.b64decode(b64_text).decode('utf-8', errors='ignore')
            
        # فیلتر کردن کانفیگ‌ها
        configs = []
        for line in raw_text.splitlines():
            line = line.strip()
            if line.startswith(("vless://", "vmess://")):
                configs.append(line)
        return configs
    except Exception as e:
        print(f"❌ خطا در دریافت از سورس: {url}\nدلیل: {e}")
        return []

def main():
    final_300_configs = []
    
    print("🚀 شروع فرآیند استخراج دقیق ۳۰۰ کانفیگ...\n")
    
    for index, url in enumerate(SOURCE_SUBS, 1):
        sourse_name = url.split('/')[-2]
        print(f"⏳ بررسی سورس شماره {index} ({sourse_name})...")
        
        raw_configs = fetch_and_decode(url)
        
        # حذف تکراری‌های احتمالی درون خودِ این سورس
        unique_source_configs = []
        for cfg in raw_configs:
            if cfg not in unique_source_configs:
                unique_source_configs.append(cfg)
        
        # گلچین کردن دقیق ۱۰۰ کانفیگ اول از این سورس
        selected_configs = unique_source_configs[:CONFIGS_PER_SOURCE]
        
        # اضافه کردن به لیست نهایی
        final_300_configs.extend(selected_configs)
        print(f"✅ تعداد {len(selected_configs)} کانفیگ با موفقیت جدا شد.\n")

    # بررسی نهایی تعداد کل کانفیگ‌ها
    total_count = len(final_300_configs)
    if total_count == 0:
        print("⚠️ هیچ کانفیگی پیدا نشد!")
        return

    # تبدیل ۳۰۰ کانفیگ نهایی به فرمت استاندارد Base64
    final_text = "\n".join(final_300_configs)
    final_b64 = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')
    
    # ذخیره در فایل خروجی
    with open("my_sub.txt", "w", encoding="utf-8") as f:
        f.write(final_b64)
        
    print("--------------------------------------------------")
    print(f"🎉 عملیات با موفقیت پایان یافت!")
    print(f"📦 فایل 'my_sub.txt' شامل دقیقاً {total_count} لینک اشتراک ساخته شد.")
    print("--------------------------------------------------")

if __name__ == "__main__":
    main()
