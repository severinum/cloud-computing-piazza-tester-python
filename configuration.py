PORT=3000
HOST='localhost'
TOKEN_SECRET='ICtxGV?SH1W^0QfxJczj4Qw8TrxdtPg8y7TvVqs$1HnnJFNz6GL_q_MtS8'


def getHost():
    return 'http://%(host)s:%(port)d/api/v1' % {"host": HOST, "port": PORT}