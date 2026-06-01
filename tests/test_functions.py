import pytest
import sys
sys.path.append(".")
from functions import *
from pathlib import Path

#parametrized testing via pytest
filepathbought = Path("tests/bought.csv")
filepathsold = Path("tests/sold.csv")
filepathexpirated = Path("tests/expired.csv")
timefilepath = Path("tests/superpytime.txt")

def test_valid_date():
    assert valid_date("2026-10-12") == dt.date(2026, 10, 12)
    


def test_add_product():
    add_product("Milk", "1.8", "2027-10-12", filepathbought)
    assert filepathbought.exists()
    with filepathbought.open("r", newline="") as boughtfile:
        last_item = list(csv.DictReader(boughtfile))[-1]
        assert last_item["Product Name"] == "Milk" 
        assert last_item["Buy Price"] == "1.8" 
        assert last_item["Expiration Date"] == "2027-10-12"

def test_sell_product():
    add_product("Orange", "1.8", "2027-10-12", filepathbought)
    sell_product("Orange", "2.5", filepathbought, filepathsold)
    selldate = superpy_time
    with filepathbought.open("r", newline="") as boughtfile:
        last_item = list(csv.DictReader(boughtfile))[-1]
        assert last_item["Sell Date"] == superpy_time.strftime("%Y-%m-%d")
    with filepathsold.open("r", newline="") as soldfile:
        last_item = list(csv.DictReader(soldfile))[-1]
        assert last_item["Product Name"] == "Orange" 
        assert last_item["Buy Price"] == "1.8" 
        assert last_item["Expiration Date"] == "2027-10-12"
        assert last_item["Sell Price"] == "2.5"


# add_product("Apple", "1.8", "2026-10-12")
# add_product("Apple", "1.8", "2026-10-12")
# add_product("oRAnge", "2", "2026-10-12")
# add_product("Orange", "2", "2026-10-12")
# add_product("Apple", "1.8", "2026-10-12")
# add_product("Apple", "1.8", "2026-10-12")
# add_product("Banana", "50", "2020-10-12")
# add_product("bAnana", "1.8", "2026-10-12")
# add_product("Milk", "1.8", "2020-10-12")
# add_product("Milk", "1.8", "2027-10-12")
# # sell_product("Orange", "1.8")

# #report_inventory("yesterday")

# #report_revenue("yesterday")

# testmonth = dt.date.strptime("2026-05", "%Y-%m")
# barplot_monthprofit(testmonth)