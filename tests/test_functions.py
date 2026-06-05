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
    set_time(valid_date("2026-5-10"))
    file_pathbought = tmp_path / "bought.csv"
    file_pathsold = tmp_path / "sold.csv"
    add_product("Orange", "1.8", "2027-10-12", file_pathbought)
    sell_product("Orange", "2.5", file_pathbought, file_pathsold)
    #selldate = superpy_time
    with file_pathbought.open("r", newline="") as boughtfile:
        last_item = list(csv.DictReader(boughtfile))[-1]
        assert last_item["Sell Date"] == "2026-05-10"
    with file_pathsold.open("r", newline="") as soldfile:
        last_item = list(csv.DictReader(soldfile))[-1]
        assert last_item["Product Name"] == "Orange" 
        assert last_item["Buy Price"] == "1.8" 
        assert last_item["Expiration Date"] == "2027-10-12"
        assert last_item["Sell Price"] == "2.5"

def test_sell_report_inventory(tmp_path, capsys):
    bought_file = tmp_path / "bought.csv"
    sold_file = tmp_path / "sold.csv"
    set_time(valid_date("2026-5-10"))
    add_product("Orange", "1.80", "2026-12-31", bought_file)
    add_product("Strawberry", "3", "2026-12-31", bought_file)
    sell_product("Orange", "2.50", bought_file, sold_file)
    report_inventory("now", bought_file)
    captured = capsys.readouterr()
    assert "Orange" not in captured.out

def test_count_report_inventory(tmp_path, capsys):
    bought_file = tmp_path / "bought.csv"
    set_time(valid_date("2026-5-10"))
    add_product("Orange", "1.80", "2026-12-31", bought_file)
    add_product("Orange", "1.80", "2026-12-31", bought_file)
    add_product("Strawberry", "3", "2026-12-31", bought_file)
    report_inventory("now", bought_file)
    captured = capsys.readouterr()
    assert "Orange" in captured.out
    assert "2" in captured.out

def test_report_expired(tmp_path, capsys):
    bought_file = tmp_path / "bought.csv"
    set_time(valid_date("2026-5-10"))
    add_product("Orange", "3", "2026-02-10", bought_file)
    report_expired("now", bought_file)
    captured = capsys.readouterr()
    assert "Orange" in captured.out
    assert "3" in captured.out
    assert "2026-02-10" in captured.out

def test_report_nonexpired(tmp_path, capsys):
    bought_file = tmp_path / "bought.csv"
    set_time(valid_date("2026-5-10"))
    add_product("Orange", "3", "2026-06-10", bought_file)
    report_expired("now", bought_file)
    captured = capsys.readouterr()
    assert "Orange" not in captured.out
    assert "3" not in captured.out
    assert "2026-06-10" not in captured.out

### Revenue tests
def test_report_todays_revenue(tmp_path):
    bought_file = tmp_path / "bought.csv"
    sold_file = tmp_path / "sold.csv"
    set_time(valid_date("2026-5-10"))
    add_product("Orange", "1.80", "2026-12-31", bought_file)
    add_product("Orange", "1.80", "2026-12-31", bought_file)
    add_product("Strawberry", "3", "2026-12-31", bought_file)
    add_product("Strawberry", "3", "2026-12-31", bought_file)
    add_product("Strawberry", "3", "2026-12-31", bought_file)
    sell_product("Orange", "2.50", bought_file, sold_file)
    sell_product("Strawberry", "5", bought_file, sold_file)
    result = report_revenue("today", sold_file)
    # Orange revenue: 2.50 Strawberry revenue: 5
    assert result == 7.50

def test_report_yesterdays_revenue1(tmp_path):
    bought_file = tmp_path / "bought.csv"
    sold_file = tmp_path / "sold.csv"
    set_time(valid_date("2026-5-10"))
    add_product("Orange", "1.80", "2026-12-31", bought_file)
    add_product("Orange", "1.80", "2026-12-31", bought_file)
    add_product("Strawberry", "3", "2026-12-31", bought_file)
    sell_product("Orange", "2.50", bought_file, sold_file)
    sell_product("Strawberry", "5", bought_file, sold_file)
    result = report_revenue("yesterday", sold_file)
    # Nothing was sold yesterday
    assert result == 0

def test_report_yesterdays_revenue2(tmp_path):
    bought_file = tmp_path / "bought.csv"
    sold_file = tmp_path / "sold.csv"
    time_path = tmp_path / "superpytime.txt"
    set_time(valid_date("2026-5-10"))
    add_product("Orange", "1.80", "2026-12-31", bought_file)
    add_product("Orange", "1.80", "2026-12-31", bought_file)
    add_product("Strawberry", "3", "2026-12-31", bought_file)
    sell_product("Orange", "2.50", bought_file, sold_file)
    sell_product("Strawberry", "5", bought_file, sold_file)
    #advance 1 day so the above was sold yesterday
    advanced_time(1, time_path)
    result = report_revenue("yesterday", sold_file)
    # Strawberry and Orange was sold yesterdy was sold yesterday
    assert result == 7.50

def test_report_month_revenue(tmp_path):
    bought_file = tmp_path / "bought.csv"
    sold_file = tmp_path / "sold.csv"
    set_time(valid_date("2026-5-10"))
    add_product("Orange", "1.80", "2026-12-31", bought_file)
    add_product("Strawberry", "3", "2026-12-31", bought_file)
    sell_product("Orange", "2.50", bought_file, sold_file)
    result = report_revenue(valid_month("2026-05"), sold_file)
    #only orange was sold
    assert result == 2.50

### Profit tests
def test_report_todays_profit(tmp_path):
    bought_file = tmp_path / "bought.csv"
    sold_file = tmp_path / "sold.csv"
    set_time(valid_date("2026-5-10"))
    add_product("Orange", "1.80", "2026-12-31", bought_file)
    add_product("Orange", "1.80", "2026-12-31", bought_file)
    add_product("Strawberry", "3", "2026-12-31", bought_file)
    add_product("Strawberry", "3", "2026-12-31", bought_file)
    add_product("Strawberry", "3", "2026-12-31", bought_file)
    sell_product("Orange", "2.50", bought_file, sold_file)
    sell_product("Strawberry", "5", bought_file, sold_file)
    result = report_profit("today", sold_file)
    # Orange: (2.5 - 1.8) = 0.7
    # Strawberry: (5 - 3) = 2
    assert result == 2.7

def test_report_yesterday_profit1(tmp_path):
    bought_file = tmp_path / "bought.csv"
    sold_file = tmp_path / "sold.csv"
    set_time(valid_date("2026-5-10"))
    add_product("Orange", "1.80", "2026-12-31", bought_file)
    add_product("Orange", "1.80", "2026-12-31", bought_file)
    add_product("Strawberry", "3", "2026-12-31", bought_file)
    sell_product("Orange", "2.50", bought_file, sold_file)
    sell_product("Strawberry", "5", bought_file, sold_file)
    result = report_profit("yesterday", sold_file)
    assert result == 0

def test_report_yesterday_profit2(tmp_path):
    bought_file = tmp_path / "bought.csv"
    sold_file = tmp_path / "sold.csv"
    time_path = tmp_path / "superpytime.txt"
    set_time(valid_date("2026-5-10"))
    add_product("Orange", "1.80", "2026-12-31", bought_file)
    add_product("Strawberry", "3", "2026-12-31", bought_file)
    sell_product("Orange", "2.50", bought_file, sold_file)
    sell_product("Strawberry", "5", bought_file, sold_file)
    advanced_time(1, time_path)
    result = report_profit("yesterday", sold_file)
    # Strawberry + Orange both count as "yesterday"
    # Orange: 0.7 + Strawberry: 2.0
    assert result == 2.7

def test_report_month_profit(tmp_path):
    bought_file = tmp_path / "bought.csv"
    sold_file = tmp_path / "sold.csv"
    set_time(valid_date("2026-5-10"))
    add_product("Orange", "1.80", "2026-12-31", bought_file)
    add_product("Strawberry", "3", "2026-12-31", bought_file)
    sell_product("Orange", "2.50", bought_file, sold_file)
    result = report_profit(valid_month("2026-05"), sold_file)
    # only Orange sold in May
    assert result == 0.7

### Loss
def test_report_todays_loss(tmp_path):
    bought_file = tmp_path / "bought.csv"
    set_time(valid_date("2026-5-10"))
    add_product("Orange", "1.80", "2026-05-10", bought_file)
    add_product("Strawberry", "3", "2026-05-10", bought_file)
    result = report_loss("today", bought_file)
    assert result == 4.80

def test_report_yesterday_loss(tmp_path):
    bought_file = tmp_path / "bought.csv"
    sold_file = tmp_path / "sold.csv"
    time_path = tmp_path / "superpytime.txt"
    set_time(valid_date("2026-5-10"))
    add_product("Orange", "1.80", "2026-05-11", bought_file)
    add_product("Orange", "1.80", "2026-05-10", bought_file)
    add_product("Strawberry", "3", "2026-05-10", bought_file)
    sell_product("Strawberry", "5", bought_file, sold_file)
    #advance 1 day to the future
    advanced_time(1, time_path)
    sell_product("Orange", "2.50", bought_file, sold_file)
    result = report_loss("yesterday", bought_file)
    assert result == 1.80

def test_report_month_loss(tmp_path):
    bought_file = tmp_path / "bought.csv"
    sold_file = tmp_path / "sold.csv"
    set_time(valid_date("2026-5-10"))
    add_product("Orange", "1.80", "2026-05-11", bought_file)
    add_product("Orange", "1.80", "2026-05-20", bought_file)
    add_product("Orange", "1.80", "2026-05-15", bought_file)
    add_product("Strawberry", "3", "2026-05-12", bought_file)
    sell_product("Orange", "2.50", bought_file, sold_file)
    result = report_loss(valid_month("2026-05"), bought_file)
    # only Orange sold in May
    assert result == 6.6

##### testing time values
def test_advanced_time(tmp_path):
    file_path = tmp_path / "superpytime.txt"
    superpytime_file(file_path)
    result_advancedtime = advanced_time(3, file_path)
    result_superpytime = superpytime_file(file_path)
    assert result_superpytime.strftime("%A %d %B %Y") == result_advancedtime

def test_set_time(tmp_path):
    file_path = tmp_path / "superpytime.txt"
    superpytime_file(file_path)
    resultdate = set_time(testdate, file_path)
    testdatefull = testdate.strftime("%A %d %B %Y")
    assert resultdate == testdatefull
    result = set_time("today", file_path)
    expected_today = dt.date.today()
    assert result == expected_today.strftime("%A %d %B %Y")
    with file_path.open() as timetoday:
        assert timetoday.read() == expected_today.strftime("%Y-%m-%d")
    result = set_time("yesterday", file_path)
    expected_yeasterday = dt.date.today() - dt.timedelta(days=1)
    assert result == expected_yeasterday.strftime("%A %d %B %Y")
    with file_path.open() as timeyesterday:
        assert timeyesterday.read() == expected_yeasterday.strftime("%Y-%m-%d")


