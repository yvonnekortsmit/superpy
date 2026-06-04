import pytest
import sys
sys.path.append(".")
from functions import *
from pathlib import Path

#parametrized testing via pytest
testdatestring = "2026-10-12"
testdate = dt.datetime.strptime(testdatestring, "%Y-%m-%d").date()

def test_valid_date():
    assert valid_date("2026-10-12") == dt.datetime.strptime("2026-10-12", "%Y-%m-%d").date()
    assert valid_date("2026-10-12") == dt.date(2026, 10, 12)
    assert valid_date("2026-10-12") == dt.date(2026, 10, 12)
    assert valid_date("2026-10-12") == testdate
    
def test_valid_month():
    assert valid_month("2026-10") == dt.datetime.strptime("2026-10", "%Y-%m").date()
    assert valid_month("2026-10") == dt.date(2026, 10, 1)
    assert valid_month("2026-10").month == testdate.month
    assert valid_month("2026-10").year == testdate.year

def test_valid_year():
    assert valid_year("2026") == dt.datetime.strptime("2026", "%Y").date()
    assert valid_year("2026") == dt.date(2026, 1, 1)
    assert valid_year("2026").year == testdate.year

def test_superpytime_file(tmp_path):
    file_path = tmp_path / "superpytime.txt"
    superpytime_file(file_path)
    result = superpytime_file(file_path)
    assert file_path.exists()
    assert isinstance(result, dt.date)
    assert file_path.read_text().strip() == result.strftime("%Y-%m-%d")




def test_advanced_time(tmp_path):
    file_path = tmp_path / "superpytime.txt"
    superpytime_file(file_path)
    result = advanced_time(3, file_path)
    assert superpy_time == result



def test_add_product(tmp_path):
    file_path = tmp_path / "bought.csv"
    add_product("Milk", "1.8", "2027-10-12", file_path)
    assert file_path.exists()
    with file_path.open("r", newline="") as boughtfile:
        last_item = list(csv.DictReader(boughtfile))[-1]
        assert last_item["Product Name"] == "Milk" 
        assert last_item["Buy Price"] == "1.8" 
        assert last_item["Expiration Date"] == "2027-10-12"

def test_sell_product(tmp_path):
    file_pathbought = tmp_path / "bought.csv"
    file_pathsold = tmp_path / "sold.csv"
    add_product("Orange", "1.8", "2027-10-12", file_pathbought)
    sell_product("Orange", "2.5", file_pathbought, file_pathsold)
    selldate = superpy_time
    with file_pathbought.open("r", newline="") as boughtfile:
        last_item = list(csv.DictReader(boughtfile))[-1]
        assert last_item["Sell Date"] == superpy_time.strftime("%Y-%m-%d")
    with file_pathsold.open("r", newline="") as soldfile:
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