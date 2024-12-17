if __name__ == 'wsgi':
    print('UWSGI Server Running App...')
    from main import app as application
