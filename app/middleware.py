from db.base import db


def PeeweeConnectionMiddleware(get_response):
    def middleware(request):
        db.connect()
        try:
            response = get_response(request)
        finally:
            if not db.is_closed():
                db.close()
        return response

    return middleware
