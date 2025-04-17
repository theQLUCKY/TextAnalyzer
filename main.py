from flask import Flask
from flask import render_template, request
from collections import Counter
from app.DataBase.models import Document, session, start
from app.handlers import get_words, get_idf
from sqlalchemy import select

app = Flask(__name__)

text ='Загрузите txt файл и узнайте TF, IDF, количество слов в файле и Количество встреч слова в файле'

@app.route('/', methods=['GET', 'POST'])
def index() -> str | None:
    """Функция принимает файл и отдает результат в index.html для формирования таблицы"""
    if request.method == 'POST':
        file = request.files['file']
        table = session.scalar(select(Document).where(Document.filename == file.filename)) # Проверяем есть ли файл с
                                                                                           # таким же названием в Базе
                                                                                           # если нет то добавляем иначе
                                                                                           # берем файл из Базы
        if file and file.filename.endswith('.txt'): #Проверяем является ли формат файла .txt
            if table is None: #Проверяем есть ли файл
                filename = file.filename

                with open(file.stream, 'r', encoding='utf-8') as f:
                    content = f.read() #Получаем список из элементов файла
                new_doc = Document(filename=filename, content=content) #Формируем объект
                session.add(new_doc)  #Добавляем документ в базу
                session.commit()      #Сохраняем документ

                all_docs = session.query(Document).all() #Достаем все файлы из базы
                all_words = [get_words(doc.content) for doc in all_docs] # Из каждого файла извлекаем содержимое
                                                                                  # и передаем ее в функцию
                                                                                  # для извлечения слов

                idf_score = get_idf(all_words) # Передаем список со списками слов для получения idf
                words = get_words(content)  #Фильтруем элементы из файла
                word_counts = Counter(words) #Считаем сколько раз какое слово встречается в файле

                table_data = [{
                    'word': word,
                    'tf': round(count / len(words), 6),
                    'count': count,
                    'length': len(all_words),
                    'idf': round(idf_score.get(word, 0.0), 4)
                } for word, count in word_counts] #Создаем список словарей для каждого слова с результатами
                print('я родился')
                table_data = sorted(table_data, key=lambda x: x['idf'], reverse=True)[:50] #Сортируем в порядке убывания
                                                                                           #и ограничиваем 50-ю словами
                return render_template('index.html', table_data=table_data)   #Отдаем результат для формирования таблицы

            doc = session.scalar(select(Document).where(Document.filename == file.filename)) #Достаем файл с таким же именем из базы
            print('я уже существую')
            all_docs = session.query(Document).all() #Достаем все файлы из базы
            all_words = [get_words(doc.content) for doc in all_docs]# Из каждого файла извлекаем содержимое
                                                                                  # и передаем ее в функцию
                                                                                  # для извлечения слов
            idf_score = get_idf(all_words) # Передаем список со списками слов для получения idf

            words = get_words(doc.content) #Фильтруем элементы из файла
            word_counts = Counter(words).most_common(50) #Считаем сколько раз какое слово встречается в файле

            table_data = [{
                'word': word,
                'tf': round(count / len(words), 6),
                'count': count,
                'length': len(words),
                'idf': round(idf_score.get(word, 0.0), 4)
            } for word, count in word_counts]
            table_data = sorted(table_data, key=lambda x: x['idf'], reverse=True) #Сортируем в порядке убывания
                                                                                  #и ограничиваем 50-ю словами

            return render_template('index.html', table_data=table_data)  #Отдаем результат для формирования таблицы
    return render_template('index.html', new=text)


if __name__ == '__main__':
    start()
    app.run(debug=True) #debug служит для отладки сайта (показывает информацию об ошибках на сайте)
                        #Если такая функция не требуется можно спокой убирать
