import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

RAW = os.path.join(ROOT, "data", "raw")
COST_FILES = [
    "01_خدمات_فناوری_خرداد_1405.xlsx",
    "02_پشتیبانی_خرداد_1405.xlsx",
    "04_خدمات_فناوری_تیر_1405.xlsx",
    "05_پشتیبانی_تیر_1405.xlsx",
]
HEADCOUNT_FILES = [
    "03_تعداد_نفرات_خرداد_1405.xlsx",
    "06_تعداد_نفرات_تیر_1405.xlsx",
]
