import json
from lib2to3.pytree import Base
from apps.models import schema
from unittest import result
from apps.helper import Log
from apps.schemas import BaseResponse
from apps.schemas.SchemaData import RequestLink, Scrap, ResponseLink
from apps.helper.ConfigHelper import encoder_app
from main import PARAMS
from apps.models.DataModel import Datas
from apps.fira.YahooScrap import get_all_article, get_article_content


# SALT = PARAMS.SALT.salt

class ControllerData(object):
    @classmethod
    def get_contents(cls):
        result = BaseResponse()
        result.status = 400

        try:
            content = get_article_content()
            result.status = 200
            result.message = "Data Ada"
            result.data = content
            Log.info(result.message)

        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)
        
        return result

    @classmethod
    def save_to_db(cls):
        result = BaseResponse()
        result.status = 400

        article = get_article_content()
        panjang_article = len(article)

        #kalo ga ada db nya
        if not schema.has_table("scrap"):
            with schema.create("scrap") as attribute:
                attribute.text("link")
                attribute.text("title")
                attribute.text("news_provider")
                attribute.text("author").nullable()
                attribute.date("date_published")
                attribute.text("image_url")
                attribute.text("text")

        for i in range(panjang_article):
            try:
                if article[i]['link'] not in Datas.lists("link"):
                    data_article = Datas()

                    data_article.link = article[i]['link']
                    data_article.title = article[i]['title']
                    data_article.news_provider = article[i]['news_provider']
                    data_article.author = article[i]['author']
                    data_article.date_published = article[i]['date_published']
                    data_article.image_url = article[i]['image_url']
                    data_article.text = article[i]['text']

                    data_article.save()

                    result.status = 200
                    result.message = "Berhasil Upload Data"
                else:
                    result.message = "Data Sudah Ada"
            except Exception as e:
                Log.error(e)
                result.status = 400
                result.message = str(e)
        
        return result
        
    @classmethod
    def update_author(cls):
        result = BaseResponse()
        result.status = 400
        isi = "Unknown"

        try:
            data = Datas.where('author','=', '').get()

            if data:
                Datas.where('author', '=', '').update(author=isi)
                result.status = 200
                result.message = "Berhasil Update Data"
            else:
                result.message = "Data Tidak Ada"

        except Exception as e:
            Log.error(e)
            result.status = 400
            result.message = str(e)
        
        return result

    @classmethod
    def delete_publisher(cls,publisher=None):
        result = BaseResponse()
        result.status = 400
        
        try:
            if publisher is not None and publisher in Datas.lists("news_provider"):
                Datas.where('news_provider', '=', publisher).delete()
                result.status = 200
                result.message = f"Berhasil Menghapus Data News Provider: {publisher}"        
            elif publisher not in Datas.lists("news_provider"):
                result.status = 404
                result.message = "News Provider Tidak Ditemukan"
            else:
                result.status = 400
                result.message = "Input Kosong"
                Log.info(result.message)
        except:
            m = "Error"
            Log.error(m)
            result.status = 400
            result.message = str(m)

        return result    

       