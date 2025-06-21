URL = "https://www.tokopedia.com/eigeradventure/review"  # :contentReference[oaicite:0]{index=0}
MAX_PAGES = 3  # :contentReference[oaicite:1]{index=1}
OUTPUT_FILE = "treviews.xlsx"  # :contentReference[oaicite:2]{index=2}

# CSS selector / class
ARTICLE_CLASS             = "css-1pr2lii"               # blok review :contentReference[oaicite:3]{index=3}
PRODUCT_NAME_CLASS        = "css-akhxpb-unf-heading"    # nama produk :contentReference[oaicite:4]{index=4}
PRODUCT_VARIANT_CLASS     = "css-19mbq85-unf-heading"   # varian produk :contentReference[oaicite:5]{index=5}
RATING_DATA_TESTID        = "icnStarRating"            # rating element :contentReference[oaicite:6]{index=6}
REVIEW_TIME_CLASS         = "css-1rpz5os-unf-heading"   # waktu ulasan :contentReference[oaicite:7]{index=7}
REVIEWER_NAME_CLASS       = "name"                      # nama reviewer :contentReference[oaicite:8]{index=8}
REVIEW_TEXT_DATA_TESTID    = "lblItemUlasan"            # teks review :contentReference[oaicite:9]{index=9}

# Selector "Laman berikutnya"
NEXT_BUTTON_SELECTOR      = "button[aria-label='Laman berikutnya']"  # :contentReference[oaicite:10]{index=10}

# User agent untuk menghindari deteksi bot
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/90.0.4430.93 Safari/537.36"
)
