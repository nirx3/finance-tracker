import csv
import os
from tabulate import tabulate
from datetime import datetime,date
import matplotlib.pyplot as plt



# Add transaction
def add_transactions():
    category_allowed=["Basic needs", "Transportation" , "Health" ,"Education" , "Refreshment" , "Others" ,"Saving/Investment"]
    print("Transaction details: ")
    date_=input("Enter the date: ").strip()
    category=input("\nCategories allowed:\n-Basic needs (food, clothing, shelter)\n-Transportation\n-Health\n-Education\n-Refreshment\n-Saving/Investment\n-Others\n\nEnter the category: " ).strip().capitalize()
    amount=float(input("\nEnter the transaction amount: "))
    note=input("\nEnter the notes: ").strip()


    #Basic input validation
    set_date=(date_ if date_!="" else date.today())
    set_category= (category if category in category_allowed else "Others")
    set_amount=amount
    set_note=(note if note!="" else "N/A")


    data =[set_date,set_amount,set_category,set_note]
    # writing and storing transactions into a file
    with open("transactions.csv" , "a+" , newline="") as fwrite:
        file_write=csv.writer(fwrite)
        check=os.path.getsize("transactions.csv")
        if check==0:
            header=["Date", "Amount", "Category" ,"Notes"]
            file_write.writerow(header)
        file_write.writerow(data)
    print("Transaction added...")




#Viewing transaction
def view_transactions():
    rows=[]
    print("Viewing transactions...")
    # reading transactions into a terminal
    with open("transactions.csv" , "r") as fread:
        file_read=csv.reader(fread)
        field_name=next(file_read)
        for row in file_read:
            rows.append(row)
    #dispalying transactions in tabular format using tabulate
    table=tabulate(rows, headers=field_name,tablefmt="grid", colalign=("center","center","center"))
    print(f"##TRANSACTION RECORDS##\n{table}")
    print(f"Total no of transactions is {len(rows)}")







#filtering data

#by date
def filter_transactions_by_date():
    start_date=input("Enter start date in YYYY-MM-DD: ")
    end_date=input("Enter end date in YYYY-MM-DD: ")
    newrow=[]
    data_timestamp_list=[]
    filtered_by_date_list=[]
    with open("transactions.csv" , "r") as ffilter_by_Date:
        ffilter_by_date=csv.reader(ffilter_by_Date)
        field_name_filter_date=next(ffilter_by_date)
        for record in ffilter_by_date:
            newrow.append(record)
    #creating a list of timestamp for date for each records
    for date_data in newrow:
        dt=datetime.strptime(date_data[0], "%Y-%m-%d")
        data_timestamp_list.append(dt.timestamp())
    #converting start date and end date into timestamps for filtering
    start_date_conversion=datetime.strptime(start_date,"%Y-%m-%d")
    end_date_conversion=datetime.strptime(end_date,"%Y-%m-%d")
    start_date_timestamp=start_date_conversion.timestamp()
    end_date_timestamp=end_date_conversion.timestamp()
    #checking if the timestamp for each row lies within a filtering range
    for index,element in enumerate(data_timestamp_list):
        if start_date_timestamp<=element<=end_date_timestamp:
            filtered_by_date_list.append(newrow[index])
    if len(filtered_by_date_list)>0:
        print(f"Transactions in between {start_date_conversion} to {end_date_conversion}")
        print(tabulate(filtered_by_date_list, headers=field_name_filter_date, tablefmt="grid", colalign=("center","center","center")))
    else:
        print("No any record of transaction within the user-given date range has been found.")





#by Category
def filter_transactions_by_category():
    category_=input("Enter filtering category: ").strip().capitalize()
    newrow_=[]
    filtered_by_category_list=[]
    with open("transactions.csv" ,"r") as ffilter_by_category:
        ffilter_by_Category=csv.reader(ffilter_by_category)
        field_name_filter_category=next(ffilter_by_Category)
        for record in ffilter_by_Category:
            newrow_.append(record)
    for element in newrow_:
        if element[2]==category_:
            filtered_by_category_list.append(element)
    if len(filtered_by_category_list)>0:
        print(f"Transactions under {category_} category")
        print(tabulate(filtered_by_category_list, headers=field_name_filter_category, tablefmt="grid" ,colalign=("center" , "center" , "center")))
    else:
        print("No any record of transaction under the user-given category has been found.")








# View summary
def view_summary():
    summary_list=[]
    category_list=["Basic needs", "Transportation" , "Health" ,"Education" , "Refreshment" , "Saving/Investment", "Others"]
    with open("transactions.csv","r") as fsummary:
        check_filesize = os.path.getsize("transactions.csv")
        if check_filesize!=0:
            file_summary=csv.reader(fsummary)
            summary_header=next(file_summary)
            for record in file_summary:
                summary_list.append(record)
        else:
            print("No transactions recordered in transactions.csv")
    if check_filesize !=0:
        basic_needs,transportation,health,education,refreshment,saving_investment,others=0,0,0,0,0,0,0
        for data in summary_list:
            amount_in_float=float(data[1])
            if data[2] == "Basic needs":
                basic_needs+=amount_in_float
            elif data[2] == "Transportation" :
                transportation+=amount_in_float
            elif data[2] == "Health":
                health+=amount_in_float
            elif data[2] == "Education":
                education+=amount_in_float
            elif data[2] == "Refreshment":
                refreshment+=amount_in_float
            elif data[2] == "Saving/Investment":
                saving_investment+=amount_in_float
            else:
                others+=amount_in_float
        amount_list=[basic_needs,transportation,health,education,refreshment,saving_investment,others]
        actual_category_list=[]
        actual_amount_list=[]
        for category,amount in zip(category_list,amount_list):
            if amount != 0:
                actual_category_list.append(category)
                actual_amount_list.append(amount)
        plt.pie(actual_amount_list,labels=actual_category_list,autopct='%1.1f%%',startangle=90)
        plt.title("Pie-Chart visualization for expenses categorization")
        plt.show()






#main function
print("Welcome to your expenses/finance tracker\n\n")
print("All features you will ever need are listed below:\n1.Add transaction\n2.View transactions\n3.Filter transactions\n4.Transaction summary\n5.Exit")
while True:
    user_choice=int(input("\n\nPlease, enter your choice as a number corresponding to the feature that you wish to utilize: "))
    if user_choice not in [1,2,3,4,5]:
        print("Invalid input.Please try again..")
        continue
    else:
        if user_choice ==1:
            add_transactions()
        elif user_choice == 2:
            view_transactions()
        elif user_choice == 3:
            print("Filter mode available:\n1.By date\n2.By category")
            user_filter_choice = int(input("\nEnter your choice:"))
            if user_filter_choice==1:
                filter_transactions_by_date()
            elif user_filter_choice ==2:
                filter_transactions_by_category()
        elif user_choice == 4:
            view_summary()
        else:
            print("We are sorry to let you go")
            break
        continue_prompt=input("Do you wish to continue (Y/N): ").strip().capitalize()
        if continue_prompt in ["Y","Yes"]:
            print("1.Add transaction\n2.View transactions\n3.Filter transactions\n4.Transaction summary\n5.Exit")
            continue
        elif continue_prompt in ["N", "No"]:
            print("We are extremely sorry to let you go! ")
            break
        else:
            print("Invalid Choice\nTry again next time!")
            break

       
