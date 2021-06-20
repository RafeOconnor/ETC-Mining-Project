# GUI Mining Profit Calculator
# Version 4
# Changed vars in update details to global
# This removes the need to constantly web scrape everytime user wants to calculate profit
# Now only scrapes whenever user presses update button

# Import necessary modules

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import yfinance as yf
from selenium import webdriver
from etc_network_hash import etc_network_hashrate,etc_block_reward,etc_block_time

# Set browser

browser = webdriver.safari.webdriver.WebDriver(quiet=False)

# ETC details assumed
# User hash can be changed by user during runtime

nhash = etc_network_hashrate(browser)
user_hash = 113.2
block_reward = etc_block_reward(browser)
avg_time = etc_block_time(browser)

browser.quit() # Close browser once all values are scraped

# Function to calculate mining profit (applies to any coin)

def set_values():
    try:

        user_hash_rate = user_hash_rate_var.get()
    except tk.TclError:
        tk.messagebox.showerror(title="Invalid Input",message="Please enter numeric values only")
        root.update()
        return

    network_hashrate_lbl.config(text="Network HashRate: {0}Thash/s".format(nhash))
    network_block_reward_lbl.config(text="Block Reward: {0} ETC".format(block_reward))
    network_block_time_lbl.config(text="Avg Block Time: {0}s".format(avg_time))

    # GET COIN PRICE FROM YAHOO FINANCE
    #etc_ticker = yf.Ticker(coin)
    #etc_history = etc_ticker.history(period="1d") # Get current price history
    #etc_price = round(etc_history.iloc[0,3],2) # store current price in variable

    #current_price["text"] = "Current Price of {0}: £{1}".format(coin,etc_price)


    #mining_profit(system_wattage,electricity_cost,etc_price,coin_mined)
    calculate_etc(nhash,user_hash_rate_var,block_reward,avg_time)

def mining_profit(total_electricty,price_per_kwh,coin_price,coin_per_day):
    cost_per_day = round((total_electricty / 1000) * price_per_kwh * 24,2)
    gross_profit_per_day = round(coin_per_day * coin_price,2)
    net_profit_per_day = round(gross_profit_per_day - cost_per_day,2)

    profit = "It cost £{0} per day to mine £{1} worth of ETC, generating £{2} per day in profit".format(cost_per_day,
                                                                                                gross_profit_per_day,
                                                                                                net_profit_per_day)

    weekly_mined = round(coin_per_day * 7,4)
    monthly_mined = round(coin_per_day * 30,4)
    yearly_mined = round(monthly_mined * 12,4)

    if net_profit_per_day > 0:
        daily_profit.config(text="Daily Profit = £{0} | Daily mined {1}".format(net_profit_per_day,round(coin_per_day,4)),fg=profit_fg_colour)
        weekly_profit.config(text="Weekly Profit = £{0} | Weekly mined {1}".format(round(net_profit_per_day * 7,2),weekly_mined),fg=profit_fg_colour)
        monthly_profit.config(text="Monthly Profit = £{0} | Monthly mined {1}".format(round(net_profit_per_day * 30,2),monthly_mined),fg=profit_fg_colour)
        yearly_profit.config(text="Yearly Profit = £{0} | Yearly mined {1}".format(round(net_profit_per_day * 365,2),yearly_mined),fg=profit_fg_colour)
        #return profit
        #print(total_electricty,price_per_kwh,coin_price,coin_per_day,profit)
    else:
        daily_profit.config(text="Daily Profit = £{0} | Daily mined {1}".format(net_profit_per_day,round(coin_per_day,4)),fg=loss_fg_colour)
        weekly_profit.config(text="Weekly Profit = £{0} | Daily mined {1}".format(round(net_profit_per_day * 7,2),weekly_mined),fg=loss_fg_colour)
        monthly_profit.config(text="Monthly Profit = £{0} | Daily mined {1}".format(round(net_profit_per_day * 30,2),monthly_mined),fg=loss_fg_colour)
        yearly_profit.config(text="Yearly Profit = £{0} | Yearly mined {1}".format(round(net_profit_per_day * 365,2),yearly_mined),fg=loss_fg_colour)

# Function to calculate ETC mined based on hash rate

def calculate_etc(network_hash,user_hash,block_reward,avg_block_time):
    print(nhash)
    electricity_cost = electricity_var.get()
    system_wattage = system_wattage_var.get()
    #coin = coin_var.get()

    # GET COIN PRICE FROM YAHOO FINANCE
    etc_ticker = yf.Ticker("ETC-GBP")
    etc_history = etc_ticker.history(period="1d") # Get current price history
    etc_price = round(etc_history.iloc[0,3],2) # store current price in variable

    current_price["text"] = "Current Price of ETC-GBP: £{0}".format(etc_price)


    million.set(1e6)
    billion.set(1e12)
    # calculate user ratio
    #print(type(user_hash))
    user_ratio = user_hash.get() * million.get() / (network_hash * billion.get())

    # calculate block reward per mine
    block_per_min = 60/avg_block_time

    # calculate etc reward per mine

    reward_per_min = block_per_min * block_reward

    # calculate etc mined per min
    etc_per_min = user_ratio * reward_per_min

    # per hour
    etc_per_hour = etc_per_min * 60

    # per day
    etc_per_day = etc_per_hour * 24

    print(round(etc_per_day,2))

    #return round(etc_per_day,5)

    mining_profit(system_wattage,electricity_cost,etc_price,etc_per_day)

# REMOVE THIS FUNCTION
def update_details():
    # Invoke browser each time button is pressed
    # This allows multiple scrapes to happen while the program is running
    browser = webdriver.safari.webdriver.WebDriver(quiet=False)

    # Create global variables
    global nhash,block_reward,avg_time

    nhash = etc_network_hashrate(browser)
    block_reward = etc_block_reward(browser)
    avg_time = etc_block_time(browser)

    network_hashrate_lbl.config(text="Network HashRate: {0}Thash/s".format(nhash))
    network_block_reward_lbl.config(text="Block Reward: {0} ETC".format(block_reward))
    network_block_time_lbl.config(text="Avg Block Time: {0}s".format(avg_time))

    # Close browser once all data is scraped
    browser.quit()


# Create core components for GUI

root = tk.Tk()
root.title("ETC Mining Profit")
root.geometry("900x200")

######################## DECLARING VARS TO STORE ENTRY VALUES ########################

electricity_var = tk.DoubleVar()
system_wattage_var = tk.IntVar()
#coin_var = tk.StringVar()
user_hash_rate_var = tk.DoubleVar()
million = tk.DoubleVar()
billion = tk.DoubleVar()

######################## LABELFRAME AREA ########################

user_variables_frame = tk.LabelFrame(root,padx=20,pady=10)
user_variables_frame.grid(row=0,column=0,columnspan=5)

variable_lables_frame = tk.LabelFrame(root,padx=20,pady=10)
variable_lables_frame.grid(row=1,column=0,columnspan=4)

profits_frame = tk.LabelFrame(root,padx=20,pady=10,width=400,height=200)
profits_frame.grid(row=2,column=0,columnspan=3)

# Store details about the ETC network

network_frame = tk.LabelFrame(root,padx=20,pady=10,width=400,height=200)
network_frame.grid(row=2,column=3,columnspan=3)

######################## user_variables_frame widgets ########################

electricity_cost_entry = tk.Entry(user_variables_frame,textvariable=electricity_var)
electricity_cost_entry.grid(row=1,column=0)

system_wattage_entry = tk.Entry(user_variables_frame,textvariable=system_wattage_var)
system_wattage_entry.grid(row=1,column=1)

#coin_entry = tk.Entry(user_variables_frame,textvariable=coin_var)
#coin_entry.grid(row=1,column=2)

user_hash_rate_entry = tk.Entry(user_variables_frame,textvariable=user_hash_rate_var)
user_hash_rate_entry.grid(row=1,column=2)

calculate_bttn = tk.Button(user_variables_frame,text="Calculate Profits",command=set_values)
calculate_bttn.grid(row=1,column=3)

######################## user_variables_frame labels ########################

electricity_cost_lbl = tk.Label(user_variables_frame,text="Electricity Cost")
electricity_cost_lbl.grid(row=0,column=0,sticky="W")

system_wattage_lbl = tk.Label(user_variables_frame,text="System Wattage")
system_wattage_lbl.grid(row=0,column=1,sticky="W")

#coin_lbl = tk.Label(user_variables_frame,text="Coin")
#coin_lbl.grid(row=0,column=2,sticky="W")

# NEW EDIT HERE
# CHANGED TO USER HASH RATE
user_hash_rate_lbl = tk.Label(user_variables_frame,text="Hash Rate MH/s")
user_hash_rate_lbl.grid(row=0,column=2,sticky="W")

######################## profits_frame widgets ########################

profit_fg_colour = "green"
loss_fg_colour = "red"

frame_title = tk.Label(profits_frame,text="PROFIT CALCULATOR",fg="red")
frame_title.place(x=200, y=10, anchor="center")

current_price = tk.Label(profits_frame,text="Current Price of: Insert Coin",fg=profit_fg_colour)
current_price.place(x=200, y=50, anchor="center")

daily_profit = tk.Label(profits_frame,text="DAILY PROF",fg=profit_fg_colour)
daily_profit.place(x=200, y=75, anchor="center")

weekly_profit = tk.Label(profits_frame,text="WEEKLY PROF HOLDER",fg=profit_fg_colour)
weekly_profit.place(x=200, y=100, anchor="center")

monthly_profit = tk.Label(profits_frame,text="MONTHLY PROF HOLDER",fg=profit_fg_colour)
monthly_profit.place(x=200, y=125, anchor="center")

yearly_profit = tk.Label(profits_frame,text="YEARLY PROF HOLDER",fg=profit_fg_colour)
yearly_profit.place(x=200,y=150,anchor="center")

######################## ETC network widgets ########################

network_title_lbl = tk.Label(network_frame,text="ETC NETWORK DETAILS")
network_title_lbl.place(x=200,y=10,anchor="center")

network_hashrate_lbl = tk.Label(network_frame,text="Network HashRate: {0}Thash/s".format(nhash))
network_hashrate_lbl.place(x=200,y=50,anchor="center")

network_block_reward_lbl = tk.Label(network_frame,text="Block Reward: {0} ETC".format(block_reward))
network_block_reward_lbl.place(x=200,y=75,anchor="center")

network_block_time_lbl = tk.Label(network_frame,text="Avg Block Time: {0}s".format(avg_time))
network_block_time_lbl.place(x=200,y=100,anchor="center")

update_network_btn = tk.Button(network_frame,text="Press to update details",command=update_details)
update_network_btn.place(x=200,y=125,anchor="center")

root.mainloop()
