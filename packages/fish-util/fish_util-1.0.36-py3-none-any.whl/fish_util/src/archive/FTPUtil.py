from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer

authorizer = DummyAuthorizer()
authorizer.add_user('python', '123456', 'D:\\')
handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(('0.0.0.0', 9010), handler)
server.serve_forever()