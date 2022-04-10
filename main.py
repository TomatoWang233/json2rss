# main.py
from tornado import httpclient
import tornado.ioloop
import tornado.web
from loguru import logger
import PyRSS2Gen
import json

logger.info("booting rss2json server...")

class LectureHandler(tornado.web.RequestHandler):
    url="https://lecture.idealclover.cn/getAll"
    async def get(self):
        response=await httpclient.AsyncHTTPClient().fetch(self.url)
        response=json.loads(response.body.decode(encoding="utf-8"))
        rss=PyRSS2Gen.RSS2("南哪讲座","https://lecture.idealclover.cn/","南京大学讲座信息收集")
        for i in response["data"]:
            author=i["teacher"]+"@"+i["department"] if i["department"] else i ["teacher"]
            pubDate=i["startTime"]+"~"+i["endTime"]
            rss.items.append(PyRSS2Gen.RSSItem(title=i["title"],author=author,description=i["info"],pubDate=pubDate))
        xml=rss.to_xml("utf-8")
        self.finish(xml)

app =  tornado.web.Application([(r"/lecture", LectureHandler),])
app.listen(1200)
tornado.ioloop.IOLoop.current().start()