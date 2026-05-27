import pytest
from functions import *
from pathlib import Path
filepathbought = Path("bought.csv")


def test_add_product():
    add_product("Milk", "1.8", "2027-10-12")
    assert filepathbought.exists()
    with filepathbought.open("r", newline="") as boughtfile:
        last_item = list(csv.DictReader(boughtfile))[-1]
        assert last_item["Product Name"] == "Milk" 
        assert last_item["Buy Price"] == "1.8" 
        assert last_item["Expiration Date"] == "2027-10-12"

#def test_sell_product():


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