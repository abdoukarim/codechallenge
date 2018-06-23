# coding=utf-8
import json
import logging
import operator
import re
import os
from ast import literal_eval

import requests
import tornado.ioloop
import tornado.web
from tornado_mysql import pools, connect, err
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.parse
import urllib.request

from tornado import gen

from blacklist import get_blacklist
from utils import generate_keys, export_private_key, export_public_key, hash_word, encrypt_message, import_public_key, \
    decrypt_message, import_private_key

log = logging.getLogger(__name__)

fname = os.path.join(os.path.dirname(__file__), "database.json")
with open(fname) as f:
    database = json.load(f)
# connection = connect(**database)

pools.DEBUG = True


POOL = pools.Pool(
    dict(database),
    max_idle_connections=1,
    max_recycle_sec=3)


def show_visible_tags(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def remove_non_alpha_num(words):
    return re.compile(r'\W+', re.UNICODE).split(words)


def remove_blacklist_words(words):
    return [word.lower() for word in words if all([word.lower() not in get_blacklist(), not word.isdigit(),
                                                   len(word) > 1])]


def parse_word_frequency_to_dict(words):
    word_freq = [words.count(word) for word in words]
    word_freq_zip = zip(words, word_freq)
    return dict(word_freq_zip)


def desc_words(words):
    return sorted(words.items(), key=operator.itemgetter(1), reverse=True)


@gen.coroutine
def mysql_connect():
    fname = os.path.join(os.path.dirname(__file__), "database.json")
    with open(fname) as f:
        database = json.load(f)
    connection = yield connect(**database)
    return connection


@gen.coroutine
def safe_create_table(tablename, req, cleanup=False):
        """create a table.
        Ensures any existing version of that table
        is first dropped.
        Also adds a cleanup rule to drop the table if necessary
        """
        yield POOL.execute("drop table if exists %s" % tablename)
        # yield cursor.execute("create table test (data varchar(10))")
        yield POOL.execute(req)
        if cleanup:
            # self.addCleanup(self.drop_table, connection, tablename)
            drop_table(tablename)


def drop_table(tablename):
        # @self.io_loop.run_sync
        @gen.coroutine
        def _drop_table_inner():
            # cursor = yield POOL.cursor()
            # with warnings.catch_warnings():
            #     warnings.simplefilter("ignore")
            yield POOL.execute("drop table if exists %s" % tablename)
            # yield cursor.close()


@gen.coroutine
def get_top_words(limit=False):
    words = []
    if limit:
        cursor = yield POOL.execute("SELECT Word, TotalFrequency FROM words ORDER BY TotalFrequency DESC LIMIT 100;")
    else:
        cursor = yield POOL.execute("SELECT Word, TotalFrequency FROM words ORDER BY TotalFrequency DESC;")
    private_key = import_private_key()
    if cursor.rowcount > 0:
        for row in cursor:
            Word, TotalFrequency = row
            words.append({'word': decrypt_message(Word, private_key), 'frequency': str(TotalFrequency+10)+'px'})
    return words


@gen.coroutine
def get_urls():
    urls = []
    cursor = yield POOL.execute("SELECT Url, Sentiment FROM urls;")
    if cursor.rowcount > 0:
        for row in cursor:
            Url, Sentiment = row
            urls.append({'url': Url, 'sentiment': Sentiment})
    return urls


class AdminHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        words = yield get_top_words()
        urls = yield get_urls()
        self.render("admin.html", words=words, urls=urls)


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        try:
            publickey_file = open("pub.pem", "rb")
        except FileNotFoundError:
            # lets create public and private key files
            privatekey, publickey = generate_keys()
            export_private_key(privatekey)
            export_public_key(publickey)
        else:
            publickey_file.close()
        
        words = []
        try:
            words = yield get_top_words()
        except err.ProgrammingError:
            sql = "CREATE TABLE IF NOT EXISTS words (WordHash VARCHAR(100) NOT NULL ,"" \
            ""Word VARCHAR(255) NOT NULL,"" \
            ""TotalFrequency INT NOT NULL,"" \
            ""PRIMARY KEY (WordHash)"" \
            "");"
            yield safe_create_table('words', sql)
            sql = "CREATE TABLE IF NOT EXISTS urls (UrlHash VARCHAR(100) NOT NULL ,"" \
            ""Url VARCHAR(100) NOT NULL,"" \
            ""Sentiment VARCHAR(10) NOT NULL,"" \
            ""PRIMARY KEY (UrlHash, Url)"" \
            "");"
            yield safe_create_table('urls', sql)

        
        self.render("home.html", words=words)

    @staticmethod
    def word_records(words):
        data = []
        for record in words:
            word, freq = record
            WordHash = hash_word(word)
            public_key = import_public_key()
            Word = encrypt_message(word, public_key)
            TotalFrequency = freq
            # yield (WordHash, Word, TotalFrequency)
            data.append((WordHash, Word, TotalFrequency))
        return data

    @gen.coroutine
    def post(self):
        url = self.get_argument("url")
        print(url)
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(show_visible_tags, texts)
        words = u" ".join(t.strip() for t in visible_texts)
        words = remove_non_alpha_num(words)
        words = remove_blacklist_words(words)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'Authorization': 'Bearer LYDNXBKA4Z4DY7ROH2LHCU5AY7NSUGZL', 'User-Agent': user_agent}
        wit_ai_url = 'https://api.wit.ai/message'
        values = {'v': '20180622', 'q': u" ".join(words[20:50])}
        data = urllib.parse.urlencode(values)
        req = urllib.request.Request(wit_ai_url, data, headers)
        response = requests.get(req.get_full_url()+'?%s' % data, headers=headers)
        sentiment = literal_eval(response.text)['entities']['sentiment'][0]['value']
        words = parse_word_frequency_to_dict(words)
        words_desc = desc_words(words)
        # Save the top 100 words to MySQL DB
        records = self.word_records(words_desc[0:100])
        for record in records:
            WordHash, Word, TotalFrequency = record
            cursor = yield POOL.execute("SELECT * FROM  words WHERE WordHash='{0}';".format(WordHash))
            if cursor.rowcount > 0:
                # UPDTATE
                sql = "UPDATE words SET WordHash='{0}', Word='{1}', TotalFrequency='{2}' WHERE WordHash='{3}'"
                yield POOL.execute(sql.format(WordHash, Word.decode("utf-8"), TotalFrequency, WordHash))
            else:
                sql = "INSERT INTO words (WordHash, Word, TotalFrequency) VALUES (%s, %s, %s)"
                yield POOL.execute(sql, (WordHash, Word.decode("utf-8"), TotalFrequency))
                # yield POOL.execute("INSERT INTO words (WordHash, Word, TotalFrequency) VALUES (%s, %s, %d)" % (WordHash, Word.decode("utf-8"), TotalFrequency))
        # Save URL & the sentiment analysis to MySQL DB
        UrlHash = hash_word(url)
        cursor = yield POOL.execute("SELECT * FROM  urls WHERE UrlHash='{0}';".format(UrlHash))
        if cursor.rowcount > 0:
            sql = "UPDATE urls SET UrlHash='{0}', Url='{1}', Sentiment='{2}' WHERE UrlHash='{3}'"
            yield POOL.execute(sql.format(UrlHash, url, sentiment, UrlHash))
        else:
            sql = "INSERT INTO urls (UrlHash, Url, Sentiment) VALUES (%s, %s, %s)"
            yield POOL.execute(sql, (UrlHash, url, sentiment))

        self.redirect("/")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/admin", AdminHandler)
    ], autoreload=True, debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
