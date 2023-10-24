#### Local Environment
PORT=3000
HOST='localhost'

#### Production Environment (K8S Cluster GCP)
# HOST='34.41.98.117'
# PORT=80


TOKEN_SECRET='ICtxGVsSH1W40QfxJczj4Qw8TrxdtPg8y7TvVqsa1HnnJFNz6GL_q_MtS8'


def getHost():
    return 'http://%(host)s:%(port)d/api/v1' % {"host": HOST, "port": PORT}