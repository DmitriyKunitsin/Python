# Шпаргалка по SEABORN
### Библиотека Seaborn поставляется с несколькими важными
наборами данных. Если Seaborn доступен, наборы данных
загружаются автоматически. Вы можете использовать любой из этих
наборов данных для обучения. С помощью следующей функции вы
можете загрузить необходимый набор данных из 18, доступных в
Seaborn: **load_dataset().**
Чтобы просмотреть все доступные наборы данных в библиотеке
Seaborn, вы можете использовать следующую команду с функцией
**get_dataset_names(): sb.get_dataset_names().**

```
Импорт набора данных 'tips' – чаевые
df = sb.load_dataset('tips')
df.head()
```

DataFrame хранит данные в форме прямоугольных сеток, с помощью
которых можно легко просматривать данные. Каждая строка
прямоугольной сетки содержит значения экземпляра, а каждый
столбец сетки представляет собой вектор, который содержит данные
для определенной переменной. Это означает, что строки DataFrame
не обязательно должны содержать значения одного и того же типа
данных, они могут быть числовыми, символьными, логическими и т.д.
DataFrames для Python поставляются с библиотекой Pandas и
определяются как двумерные структуры данных с потенциально
разными типами столбцов

## Визуализация в Seaborn: представление данных эффективным и простым способом

Библиотека Matplotlib отлично поддерживает настройку графиков и
рисунков, но для ее использования необходимо знать, какие
параметры нужно настроить для получения привлекательного и
желаемого изображения. В отличие от Matplotlib, Seaborn
поставляется с настроенными функциями и высокоуровневым
интерфейсом для настройки и управления внешним видом фигур
Matplotlib.

- по умолчанию в
Seaborn, используя функцию set()
```
def sinplot(flip = 1):
x = np.linspace(0, 14, 100)
 for i in range(1, 5):
plt.plot(x, np.sin(x + i*.5)*(7 - i)*flip)
sb.set()
sinplot()
plt.show()
```
#### По сути, Seaborn разбивает параметры Matplotlib на две группы:
- Стили фона
- Масштаб рисунка

## Seaborn Figure Styles
Интерфейсом для манипулирования стилями является
set_style(). С помощью этой функции вы можете установить
«стиль» фона. Ниже представлены пять доступных «стилей»:
- "darkgrid" – темный фон, белая сетка
- "whitegrid" – белый фон, темная сетка
- "dark" – темный фон
- "white" – белый фон
- "ticks" – белый фон, обрамление рисунка

```
def sinplot(flip=1):
 x = np.linspace(0, 14, 100)
 for i in range(1, 5):
 plt.plot(x, np.sin(x + i*.5)*(7 - i)*flip)
sb.set_style("whitegrid")
sinplot()
plt.show()
```

#### Удаление осей сетки
В стилях "white" и "ticks" мы можем удалить верхнюю и правую
оси (границы рисунка), используя функцию despine() (что не
поддерживается в Matplotlib).
```
    def sinplot(flip=1):
    x = np.linspace(0, 14, 100)
    for i in range(1, 5):
    plt.plot(x, np.sin(x + i*.5)*(7 - i)*flip)
    sb.set_style("white")
    sinplot()
    sb.despine()
    6
    plt.show()
```
###  Переопределение элементов
Если вы хотите настроить стили Seaborn, вы можете
воспользоваться словарем параметров функции set_style().
Доступные параметры просматриваются с помощью функции
axes_style().
```
sb.axes_style()
```
- Изменение значений любого параметра изменит стиль графика
```
def sinplot(flip=1):
 x = np.linspace(0, 14, 100)
 for i in range(1, 5):
 plt.plot(x, np.sin(x + i * .5) * (7 - i) * flip)
sb.set_style("darkgrid", {'axes.axisbelow': False}) # Изменили здесь
sinplot()
sb.despine()
plt.show()
```

## Цветовая палитра Seaborn

Цвет играет важную роль, чем любой другой аспект визуализации.
Seaborn предоставляет функцию color_palette(), которую можно
использовать для придания цвета графикам и для большего
эстетического вида.
- Синтаксис функции
```
seaborn.color_palette (palette = None, n_colors = None, desat = None)
```
### Параметры для построения цветовой палитры:
- n_colors – количество цветов в палитре.
Если None, значение по умолчанию будет зависеть от того, как
указана палитра.
- Desat – пропорция для варьирования каждого цвета.

Доступные палитры Seaborn:
- глубокий
- приглушенный
- яркий
- пастельный
- темный

### Иногда трудно решить, какую палитру следует использовать для
данного набора данных, не зная характеристик данных. Приведем
различные способы использования типов color_palette():
- качественные палитры
- последовательные палитры
- расходящаяся палитра

Есть и другая функция **seaborn.palplot()**, которая работает с
цветовой палитрой. Эта функция отображает цветовую палитру как
горизонтальный массив. Узнаем больше о seaborn.palplot () из
следующих примеров.

### Качественные цветовые палитры
Качественные или категориальные палитры лучше всего подходят
для построения категориальных данных.
```
current_palette = sb.color_palette()
sb.palplot(current_palette)
plt.show()
```
![alt text](./screens/image.png)
- Вы можете увидеть желаемое количество цветов,
передав значение в параметр n_colors. Здесь palplot() используется
для горизонтального построения массива цветов.

### Последовательные цветовые палитры
Последовательные палитры подходят для отображения
распределения данных в диапазоне от относительно более низких
значений до более высоких значений в пределах диапазона.
При добавлении дополнительного символа **‘s’** к цвету, переданному
параметру цвета, будет построен график «Последовательная
палитра».
```
current_palette = sb.color_palette()
sb.palplot(sb.color_palette("Greens"))
plt.show()
```
![alt text](./screens/image_2.png)

### Расходящаяся палитра

Расходящиеся палитры используют два разных цвета. Каждый цвет
представляет изменение значения в пределах от общей точки в
любом направлении.
Предположим, что данные располагаются в диапазоне от -1 до 1.
Значения от -1 до 0 принимают один цвет, а от 0 до +1 – другой цвет.
По умолчанию значения центрированы от нуля. Вы можете управлять
ими с помощью параметра center, передавая значение.

```
current_palette = sb.color_palette()
sb.palplot(sb.color_palette("BrBG", 7))
plt.show()
```
![alt text](./screens/image_3.png)

### Настройка цветовой палитры по умолчанию
У функций color_palette() есть сопутствующий элемент set_palette().
Аргументы одинаковы как для set_palette(), так и для color_palette().
Параметры Matplotlib по умолчанию настроены так, что палитра
используется для всех графиков.
```
def sinplot(flip = 1):
 x = np.linspace(0, 14, 100)
 for i in range(1, 5):
 plt.plot(x, np.sin(x + i * .5) * (7 - i)*flip)
sb.set_style("white")
sb.set_palette("husl")
sinplot()
plt.show()
```

## Пройдемся по основным видам графиков

### Построение одномерного распределения
Распределение данных – это главное, что нужно знать при анализе
данных. Здесь мы увидим, как seaborn помогает в понимании
одномерного распределения данных.
```
Набор данных 'чаевые'
tips = sb.load_dataset('tips')
ax = sb.scatterplot(x = 'total_bill', y='tip', data = tips)
plt.show()
```

###  Гистограмма
