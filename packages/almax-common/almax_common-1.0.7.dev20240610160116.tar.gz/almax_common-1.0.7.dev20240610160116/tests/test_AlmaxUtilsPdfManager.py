import os;
from AlmaxUtils.PdfManager import GeneratePdf;
import AlmaxUtils.Time as TimeLib;

class Order:
    def __init__(self, description, quantity, price):
        self.Description = description;
        self.Quantity = "{:,.1f}".format(quantity);
        self.Price = "{:,.2f}".format(price);
        self.Total = "{:,.2f}".format(quantity * price);

def test_GeneratePdf():
    now = TimeLib.now;
    now_month = now.month if now.month > 9 else f"0{now.month}";
    now_day = now.day if now.day > 9 else f"0{now.day}";
    now_hour = now.hour if now.hour > 9 else f"0{now.hour}";
    now_minute = now.minute if now.minute > 9 else f"0{now.minute}";
    now_second = now.second if now.second > 9 else f"0{now.second}";
    file_path = f"{now.year}/{now_month}/{now_day}_{now_hour}{now_minute}{now_second}.pdf";
    
    client_info = {
        "name": "Ali Srls"
    };
    orders = [
        Order('fbewkjfbwebfjewbfkjewbfkewfewfvjewbfjwebfjkewjfbewfjwebjfwejfjwebfjewbfjwefwebfwefweeffwe', 2.6, 31.5),
        Order('ciao', 2.6, 34090.5),
        Order('fbewkjfbwebfjewbfkjewbfkewfewfvjewbfjwebfjkewjfbewfjwebjfwejfjwebfjewbfjwefwebfwefweeffwe', 2.6, 32.5),
        Order('fbewkjfbwebfjewbfkjewbfkewfewfvjewbfjwebfjkewjfbewfjwebjfwejfjwebfjewbfjwefwebfwefweeffwe', 2.6, 33.5),
        Order('fbewkjfbwebfjewbfkjewbfkewfewfvjewbfjwebfjkewjfbewfjwebjfwejfjwebfjewbfjwefwebfwefweeffwe', 2.6, 34.5)
    ];

    GeneratePdf(client_info, Order, orders);
    assert os.path.exists(file_path);