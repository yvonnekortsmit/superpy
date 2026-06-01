# _User Guide SuperPy_

## Superpy introduction
Via this application you can manage your supermarket. 
## Starting the app

## What can the app do?

## Uses of the app



### How to **buy and sell** products
Via this application you can buy products to add to your invintory. You can also sell them for a specified price.

#### Buy products
Via the terminal you can buy products by specifying the product name, price and expiration date (Date must be in format YYYY-MM-DD). 

``python main.py buy --product-name apple --price 1.0 --expiration-date 2026-06-29``

When the product is added to bought.csv and the terminal will print the following:

``Buying apple for 1.00, expires at 2026-06-29.``

#### Sell products
When products are in your inventory you van sell the product for a specific price. Via the terminal you can sell sepcific products that will be added to the csv file sold.csv

``python main.py sell --product-name apple --price 2.00``

When a product is not in stock the following message will display:

``python main.py sell --product-name strawberry --price 4``

``Error: Strawberry is not in stock.``

### Report serveral different values
Via the option report you can report the inventory, profit and revenue of your supermarket in different timeframes.

#### Report inventory
To report the inventory of your supermarket you will need to specify on which day you want to report the inventory. The options are now and yesterday.

``python main.py report inventory --now``

This will print all products that are currently in stock/in your inventory via a table:

|Product Name|Count|Buy Price|Expiration Date|
|------------|-----|---------|---------------|
|Banana      |    3|      1.8|     2026-10-12|
| Apple      |    3|        1|     2026-06-29|
| Apple      |    1|        1|     2026-06-02|

The table shows the amount op products with that specific expiration date and name that are present in the inventory of the suppermarkter. The inventory can of course differ when there are products sold. So the inventory can be different in another time. You can also check the inventory of yesterday.

``python main.py report inventory --yesterday``

The inventory of yesterday can of course be different compared with the current inventory:

|Product Name|Count|Buy Price|Expiration Date|
|------------|-----|---------|---------------|
|Banana      |    3|      1.8|     2026-10-12|
| Apple      |    3|        1|     2026-06-29|

#### Report revenue

You can report the revenue of your supermarket, based on your bought and sold products. You can do this for different times. For today, yesterday or a specific month (Date must be in format YYYY-MM).

``python main.py report revenue --today``

``python main.py report revenue --yesterday``

``python main.py report revenue --date 2026-05``

Depending on which option you choose, it will print the corresponding revenue of your supermarket for the choosen time period:

``Yesterday's revenue: 2.00.``

#### Report profit
You can report the profit of your supermarket, based on your bought and sold products. You can do this for different times. For today, yesterday or a specific month (Date must be in format YYYY-MM).

``python main.py profit revenue --today``

``python main.py profit revenue --yesterday``

``python main.py profit revenue --date 2026-05``

Depending on which option you choose, it will print the corresponding profit of your supermarket:

``Yesterday's profit: 4.60.``

### Change time in the application
You can change the time that is perceived as *today* in the application.

#### Advance the time
You can advance the time with X number of days. In this example 2 days, the terminal will print which date will be perceived as *today*:

``python main.py --advance-time 2``

``Time is set 2 days in the future. Current application date is: Sunday 31 May 2026.``

For all actions after this command the *today* time of the application will be set to: Sunday 31 May 2026.

#### Change the application time

Next to setting the application date to 2 days in the future, you can set the application date to a specific date. Via this method you can set the application time to the real today, yesterday or a specific date (Date must be in format YYYY-MM-DD).

``python main.py application-time --today``

``python main.py application-time --yesterday``

``python main.py application-time --date 2026-05-05``

The application will print the time that is perceived as today:

``Application date is set to: Tuesday 05 May 2026.``
