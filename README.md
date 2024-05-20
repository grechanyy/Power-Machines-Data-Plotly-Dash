## Дашборд о турбинах "Силовых турбин"

### 1. Парсер

При помощи библиотеки *Beautiful Soup* с сайта "Силовые машины" была спарсена информация о произведенных турбинах с 1924 по 2020 гг.
Данные были предобработаны и очищены от лишних категорий оборудования, таких как трансформаторы, гидрогенераторы, турбогенераторы.
Далее был создан датафрейм с данными, готовыми для работы над дашбордом (хранятся в файле *power_machines.csv*).

---
### 2. Дашборд
На основе импортированного csv-файла *power_machines.csv* и библиотек *dash* и *plotly* был создан интерактивный дашборд.
Дашборд поделен на две не равные части:
- боковая панель, содержащая два дропдауна с выбором страны и типом турбины (Парвые турбины/Гидротурбины),
  а также информация общее число выпущенных турбин и суммарная мощность (показатели считаются в зависимости от выбранных категорий в дропдаунах);
- контентная часть, содержащая два графика и таблицу.
---
### Графики:
- Гистограма показывает кол-во турбин разных мощностей, произведенных за весь период (в зависимости от заданной страны и типа турбины);
- Скаттерплот показывает в какие годы и какой суммарной мощности поставлялись турбины в зависимости от типа станции (ТЭС, ТЭЦ, ГРЭС или АЭС).

### Таблица:
- отображает более полную информацию о проектах по заданным параметрам (проект, год выпуска, мощность, кол-во, суммарная мощность).

---
Итоговый вид дашборда:
![image](https://github.com/grechanyy/Power-Machines-Data-Plotly-Dash/assets/128630067/f6af354c-185c-422f-baf3-9b4519041607)
