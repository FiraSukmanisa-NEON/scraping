from apps.models import Model


class Loan(Model):
    __table__ = 'lendings'
    __primary_key__ = 'loanid'
