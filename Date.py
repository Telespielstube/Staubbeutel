import datetime 
 
class Date():

     # Function to get the current minutes, hour, day, month and year.
    def get_date(self):
        now = datetime.datetime.now() 
        return now
