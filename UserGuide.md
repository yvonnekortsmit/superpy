# _User Guide SuperPy_

## SuperPy introduction
Via SuperPy you can manage your supermarket. You can get insights into a few different things. Such as:

1. Buying products
2. Selling products
3. Report different aspects of the supermarket:
    - Current inventory
    - Revenue
    - Profit
    - Losses
4. Plotting different aspects of the supermarket:
    - Revenue
    - Profit
    - Losses
5. Changing the application time:
    - To a specific number days in the future
    - To the current time (real time)
    - To yesterday (real time)
    - To a specific date

## Command Overview

| Command | Description |
|----------|-------------|
| buy | Add products to inventory |
| sell | Sell products |
| report inventory | Show current inventory |
| report revenue | Show revenue |
| report profit | Show profit |
| report loss | Show losses caused by expired products |
| plot revenue | Create revenue plots |
| plot profit | Create profit plots |
| plot loss | Create loss plots |
| application-time | Set application date |
| --advance-time | Advance application date |

## Starting the app
Before using the application, install Python on your system.

Via the following command you can read the command options:

``python main.py buy --help``

## What can the app do?
SuperPy simulates a real supermarket system with time-aware inventory management.

It tracks:
-   Products bought and stored in inventory
-   Products sold and their revenue
-   Profit based on buy vs sell price
-   Loss from expired products
-   Inventory changes over time using a simulated date system

The system uses CSV files to store all data permanently, so your data remains available between runs.

## Data Storage

SuperPy uses the following data storage files:
| File | Purpose |
|------|---------|
|bought.csv|Stores all purchased products|
|sold.csv|Stores all sold products|
|superpytime.txt|Stores the current application date|

Each product is tracked using a unique ID to link purchases and sales.

## How to **buy and sell** products
Via this application you can buy products to add to your inventory. You can also sell them for a specified price.

### Buy products
Via the terminal you can buy products by specifying the product name, price and expiration date (Date must be in format YYYY-MM-DD). 

``python main.py buy --product-name apple --price 0.5 --expiration-date 2026-06-19``

When the product is added to bought.csv and the terminal will print the following:

``Buying apple for €0.50, expires at 2026-06-19.``

### Sell products
When products are in your inventory you van sell the product for a specific price. Via the terminal you can sell specific products that will be added to the csv file sold.csv

``python main.py sell --product-name apple --price 2.00``

When a product is not in stock the following message will display:

``python main.py sell --product-name strawberry --price 4``

``Error: Strawberry is not in stock.``

When products are expired they can not be sold:

``Error: Pineapple is expired and can not be sold.``

## Report serveral different values
Via the option report you can report the inventory, profit, revenue and loss of your supermarket in different timeframes.

### Report inventory
To report the inventory of your supermarket you will need to specify on which day you want to report the inventory. The options are now and yesterday.

``python main.py report inventory --now``

``python main.py report inventory --yesterday``

This will print all products that are currently in stock/in your inventory via a table. For example:

|Product Name|Count|Buy Price|Expiration Date|
|------------|-----|---------|---------------|
|Apple       |    2|      0.5|     2026-05-18|
|  Kiwi      |    1|      5.1|     2026-05-09 |
| Apple      |    2|        2|     2026-06-09|

The table shows the amount op products with that specific expiration date and name that are present in the inventory of the suppermarkter. The inventory can of course differ when there are products sold. So the inventory can be different in another time. The inventory of yesterday can of be different compared with the current inventory. This depends on the bought and sold products.


### Report revenue

You can report the revenue of your supermarket, based on your bought and sold products. You can do this for different times. For today, yesterday or a specific month (Date must be in format YYYY-MM).

``python main.py report revenue --today``

``python main.py report revenue --yesterday``

``python main.py report revenue --date 2026-05``

Depending on which option you choose, it will print the corresponding revenue of your supermarket for the choosen time period:

``Revenue from May 2026: €183.70``

### Report profit
You can report the profit of your supermarket, based on your bought and sold products. You can do this for different times. For today, yesterday or a specific month (Date must be in format YYYY-MM).

``python main.py profit revenue --today``

``python main.py profit revenue --yesterday``

``python main.py profit revenue --date 2026-05``

Depending on which option you choose, it will print the corresponding profit of your supermarket:

``Yesterday's profit: €4.60.``

### Report loss
You can report the losses of your supermarket, based on your bought and sold products. You can do this for different times. For today, yesterday or a specific month (Date must be in format YYYY-MM).

``python main.py loss revenue --today``

``python main.py loss revenue --yesterday``

``python main.py loss revenue --date 2026-05``

Depending on which option you choose, it will print the corresponding loss of your supermarket:

``Today's loss: €7.05.``

## Plot serveral different values
Via the option report you can plot the profit, revenue and loss of your supermarket in different timeframes.

### Plot profit

You can plot the profit of your supermarket, based on your bought and sold products. You can do this per month or per year. For today, yesterday or a specific month. Plotting per month needs a format like: YYYY-MM. Plotting per year needs a format like: YYYY-MM.

``python main.py plot profit --month 2026-05``

``python main.py plot profit --year 2026``

Depending on which option you choose, the plot will have different axis:
-   Monthly plots will show profits per day
-   Yearly plots will show profits per month
A graph will open, please close the window of the plot before continuing with the application. 

### Plot revenue

You can plot the revenue of your supermarket, based on your bought and sold products. You can do this per month or per year. For today, yesterday or a specific month. Plotting per month needs a format like: YYYY-MM. Plotting per year needs a format like: YYYY-MM.

``python main.py plot revenue --month 2026-05``

``python main.py plot revenue --year 2026``

Depending on which option you choose, the plot will have different axis:
-   Monthly plots will show profits per day
-   Yearly plots will show profits per month
A graph will open, please close the window of the plot before continuing with the application. 

### Plot loss

You can plot the loss of your supermarket, based on your bought and sold products. You can do this per month or per year. For today, yesterday or a specific month. Plotting per month needs a format like: YYYY-MM. Plotting per year needs a format like: YYYY-MM.

``python main.py plot loss --month 2026-05``

``python main.py plot loss --year 2026``

Depending on which option you choose, the plot will have different axis:
-   Monthly plots will show profits per day
-   Yearly plots will show profits per month
A graph will open, please close the window of the plot before continuing with the application. 

## Change time in the application
SuperPy uses a specifically stored date instead of a real time system. This allows different dates being perceived as *today* in the application.

### Advance the time
You can advance the time with X number of days. In this example 2 days, the terminal will print which date will be perceived as *today*:

``python main.py --advance-time 2``

``Time is set 2 days in the future. Current application date is: Sunday 31 May 2026.``

All future actions will now use this updated date (Sunday 31 May 2026). 

### Change to a specific application time

Next to setting the application date to 2 days in the future, you can set the application date to a specific date. Via this method you can set the application time to the real today, yesterday or a specific date (Date must be in format YYYY-MM-DD).

``python main.py application-time --today``

``python main.py application-time --yesterday``

``python main.py application-time --date 2026-05-05``

The application will print the time that is perceived as today:

``Application date is set to: Tuesday 05 May 2026.``
