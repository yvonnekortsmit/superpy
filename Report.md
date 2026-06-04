# Report SuperPy

## Introduction
SuperPy is a command-line application that tracks products, sales, and financial results like revenue, profit, and loss using CSV files and a custom application date system.

## Application time
SuperPy has a costum time system. HThe current application date is stored in a text file (superpytime.txt). This file is read when the program starts and updated whenever the user changes or advances the time. This makes it very easy to set the application different time periods, which is useful for testing things like revenue, profit, and expired products without waiting in real time. The application can also buy and sell products at different times due to this feature.

The application can also easily be set to the *real* time via the argparse *application-time*.

When the tekst file (superpytime.txt) is not yet present during running of the application, it will automatically be created. Making sure that there are no manual setups required.

## Time validation functions
SuperPy uses some custom time validation functions: *valid_date()*, *valid_month()* and *valid_year()*. These functions are used in argparse to make sure that the user input are set to the correct format.

The functions converts the string input into a datetime object. If the format is incorrect it raises an error. This keeps the code more clear and prevents confusing error messages for the user.

## Automatic file creation
SuperPy automatically creates the external .csv and .txt files needed if they are not yet present within the project folder. The correct headers are added in the .csv files when created to make sure that the application will run smoothly. This automatic feature ensures the application works without needing a manual file setup. 

## Conclusion
SuperPy has an flexible time storage option, prevents unnescessery and unclear errors in tiem format and is made to run without first needing to setup manual documents.
