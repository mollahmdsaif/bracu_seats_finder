import os 
import sys 
import pandas as pd 
from bs4 import BeautifulSoup
import requests

url = requests.get('http://admissions.bracu.ac.bd/academia/admissionRequirement/getAvailableSeatStatus')

def update_seats_data():
    data = [] 
    list_header = [] 
    soup = BeautifulSoup(url.content,'html.parser') 
    header = soup.find_all("table")[0].find("tr") 
    for items in header: 
    	try: 
            list_header.append(items.get_text()) 
        except: 
            continue
    HTML_data = soup.find_all("table")[0].find_all("tr")[1:] 
    for element in HTML_data: 
        sub_data = [] 
        for sub_element in element: 
            try: 
                sub_data.append(sub_element.get_text()) 
            except: 
                continue
        data.append(sub_data) 
    dataFrame = pd.DataFrame(data = data, columns = list_header) 
    dataFrame.to_csv('seats_data.csv')
    #'seat update message'
    #print('Seats Data Updated')
    org_data = {}
    with open('seats_data.csv', 'r') as f:
        data = f.readlines()
        for course in data:
            course_data = course.strip().split(',')
            org_data[course_data[2]+'_S'+course_data[6]] = {
                                        'Time'   : course_data[7].replace(') ', ')  ').split('  '),
                                        'Seat'   : {
                                                    'Total'     : int(course_data[8]),
                                                    'Booked'    : int(course_data[9]),
                                                    'Remaining' : int(course_data[10]),
                                                    }
                                        }
    return org_data
    
    
def find_data(course_name, section, *args):
    data = update_seats_data()
    for attribute in args:
        print(data[course_name+'_S'+section][attribute])
    
    
    
def main():
    
    print('CSE437, S02, Seats:    ', end='')
    find_data('CSE437', '01', 'Seat')
    

if __name__ == '__main__':
    main()
