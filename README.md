# xaxaton_sokol


##Start

###Как поднять Апи

1. При первом запуске необходимо положить данные датчиков в папку на сервере `/root/data`. 
Важно использовать всего 2-3 файла для тестового запуска т.к. загрузка и обработка данных
с всех датчиков из датасета может занять до 10 часов.
2. Выполнить в терминале команду `git clone https://github.com/rokv1l/xaxaton_sokol`
3. Выполнить в терминале команду `cd xaxaton_sokol`
4. Выполнить в терминале команду `mv .env.example .env`
5. `docker-compose up -d --build`

Всё, работает :) 

Необходимо некоторое время для скачивания графов и обработки данных.
Если в первом пункте вы последовали нашему совету и использовали 2-3 файла, то инициализация
базы и графов будет длиться около 5-15 минут.

Когда инициализация будет закончена при команде `docker-compose logs api` вы увидите строку `All systems initialized, its ready to work!`.
После этого и только после этого апи будет работать корректно.

Сервис в разработке

Для загрузки данных датчиков нужно указать где лежат данные в  формате .xls и записать это в .env SENSORS_DATA_PATH

