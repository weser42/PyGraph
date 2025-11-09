import matplotlib.pyplot as plt
import numpy as np

def plot_from_file(filename):
    try:
        # Автоматическое определение разделителя
        with open(filename, 'r') as f:
            first_line = f.readline().strip()
        
        # Пробуем разные разделители
        if ',' in first_line:
            data = np.loadtxt(filename, delimiter=',', comments='#')
        elif ';' in first_line:
            data = np.loadtxt(filename, delimiter=';', comments='#')
        else:
            data = np.loadtxt(filename, comments='#')
        
        # Построение графика
        plt.figure(figsize=(12, 8))
        
        if data.shape[1] == 2:
            # Один набор данных (X, Y)
            plt.plot(data[:, 0], data[:, 1], 'ro-', linewidth=2, markersize=6)
        elif data.shape[1] > 2:
            # Несколько наборов данных
            for i in range(1, data.shape[1]):
                plt.plot(data[:, 0], data[:, i], 'o-', linewidth=2, markersize=4, 
                        label=f'Данные {i}')
            plt.legend()
        
        plt.title(f'График из файла: {filename}')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Ошибка: {e}")

# Запуск программы
if __name__ == "__main__":
    filename = input("Введите имя файла (например: data.txt): ").strip()
    plot_from_file(filename)