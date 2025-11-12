import tabulate
import os
import pandas as pd
import datetime

class Main:
    def __init__(self, Main_Path, Sub_Path):
        self.main_path = Main_Path
        self.sub_path = Sub_Path
        self.attendance = pd.DataFrame()
        self.subject_data = {}
        self.Extract_data()
        self.Main()

    def Extract_data(self):
        self.attendance = pd.read_csv(self.main_path + '.csv')
        for subject in os.listdir(self.sub_path):
            subject_name = subject[:-4]
            self.subject_data[subject_name] = pd.read_csv(os.path.join(self.sub_path, subject))
    
    def Store_data(self):
        self.attendance.to_csv(self.main_path + '.csv', index=False)
        for subject_name, data in self.subject_data.items():
            data.to_csv(os.path.join(self.sub_path, subject_name + '.csv'), index=False)
        self.Main()
    
    def Display_data(self,Table_Format='pretty',Table=True):
        if Table:
            print(tabulate.tabulate(self.attendance, headers='keys', tablefmt=Table_Format))
            for subject_name, data in self.subject_data.items():
                print(f"\nSubject: {subject_name}")
                print(tabulate.tabulate(data, headers='keys', tablefmt=Table_Format))
        else:
            print(self.attendance)
            for subject_name, data in self.subject_data.items():
                print(f"\nSubject: {subject_name}")
                print(data)
    
    def Main(self):
        self.Display_data()
        print("\n")
        print('What do you want to do?')
        print('1. Add Attendance')
        print('2. Toggle Attendance')
        print("3. Exit")
        print("\n")
        User_input=int(input("Enter your choice (1/2/3): "))
        if User_input==1:
            Subject_list=self.attendance['Subject'].tolist()
            print("Chose Subject Name: ")
            print(Subject_list)
            subject=input("Enter Subject Name or Index: ") 
            if subject.isdigit():
                subject=Subject_list[int(subject)]
            present = input("Present? (Y/N): ").capitalize()[0] in ['Y','T',1]
            self.Add_Attendance(subject, present)
        elif User_input==2:
            Subject_list=self.attendance['Subject'].tolist()
            print("Chose Subject Name: ")
            print(Subject_list)
            subject=input("Enter Subject Name or Index: ") 
            if subject.isdigit():
                subject=Subject_list[int(subject)]
            input_date = input("Enter Date [Format: Wed Nov 12 2025]: ")
            self.Toggle_Attendance(subject, datetime.datetime.strptime(input_date, "%a %b %d %Y"))
        elif User_input==3:
            exit()
        else:
            print("Invalid Input")
            self.Main()
        
    def Add_Attendance(self, subject, present):
        subject_df = self.subject_data[subject]
        new_row = pd.DataFrame([{
            'Lec_Date': datetime.datetime.now().strftime("%a %b %d %Y"),
            'Status': bool(present)
        }])
        subject_df = pd.concat([subject_df, new_row], ignore_index=True)
        self.attendance.loc[self.attendance['Subject'] == subject, 'Total Classes'] += 1
        if present:
            self.attendance.loc[self.attendance['Subject'] == subject, 'Present'] += 1
        self.attendance.loc[self.attendance['Subject'] == subject, 'Attendance Percentage'] = \
            (self.attendance.loc[self.attendance['Subject'] == subject, 'Present'] / 
             self.attendance.loc[self.attendance['Subject'] == subject, 'Total Classes'] * 100).round(2)
        self.attendance.loc[self.attendance['Subject'] == subject, 'Last Updated'] = datetime.datetime.now().strftime("%a %b %d %Y")
        self.subject_data[subject] = subject_df
        self.Store_data()

    def Toggle_Attendance(self, subject, date):
        print(self.subject_data[subject].loc[datetime.datetime.strptime(self.subject_data[subject]['Lec_Date'],"%a %b %d %Y") == date, 'Status'])
        #present = bool(self.subject_data[subject].loc[self.subject_data[subject]['Lec_Date'] == date, 'Status'].values[0])
        present = True
        self.subject_data[subject].loc[self.subject_data[subject]['Lec_Date'] == date, 'Status'] = not present
        if present:
            self.attendance.loc[self.attendance['Subject'] == subject, 'Present'] -= 1
        else:
            self.attendance.loc[self.attendance['Subject'] == subject, 'Present'] += 1
        self.attendance.loc[self.attendance['Subject'] == subject, 'Attendance Percentage'] = \
            (self.attendance.loc[self.attendance['Subject'] == subject, 'Present'] / 
             self.attendance.loc[self.attendance['Subject'] == subject, 'Total Classes'] * 100).round(2)
        self.attendance.loc[self.attendance['Subject'] == subject, 'Last Updated'] = datetime.datetime.now().strftime("%a %b %d %Y")
        self.Store_data()

if __name__ == '__main__':
    Main('Data/Overall/Attendance', 'Data/Subject_Data/')