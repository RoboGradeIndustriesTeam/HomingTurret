# Турель с самонаведением ArduinoDay 2021 [созданная им](https://github.com/nosqd)

Для конкурса [Arduino Day 2021](https://vk.com/arduinday2021_rostov_on_don)

[Ссылка на репозиторий чертежей](https://github.com/RoboGradeIndustriesTeam/HomingTurret/tree/schemes)

[Ссылка на репозиторий блок-схем (не актуально)](https://github.com/RoboGradeIndustriesTeam/HomingTurret/tree/diagrams)

# Установка прошивки
[Ссылка на репозиторий прошивки](https://github.com/RoboGradeIndustriesTeam/HomingTurret/tree/arduino)

Для прошивки требуется Arduino IDE, скачать можно с сайта [Arduino](https://arduino.cc)
```
git clone --single-branch -b arduino https://github.com/RoboGradeIndustriesTeam/HomingTurret
```
Откройте Arduino IDE

Выберите Файл->Открыть и откройте папку с репозиторием

Выберите Инструменты->Порт и выберите ваш порт

Выберите Инструменты->Плата и выберите вашу плату

Нажмите Ctrl->U и программа загрузится


# Установка программы
Для установки требуется Python 3 скачать можно с сайта [Python](https://python.org)

Важно указать галоку Add Python To Path
```
git clone https://github.com/RoboGradeIndustriesTeam/HomingTurret
```
```
cd HomingTurret
```
```
pip install opencv-python pyqt5 pyserial
```

# Запуск программы
Перейдите в папку HomingTurret

И пропишите
```
python main.py
```

# Технечиские характеристки
+ Турелью - гир-бокс созданный в кружке [Robo.Grade](https://robograde.ru/) (Сайт времмено не работает)
+ Язык программирования - [Python](https://python.org/)
+ Фреймворк для распознавания лиц - [OpenCV](https://opencv.org/)
+ Фреймворк для создание графического интерфеса - [Qt](https://qt.io) и [PyQT](https://ru.wikipedia.org/wiki/PyQt)
+ Библиотека для передачи данных из ПО в Турель - [PySerial](https://pypi.org/project/pyserial/)


# API
Турель получает символ означаюший куда ей двигатся
+ U - вверх
+ D - вниз
+ L - влево
+ R - вправо
