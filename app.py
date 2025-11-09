import streamlit as st
import pandas as pd
import plotly.express as px

# Заголовок приложения
st.title('📊 Построитель графиков из таблицы')

# Шаг 1: Загрузка файла
uploaded_file = st.file_uploader("Загрузите CSV или Excel файл", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # Чтение файла в DataFrame
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Ошибка при чтении файла: {e}")
        st.stop()

    # Показываем таблицу
    st.subheader("Исходные данные")
    st.dataframe(df)

    # Шаг 2: Выбор типа графика и колонок
    st.subheader("Настройка графика")

    col1, col2 = st.columns(2)

    with col1:
        chart_type = st.selectbox(
            "Выберите тип графика",
            ["Линейный", "Столбчатый", "Точечный", "Круговой", "Гистограмма"]
        )

    with col2:
        x_column = st.selectbox("Выберите столбец для оси X", df.columns)
        y_column = st.selectbox("Выберите столбец для оси Y", df.columns)

    # Шаг 3: Построение графика
    st.subheader("График")

    try:
        fig = None

        if chart_type == "Линейный":
            fig = px.line(df, x=x_column, y=y_column, title=f"{y_column} от {x_column}")
        elif chart_type == "Столбчатый":
            fig = px.bar(df, x=x_column, y=y_column, title=f"{y_column} от {x_column}")
        elif chart_type == "Точечный":
            fig = px.scatter(df, x=x_column, y=y_column, title=f"{y_column} от {x_column}")
        elif chart_type == "Круговой":
            # Для круговой диаграммы обычно нужны категории и значения
            fig = px.pie(df, names=x_column, values=y_column, title=f"Доля {y_column} по {x_column}")
        elif chart_type == "Гистограмма":
            # Гистограмма строится по одному столбцу
            fig = px.histogram(df, x=x_column, title=f"Распределение {x_column}")

        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Выберите корректные данные для выбранного типа графика.")

    except Exception as e:
        st.error(f"Ошибка при построении графика: {e}")