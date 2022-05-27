import click
from typing import List, Tuple, Dict
import sys
import math
import requests
import pprint

UNITS = ["", "K", "M", "B"]

TICK = "▇"
SM_TICK = "▏"

@click.group()
def base():
    """Simple CLI tool to print graphs in the terminal"""
    pass

@click.option(
    '--end',
    help="enter the end date here in the form dd-MM-YYYY, for example, 01-11-2022", 
    required=True,
)
@click.option(
    '--start', 
    help="enter the start date here in the form dd-MM-YYYY, for example, 14-01-2022", 
    required=True,
)
@click.option(
    '--url', 
    help="url of the API endpoint", 
    required=True,
)
@click.command(name="plot")
def plot(url, start, end):
    """Plot graphs"""

    labels, data = read_data(url, start, end)

    chart(data, labels)

@click.option(
    '--url', 
    help="url of the API endpoint", 
    required=True,
)
@click.command(name="view")
def view(url):
    """Inspect your data"""
    result = requests.get(url)
    result_dict = result.json()
    pprint.pprint(result_dict)


def find_min(data: List):
    """Return the minimum value in sublist of list."""
    return min(data)


def find_max(data: List):
    """Return the maximum value in sublist of list."""
    return max(data)

def normalize(data: List, width = 50) -> List:
    """Normalize the data and return it."""

    # We offset by the minimum if there's a negative.
    data_offset = []
    data_offset = data
    min_datum = find_min(data_offset)
    max_datum = find_max(data_offset)

    if min_datum == max_datum:
        return data_offset

    # max_dat / width is the value for a single tick. norm_factor is the
    # inverse of this value
    # If you divide a number to the value of single tick, you will find how
    # many ticks it does contain basically.
    norm_factor = width / float(max_datum)
    normal_data = []
    for datum in data_offset:
        normal_data.append(datum * norm_factor)

    return normal_data

def find_max_label_length(labels: List) -> int:
    """Return the maximum length for the labels."""
    return max([len(label) for label in labels])

def cvt_to_readable(num):
    """Return the number in a human readable format
    Eg:
    125000 -> 125.0K
    12550 -> 12.55K
    19561100 -> 19.561M
    """
    if num != 0:
        neg = num < 0
        num = abs(num)

        # Find the degree of the number like if it is in thousands or millions, etc.
        index = math.floor(math.log(num) / math.log(1000))

        # Converts the number to the human readable format and returns it.
        newNum = round(num / (1000 ** index), 3)
        newNum *= -1 if neg else 1
        degree = UNITS[index]

    else:
        newNum = 0
        degree = UNITS[0]
    if num < 100000:
        newNum = num
        degree = ""

    return f'{newNum} {degree}'

def horiz_rows(
    labels: List,
    data: List,
    normal_dat: List
):
    """Prepare the horizontal graph.
    Each row is printed through the print_row function."""
    val_min = find_min(data)

    values = data
    num_blocks = normal_dat

    for i in range(len(labels)):
        fmt = "{:<{x}}: "
        label = fmt.format(labels[i], x=find_max_label_length(labels))

        len_label = len(label)
        # label = " " * len_label

        fmt = "{}{}{}"

        yield (
            values[i],
            int(num_blocks[i]),
            val_min,
            label,
        )

# Prints a row of the horizontal graph.
def print_row(
    value,
    num_blocks: int,
    val_min: int,
    label: bool = False,
):
    """A method to print a row for a horizontal graphs.
    i.e:
    1: ▇▇ 2
    2: ▇▇▇ 3
    3: ▇▇▇▇ 4
    """

    print(label, " ", end="")

    if (num_blocks < 1 and (value > val_min or value > 0)) or ( value == 0.0
    ):
        sys.stdout.write(SM_TICK)
        print(cvt_to_readable(value))
    else:
        for _ in range(num_blocks):
            sys.stdout.write(TICK)
        print(cvt_to_readable(value))


def chart(data: List, labels: List, width = 50) -> None:
    """Handle the normalization of data and the printing of the graph."""

    normal_dat = normalize(data, width)

    for row in horiz_rows(labels, data, normal_dat):
        print_row(*row)


def read_data(url, start, end) -> Tuple[List, List]:

    # url = args["url"]
    # startDate = args["startDate"]
    # endDate = args["endDate"]

    # pulls in data from the API
    result = requests.get(url)
    result_dict = result.json()

    labels = list(result_dict.keys())
    data = list(result_dict.values())
    
    try:
        startDateIndex = labels.index(start)
    except ValueError:
        print("Invalid start date. Use the view function to view the data to see available dates")
    
    try:
        endDateIndex = labels.index(end)
    except ValueError:
        print("Invalid end date. Use the view function to view the data to see available dates")

    if startDateIndex >= endDateIndex:
        print("""
The start date must come before the end date. The assumption here is that the data is ordered chronologically.

Use plotter view --help to see how to use the view function to inspect your data
        """)
        sys.exit(1) #exit the program if the dates are incorrect

    # logic regarding subsetting data based on start and end dates
    if start and end:
        labels = labels[startDateIndex: endDateIndex + 1]
        data = data[startDateIndex: endDateIndex + 1]
    elif start:
        labels = labels[startDateIndex: ]
        data = data[startDateIndex: ]
    elif end:
        labels = labels[ : endDateIndex + 1]
        data = data[ : endDateIndex + 1]

    return labels, data


base.add_command(plot)
base.add_command(view)
