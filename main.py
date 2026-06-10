import base64
import requests

# معتبرترین سورس‌های گیت‌هاب که مرتب آپدیت می‌شوند
SOURCE_SUBS = [
    # سورس 1: ریپازیتوری V2go (آپدیت هر ۶ ساعت، بدون کانفیگ تکراری)
    "https://raw.githubusercontent.com/Danialsamadi/v2go/main/AllConfigsSub.txt",
    
    # سورس 2: ریپازیتوری معروف Mahdibland (تجمیع‌کننده بزرگ Eternity)
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity.txt",
    
    # سورس 3: ریپازیتوری Sevcator (کالکشن اختصاصی vless و vmess)
    "https://raw.githubusercontent.com/sevcator/5ubscrpt10n/main/protocols/vl.txt"
]

CONFIGS_PER_SOURCE = 100

def fix_base64_padding(b64_string):
    """رفع مشکل پدینگ Base64 در ساب‌لینک‌ها"""
    padding = len(b64_string) % 4
    if padding != 0:
        b64_string += '=' * (4 - padding)
    return b64_string

def fetch_and_decode(url):
    """دریافت ساب‌لینک و تشخیص هوشمند Base64 یا متن خام"""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        text_content = response.text.strip()
        
        # تشخیص اینکه آیا محتوا از قبل متن خام است یا باید Base64 دیکد شود
        if text_content.startswith(("vmess://", "vless://", "trojan://")):
            raw_text = text_content
        else:
            b64_text = fix_base64_padding(text_content)
            raw_text = base64.b64decode(b64_text).decode('utf-8', errors='ignore')
            
        # فیلتر کردن و جداسازی کانفیگ‌های vless و vmess
        configs = []
        for line in raw_text.splitlines():
            line = line.strip()
            if line.startswith(("vless://", "vmess://")):
                configs.append(line)
                
        return configs
    except Exception as e:
        print(f"❌ خطا در دریافت از سورس:\n{url}\nدلیل خطا: {e}\n")
        return []

def main():
    all_configs = []
    
    print("🚀 در حال استخراج کانفیگ‌ها از سورس‌های معتبر گیت‌هاب...\n")
    
    for url in SOURCE_SUBS:
        print(f"⏳ در حال بررسی: {url.split('/')[-2]}/{url.split('/')[-1]}")
        configs = fetch_and_decode(url)
        
        # برداشتن دقیق ۱۰۰ کانفیگ از هر سورس (یا کمتر اگر موجودی سورس کمتر بود)
        selected_configs = configs[:CONFIGS_PER_SOURCE]
        all_configs.extend(selected_configs)
        
        print(f"✅ {len(selected_configs)} کانفیگ استخراج شد.\n")

    if not all_configs:
        print("⚠️ متأسفانه هیچ کانفیگی یافت نشد! وضعیت اینترنت یا لینک‌ها را بررسی کنید.")
        return

    # حذف کانفیگ‌های تکراری احتمالی بین سورس‌های مختلف
    unique_configs = list(set(all_configs))
    
    # ترکیب نهایی و تبدیل به فرمت استاندارد ساب‌لینک (Base64)
    final_text = "\n".join(unique_configs)
    final_b64 = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')
    
    # ذخیره در فایل
    with open("my_sub.txt", "w", encoding="utf-8") as f:
        f.write(final_b64)
        
    print(f"🎉 عملیات موفقیت‌آمیز بود!")
    print(f"🔥 ساب‌لینک نهایی شما با {len(unique_configs)} کانفیگ خالص و بدون تکرار در فایل 'my_sub.txt' ذخیره شد.")

if __name__ == "__main__":
    main()
