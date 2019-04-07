import requests
import jdatetime
from bs4 import BeautifulSoup
import re
import mysql.connector
from googletrans import Translator
from sklearn import tree

def update_tables_list():
    cursor.execute("SHOW TABLES")
    my_tables = list(cursor.fetchall())
    my_tables_final = []
    for each in my_tables:
        my_tables_final.append(each[0])
    return my_tables_final

def create_table(table_name):
    cursor.execute("CREATE TABLE %s (car_model varchar(100), car_year varchar(100), car_usage varchar(100), car_city varchar(100), car_price varchar(100));" % (table_name))

def fetch_data(car_model):
    page_counter = 1
    translator = Translator()
    while page_counter <= 2:
        read = requests.get("https://bama.ir/car/%s?page=%i" % (car_model, page_counter))
        soup = BeautifulSoup(read.text, 'html.parser')
        result = soup.find_all('li', attrs={'itemtype': 'http://schema.org/Car'})
        for each in result:
            name = each.find('a', attrs={'class': 'cartitle cartitle-desktop'})
            province = each.find('span', attrs={'class': 'provice-mobile'})
            usage = each.find('p', attrs={'class': 'price hidden-xs'})
            price = each.find('p', attrs={'class': 'cost'})
            name = re.sub(r'\s+', ' ', name.text).strip()
            name_parts = name.split("،")
            year = name_parts[0]
            year = jdatetime.date(int(year),1,1).togregorian().year if year[:2] == "13" else year
            model = name_parts[2].strip()
            model = translator.translate(model).text
            if model.find("(") != -1:
                model = model[0:model.find("(") - 1]
            province = re.sub(r'\s+', ' ', province.text).strip()
            province = province[:len(province) - 1]
            province = translator.translate(province).text
            usage = re.sub(r'\s+', ' ', usage.text).strip()
            usage_parts = usage.split(" ")
            price = re.sub(r'\s+', ' ', price.text).strip()
            price_parts = price.split(" ")
            price = "N/A" if price.find("تماس بگيريد") != -1 or price.find("تماس بگیرید") != -1 else ("N/A" if price_parts[0].isalpha() else price_parts[0])
            if len(usage_parts) == 3:
                usage = "0" if usage_parts[1] == "صفر" else usage_parts[1]
            else:
                usage = "0"

            print(year)
            print(model)
            print(province)
            print(usage)
            print(price)

            cursor.execute('select count(1) from %s where car_model = "%s" and car_year = "%s" and car_usage = "%s" and car_city = "%s" and car_price = "%s";' % (car_model, model, year, usage, province, price))
            if cursor.fetchone()[0] == 0:
                print("INSERTED !")
                cursor.execute('INSERT INTO %s VALUES ("%s", "%s", "%s", "%s", "%s")' % (car_model,
                model, year, usage, province, price))
                cnx.commit()
            else:
                print("DENIED ! (found an equal record in the database !)")
            print("------------------------------------")
        print("PAGE", page_counter)
        print("------------------------------------")
        page_counter += 1

cnx = mysql.connector.connect(user="localhost", password="", host='127.0.0.1', database="Project")
cursor = cnx.cursor()
my_tables_final = update_tables_list()
cars_to_be_selected = {1: 'peugeot', 2: 'hyundai', 3: 'renault', 4: 'kia', 5: 'toyota', 6: 'bmw', 7: 'pride', 8: 'mvm', 9: 'lexus', 10: 'nissan', 11: 'mercedes-benz', 12: 'jac', 13: 'chery', 14: 'samand', 15: 'brilliance', 16: 'mazda', 17: 'dena', 18: 'haima', 19: 'tiba', 20: 'mitsubishi', 21: 'volkswagen', 22: 'ssang-yong', 23: 'dongfeng', 24: 'porsche', 25: 'mg', 26: 'henteng', 27: 'changan', 28: 'besturn', 29: 'lifan', 30: 'geely', 31: 'suzuki', 32: 'volvo', 33: 'citroen', 34: 'haval', 35: 'saina', 36: 'runna', 37: 'alfa-romeo', 38: 'zotye', 39: 'quick', 40: 'pick-up', 41: 'honda', 42: 'peykan', 43: 'jeep', 44: 'byd', 45: 'proton', 46: 'mini', 47: 'ds', 48: 'rigan', 49: 'foton', 50: 'chevrolet', 51: 'daewoo', 52: 'opel', 53: 'pazhan', 54: 'gac-gonow', 55: 'great-wall', 56: 'capra', 57: 'borgward', 58: 'land-rover', 59: 'maserati', 60: 'audi', 61: 'baic', 62: 'van', 63: 'amico', 64: 'ford', 65: 'landmark', 66: 'domy', 67: 'fiat', 68: 'dodge', 69: 'lotus', 70: 'jaguar', 71: 'oldsmobile', 72: 'buick', 73: 'chrysler', 74: 'hummer', 75: 'smart', 76: 'lincoln', 77: 'gmc', 78: 'pontiac', 79: 'subaru', 80: 'lamborghini', 81: 'maclaren', 82: 'bentley', 83: 'rolls-royce', 84: 'seat', 85: 'rayen', 86: 'cadillac'}
#
# for i in range(0,86):
#     read = requests.get("https://bama.ir/car")
#     soup = BeautifulSoup(read.text, 'html.parser')
#     result = soup.find('li', attrs={'id': 'brand-' + str(i)})
#     final_result = result.find('a', href=True)
#     cars_to_be_selected[i + 1] = final_result['href'][5:]
#     print(str(i + 1), "-", cars_to_be_selected[i + 1])

while True:
    counter = 1
    for each in cars_to_be_selected:
        print(counter, "-", cars_to_be_selected[counter])
        counter += 1

    selected = int(input("Please insert the number of your selected Brand (0-EXITE) : "))
    if selected != 0:
        while True:
            print("\033[H\033[J")
            print("------------------------------------")
            my_tables_final = update_tables_list()
            print("1-UPDATE DATABASE 2-PREDICT 3-BACK")
            order = int(input("Command : "))
            if order == 1:
                if cars_to_be_selected[selected] not in my_tables_final:
                    create_table(cars_to_be_selected[selected])
                fetch_data(cars_to_be_selected[selected])
                print("------------------------------------")
                print("UPDATED !")
                print("------------------------------------")
            elif order == 2:
                if cars_to_be_selected[selected] in my_tables_final:
                    cursor.execute("SELECT * FROM %s" % cars_to_be_selected[selected])
                    selected_brand_records = list(cursor.fetchall())
                    x = []
                    y = []
                    model_lists = []
                    city_lists = []
                    for each in selected_brand_records:
                        tmp_list = []
                        if each[0] not in model_lists:
                            model_lists.append(each[0])
                            tmp_list.append(len(model_lists) - 1)
                        else:
                            tmp_list.append(model_lists.index(each[0]))

                        tmp_list.append(int(each[1]))
                        prc = each[2][:each[2].find(",")] + each[2][each[2].find(",") + 1:]
                        tmp_list.append(int(prc))
                        if each[3] not in city_lists:
                            city_lists.append(each[3])
                            tmp_list.append(len(model_lists) - 1)
                        else:
                            tmp_list.append(city_lists.index(each[3]))
                        x.append(tmp_list)
                        y.append(each[4])

                    clf = tree.DecisionTreeClassifier()
                    clf = clf.fit(x, y)
                    print("Please enter the preferred %s Brand car details: " % cars_to_be_selected[selected])
                    all_models = ""
                    counter = 1
                    for each_car in model_lists:
                        all_models += " " + str(counter) + "-" + each_car
                        counter += 1
                    print("Models : " + all_models[1:])
                    preferred_model = int(input("Model  Number : "))
                    preferred_year = input("Year : ")
                    preferred_usage = input("Usage : ")
                    all_cities = ""
                    counter = 1
                    for each_city in city_lists:
                        all_cities += " " + str(counter) + "-" + each_city
                        counter += 1
                    print("Models : " + all_cities[1:])
                    preferred_city = int(input("City  Number : "))
                    data_to_be_calculated = []
                    data_to_be_calculated.append([preferred_model - 1, preferred_year, preferred_usage, preferred_city])
                    calculated_price = clf.predict(data_to_be_calculated)
                    print("Estimated Answer :", calculated_price[0])

                else:
                    print("NO RECORDS FOUND ! (Solution: UPDATE DATABASE)")
            elif order == 3:
                break
    else:
        print("------------------------------------")
        print("GOOD BYE :(")
        print("------------------------------------")
        break
cnx.close()