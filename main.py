from argparse import *
import datetime as dt 
import csv 
from functions import *
from rich.console import Console
console = Console()
#Argparse SuperPy
parser = ArgumentParser(description='Welcome to SuperPy, use this to check supermarket products.')

#creat subparsers
subparsers = parser.add_subparsers(dest='command')#, required=True)

#creat subparser 1 (buy)
buy_parser = subparsers.add_parser('buy', help='Add what products to buy.')
buy_parser.add_argument('--product-name', type=str, help='Specify product name.')
buy_parser.add_argument('--price', type=float, help='Specify product price.')
buy_parser.add_argument('--expiration-date', type=valid_date, help='Specify product expiration date as YYYY-MM-DD.')

#creat subparser 2 (sell)
sell_parser = subparsers.add_parser('sell', help='Add what products to sell.')
sell_parser.add_argument('--product-name', type=str, help='Specify product name.')
sell_parser.add_argument('--price', type=float, help='Specify product price.')

#create report subparser (report inventory, revenue, profit)
report_parser = subparsers.add_parser('report', help='Report the inventory, revenue or profit.')
report_subparser = report_parser.add_subparsers(dest="report", help='Report the inventory, revenue or profit.')

#create inventory subparsers
inventory_parser = report_subparser.add_parser('inventory')
inventory_parser.add_argument('--now', action='store_true', help='Report current inventory.')
inventory_parser.add_argument('--yesterday', action='store_true', help='Report yesterdays inventory.')

#create expired subparsers
expired_parser = report_subparser.add_parser('expired')
expired_parser.add_argument('--now', action='store_true', help='Report current expired products.')
expired_parser.add_argument('--yesterday', action='store_true', help='Report yesterdays expired products.')

#create revenue subparsers
revenue_parser = report_subparser.add_parser('revenue')
revenue_parser.add_argument('--today', action='store_true', help='Report todays revenue.')
revenue_parser.add_argument('--yesterday', action='store_true', help='Report yesterdays revenue.')
revenue_parser.add_argument('--date', type=valid_month, help='Report revenue on which date?') 

#create profit subparsers
profit_parser = report_subparser.add_parser('profit')
profit_parser.add_argument('--today', action='store_true', help='Report todays profit.')
profit_parser.add_argument('--yesterday', action='store_true', help='Report yesterdays profit.')
profit_parser.add_argument('--date', type=valid_month, help='Report profit on which date?') 

#create loss subparsers
loss_parser = report_subparser.add_parser('loss')
loss_parser.add_argument('--today', action='store_true', help='Report todays loss.')
loss_parser.add_argument('--yesterday', action='store_true', help='Report yesterdays loss.')
loss_parser.add_argument('--date', type=valid_month, help='Report loss on which date?') 


# create --advance-time 2 -- what should this do?? look into the future?
parser.add_argument('--advance-time', type=int, default=0, help='Look into the future, for how many days?.')

#create set specific time
time_parser = subparsers.add_parser('application-time', help='Add what products to buy.')
time_parser.add_argument('--today', action='store_true', help='Set applicationd date to today.')
time_parser.add_argument('--yesterday', action='store_true', help='Set applicationd date to yesterday.')
time_parser.add_argument('--date', type=valid_date, help='Set application date to which date? Please specify the date as YYYY-MM-DD.')

#create plot subparser (plot inventory, revenue, profit)
plot_parser = subparsers.add_parser('plot', help='Plot the inventory, revenue or profit.')
plot_subparser = plot_parser.add_subparsers(dest="plot", help='Plot the inventory, revenue or profit.')

#create profit plot subparsers
plotprofit_parser = plot_subparser.add_parser('profit')
plotprofit_parser.add_argument('--month', type=valid_month, help='Plot profit on which date? Please specify the date as YYYY-MM.')
plotprofit_parser.add_argument('--year', type=valid_year, help='Plot profit on which year? Please specify the year as YYYY.')

#create revenue plot subparsers
plotrevenue_parser = plot_subparser.add_parser('revenue')
plotrevenue_parser.add_argument('--month', type=valid_month, help='Plot revenue on which date? Please specify the date as YYYY-MM.')
plotrevenue_parser.add_argument('--year', type=valid_year, help='Plot revenue on which year? Please specify the year as YYYY.')

#create loss plot subparsers
plotloss_parser = plot_subparser.add_parser('loss')
plotloss_parser.add_argument('--month', type=valid_month, help='Plot loss on which date? Please specify the date as YYYY-MM.')
plotloss_parser.add_argument('--year', type=valid_year, help='Plot loss on which year? Please specify the year as YYYY.')

#Parse arguments
args = parser.parse_args()

#advance time parser and reset current time parser
if args.advance_time:
    advanced_time(args.advance_time)
    print_date = advanced_time(args.advance_time)
    print(f"Time is set {args.advance_time} days in the future. Current application date is: {print_date}.")

#set the application time
elif args.command == "application-time":
    if not (args.today or args.yesterday or args.date):
        console.print("\nPlease set the application time via one of the following methods:\n\n[#B0C4DE][#87CEEB]1.[/#87CEEB] application-time --today\n[#87CEEB]2.[/#87CEEB] application-time --yesterday\n[#87CEEB]3.[/#87CEEB] application-time --date [#FFFF00]APPLICATION_DATE[/#FFFF00] ([#00BFFF]YYYY-MM-DD[/#00BFFF])[/#B0C4DE]\n")
    else:
        if args.today:
            set_time("today")
            print(f"\nApplication date is set to today: {set_time("today")}.\n")
        elif args.yesterday:
            set_time("yesterday")
            print(f"\nApplication date is set to yesterday: {set_time("yesterday")}.\n")
        elif args.date:
            set_time(args.date)
            print(f"\nApplication date is set to: {set_time(args.date)}.\n")

#outcome for buy parser
elif args.command == "buy":
    if not all([args.product_name, args.price, args.expiration_date]):
        console.print("\nPlease specify the product you want to buy:\n\n[#B0C4DE]buy --product-name [#FFFF00]PRODUCT_NAME[/#FFFF00] --price [#FFFF00]PRICE[/#FFFF00] --expiration-date [#FFFF00]EXPIRATION_DATE[/#FFFF00] ([#00BFFF]YYYY-MM-DD[/#00BFFF])[/#B0C4DE]\n")
    else:
        add_product(args.product_name, args.price, args.expiration_date)
        print(f"Buying {args.product_name} for €{args.price:.2f}, expires at {args.expiration_date}.")

#outcome for sell parser
elif args.command == "sell":
    if not all([args.product_name, args.price]):
        console.print("\nPlease specify the product you want to sell:\n\n[#B0C4DE]sell --product-name [#FFFF00]PRODUCT_NAME[/#FFFF00] --price [#FFFF00]SELL_PRICE[/#FFFF00][/#B0C4DE]\n")
    else:
        try:
            sell_product(args.product_name, args.price)
            print(f"\nSelling {args.product_name} for €{args.price:.2f}\n")
        except ValueError as producterror:
            console.print(f"[#FF6B6B]\nError:[/#FF6B6B] {producterror}\n")

#outcome for inventory parser
elif args.command == "report" and args.report == "inventory":
    if args.now:
        report_inventory("now")
    elif args.yesterday:
        report_inventory("yesterday")

#outcome for expired parser
elif args.command == "report" and args.report == "expired":
    if args.now:
        report_inventory("now")
    elif args.yesterday:
        report_inventory("yesterday")

#Raport revenue parser
elif args.command == "report" and args.report == "revenue":
    if args.today:
        print(f"\nToday's revenue so far: €{report_revenue("today"):.2f}.\n")
    elif args.yesterday:
        print(f"\nYesterday's revenue: €{report_revenue("yesterday"):.2f}.\n")
    elif args.date:
        print_date = args.date.strftime("%B %Y")
        print(f"\nRevenue from {print_date}: €{report_revenue(args.date):.2f}.\n")

#Raport profit parser
elif args.command == "report" and args.report == "profit":
    if args.today:
        print(f"\nToday's profit so far: €{report_profit("today"):.2f}.\n")
    elif args.yesterday:
        print(f"\nYesterday's profit: €{report_profit("yesterday"):.2f}.\n")
    elif args.date:
        print_date = args.date.strftime("%B %Y")
        print(f"\nProfit from {print_date}: €{report_profit(args.date):.2f}.\n")

#Report Loss parse
elif args.command == "report" and args.report == "loss":
    if args.today:
        print(f"\nToday's loss: €{report_loss("today"):.2f}.\n")
    elif args.yesterday:
        print(f"\nYesterday's loss: €{report_loss("yesterday"):.2f}.\n")
    elif args.date:
        print_date = args.date.strftime("%B %Y")
        print(f"\nLoss from {print_date}: €{report_loss(args.date):.2f}.\n")


######Plot Parsers
elif args.command == "plot" and args.plot == "profit":
    if args.month:
        console.print("\n[green]Profit plot will be visible via pop-up screen.[/green] Please [bold red]close[/bold red] the plotwindow to continue this program.\n")
        barplot_monthprofit(args.month)
    elif args.year:
        console.print("\n[green]Profit plot will be visible via pop-up screen.[/green] Please [bold red]close[/bold red] the plotwindow to continue this program.\n")
        barplot_yearprofit(args.year)

elif args.command == "plot" and args.plot == "revenue":
    if args.month:
        console.print("\n[green]Revenue plot will be visible via pop-up screen.[/green] Please [bold red]close[/bold red] the plotwindow to continue this program.\n")
        barplot_monthrevenue(args.month)
    elif args.year:
        console.print("\n[green]Revenue plot will be visible via pop-up screen.[/green] Please [bold red]close[/bold red] the plotwindow to continue this program.\n")
        barplot_yearrevenue(args.year)

elif args.command == "plot" and args.plot == "loss":
    if args.month:
        console.print("\n[green]Loss plot will be visible via pop-up screen.[/green] Please [bold red]close[/bold red] the plotwindow to continue this program.\n")
        barplot_monthloss(args.month)
    elif args.year:
        console.print("\n[green]Loss plot will be visible via pop-up screen.[/green] Please [bold red]close[/bold red] the plotwindow to continue this program.\n")
        barplot_yearloss(args.year)