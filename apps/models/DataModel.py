from apps.models import Model


class Datas(Model):
    __table__ = 'scrap'
    __primary_key__ = 'link'
    __timestamps__ = False