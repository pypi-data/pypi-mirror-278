

class JsonResponse:

    @staticmethod
    def success(data):
        return {
            'code': 0,
            'message': 'success',
            'data': data
        }

    @staticmethod
    def fail(code: int,message: str):
        return {
            'code': code,
            'message': message,
            'data': None
        }