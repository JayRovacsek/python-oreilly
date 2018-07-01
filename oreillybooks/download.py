import os
import sys
import json
import traceback
from multiprocessing import Pool
import robobrowser as RoboBrowser

class Oreilly:
    def __init__(self,books_file):
        self.books = self.parse_json(self.read_json(books_file))
        self.base_urls = {
            'programming':'https://www.oreilly.com/programming/free/files/',
            'webops':'https://www.oreilly.com/webops-perf/free/files/',
            'iot':'https://www.oreilly.com/iot/free/files/',
            'data':'https://www.oreilly.com/data/free/files/',
            'security':'https://www.oreilly.com/security/free/files/',
            'webplatform':'https://www.oreilly.com/web-platform/free/files/'
        }
        for key, value in self.base_urls.items():
            if not os.path.isdir(os.getcwd()+"/books/"+key):
                os.mkdir(os.getcwd()+"/books/"+key)

    def read_json(self,file):
        with open(file) as f:
            return json.loads(f.read())

    def parse_json(self,books):
        values = {}
        for key, value in books.items():
            values[key] = value
        return values

    def download(self,book):
        if not os.path.isfile(os.getcwd()+"/books/" + book[1][:-5] + '/' + book[0]):
            base_url = self.base_urls[book[1][:-5]]
            browser = RoboBrowser.RoboBrowser(history=False)
            request = browser.session.get(base_url+book[0], stream=True)
            with open("books/" + book[1][:-5] + '/' + book[0], 'wb') as pdf_file:
                pdf_file.write(request.content)
        else:
            print('{} exists already, skipping!'.format(book[0]))

if __name__ == '__main__':
    if not os.path.isdir(os.getcwd()+"/books"):
        os.mkdir(os.getcwd()+"/books")
    oreilly = Oreilly('books.json')
    try:
        pool = Pool()
        pool.map(oreilly.download,oreilly.books.items())
    finally:
        pool.close()
        pool.join()