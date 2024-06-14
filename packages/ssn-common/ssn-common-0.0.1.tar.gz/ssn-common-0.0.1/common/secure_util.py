import hashlib

class SecureUtil:

    @staticmethod
    def get_content_md5(content):
        hash = hashlib.md5()
        hash.update(content.encode('utf-8'))
        return hash.hexdigest()

    @staticmethod
    def get_bytes_md5(content):
        hash = hashlib.md5()
        hash.update(content)
        return hash.hexdigest()

    @staticmethod
    def get_file_md5(fname):
        m = hashlib.md5()
        with open(fname, 'rb') as fobj:
            while True:
                data = fobj.read(5096)
                if not data:
                    break
                m.update(data)
        return m.hexdigest()