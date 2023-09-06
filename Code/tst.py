import pandas as pd
import pathlib
import rich

# paymentAppDBPath = pathlib.Path("./tstDB/paymentAppDB.csv")

# df=pd.DataFrame({"name": ['Samir','Taher','Hefney','Helmy'], "number": ['1234567891234567','7654321987654321','1122334455667788','8877665544332211'], "exp_month": [9,7,5,12],
#              "exp_year": [2025,2024,2026,2025], "cvv": [123,456,789,321]})


# df.to_csv(paymentAppDBPath,index=False)

# print(pd.read_csv(paymentAppDBPath).head(5))

def print_msg_box(msg, indent=1, width=None, title=None):
    """Print message-box with optional title."""
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{" " * len(title):<{width}}{space}║\n'  # underscore
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(box)

# print_msg_box(msg=msg, indent=2, title='In a nutshell:')
# print(' ╔==============================================================================================================================╗')
print_msg_box("You stand in front of the payment device, ready to pay for your purchases.\nYou open your phone and launch the app, which is 99.9999999% secure and doesn't share your credit card information with the merchant.\nYou scan the barcode on the payment device, and the app quickly processes the payment.\nYou're on your way in no time.\n", 3, title='Assumption')
# print(' ===============================================================================================================================╝')


# import textwrap

# paragraph = "This is a paragraph."

# # Set the box width to 80 characters
# width = 80

# # Wrap the paragraph to the specified width
# wrapped_paragraph = textwrap.fill(paragraph, width)

# # Create a border
# border = "*" * width

# # Print the paragraph in a box
# print(border)
# print(wrapped_paragraph)
# print(border)

# paragraph = "This is a paragraph."

# # Create a frame
# frame = rich.box(paragraph, border_style="solid")

# # Print the frame
# print(frame)