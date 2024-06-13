import numpy as np
from mysqlquerys import connect
from mysqlquerys import mysql_rm
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import traceback
import sys, os


class Masina:
    def __init__(self, ini_file, table_name='hyundai_ioniq'):
        '''
        :param ini_file:type=QFileDialog.getOpenFileName name=filename file_type=(*.ini;*.txt)
        '''
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        if isinstance(ini_file, dict):
            credentials = ini_file
        else:
            self.conf = connect.Config(ini_file)
            credentials = self.conf.credentials
        self.alimentari = mysql_rm.Table(credentials, table_name)
        self.types_of_costs = ["electric", "benzina", "intretinere", "asigurare", 'impozit', 'TüV']
        # try:
        #     self.dataBase = self.sql_rm.DataBase(self.conf.credentials)
        # except Exception as err:
        #     print(traceback.format_exc())

    # @property
    # def sql_rm(self):
    #     # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
    #     if self.conf.db_type == 'mysql':
    #         sql_rm = mysql_rm
    #     return sql_rm

    @property
    def no_of_records(self):
        return self.alimentari.noOfRows

    @property
    def default_interval(self):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        startDate = datetime(datetime.now().year - 1, datetime.now().month, datetime.now().day)
        endDate = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        return startDate, endDate

    @property
    def total_money(self):
        col = self.alimentari.returnColumn('brutto')
        return round(sum(col), 2)

    @property
    def tot_benzina(self):
        matches = [('type', 'benzina')]
        col = self.alimentari.returnCellsWhere('brutto', matches)
        return round(sum(col), 2)

    @property
    def tot_electric(self):
        matches = [('type', 'electric')]
        col = self.alimentari.returnCellsWhere('brutto', matches)
        return round(sum(col), 2)

    @property
    def monthly(self):
        return round((self.monthly_benzina+self.monthly_electric), 2)

    @property
    def monthly_benzina(self):
        matches = [('type', 'benzina')]
        money = self.alimentari.returnCellsWhere('brutto', matches)
        all_dates = self.alimentari.returnColumn('data')
        start_date = min(all_dates)
        finish_date = max(all_dates)
        total_money = round(sum(money), 2)
        days = (finish_date - start_date).days
        average_day_per_month = 365/12
        monthly = (average_day_per_month * total_money) / days
        return round(monthly, 2)

    @property
    def monthly_electric(self):
        matches = [('type', 'electric')]
        money = self.alimentari.returnCellsWhere('brutto', matches)
        all_dates = self.alimentari.returnColumn('data')
        start_date = min(all_dates)
        finish_date = max(all_dates)
        total_money = round(sum(money), 2)
        days = (finish_date - start_date).days
        average_day_per_month = 365/12
        monthly = (average_day_per_month * total_money) / days
        return round(monthly, 2)

    @property
    def db_start_date(self):
        all_dates = self.alimentari.returnColumn('data')
        start_date = min(all_dates)
        return start_date

    @property
    def db_last_record_date(self):
        all_dates = self.alimentari.returnColumn('data')
        finish_date = max(all_dates)
        return finish_date

    @property
    def table_alimentari(self):
        arr = [('', 'Alimentari[€]', 'Benzina[€]', 'Electric[€]')]
        if self.no_of_records > 0:
            total_alim = self.tot_benzina + self.tot_electric
            arr.append(('Monthly', self.monthly, self.monthly_benzina, self.monthly_electric))
            arr.append(('Total', total_alim, self.tot_benzina, self.tot_electric))
        else:
            arr.append(('Monthly', None, None, None))
            arr.append(('Total', None, None, None))

        arr = np.atleast_2d(arr)
        return arr

    @property
    def table_totals(self):
        types = ['benzina', 'electric', 'asigurare', 'impozit', 'TüV', 'intretinere']
        table = []
        for year in reversed(range(self.db_start_date.year, self.db_last_record_date.year+1)):
            # print(year)
            dd = {}
            dd['year'] = year
            startTime = datetime(year, 1, 1)
            endTime = datetime(year+1, 1, 1)
            rows = self.alimentari.returnRowsOfYear('data', startTime, 'data', endTime)
            arr = np.atleast_2d(rows)
            tot = 0
            for t in types:
                indx = np.where(arr[:,self.alimentari.columnsNames.index('type')] == t)
                col = arr[indx, self.alimentari.columnsNames.index('brutto')]
                value = sum(col[0])
                value = round(value, 2)
                dd[t] = value
                tot += value
            dd['total/row'] = round(tot, 2)
            table.append(dd)
        table_head = tuple(dd.keys())
        arr = [table_head]
        for tab in table:
            row = []
            for k, v in tab.items():
                row.append(v)
            arr.append(tuple(row))
        arr = np.atleast_2d(arr)
        row_totals = ['totals']
        total_total = 0
        for col in range(1, arr.shape[1]):
            # print(arr[0, col], round(sum(arr[1:, col].astype(float)), 2))
            val = round(sum(arr[1:, col].astype(float)), 2)
            row_totals.append(val)
            total_total += val
        row_tot = np.array(row_totals)
        new_arr = np.insert(arr, 1, row_tot, axis=0)
        return new_arr

    @property
    def last_records(self):
        table_head = self.alimentari.columnsNames
        table_head.remove('file')
        last_records = [table_head]
        for typ in self.types_of_costs:
            matches = [('type', typ)]
            table = self.alimentari.filterRows(matches, order_by=('data', 'DESC'))
            if typ == 'electric':
                already_listed = []
                for row in table:
                    provider = row[table_head.index('comment')]
                    if provider not in already_listed:
                        last_records.append(row)
                        already_listed.append(provider)
                continue
            if table:
                last_records.append(table[0])

        last_records = np.atleast_2d(last_records)
        # for i in last_records:
        #     print(i)
        # print(50*'+')
        return last_records

    def get_monthly_interval(self, month:str, year):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        mnth = datetime.strptime(month, "%B").month
        startDate = datetime(year, mnth, 1)

        if mnth != 12:
            lastDayOfMonth = datetime(year, mnth + 1, 1) - timedelta(days=1)
        else:
            lastDayOfMonth = datetime(year + 1, 1, 1) - timedelta(days=1)

        return startDate, lastDayOfMonth

    def get_all_alimentari(self):
        cols = []
        for k, v in self.alimentari.columnsDetProperties.items():
            if v[0] == 'longblob':
                continue
            cols.append(k)
        alimentari = self.alimentari.returnColumns(cols)
        # alimentari = self.alimentari.returnAllRecordsFromTable()
        alimentari = np.atleast_2d(alimentari)
        alimentari = np.insert(alimentari, 0, cols, axis=0)
        return alimentari

    def get_alimentari_for_interval_type(self, selectedStartDate, selectedEndDate, alim_type):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        matches = [('data', (selectedStartDate, selectedEndDate))]
        if alim_type:
            matches.append(('type', alim_type))
        # print(matches)
        table = self.alimentari.filterRows(matches, order_by=('data', 'DESC'))

        if table:
            table_head = []
            for col_name, prop in self.alimentari.columnsDetProperties.items():
                # print(col_name, prop)
                if prop[0] == 'longblob':
                    continue
                table_head.append(col_name)
            arr = np.atleast_2d(table)
            arr = np.insert(arr, 0, np.array(table_head), axis=0)
        else:
            arr = np.atleast_2d(np.array(self.alimentari.columnsNames))
        return arr

    def upload_file(self, file, id):
        print(file, id)
        self.alimentari.changeCellContent('file', file, 'id', id)
        _, file_name = os.path.split(file)
        self.alimentari.changeCellContent('file_name', file_name, 'id', id)
        # self.alimentari.addNewRow(cols, vals)

    def insert_new_alim(self, data, alim_type, brutto, amount, refuel, other, recharges, km, comment, file):
        '''
        :param data:type=dateTime name=date
        :param alim_type:type=comboBox name=alim_type items=[electric,benzina,TüV,intretinere]
        :param brutto:type=text name=brutto
        :param amount:type=text name=amount
        :param refuel:type=text name=refuel
        :param other:type=text name=other
        :param recharges:type=text name=recharges
        :param km:type=text name=km
        :param comment:type=text name=comment
        :param file:type=QFileDialog.getOpenFileName name=file
        '''
        _, file_name = os.path.split(file)
        cols = ['data', 'type', 'brutto', 'amount', 'refuel', 'other', 'recharges', 'ppu', 'km', 'comment', 'file', 'file_name']
        try:
            if isinstance(brutto, str) and ',' in brutto:
                brutto = brutto.replace(',', '.')
            brutto = float(brutto)
        except:
            brutto = None
        try:
            if isinstance(amount, str) and ',' in amount:
                amount = amount.replace(',', '.')
            amount = float(amount)
        except:
            amount = None
        try:
            if isinstance(refuel, str) and ',' in refuel:
                refuel = refuel.replace(',', '.')
            refuel = float(refuel)
        except:
            refuel = None
        try:
            if isinstance(other, str) and ',' in other:
                other = other.replace(',', '.')
            other = float(other)
        except:
            other = None
        try:
            if isinstance(recharges, str) and ',' in recharges:
                recharges = recharges.replace(',', '.')
            recharges = float(recharges)
        except:
            recharges = None
        try:
            km = int(km)
        except:
            km = None

        ppu = round(float(brutto) / float(amount), 3)
        vals = [data, alim_type, brutto, amount, refuel, other, recharges, ppu, km, comment, file, file_name]

        # for i in range(len(cols)):
        #     print(cols[i], vals[i], type(vals[i]))
        self.alimentari.addNewRow(cols, vals)

    def create_sql_table(self, table_name):
        masina_sql = r'static\sql\auto.sql'
        mysql_rm.DataBase(self.conf.credentials).createTableFromFile(masina_sql, table_name)
