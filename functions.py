import csv
import datetime as dt 
from tabulate import tabulate
from pathlib import Path
import argparse
import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
import calendar
console = Console()
##variables
#other variables
file_pathbought = Path("bought.csv")
file_pathsold = Path("sold.csv")
time_filepath = Path("superpytime.txt")

#headers for csv
boughtheaders = ["ID", "Product Name", "Count", "Buy Price", "Expiration Date", "Buy Date", "Sell Date"]
soldheaders = ["ID", "ID bought","Product Name", "Count", "Buy Price", "Expiration Date", "Sell Price", "Buy Date", "Sell Date"]

##valid date for argparse with error message
def valid_date(date_string):
    try:
        return dt.datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Date must be in format YYYY-MM-DD"
        )

def valid_month(date_string):
    try:
        return dt.datetime.strptime(date_string, "%Y-%m").date()
    except ValueError:
        raise argparse.ArgumentTypeError("Date must be in format YYYY-MM")

def valid_year(date_string):
    try:
        return dt.datetime.strptime(date_string, "%Y").date()
    except ValueError:
        raise argparse.ArgumentTypeError("Date must be in format YYYY")
    
#functions for the parsers
#write the application file to an txt
def superpytime_file(timefilepath=time_filepath):
    if not timefilepath.exists():
        with timefilepath.open("w", newline="") as timefile:
            today = dt.datetime.today().date()
            timefile.write(today.strftime("%Y-%m-%d"))
    with timefilepath.open("r") as timefile:
        saved_date = timefile.read().strip()
    return dt.datetime.strptime(saved_date, "%Y-%m-%d").date()
superpy_time = superpytime_file()

##########
#Time functions
def advanced_time(advanced_days:int,timefilepath=time_filepath):
    global superpy_time
    superpy_time += dt.timedelta(days=advanced_days)
    with timefilepath.open("w") as timefile:
        timefile.write(superpy_time.strftime("%Y-%m-%d"))
    superpy_date = superpy_time.strftime("%A %d %B %Y")
    return superpy_date

def set_time(application_time, timefilepath=time_filepath):
    global superpy_time
    if application_time == "today":
        application_time = dt.date.today()
        print_app_time = application_time.strftime("%A %d %B %Y")
    elif application_time == "yesterday":
        application_time = dt.date.today() - dt.timedelta(days=1)
        print_app_time = application_time.strftime("%A %d %B %Y")
    else: #met datum zoals bv --date 2019-12
        print_app_time = application_time.strftime("%A %d %B %Y")
    superpy_time = application_time
    with timefilepath.open("w") as timefile:
        timefile.write(superpy_time.strftime("%Y-%m-%d"))
    return print_app_time

##########
#product functions
def add_product(product_name, buy_price:float, expiration_date, filepathbought=file_pathbought):
    buy_date = superpy_time 
    if not filepathbought.exists():
        with filepathbought.open("w", newline="") as boughtfile:
            writer = csv.DictWriter(boughtfile, fieldnames=boughtheaders)
            writer.writeheader()
    with filepathbought.open("r", newline="") as boughtfile:
        rows = list(csv.DictReader(boughtfile))
        # count van producten toevoegen
        if rows:
            new_id = (
                int(rows[-1]["ID"]) + 1
            )  # telt 1 bij de voorgaande ID op wanneer die al bestaat
        else:
            new_id = 1  # wanneer er geen voorgaande id is neemt hij 1
        added_product_name = product_name.strip().lower().capitalize()
        rows.append(
            {
                "ID": new_id,
                "Product Name": added_product_name,
                "Count": 1,
                "Buy Price": buy_price,
                "Expiration Date": expiration_date,
                "Buy Date": buy_date.strftime('%Y-%m-%d'),
            }
        )
    with filepathbought.open("w", newline="") as boughtfile:
        writer = csv.DictWriter(boughtfile, fieldnames=boughtheaders)
        writer.writeheader()
        writer.writerows(rows)


def sell_product(product_name, sell_price: float, filepathbought=file_pathbought, filepathsold=file_pathsold):
    sell_date = superpy_time 
    if not filepathsold.exists():
        with filepathsold.open("w", newline="") as soldfile:
            writer = csv.DictWriter(soldfile, fieldnames=soldheaders)
            writer.writeheader()
    with filepathbought.open("r", newline="") as boughtfile:
        boughtrows = list(csv.DictReader(boughtfile))
    with filepathsold.open("r", newline="") as soldfile:
        soldrows = list(csv.DictReader(soldfile))
    sold_row = None
    expired_product = False
    #kopieren van bought rows voor selling
    for row in boughtrows:
        expirationdate = dt.datetime.strptime(row["Expiration Date"], '%Y-%m-%d').date()
        if row["Product Name"].strip().lower() == product_name.strip().lower() and row["Sell Date"] == "":
            if sell_date > expirationdate:
                expired_product = True
                continue

            sold_row = row.copy() 
            row["Sell Date"] = sell_date.strftime('%Y-%m-%d')
            break
    #updaten van sold csv
    if sold_row:
        if soldrows:
            new_id = (
            int(soldrows[-1]["ID"]) + 1
            ) 
        else:
            new_id = 1
        soldrows.append(
            {
                "ID": new_id,
                "ID bought": sold_row["ID"],
                "Product Name": sold_row["Product Name"],
                "Count": 1,
                "Buy Price": sold_row["Buy Price"],
                "Sell Price": sell_price,
                "Expiration Date": sold_row["Expiration Date"],
                "Buy Date": sold_row["Buy Date"],
                "Sell Date": sell_date.strftime('%Y-%m-%d'),
            }
        )
    if sold_row is None:
        if expired_product:
            raise ValueError(f"{product_name.strip().title()} is expired and can not be sold.") 
        else:
            raise ValueError(f"{product_name.strip().title()} is not in stock.")
    #update sold file
    with filepathsold.open("w", newline="") as soldfile:
        writer = csv.DictWriter(soldfile, fieldnames=soldheaders)
        writer.writeheader()
        writer.writerows(soldrows)
    # update bought file
    with filepathbought.open("w", newline="") as boughtfile:
        writer = csv.DictWriter(boughtfile, fieldnames=boughtheaders)
        writer.writeheader()
        writer.writerows(boughtrows)


#Report functions
def report_inventory(inventory_time, filepathbought=file_pathbought):
    if inventory_time == "yesterday":
        inventory_time = superpy_time - dt.timedelta(days=1)
    elif inventory_time == "now":
        inventory_time = superpy_time
    with filepathbought.open("r", newline="") as boughtfile:
        rows = list(csv.DictReader(boughtfile))
        inventory = []
        for row in rows:
            buydate = dt.datetime.strptime(row["Buy Date"], '%Y-%m-%d').date()
            expirationdate = dt.datetime.strptime(row["Expiration Date"], '%Y-%m-%d').date()
            if row["Sell Date"] != "":
                selldate = dt.datetime.strptime(row["Sell Date"], "%Y-%m-%d").date()
            else:
                selldate = None
            if(
                buydate <= inventory_time 
                and (selldate is None or selldate > inventory_time)
                and inventory_time <= expirationdate): 
                matched_products = False
                for products in inventory:
                    matching_products = products["Product Name"] == row["Product Name"]
                    matching_price = products["Buy Price"] == row["Buy Price"]
                    matching_expirationdate = products["Expiration Date"] == row["Expiration Date"]
                    if matching_products and matching_price and matching_expirationdate:
                        products["Count"] += 1
                        matched_products = True
                        break
                if not matched_products:
                    inventory.append(
                        {
                            "Product Name": row["Product Name"],
                            "Count": 1,
                            "Buy Price": row["Buy Price"],
                            "Expiration Date": row["Expiration Date"],
                        }
                    )
        print(tabulate(inventory, headers="keys", tablefmt="grid"))

#Report functions
def report_expired(expiration_time, filepathbought=file_pathbought):
    if expiration_time == "yesterday":
        expiration_time = superpy_time - dt.timedelta(days=1)
    elif expiration_time == "now":
        expiration_time = superpy_time
    with filepathbought.open("r", newline="") as boughtfile:
        rows = list(csv.DictReader(boughtfile))
        expired = []
        for row in rows:
            buydate = dt.datetime.strptime(row["Buy Date"], '%Y-%m-%d').date()
            expirationdate = dt.datetime.strptime(row["Expiration Date"], '%Y-%m-%d').date()
            if row["Sell Date"] != "":
                selldate = dt.datetime.strptime(row["Sell Date"], "%Y-%m-%d").date()
            else:
                selldate = None
            if(
                buydate <= expiration_time 
                and (selldate is None or selldate > expiration_time)
                and expirationdate < expiration_time): 
                matched_products = False
                for products in expired:
                    matching_products = products["Product Name"] == row["Product Name"]
                    matching_price = products["Buy Price"] == row["Buy Price"]
                    matching_expirationdate = products["Expiration Date"] == row["Expiration Date"]
                    if matching_products and matching_price and matching_expirationdate:
                        products["Count"] += 1
                        matched_products = True
                        break
                if not matched_products:
                    expired.append(
                        {
                            "Product Name": row["Product Name"],
                            "Count": 1,
                            "Buy Price": row["Buy Price"],
                            "Expiration Date": row["Expiration Date"],
                        }
                    )
        print(tabulate(expired, headers="keys", tablefmt="grid"))

def report_revenue(revenue_time, filepathsold=file_pathsold):
    if revenue_time == "yesterday":
        revenue_time = superpy_time - dt.timedelta(days=1)
        time_period = "day"
    elif revenue_time == "today":
        revenue_time = superpy_time
        time_period = "day"
    else: #met datum zoals bv --date 2019-12
        revenue_time 
        time_period = "month"
    total_revenue = 0
    with filepathsold.open("r", newline="") as soldfile:
        rows = list(csv.DictReader(soldfile))
        for row in rows:
            buydate = dt.datetime.strptime(row["Buy Date"], '%Y-%m-%d').date()
            selldate = dt.datetime.strptime(row["Sell Date"], '%Y-%m-%d').date()
            revenue = float(row["Sell Price"]) * float(row["Count"])
            if time_period == "day":
                if buydate <= selldate <= revenue_time and selldate == revenue_time: 
                    total_revenue += revenue
            elif time_period == "month":
                if selldate.year == revenue_time.year and selldate.month == revenue_time.month:
                    total_revenue += revenue
    return total_revenue

def report_profit(profit_time, filepathsold=file_pathsold):
    if profit_time == "yesterday":
        profit_time = superpy_time - dt.timedelta(days=1)
        time_period = "day"
    elif profit_time == "today":
        profit_time = superpy_time
        time_period = "day"
    else: #met datum zoals bv --date 2019-12
        profit_time 
        time_period = "month"
    total_profit = 0
    with filepathsold.open("r", newline="") as soldfile:
        rows = list(csv.DictReader(soldfile))
        for row in rows:
            buydate = dt.datetime.strptime(row["Buy Date"], '%Y-%m-%d').date()
            selldate = dt.datetime.strptime(row["Sell Date"], '%Y-%m-%d').date()
            profit = (float(row["Sell Price"]) - float(row["Buy Price"])) * float(row["Count"])
            if time_period == "day":
                if buydate <= profit_time and selldate == profit_time: 
                    total_profit += profit
            elif time_period == "month":
                if selldate.year == profit_time.year and selldate.month == profit_time.month:
                    total_profit += profit
    return total_profit

def report_loss(loss_time, filepathbought=file_pathbought):
    if loss_time == "yesterday":
        loss_time = superpy_time - dt.timedelta(days=1)
        time_period = "day"
    elif loss_time == "today":
        loss_time = superpy_time
        time_period = "day"
    else: #met datum zoals bv --date 2019-12
        time_period = "month"
    total_loss = 0
    with filepathbought.open("r", newline="") as boughtfile:
        rows = list(csv.DictReader(boughtfile))
        for row in rows:
            buydate = dt.datetime.strptime(row["Buy Date"], '%Y-%m-%d').date()
            expirationdate = dt.datetime.strptime(row["Expiration Date"], '%Y-%m-%d').date()
            loss = (float(row["Buy Price"])) * float(row["Count"])
            if row["Sell Date"] != "":
                selldate = dt.datetime.strptime(row["Sell Date"], "%Y-%m-%d").date()
            else:
                selldate = None
                if time_period == "day":
                    if expirationdate == loss_time and (buydate <= loss_time and (selldate is None or selldate > loss_time)):
                        total_loss += loss
                elif time_period == "month":
                    if expirationdate.year == loss_time.year and expirationdate.month == loss_time.month and ((buydate.year <= loss_time.year and buydate.month <= loss_time.month) and (selldate is None or (selldate.year and selldate.month) > (loss_time.year and loss_time.month))):
                        total_loss += loss
    return total_loss

#########
### Plots
#########

### Profit
def barplot_monthprofit(profit_time, filepathsold=file_pathsold):
    profits = []
    days = []
    profit_time_month = profit_time.strftime("%Y-%m")
    print_profit_time = profit_time.strftime("%B %Y")
    year = profit_time.year
    month = profit_time.month
    num_days = calendar.monthrange(year, month)[1]
    profitdata = {day: 0 for day in range(1, num_days + 1)}
    with filepathsold.open("r", newline="") as soldfile:
        rows = list(csv.DictReader(soldfile))
        for row in rows:
            selldate = dt.datetime.strptime(row["Sell Date"], '%Y-%m-%d').date()
            if selldate.strftime("%Y-%m") == profit_time_month:
                day = selldate.day
                profit = (float(row["Sell Price"]) - float(row["Buy Price"])) * float(row["Count"])
                if day in profitdata:
                    profitdata[day] = profitdata[day] + profit
                else:
                    profitdata[day] = profit  
    #list for plot
    for day in sorted(profitdata):
        days.append(day)
        profits.append(profitdata[day])

    #plot
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(days, profits, width=0.8)
    ax.set(
        xlabel="Day of month",
        ylabel="Profit (€)",
        title=f"Profit per day - {print_profit_time}"
    )
    ax.set_xticks(days)
    plt.show()

def barplot_yearprofit(profit_time, filepathsold=file_pathsold):
    profits = []
    months = []
    profitdata = {month: 0 for month in range(1, 13)} #0 as temporary profit for all months
    profit_time_year = profit_time.year
    print_profit_time = profit_time.year
    with filepathsold.open("r", newline="") as soldfile:
        rows = list(csv.DictReader(soldfile))
        for row in rows:
            selldate = dt.datetime.strptime(row["Sell Date"], '%Y-%m-%d').date()
            if selldate.year == profit_time_year:
                month = selldate.month
                profit = (float(row["Sell Price"]) - float(row["Buy Price"])) * float(row["Count"])
                if month in profitdata:
                    profitdata[month] = profitdata[month] + profit
                else:
                    profitdata[month] = profit  
    #list for plot
    for month in sorted(profitdata):
        months.append(month)
        profits.append(profitdata[month])

    #plot
    fig, ax = plt.subplots()
    ax.bar(months, profits, width=0.8)
    ax.set(
        xlabel="Month",
        ylabel="Profit (€)",
        title=f"Profit per month - {print_profit_time}"
    )
    ax.set_xticks(months)
    plt.show()

## Revenue
def barplot_monthrevenue(revenue_time, filepathsold=file_pathsold):
    revenues = []
    days = []
    revenue_time_month = revenue_time.strftime("%Y-%m")
    print_revenue_time = revenue_time.strftime("%B %Y")
    year = revenue_time.year
    month = revenue_time.month
    num_days = calendar.monthrange(year, month)[1]
    revenuedata = {day: 0 for day in range(1, num_days + 1)}
    with filepathsold.open("r", newline="") as soldfile:
        rows = list(csv.DictReader(soldfile))
        for row in rows:
            selldate = dt.datetime.strptime(row["Sell Date"], '%Y-%m-%d').date()
            if selldate.strftime("%Y-%m") == revenue_time_month:
                day = selldate.day
                revenue = float(row["Sell Price"]) * float(row["Count"])
                if day in revenuedata:
                    revenuedata[day] = revenuedata[day] + revenue
                else:
                    revenuedata[day] = revenue  
    #list for plot
    for day in sorted(revenuedata):
        days.append(day)
        revenues.append(revenuedata[day])

    #plot
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(days, revenues, width=0.8)
    ax.set(
        xlabel="Day of month",
        ylabel="Revenue (€)",
        title=f"Revenue per day - {print_revenue_time}"
    )
    ax.set_xticks(days)
    plt.show()

def barplot_yearrevenue(revenue_time, filepathsold=file_pathsold):
    revenues = []
    months = []
    revenuedata = {month: 0 for month in range(1, 13)} #0 as temporary revenue for all months
    revenue_time_year = revenue_time.year
    print_revenue_time = revenue_time.year
    with filepathsold.open("r", newline="") as soldfile:
        rows = list(csv.DictReader(soldfile))
        for row in rows:
            selldate = dt.datetime.strptime(row["Sell Date"], '%Y-%m-%d').date()
            if selldate.year == revenue_time_year:
                month = selldate.month
                revenue = float(row["Sell Price"]) * float(row["Count"])
                if month in revenuedata:
                    revenuedata[month] = revenuedata[month] + revenue
                else:
                    revenuedata[month] = revenue  
    #list for plot
    for month in sorted(revenuedata):
        months.append(month)
        revenues.append(revenuedata[month])

    #plot
    fig, ax = plt.subplots()
    ax.bar(months, revenues, width=0.8)
    ax.set(
        xlabel="Month",
        ylabel="Revenue (€)",
        title=f"Revenue per month - {print_revenue_time}"
    )
    ax.set_xticks(months)
    plt.show()

## Loss
def barplot_monthloss(loss_time, filepathbought=file_pathbought):
    losses = []
    days = []
    loss_time_month = loss_time.strftime("%Y-%m")
    print_loss_time = loss_time.strftime("%B %Y")
    year = loss_time.year
    month = loss_time.month
    num_days = calendar.monthrange(year, month)[1]
    lossdata = {day: 0 for day in range(1, num_days + 1)}
    with filepathbought.open("r", newline="") as boughtfile:
        rows = list(csv.DictReader(boughtfile))
        for row in rows:
            if row["Sell Date"] != "":
                selldate = dt.datetime.strptime(row["Sell Date"], "%Y-%m-%d").date()
            else:
                selldate = None
            expirationdate = dt.datetime.strptime(row["Expiration Date"], '%Y-%m-%d').date()
            if expirationdate.strftime("%Y-%m") == loss_time_month and selldate is None:
                day = expirationdate.day
                loss = (float(row["Buy Price"])) * float(row["Count"])
                if day in lossdata:
                    lossdata[day] = lossdata[day] + loss
                else:
                    lossdata[day] = loss  
    #list for plot
    for day in sorted(lossdata):
        days.append(day)
        losses.append(lossdata[day])

    #plot
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(days, losses, width=0.8)
    ax.set(
        xlabel="Day of month",
        ylabel="Loss (€)",
        title=f"Losses per day - {print_loss_time}"
    )
    ax.set_xticks(days)
    plt.show()

def barplot_yearloss(loss_time, filepathbought=file_pathbought):
    losses = []
    months = []
    lossdata = {month: 0 for month in range(1, 13)} #0 as temporary loss for all months
    loss_time_year = loss_time.year
    print_loss_time = loss_time.year
    with filepathbought.open("r", newline="") as boughtfile:
        rows = list(csv.DictReader(boughtfile))
        for row in rows:
            if row["Sell Date"] != "":
                selldate = dt.datetime.strptime(row["Sell Date"], "%Y-%m-%d").date()
            else:
                selldate = None
            expirationdate = dt.datetime.strptime(row["Expiration Date"], '%Y-%m-%d').date()
            if expirationdate.year == loss_time_year and selldate is None:
                month = expirationdate.month
                loss = (float(row["Buy Price"])) * float(row["Count"])
                if month in lossdata:
                    lossdata[month] = lossdata[month] + loss
                else:
                    lossdata[month] = loss  
    #list for plot
    for month in sorted(lossdata):
        months.append(month)
        losses.append(lossdata[month])

    #plot
    fig, ax = plt.subplots()
    ax.bar(months, losses, width=0.8)
    ax.set(
        xlabel="Month",
        ylabel="Loss (€)",
        title=f"Losses per month - {print_loss_time}"
    )
    ax.set_xticks(months)
    plt.show()

