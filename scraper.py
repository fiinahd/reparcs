import time
import random
from datetime import datetime, timezone, timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, NoSuchElementException, ElementClickInterceptedException)
from bs4 import BeautifulSoup
import config

def scrape_tokopedia_reviews():
    """Scrape review dari config.URL hingga config.MAX_PAGES halaman."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={config.USER_AGENT}")

    driver = webdriver.Chrome(options=chrome_options)
    all_reviews = []

    try:
        driver.get(config.URL)
        time.sleep(random.uniform(4, 6))

        current_page = 1
        while current_page <= config.MAX_PAGES:
            # Scroll
            for _ in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(0.5, 1.5))

            soup = BeautifulSoup(driver.page_source, "html.parser")
            reviews = soup.find_all(
                "article",
                class_=config.ARTICLE_CLASS
            )

            print(f"[Page {current_page}] Ditemukan {len(reviews)} review")

            for review in reviews:
                tz_jkt = timezone(timedelta(hours=7))
                now = datetime.now(tz_jkt)
                ms2 = now.strftime("%f")[:2]  # dua digit milidetik
                scraped_at = f"{now.strftime('%Y-%m-%d_%H:%M:%S')}.{ms2}"

                # ekstract
                product_name = review.find(
                    "p", class_=config.PRODUCT_NAME_CLASS
                )
                product_name = product_name.text.strip() if product_name else "Tidak tersedia"

                product_variant = review.find(
                    "p", class_=config.PRODUCT_VARIANT_CLASS
                )
                product_variant = product_variant.text.strip() if product_variant else "Tidak tersedia"

                rating_el = review.find(
                    "div", {"data-testid": config.RATING_DATA_TESTID}
                )
                rating = len(rating_el.find_all("svg")) if rating_el else 0

                review_time = review.find(
                    "p", class_=config.REVIEW_TIME_CLASS
                )
                review_date = review_time.text.strip() if review_time else "Tidak tersedia"

                reviewer_el = review.find(
                    "span", class_=config.REVIEWER_NAME_CLASS
                )
                reviewer_name = reviewer_el.text.strip() if reviewer_el else "Anonim"

                review_text_el = review.find(
                    "span", {"data-testid": config.REVIEW_TEXT_DATA_TESTID}
                )
                review_text = review_text_el.text.strip() if review_text_el else "Tidak ada ulasan"

                all_reviews.append({
                    "scraped_at":       scraped_at,
                    "review_date":      review_date,
                    "product_name":     product_name,
                    "product_variant":  product_variant,
                    "reviewer_name":    reviewer_name,
                    "rating":           rating,
                    "review_text":      review_text,
                })

            # next
            try:
                nxt = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, config.NEXT_BUTTON_SELECTOR))
                )
                driver.execute_script("arguments[0].click();", nxt)
                time.sleep(random.uniform(3, 5))
                current_page += 1

            except (TimeoutException, NoSuchElementException):
                print("→ Tidak ada halaman berikutnya, scraping selesai.")
                break

            except ElementClickInterceptedException:
                print("→ Tombol next terhalang, coba alternatif klik.")
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", nxt)
                    time.sleep(1)
                    nxt.click()
                    time.sleep(random.uniform(3, 5))
                    current_page += 1
                except Exception:
                    print("→ Gagal klik next lagi, hentikan.")
                    break

    finally:
        driver.quit()

    df = pd.DataFrame(all_reviews)
    df.to_excel(config.OUTPUT_FILE, index=False, engine="openpyxl")
    print(f"\n Selesai! Total review disimpan: {len(df)}")
    print(f"  File output: {config.OUTPUT_FILE}")

    return df

if __name__ == "__main__":
    scrape_tokopedia_reviews()
