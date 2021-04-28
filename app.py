from flask import Flask
from flask import render_template
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)


@app.route('/')
def show():
    stolen_url = 'https://ria.ru/'
    soup = BeautifulSoup(requests.get(stolen_url).text, 'lxml')

    usual_news = []

    for item in zip(soup.find_all('a', class_="cell-list__item-link color-font-hover-only"),
                    soup.find_all('div', class_="cell-list__item-info")):
        usual_news.append((item[1].text, item[0].text, item[0].get('href')))

    file = 'templates/site.html'

    usual_news.sort()
    for note in usual_news:
        if not note[0][0].isnumeric():
            a = list(reversed(usual_news[:usual_news.index(note)]))
            b = list(reversed(usual_news[usual_news.index(note):]))
            usual_news = a + b
            break

    return render_template('site.html', news=usual_news)


if __name__ == '__main__':
    app.run()
