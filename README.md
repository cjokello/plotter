Plotter 
========

A simple CLI graphing tool written in Python to display bar graphs in your terminal

Instructions:
=============

Make sure to have python and pip installed.

Clone this repo locally and from your terminal (after navigating to the directory of the cloned repo), run `pip install --editable .`

Then run `plotter --help` to get you started.

Caveats
========

The data is assumed to be in the form of a python dictionary of the form { String : Int }

The keys are dates of the form dd-MM-YYYY in String format and the values are integers.

The data in the dictionary should be arranged chronologically.

Examples:
=========

For data such as this:  

<img width="239" alt="Screenshot 2022-05-27 at 16 58 10" src="https://user-images.githubusercontent.com/77014953/170725446-2f103bf4-71ae-493b-bb0a-f9b53c02aed1.png">

The following commands could be run: 

`plotter plot --url *enter your own url here* --start 01-01-2022 --end 15-01-2022`

`plotter view --url *enter your own url here*`

The graph looks like this:  

<img width="590" alt="Screenshot 2022-05-27 at 16 55 38" src="https://user-images.githubusercontent.com/77014953/170725153-3e02c7a0-4489-4750-aba3-45a92af59e61.png">


