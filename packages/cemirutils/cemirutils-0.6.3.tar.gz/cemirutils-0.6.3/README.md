<meta charset="UTF-8">

# CemirUtils

CemirUtils, basit veri işleme işlevlerini içeren bir Python yardımcı kütüphanesidir.

## Kurulum

Öncelikle CemirUtils kütüphanesini Python projesine eklemek için aşağıdaki adımları izleyin:

```bash
pip install cemirutils
````


## Kullanım


* PostgreSQL için CRUD işlemleri.

```python
from datetime import datetime
from cemirutils import CemirUtils

# ['dict_filter_by_key', 'dict_get_keys', 'dict_get_value', 'dict_merge', 'getmethods', 'http_delete', 'http_get', 'http_patch', 'http_post', 'http_put', 'http_server', 'list_average', 'list_filter_greater_than', 'list_filter_less_than', 'list_flatten', 'list_get_frequency', 'list_get_max_value', 'list_get_min_value', 'list_head', 'list_main', 'list_multiply_by_scalar', 'list_reverse', 'list_sort_asc', 'list_sort_desc', 'list_sum_values', 'list_tail', 'list_unique_values', 'psql_create_database', 'psql_create_table', 'psql_delete', 'psql_execute_query', 'psql_insert', 'psql_parse_psql_output', 'psql_read', 'psql_update', 'str_replace_multiple', 'str_replace_with_last', 'time_add_days_and_format', 'time_add_days_to_date', 'time_business_days_between_dates', 'time_days_between_dates', 'time_days_in_month', 'time_hours_minutes_seconds_between_times', 'time_is_leap_year', 'time_is_weekend', 'time_next_weekday', 'time_since', 'time_todatetime', 'time_until_date']


# Örnek kullanım
utils = CemirUtils(data=False, dbname='test_db3', dbuser='postgres', dbpassword='', dbport=5435, dbcreate_db_if_not_exists=True)

# print(utils.psql_create_table('test_table_flat', 'id SERIAL PRIMARY KEY, name VARCHAR(100), surname VARCHAR(100)'))
# print(utils.psql_create_table('test_table_json', 'id SERIAL PRIMARY KEY, dates DATE, content JSONB'))

# print(utils.psql_insert('test_table_flat', ('id', 'name', 'surname'), (3, 'Muslu', 'Yüksektepe'), get_id=True))
print(utils.psql_insert('test_table_json', ('id', 'dates', 'content'), (2, datetime.now(), {"age": 40, "city": "İzmir"}), get_id=True))
print(utils.psql_read('test_table_json'))

print(utils.psql_update('test_table_json', {'dates': datetime.now(), 'content': '{"age": 40, "city": "Sivas"}'}, 'id = 1', get_id=True))
print(utils.psql_read('test_table_json'))

print(utils.psql_delete('test_table_json', 'id = 1'))
print(utils.psql_read('test_table_json'))
```

Kütüphane, farklı veri işleme işlevlerini sağlayan `CemirUtils` sınıfını içerir.
* Örneğin:

```python
from cemirutils import CemirUtils

# Mevcut tüm metodların isimlerini yazdır
cemir_utils = CemirUtils(None)
print(cemir_utils.getmethods())


get_response = cemir_utils.http_get("https://jsonplaceholder.typicode.com/posts/1", verify_ssl=True)
print("GET Response:", get_response)

# POST isteği
post_data = {"title": "foo", "body": "bar", "userId": 1}
post_response = cemir_utils.http_post("https://jsonplaceholder.typicode.com/posts", data=post_data, verify_ssl=True)
print("POST Response:", post_response)

# PUT isteği
put_data = {"title": "foo", "body": "bar", "userId": 1}
put_response = cemir_utils.http_put("https://jsonplaceholder.typicode.com/posts/1", data=put_data, verify_ssl=True)
print("PUT Response:", put_response)

# DELETE isteği
delete_response = cemir_utils.http_delete("https://jsonplaceholder.typicode.com/posts/1", verify_ssl=True)
print("DELETE Response:", delete_response)

# PATCH isteği
patch_data = {"title": "foo"}
patch_response = cemir_utils.http_patch("https://jsonplaceholder.typicode.com/posts/1", data=patch_data, verify_ssl=True)
print("PATCH Response:", patch_response)


data_list = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
cem = CemirUtils(data_list)
print(data_list)
print(cem.list_head(2))  # Listenin ilk 5 elemanını yazdırır.
print(cem.list_tail(4))  # Listenin son 5 elemanını yazdırır.
print(cem.list_main())  # Listenin ortadaki elemanlarını yazdırır.
print(cem.list_unique_values())  # Listenin benzersiz elemanlarını yazdırır.
print(cem.list_sort_asc())  # Listenin artan sırada sıralanmış halini yazdırır.
print(cem.list_sort_desc())  # Listenin azalan sırada sıralanmış halini yazdırır.
print(cem.list_filter_greater_than(5))  # 5'ten büyük değerleri yazdırır: [9, 6]
print(cem.list_filter_less_than(4))  # 4'ten küçük değerleri yazdırır: [3, 1, 1, 2, 3]
print(cem.list_sum_values())  # Değerlerin toplamını yazdırır: 44
print(cem.list_average())  # Değerlerin ortalamasını yazdırır: 4.0


## Zaman işlemleri
utils = CemirUtils(None)
print(utils.time_days_between_dates("2024-05-01", "2024-05-25"))  # 24
print(utils.time_hours_minutes_seconds_between_times("08:30:00", "15:45:30"))  # (7, 15, 30)
print(utils.time_until_date("2024-05-27 23:59:59"))  # Kalan gün, saat, dakika, saniye
print(utils.time_add_days_and_format("2024-05-01", 30))  # "2024-05-31 (Cuma)"
print(utils.time_is_weekend("2024-05-25"))  # True
print(utils.time_is_leap_year(2024))  # True
print(utils.time_days_in_month(2024, 2))  # 29
print(utils.time_next_weekday("2024-05-25", 0))  # 2024-05-27
print(utils.time_since("2022-01-01 00:00:00"))  # (2, 4, 24, 14, 30, 15)
print(utils.time_business_days_between_dates("2024-05-01", "2024-05-25"))  # 17


ceml = CemirUtils([[1, 2], [3, 4], [5]])
# Çok katmanlı listeyi tek katmana indirger.
print(ceml.list_flatten())  # Output: [1, 2, 3, 4, 5]


ceml = CemirUtils([1, 2, 3])
# Veri listesindeki her bir elemanı verilen skaler değer ile çarpar
print(ceml.list_multiply_by_scalar(2))  # Output: [2, 4, 6]


ceml = CemirUtils([1, 2, 3])
# Veri listesindeki en büyük değeri döner.
print(ceml.list_get_max_value())  # Output: 3


ceml = CemirUtils([1, 2, 2, 3])
# Verilen değerin veri listesinde kaç kez geçtiğini sayar.
print(ceml.list_get_frequency(2)) # Output: 2


# Sözlükteki veya sözlük listesindeki anahtarları döndürür.
data = [{'a': 1}, {'b': 2}, {'a': 3}, {"name": "sivas", "age": 10}]
cemd = CemirUtils(data)

print(cemd.dict_get_keys())
print(cemd.dict_filter_by_key('name'))
print(cemd.dict_merge({'a': 1}, {'b': 2}))

````