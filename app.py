import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import sys

class GraphPlotter:
    def __init__(self):
        self.supported_formats = ['.txt', '.csv', '.dat']
    
    def detect_delimiter(self, filename):
        """Автоматическое определение разделителя"""
        delimiters = [',', ';', '\t', ' ']
        with open(filename, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        
        for delimiter in delimiters:
            if delimiter in first_line and len(first_line.split(delimiter)) > 1:
                return delimiter
        return None
    
    def read_data(self, filename):
        """Чтение данных из файла"""
        try:
            file_ext = Path(filename).suffix.lower()
            delimiter = self.detect_delimiter(filename)
            
            if file_ext == '.csv' or delimiter == ',':
                df = pd.read_csv(filename, comment='#')
            else:
                df = pd.read_csv(filename, delimiter=delimiter, comment='#', 
                               engine='python', skipinitialspace=True)
            
            return df
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")
            return None
    
    def plot_simple(self, df, title="График данных"):
        """Построение простого графика"""
        plt.figure(figsize=(12, 8))
        
        if len(df.columns) == 2:
            # Один набор данных
            x_col, y_col = df.columns[0], df.columns[1]
            plt.plot(df[x_col], df[y_col], 'b-o', linewidth=2, markersize=6, 
                    label=y_col)
        elif len(df.columns) > 2:
            # Несколько наборов данных
            x_col = df.columns[0]
            for i in range(1, len(df.columns)):
                plt.plot(df[x_col], df[df.columns[i]], 'o-', linewidth=2, 
                        markersize=4, label=df.columns[i])
        
        plt.title(title, fontsize=14)
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel('Значения', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    def plot_scatter(self, df, title="Точечный график"):
        """Построение точечного графика"""
        plt.figure(figsize=(12, 8))
        
        if len(df.columns) >= 2:
            x_col, y_col = df.columns[0], df.columns[1]
            plt.scatter(df[x_col], df[y_col], alpha=0.7, s=50)
            
            if len(df.columns) >= 3:
                # Используем третий столбец для размера точек
                sizes = (df[df.columns[2]] - df[df.columns[2]].min()) / \
                       (df[df.columns[2]].max() - df[df.columns[2]].min()) * 100 + 10
                plt.scatter(df[x_col], df[y_col], s=sizes, alpha=0.7)
        
        plt.title(title, fontsize=14)
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def plot_bar(self, df, title="Столбчатая диаграмма"):
        """Построение столбчатой диаграммы"""
        plt.figure(figsize=(12, 8))
        
        if len(df.columns) >= 2:
            x_col, y_col = df.columns[0], df.columns[1]
            plt.bar(df[x_col], df[y_col], alpha=0.7, color='skyblue')
        
        plt.title(title, fontsize=14)
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def plot_histogram(self, df, title="Гистограмма"):
        """Построение гистограммы"""
        plt.figure(figsize=(12, 8))
        
        for i in range(min(3, len(df.columns))):  # Максимум 3 столбца
            plt.hist(df[df.columns[i]], alpha=0.7, bins=20, 
                    label=df.columns[i])
        
        plt.title(title, fontsize=14)
        plt.xlabel('Значения', fontsize=12)
        plt.ylabel('Частота', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    def show_file_info(self, df):
        """Показать информацию о файле"""
        print("\n" + "="*50)
        print("ИНФОРМАЦИЯ О ДАННЫХ:")
        print("="*50)
        print(f"Количество строк: {len(df)}")
        print(f"Количество столбцов: {len(df.columns)}")
        print("\nСтолбцы:")
        for i, col in enumerate(df.columns):
            print(f"  {i+1}. {col}")
        print(f"\nПервые 5 строк:")
        print(df.head())
        print("\nСтатистика:")
        print(df.describe())

def main():
    plotter = GraphPlotter()
    
    print("ПРИЛОЖЕНИЕ ДЛЯ ПОСТРОЕНИЯ ГРАФИКОВ")
    print("="*40)
    
    # Ввод имени файла
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Введите имя файла с данными: ").strip()
    
    # Проверка существования файла
    if not Path(filename).exists():
        print(f"Файл '{filename}' не найден!")
        return
    
    # Чтение данных
    df = plotter.read_data(filename)
    if df is None or df.empty:
        print("Не удалось прочитать данные из файла")
        return
    
    # Показать информацию о данных
    plotter.show_file_info(df)
    
    # Меню выбора типа графика
    while True:
        print("\n" + "="*50)
        print("ВЫБЕРИТЕ ТИП ГРАФИКА:")
        print("1. Линейный график")
        print("2. Точечный график")
        print("3. Столбчатая диаграмма")
        print("4. Гистограмма")
        print("5. Показать информацию о данных")
        print("6. Выход")
        
        choice = input("\nВаш выбор (1-6): ").strip()
        
        if choice == '1':
            title = input("Введите заголовок графика (или Enter для стандартного): ")
            if not title:
                title = f"Линейный график - {filename}"
            plotter.plot_simple(df, title)
        
        elif choice == '2':
            title = input("Введите заголовок графика (или Enter для стандартного): ")
            if not title:
                title = f"Точечный график - {filename}"
            plotter.plot_scatter(df, title)
        
        elif choice == '3':
            title = input("Введите заголовок графика (или Enter для стандартного): ")
            if not title:
                title = f"Столбчатая диаграмма - {filename}"
            plotter.plot_bar(df, title)
        
        elif choice == '4':
            title = input("Введите заголовок графика (или Enter для стандартного): ")
            if not title:
                title = f"Гистограмма - {filename}"
            plotter.plot_histogram(df, title)
        
        elif choice == '5':
            plotter.show_file_info(df)
        
        elif choice == '6':
            print("Выход из программы...")
            break
        
        else:
            print("Неверный выбор! Попробуйте снова.")

if __name__ == "__main__":
    main()