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

#create revenue subparsers
revenue_parser = report_subparser.add_parser('revenue')
revenue_parser.add_argument('--today', action='store_true', help='Report todays revenue.')
revenue_parser.add_argument('--yesterday', action='store_true', help='Report yesterdays revenue.')
revenue_parser.add_argument('--date', type=valid_month, help='Report revenue on which date?') 

#create profit subparsers
profit_parser = report_subparser.add_parser('profit')
profit_parser.add_argument('--today', action='store_true', help='Report todays profit.')
profit_parser.add_argument('--yesterday', action='store_true', help='Report yesterdays profit.')
profit_parser.add_argument('--date', type=valid_month, help='Report revenue on which date?.') 

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

#create profit subparsers
plotprofit_parser = plot_subparser.add_parser('profit')
plotprofit_parser.add_argument('--month', type=valid_month, help='Plot profit on which date? Please specify the date as YYYY-MM.')
plotprofit_parser.add_argument('--year', type=valid_year, help='Plot profit on which year? Please specify the year as YYYY.')



#Parse arguments
args = parser.parse_args()

#advance time parser and reset current time parser
if args.advance_time:
    advanced_time(args.advance_time)
    print_date = advanced_time(args.advance_time)
    print(f"Time is set {args.advance_time} days in the future. Current application date is: {print_date}.")

#set the application time
elif args.command == "application-time":
    if args.today:
        set_time("today")
        print(f"Application date is set to today: {set_time("today")}.")
    elif args.yesterday:
        set_time("yesterday")
        print(f"Application date is set to yesterday: {set_time("yesterday")}.")
    elif args.date:
        set_time(args.date)
        print(f"Application date is set to: {set_time(args.date)}.")

#outcome for buy parser
elif args.command == "buy":
    add_product(args.product_name, args.price, args.expiration_date)
    print(f"Buying {args.product_name} for €{args.price:.2f}, expires at {args.expiration_date}.")

#outcome for sell parser
elif args.command == "sell":
    try:
        sell_product(args.product_name, args.price)
        print(f"Selling {args.product_name} for €{args.price:.2f}")
    except ValueError as producterror:
        console.print(f"Error: {producterror}", style="bold red")

#outcome for inventory parser
elif args.command == "report" and args.report == "inventory":
    if args.now:
        report_inventory("now")
    elif args.yesterday:
        report_inventory("yesterday")

#outcome for revenue parser
elif args.command == "report" and args.report == "revenue":
    if args.today:
        print(f"Today's revenue so far: €{report_revenue("today"):.2f}.")
    elif args.yesterday:
        print(f"Yesterday's revenue: €{report_revenue("yesterday"):.2f}.")
    elif args.date:
        print_date = args.date.strftime("%B %Y")
        print(f"Revenue from {print_date}: €{report_revenue(args.date):.2f}.")

elif args.command == "report" and args.report == "profit":
    if args.today:
        print(f"Today's profit so far: €{report_profit("today"):.2f}.")
    elif args.yesterday:
        print(f"Yesterday's profit: €{report_profit("yesterday"):.2f}.")
    elif args.date:
        print_date = args.date.strftime("%B %Y")
        print(f"Profit from {print_date}: €{report_profit(args.date):.2f}.")

elif args.command == "plot" and args.plot == "profit":
    if args.month:
        console.print("[green]Plot is visible in pop-up screen.[/green] Please [bold red]close[/bold red] the window to continue this program.")
        barplot_monthprofit(args.month)
    elif args.year:
        console.print("[green]Plot is visible in pop-up screen.[/green] Please [bold red]close[/bold red] the window to continue this program.")
        barplot_yearprofit(args.year)


#outcome for sell parser
#elif args.advance_time:
#    advanced_time(args.advance_time)
    #print(f"Selling {args.product_name} for €{args.price:.2f}")
#if __name__ == "__main__":
 #   print("The outcome is:") #{outcome}") ##output for the users.