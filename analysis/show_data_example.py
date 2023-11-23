import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

df = pd.read_excel("Погода.xlsx")


# Создание графика с Matplotlib
plt.figure(figsize=(10, 4))  # Размер графика
plt.plot(df['Месяц'], df['Средняя температура'], label='Изменение погоды за год')  # Построение графика
plt.title('Пример Графика')  # Заголовок графика
plt.xlabel('Месяц')  # Название оси X
plt.ylabel('Температура')  # Название оси Y
plt.legend()  # Добавление легенды
plt.grid()  # Отображение сетки



# Настройка форматтера для осей
formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(False)  # Отключение научной нотации
plt.gca().yaxis.set_major_formatter(formatter)


# Отображение графика
plt.show()