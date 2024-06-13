from datetime import date
import auto


def get_auto_vals(ini_file, selectedStartDate, selectedEndDate):
    car = auto.Masina(ini_file)
    alimentari = car.get_alimentari_for_interval_type(selectedStartDate, selectedEndDate, None)
    for i in alimentari:
        print(i)
    # print(auto.table_totals)


def main():
    selectedStartDate = date(2021, 12, 30)
    selectedEndDate = date(2024, 1, 29)

    masina_ini = r"D:\Python\MySQL\masina.ini"
    # get_auto_vals(income_ini, selectedStartDate, selectedEndDate)
    car = auto.Masina(masina_ini)
    print(car.last_records)


if __name__ == '__main__':
    main()
