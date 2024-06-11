import base64
import json
import socket
import ssl
import struct
import subprocess
from calendar import monthrange
from datetime import datetime, timedelta
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib import request, parse


class Dict2Dot(dict):
    def __getattr__(self, key):
        if key in self:
            value = self[key]
            if isinstance(value, dict):
                return Dict2Dot(value)
            return value
        else:
            raise AttributeError(f"'{self.__class__.__name__}' objesinde '{key}' anahtarı bulunamadı.")


class CemirUtils:

    def __init__(self, data=None, dbname=None, dbuser=None, dbpassword=None, dbhost='localhost', dbport=5432, timeout=3, dbcreate_db_if_not_exists=False):
        """
        CemirUtils sınıfının yapıcı fonksiyonu.
        Verilen veriyi sınıfın 'data' değişkenine atar.

        Parametre:
        data (list, dict): İşlenecek sayısal veri listesi veya sözlük.
        """
        self.data = data
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpassword = dbpassword
        self.dbhost = dbhost
        self.dbport = dbport
        self.timeout = timeout

        if dbcreate_db_if_not_exists:
            self.psql_create_database(dbname)

    def getmethods(self):
        """
        CemirUtils sınıfının mevcut tüm metodlarının isimlerini yazdırır.
        """
        return [method for method in dir(CemirUtils) if callable(getattr(CemirUtils, method)) and not method.startswith("__")]

    def listen_for_icmp(self, print_query=False, insert_db=True):
        """
        NOT: scriptin çalışması için sudo gerektirir.

        Örnek Servis:

        sudo nano /etc/systemd/system/ping_logger.service

            [Unit]
            Description=Ping Logger Service
            After=network.target

            [Service]
            ExecStart=/usr/bin/python3 /path/to/ping_logger.py
            Restart=always
            User=root
            Group=root

            [Install]
            WantedBy=multi-user.target

        * sudo systemctl daemon-reload
        * sudo systemctl enable ping_logger
        * sudo systemctl start ping_logger

        :param insert_db: bool
        :param print_query: bool
        :return:
        """
        if insert_db:
            self.psql_insert_raw("""CREATE TABLE ping_log (id SERIAL PRIMARY KEY, contents JSONB NOT NULL);""")

        # Raw soket oluşturma
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        except:
            print("raw soket dinleme işlemleri için sudo yetkisi gerekir!!")
            exit(1)

        while True:
            # Paket alımı
            packet, addr = sock.recvfrom(65565)
            packet_length = len(packet)

            # IP başlığı ayrıştırma
            ip_header = packet[0:20]
            iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
            version_ihl = iph[0]
            version = version_ihl >> 4
            ihl = version_ihl & 0xF
            iph_length = ihl * 4
            ttl = iph[5]
            protocol = iph[6]
            source_ip = socket.inet_ntoa(iph[8])
            dest_ip = socket.inet_ntoa(iph[9])

            # ICMP başlığı ayrıştırma
            icmp_header = packet[iph_length:iph_length + 8]
            icmph = struct.unpack('!BBHHH', icmp_header)
            icmp_type = icmph[0]
            code = icmph[1]
            checksum = icmph[2]
            packet_id = icmph[3]
            sequence = icmph[4]

            if icmp_type == 8:  # Ping Request
                timestamp = datetime.now()
                contents = {
                    "sequence": sequence,
                    "dest_ip": dest_ip,
                    "source_ip": source_ip,
                    "ttl": ttl,
                    "timestamp": timestamp.isoformat(),
                    "packet_length": packet_length,

                    # "icmp_type": icmp_type,
                    # "checksum": checksum,
                    # "packet_id": packet_id,
                    # "protocol": protocol
                }

                if insert_db:
                    self.psql_insert_raw(f"""INSERT INTO ping_log (contents) VALUES ('{json.dumps(contents)}');""")

                if print_query:
                    print(contents)

    def psql_parse_psql_output(self, output):
        """
        psql komutunun çıktısını parse ederek dict yapısına çevirir.

        Args:
            output (str): psql komutunun çıktısı.

        Returns:
            dict: Dict formatında çıktı.
        """
        lines = output.strip().split('\n')
        headers = lines[0].split('|')
        data = []

        for line in lines[2:-1]:  # İlk iki satır ve son satır başlık ve ayırıcılar olduğu için atlanır
            values = line.split('|')
            data.append({header.strip(): value.strip() for header, value in zip(headers, values)})

        return data

    def psql_execute_query(self, query, dbname=None):
        """
        Veritabanına SQL sorgusu gönderir ve sonucu döndürür.

        Args:
            query (str): SQL sorgusu.
            dbname (str, optional): Veritabanı adı. Eğer verilmezse, self.dbname kullanılır.

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi.
        """
        if dbname is None:
            dbname = self.dbname

        query = query.replace("\n", "").strip()
        command = f'''PGPASSWORD={self.dbpassword} psql -h {self.dbhost} -p {self.dbport} -U {self.dbuser} -d {dbname} -c {json.dumps(query, ensure_ascii=False)}'''

        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=self.timeout)
            if result.returncode != 0:
                error_info = {
                    "error": "Query failed",
                    "message": result.stderr.strip()
                }
                return json.dumps(error_info, ensure_ascii=False)
            return result.stdout.strip()
        except subprocess.TimeoutExpired as e:
            error_info = {
                "error": "TimeOut",
                "message": f"timed out"
            }
            return json.dumps(error_info, ensure_ascii=False)

    def psql_insert_raw(self, query, print_query=False):
        if print_query: print(query)
        return self.psql_execute_query(query)

    def psql_insert(self, table_name, columns, values, get_id=False):
        """
        Veritabanına yeni kayıt ekler.

        Args:
            table_name (str): Tablo adı.
            columns (tuple): Kolon adları (örnek: ("id", "name", "data")).
            values (tuple): Kolon değerleri (örnek: (1, "John Doe", {"age": 30, "city": "Istanbul"})).
            get_id (bool): İşlem yapılan ID

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi.
        """
        columns_str = ', '.join(columns)

        formatted_values = []
        for value in values:
            if isinstance(value, dict):
                formatted_values.append(f"'{json.dumps(value)}'::jsonb")
            else:
                formatted_values.append(f"'{value}'")

        values_str = ', '.join(formatted_values)
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})"
        if get_id:
            query += f" RETURNING id;"
            try:
                result = self.psql_execute_query(query).split()[2]
                return {"error": False, "id": int(result)}
            except ValueError:
                return self.psql_execute_query(query)

        return self.psql_execute_query(query)

    def psql_create_database(self, dbname):
        """
        Belirtilen ad ile yeni bir veritabanı oluşturur.

        Args:
            dbname (str): Oluşturulacak veritabanının adı.

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi.
        """
        query = f"CREATE DATABASE {dbname};"
        return self.psql_execute_query(query, dbname='postgres')

    def psql_create_table(self, table_name, schema):
        """
        Veritabanında tablo oluşturur.

        Args:
            table_name (str): Tablo adı.
            schema (str): Tablo şeması (örnek: "id SERIAL PRIMARY KEY, name VARCHAR(100), data JSONB").

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi.
        """
        query = f"CREATE TABLE {table_name} ({schema});"
        return self.psql_execute_query(query)

    def psql_read(self, table_name, columns='*', condition=None, jsonb_field=None, jsonb_key=None):
        """
        Veritabanından kayıt okur.

        Args:
            table_name (str): Tablo adı.
            columns (str or tuple): Kolon adları veya * (örnek: "*" veya ("id", "name")).
            condition (str): Koşul (örnek: "id = 1").
            jsonb_field (str, optional): JSONB alan adı.
            jsonb_key (str, optional): JSONB alanındaki anahtar adı.

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi.
        """
        if isinstance(columns, tuple):
            columns = ', '.join(columns)

        query = f"SELECT {columns} FROM {table_name}"
        if jsonb_field and jsonb_key:
            query = f"SELECT {columns}, {jsonb_field} ->> '{jsonb_key}' AS {jsonb_key} FROM {table_name}"

        if condition:
            query += f" WHERE {condition}"
        query += ";"

        return self.psql_parse_psql_output(self.psql_execute_query(query))

    def psql_update(self, table_name, updates, condition, get_id=False):
        """
        Veritabanındaki kaydı günceller.

        Args:
            table_name (str): Tablo adı.
            updates (dict): Güncellemeler (örnek: {"name": "Jane Doe"}).
            condition (str): Koşul (örnek: "id = 1").
            get_id (bool): İşlem yapılan ID
        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi.
        """
        update_str = ', '.join(f"{k} = '{json.dumps(v)}'" if isinstance(v, dict) else f"{k} = '{v}'" for k, v in updates.items())
        query = f"UPDATE {table_name} SET {update_str} WHERE {condition}"
        if get_id:
            query += f" RETURNING id;"
            try:
                result = self.psql_execute_query(query).split()[2]
                return {"error": False, "id": int(result)}
            except ValueError:
                return self.psql_execute_query(query)

        return self.psql_execute_query(query)

    def psql_delete(self, table_name, condition):
        """
        Veritabanındaki kaydı siler.

        Args:
            table_name (str): Tablo adı.
            condition (str): Koşul (örnek: "id = 1").

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi.
        """
        query = f"DELETE FROM {table_name} WHERE {condition};"
        try:
            result = int(self.psql_execute_query(query).split()[1])
            if result >= 0:
                return {"error": False}
        except:
            return self.psql_execute_query(query)

    def time_days_between_dates(self, date1, date2):
        """
        İki tarih arasındaki gün sayısını hesaplar.


        Args:
            date1 (str): İlk tarih (YYYY-MM-DD formatında).
            date2 (str): İkinci tarih (YYYY-MM-DD formatında).


        Returns:
            int: İki tarih arasındaki gün sayısı.
        """
        date_format = "%Y-%m-%d"
        d1 = datetime.strptime(date1, date_format)
        d2 = datetime.strptime(date2, date_format)
        delta = d2 - d1
        return delta.days

    def time_hours_minutes_seconds_between_times(self, time1, time2):
        """
        İki zaman arasındaki saat, dakika ve saniye farkını hesaplar.


        Args:
            time1 (str): İlk zaman (HH:MM:SS formatında).
            time2 (str): İkinci zaman (HH:MM:SS formatında).


        Returns:
            tuple: Saat, dakika ve saniye farkı.
        """
        time_format = "%H:%M:%S"
        t1 = datetime.strptime(time1, time_format)
        t2 = datetime.strptime(time2, time_format)
        delta = t2 - t1
        total_seconds = delta.total_seconds()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return int(hours), int(minutes), int(seconds)

    def time_until_date(self, future_date):
        """
        Belirli bir tarihe kadar kalan yıl, ay, gün, saat, dakika ve saniye hesaplar.


        Args:
            future_date (str): Gelecek tarih (YYYY-MM-DD HH:MM:SS formatında).


        Returns:
            tuple: Kalan gün, saat, dakika ve saniye.
        """
        date_format = "%Y-%m-%d %H:%M:%S"
        now = datetime.now()
        future = datetime.strptime(future_date, date_format)
        delta = future - now
        days = delta.days
        seconds = delta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return days, hours, minutes, seconds

    def time_add_days_to_date(self, date, days):
        """
        Belirtilen tarihe gün sayısı ekleyerek yeni bir tarih hesaplar.


        Args:
            date (str): Başlangıç tarihi (YYYY-MM-DD formatında).
            days (int): Eklenecek gün sayısı.

        * Örnek:
        >>> utils =CemirUtils()
        >>> utils.time_add_days_to_date("2024-05-10", 100)

        Returns:
            datetime: Yeni tarih.
        """
        date_format = "%Y-%m-%d"
        d = datetime.strptime(date, date_format)
        new_date = d + timedelta(days=days)
        return new_date

    def time_add_days_and_format(self, date, days):
        """
        Belirtilen tarihe gün sayısı ekleyip yeni tarihi istenilen dilde gün adı ile birlikte formatlar.


        Args:
            date (str): Başlangıç tarihi (YYYY-MM-DD formatında).
            days (int): Eklenecek gün sayısı.
            locale (str): Dil kodu (varsayılan 'en').


        Returns:
            str: Formatlanmış yeni tarih ve gün adı.
        """
        new_date = self.time_add_days_to_date(date, days)
        formatted_date = new_date.strftime("%Y-%m-%d")
        return f"{formatted_date} ({new_date})"

    def time_is_weekend(self, date):
        """
        Bir tarihin hafta sonu olup olmadığını kontrol eder.


        Args:
            date (str): Tarih (YYYY-MM-DD formatında).


        Returns:
            bool: Hafta sonu ise True, değilse False.
        """
        date_format = "%Y-%m-%d"
        d = datetime.strptime(date, date_format)
        return d.weekday() >= 5  # 5 = Cumartesi, 6 = Pazar

    def time_is_leap_year(self, year):
        """
        Bir yılın artık yıl olup olmadığını kontrol eder.


        Args:
            year (int): Yıl.


        Returns:
            bool: Artık yıl ise True, değilse False.
        """
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def time_days_in_month(self, year, month):
        """
        Bir ay içindeki gün sayısını döndürür.


        Args:
            year (int): Yıl.
            month (int): Ay.


        Returns:
            int: Ay içindeki gün sayısı.
        """
        return monthrange(year, month)[1]

    def time_next_weekday(self, date, weekday):
        """
        Bir tarihten sonraki belirli bir günün tarihini döndürür (örneğin, bir sonraki Pazartesi).


        Args:
            date (str): Başlangıç tarihi (YYYY-MM-DD formatında).
            weekday (int): Hedef gün (0 = Pazartesi, 1 = Salı, vb.).


        Returns:
            datetime: Bir sonraki hedef günün tarihi.
        """
        date_format = "%Y-%m-%d"
        d = datetime.strptime(date, date_format)
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:  # Hedef gün zaten bu hafta geçmiş
            days_ahead += 7
        return d + timedelta(days=days_ahead)

    @staticmethod
    def time_todatetime(date):
        """
        Bir tarihi datetime türüne çevirir

        Args:
            date (str): Tarih (YYYY-MM-DD formatında).

        * Örnek:
        >>> utils =CemirUtils()
        >>> print(utils.time_todatetime("2024-05-10"))

        Returns:
            str: Formatlanmış tarih.
        """

        return datetime.strptime(date, "%Y-%m-%d")

    def time_since(self, past_date):
        """
        Belirli bir tarihten geçen yıl, ay, gün, saat, dakika ve saniyeyi hesaplar.

        Parametre:
        past_date (str): Geçmiş tarih (yyyy-mm-dd HH:MM:SS formatında)

        Dönüş:
        dict: Geçen yıl, ay, gün, saat, dakika ve saniyeleri içeren sözlük.

        Örnek:
        >>> cem = CemirUtils(None)
        >>> cem.time_since('2020-01-01 00:00:00')
        {'years': 4, 'months': 4, 'days': 25, 'hours': 14, 'minutes': 35, 'seconds': 10}
        """
        past_date = datetime.strptime(past_date, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        delta = now - past_date

        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = (delta.days % 365) % 30
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        seconds = delta.seconds % 60

        return {
            'years': years,
            'months': months,
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        }

    def time_business_days_between_dates(self, date1, date2):
        """
        İki tarih arasındaki iş günü sayısını hesaplar.


        Args:
        date1 (str): İlk tarih (YYYY-MM-DD formatında).
        date2 (str): İkinci tarih (YYYY-MM-DD formatında).


        Returns:
            int: İki tarih arasındaki iş günü sayısı.
        """
        date_format = "%Y-%m-%d"
        d1 = datetime.strptime(date1, date_format)
        d2 = datetime.strptime(date2, date_format)
        day_generator = (d1 + timedelta(x) for x in range((d2 - d1).days + 1))
        business_days = sum(1 for day in day_generator if day.weekday() < 5)
        return business_days

    def str_replace_multiple(self, text, replacements):
        """
        Verilen metinde çoklu değiştirme işlemi yapar.


        Args:
            text (str): Değiştirilecek metin.
            replacements (dict): Değiştirilecek değer çiftleri (anahtar: eski değer, değer: yeni değer).

        Örnek:

        >>> utils = CemirUtils()
        >>> print(utils.str_replace_multiple("asd muslu asd", {"asd": "muslu", "muslu": "emir"}))

        Returns:
            str: Değiştirilmiş metin.
        """
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def str_replace_with_last(self, text, values):
        """
        Verilen metinde belirtilen tüm değerleri son değer ile değiştirir.


        Args:
            text (str): Değiştirilecek metin.
            values (tuple): Değiştirilecek değerler.

        Örnek:

        >>> utils = CemirUtils()
        >>> print(utils.str_replace_with_last("asd muslu asd", ("muslu", "emir"}))


        Returns:
            str: Değiştirilmiş metin.
        """
        if not values:
            return text
        last_value = values[-1]
        for value in values[:-1]:
            text = text.replace(value, last_value)
        return text

    def list_multiply_by_scalar(self, scalar):
        """
        Veri listesindeki her bir elemanı verilen skaler değer ile çarpar.

        Parametre:
        scalar (int, float): Çarpılacak skaler değer.

        Dönüş:
        list: Skaler değer ile çarpılmış veri listesi.

        Örnek:
        >>> ceml = CemirUtils([1, 2, 3])
        >>> ceml.list_multiply_by_scalar(2)
        [2, 4, 6]
        """
        if isinstance(self.data, list):
            return [x * scalar for x in self.data]
        else:
            raise TypeError("Veri tipi liste olmalıdır.")

    def list_get_frequency(self, value):
        """
        Verilen değerin veri listesinde kaç kez geçtiğini sayar.

        Parametre:
        value: Sayılacak değer.

        Dönüş:
        int: Değerin listede kaç kez geçtiği.

        Örnek:
        >>> ceml = CemirUtils([1, 2, 2, 3])
        >>> ceml.list_get_frequency(2)
        2
        """
        if isinstance(self.data, list):
            return self.data.count(value)
        else:
            raise TypeError("Veri tipi liste olmalıdır.")

    def list_reverse(self):
        """
        Veri listesini tersine çevirir.

        Dönüş:
        list: Tersine çevrilmiş veri listesi.

        Örnek:
        >>> ceml = CemirUtils([1, 2, 3])
        >>> ceml.list_reverse()
        [3, 2, 1]
        """
        if isinstance(self.data, list):
            return self.data[::-1]
        else:
            raise TypeError("Veri tipi liste olmalıdır.")

    def list_get_max_value(self):
        """
        Veri listesindeki en büyük değeri döner.

        Dönüş:
        int, float: Veri listesindeki en büyük değer.

        Örnek:
        >>> ceml = CemirUtils([1, 2, 3])
        >>> ceml.list_get_max_value()
        3
        """
        if isinstance(self.data, list):
            return max(self.data)
        else:
            raise TypeError("Veri tipi liste olmalıdır.")

    def list_get_min_value(self):
        """
        Veri listesindeki en küçük değeri döner.

        Dönüş:
        int, float: Veri listesindeki en küçük değer.

        Örnek:
        >>> ceml = CemirUtils([1, 2, 3])
        >>> ceml.list_get_min_value()
        1
        """
        if isinstance(self.data, list):
            return min(self.data)
        else:
            raise TypeError("Veri tipi liste olmalıdır.")

    def dict_filter_by_key(self, key):
        """
        Sözlükte veya sözlüklerin bulunduğu listede belirtilen anahtara sahip elemanları filtreler.

        Parametreler:
        key: Filtreleme yapılacak anahtar.

        Dönüş:
        dict, list: Filtrelenmiş veri.

        Örnek:
        >>> cemd = CemirUtils({'a': 1, 'b': 2, 'c': 3})
        >>> cemd.dict_filter_by_key('b')
        {'b': 2}

        >>> ceml = CemirUtils([{'a': 1}, {'b': 2}, {'a': 3}])
        >>> ceml.dict_filter_by_key('a')
        [{'a': 1}, {'a': 3}]
        """
        if isinstance(self.data, dict):
            return {k: v for k, v in self.data.items() if k == key}
        elif isinstance(self.data, list):
            return [item for item in self.data if isinstance(item, dict) and key in item]
        else:
            raise TypeError("Veri tipi sözlük veya sözlük listesi olmalıdır.")

    def dict_get_keys(self):
        """
        Sözlükteki veya sözlüklerin bulunduğu listedeki anahtarları döner.

        Dönüş:
        list: Anahtarlar listesi.

        Örnek:
        >>> cemd = CemirUtils({'a': 1, 'b': 2, 'c': 3})
        >>> cemd.dict_get_keys()
        ['a', 'b', 'c']

        >>> ceml = CemirUtils([{'a': 1}, {'b': 2}, {'a': 3}])
        >>> ceml.dict_get_keys()
        ['a', 'b', 'a']
        """
        if isinstance(self.data, dict):
            return list(self.data.keys())
        elif isinstance(self.data, list):
            return [key for item in self.data if isinstance(item, dict) for key in item.keys()]
        else:
            raise TypeError("Veri tipi sözlük veya sözlük listesi olmalıdır.")

    def dict_merge(self, *dicts):
        """
        Verilen sözlükleri birleştirir.

        Parametreler:
        *dicts (dict): Birleştirilecek sözlükler.

        Dönüş:
        dict: Birleştirilmiş sözlük.

        Örnek:
        >>> cemd = CemirUtils({})
        >>> cemd.dict_merge({'a': 1}, {'b': 2})
        {'a': 1, 'b': 2}
        """
        if all(isinstance(d, dict) for d in dicts):
            merged = {}
            for d in dicts:
                merged.update(d)
            return merged
        else:
            raise TypeError("Tüm parametreler sözlük olmalıdır.")

    def list_filter_greater_than(self, threshold):
        """
        Belirtilen eşik değerinden büyük olan öğeleri filtreler.

        Parametre:
        threshold (int/float): Eşik değer.

        Dönüş:
        list: Eşik değerinden büyük olan öğeleri içeren liste.

        Örnek:
        >>> cem = CemirUtils([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
        >>> cem.list_filter_greater_than(5)
        [9, 6]
        """
        return [x for x in self.data if x > threshold]

    def list_filter_less_than(self, threshold):
        """
        Belirtilen eşik değerinden küçük olan öğeleri filtreler.

        Parametre:
        threshold (int/float): Eşik değer.

        Dönüş:
        list: Eşik değerinden küçük olan öğeleri içeren liste.

        Örnek:
        >>> cem = CemirUtils([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
        >>> cem.list_filter_less_than(4)
        [3, 1, 1, 2, 3]
        """
        return [x for x in self.data if x < threshold]

    def list_flatten(self):
        """
        Çok katmanlı listeyi tek katmana indirger.

        Dönüş:
        list: Tek katmanlı liste.

        Örnek:
        >>> ceml = CemirUtils([[1, 2], [3, 4], [5]])
        >>> ceml.flatten_list()
        [1, 2, 3, 4, 5]
        """
        if isinstance(self.data, list) and all(isinstance(i, list) for i in self.data):
            return [item for sublist in self.data for item in sublist]
        else:
            raise TypeError("Veri tipi çok katmanlı liste olmalıdır.")

    def list_sum_values(self):
        """
        Listedeki tüm sayısal değerlerin toplamını hesaplar.

        Dönüş:
        int/float: Listedeki sayısal değerlerin toplamı.

        Örnek:
        >>> cem = CemirUtils([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
        >>> cem.list_sum_values()
        44
        """
        return sum(self.data)

    def list_average(self):
        """
        Listedeki sayısal değerlerin ortalamasını hesaplar.

        Dönüş:
        float: Listedeki sayısal değerlerin ortalaması. Liste boşsa 0 döner.

        Örnek:
        >>> cem = CemirUtils([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
        >>> cem.list_average()
        4.0
        """
        return sum(self.data) / len(self.data) if self.data else 0

    def list_head(self, n=5):
        """
        Listenin ilk n elemanını döndürür.
        Args:
            n (int): Döndürülecek eleman sayısı (varsayılan 5).
        Returns:
            list: İlk n eleman.
        """
        return self.data[:n]

    def list_tail(self, n=5):
        """
        Listenin son n elemanını döndürür.
        Args:
            n (int): Döndürülecek eleman sayısı (varsayılan 5).
        Returns:
            list: Son n eleman.
        """
        return self.data[-n:]

    def list_main(self, n=5):
        """
        Listenin ortadaki elemanlarını döndürür.
        Eğer listenin uzunluğu 2n veya daha küçükse tüm listeyi döndürür.
        Args:
            n (int): Kenarlardan kesilecek eleman sayısı (varsayılan 5).
        Returns:
            list: Ortadaki elemanlar.
        """
        if len(self.data) <= 2 * n:
            return self.data
        return self.data[n:-n]

    def list_unique_values(self):
        """
        Listenin benzersiz elemanlarını döndürür.
        Returns:
            list: Benzersiz elemanlar.
        """
        return list(set(self.data))

    def list_sort_asc(self):
        """
        Listeyi artan sırada sıralar.
        Returns:
            list: Artan sırada sıralanmış liste.
        """
        return sorted(self.data)

    def list_sort_desc(self):
        """
        Listeyi azalan sırada sıralar.
        Returns:
            list: Azalan sırada sıralanmış liste.
        """
        return sorted(self.data, reverse=True)

    def http_get(self, url, params=None, headers=None, verify_ssl=True):
        """
        GET isteği gönderir.

        Parametreler:
        url (str): İstek URL'si.
        params (dict): URL parametreleri.
        headers (dict): İstek başlıkları.
        verify_ssl (bool): SSL doğrulama kontrolü.

        Dönüş:
        dict, str: JSON yanıtı veya düz metin.
        """
        if headers is None:
            headers = {}

        if params:
            url += '?' + parse.urlencode(params)

        req = request.Request(url, headers=headers)
        response = request.urlopen(req, timeout=10,
                                   context=None if verify_ssl else request._create_unverified_context())
        content = response.read().decode('utf-8')

        if 'application/json' in response.getheader('Content-Type'):
            return json.loads(content)
        else:
            return content

    def http_post(self, url, data=None, headers=None, verify_ssl=True):
        """
        POST isteği gönderir.

        Parametreler:
        url (str): İstek URL'si.
        data (dict): Gönderilecek veri.
        headers (dict): İstek başlıkları.
        verify_ssl (bool): SSL doğrulama kontrolü.

        Dönüş:
        dict, str: JSON yanıtı veya düz metin.
        """
        if headers is None:
            headers = {}

        if data:
            data = parse.urlencode(data).encode('utf-8')

        req = request.Request(url, data=data, headers=headers, method='POST')
        response = request.urlopen(req, timeout=10,
                                   context=None if verify_ssl else request._create_unverified_context())
        content = response.read().decode('utf-8')

        if 'application/json' in response.getheader('Content-Type'):
            return json.loads(content)
        else:
            return content

    def http_put(self, url, data=None, headers=None, verify_ssl=True):
        """
        PUT isteği gönderir.

        Parametreler:
        url (str): İstek URL'si.
        data (dict): Gönderilecek veri.
        headers (dict): İstek başlıkları.
        verify_ssl (bool): SSL doğrulama kontrolü.

        Dönüş:
        dict, str: JSON yanıtı veya düz metin.
        """
        if headers is None:
            headers = {}

        if data:
            data = parse.urlencode(data).encode('utf-8')

        req = request.Request(url, data=data, headers=headers, method='PUT')
        response = request.urlopen(req, timeout=10,
                                   context=None if verify_ssl else request._create_unverified_context())
        content = response.read().decode('utf-8')

        if 'application/json' in response.getheader('Content-Type'):
            return json.loads(content)
        else:
            return content

    def http_delete(self, url, headers=None, verify_ssl=True):
        """
        DELETE isteği gönderir.

        Parametreler:
        url (str): İstek URL'si.
        headers (dict): İstek başlıkları.
        verify_ssl (bool): SSL doğrulama kontrolü.

        Dönüş:
        dict, str: JSON yanıtı veya düz metin.
        """
        if headers is None:
            headers = {}

        req = request.Request(url, headers=headers, method='DELETE')
        response = request.urlopen(req, timeout=10,
                                   context=None if verify_ssl else request._create_unverified_context())
        content = response.read().decode('utf-8')

        if 'application/json' in response.getheader('Content-Type'):
            return json.loads(content)
        else:
            return content

    def http_patch(self, url, data=None, headers=None, verify_ssl=True):
        """
        PATCH isteği gönderir.

        Parametreler:
        url (str): İstek URL'si.
        data (dict): Gönderilecek veri.
        headers (dict): İstek başlıkları.
        verify_ssl (bool): SSL doğrulama kontrolü.

        Dönüş:
        dict, str: JSON yanıtı veya düz metin.
        """
        if headers is None:
            headers = {}

        if data:
            data = parse.urlencode(data).encode('utf-8')

        req = request.Request(url, data=data, headers=headers, method='PATCH')
        response = request.urlopen(req, timeout=10,
                                   context=None if verify_ssl else request._create_unverified_context())
        content = response.read().decode('utf-8')

        if 'application/json' in response.getheader('Content-Type'):
            return json.loads(content)
        else:
            return content

    def http_server(self, port=8000, ip='127.0.0.1', ssl_cert=None, ssl_key=None, username=None, password=None, directory=None):
        class CemirUtilsHTTPRequestHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=directory, **kwargs)

            def do_GET(self):
                if username and password:
                    if not self.check_basic_auth(username, password):
                        self.send_response(401)
                        self.send_header('WWW-Authenticate', 'Basic realm="CemirUtils"')
                        self.end_headers()
                        self.wfile.write(b'Unauthorized')
                        return

                super().do_GET()

            def check_basic_auth(self, username, password):
                auth_header = self.headers.get('Authorization')
                if auth_header is None:
                    return False

                auth_type, auth_value = auth_header.split(None, 1)
                if auth_type.lower() != 'basic':
                    return False

                encoded_credentials = auth_value.encode('utf-8')
                credentials = base64.b64decode(encoded_credentials).decode('utf-8')
                auth_username, auth_password = credentials.split(':', 1)

                return auth_username == username and auth_password == password

        httpd = HTTPServer((ip, port), CemirUtilsHTTPRequestHandler)

        if ssl_cert and ssl_key:
            httpd.socket = ssl.wrap_socket(httpd.socket, certfile=ssl_cert, keyfile=ssl_key, server_side=True)
            print(f"Starting HTTP server with SSL on https://{ip}:{port}")

        print(f"Starting HTTP server on http://{ip}:{port}")
        httpd.serve_forever()
