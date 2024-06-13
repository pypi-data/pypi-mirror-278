import os


class Env:
    _SYNTOOLS_PATCH = None
    _SYNTOOLS_SYN_GET_DOWNLOAD = None
    _SYNTOOLS_DOWNLOAD_RETRIES = None
    _SYNTOOLS_DOWNLOAD_WORKERS = None
    _SYNTOOLS_COPY_WORKERS = None
    _SYNTOOLS_LIST_WORKERS = None
    _SYNTOOLS_COMPARE_WORKERS = None

    @classmethod
    def SYNTOOLS_PATCH(cls):
        if cls._SYNTOOLS_PATCH is None:
            cls._SYNTOOLS_PATCH = os.environ.get('SYNTOOLS_PATCH', 'false').lower().strip() == 'true'
        return cls._SYNTOOLS_PATCH

    @classmethod
    def SYNTOOLS_SYN_GET_DOWNLOAD(cls):
        if cls._SYNTOOLS_SYN_GET_DOWNLOAD is None:
            cls._SYNTOOLS_SYN_GET_DOWNLOAD = os.environ.get('SYNTOOLS_SYN_GET_DOWNLOAD',
                                                            'false').lower().strip() == 'true'
        return cls._SYNTOOLS_SYN_GET_DOWNLOAD

    @classmethod
    def SYNTOOLS_DOWNLOAD_RETRIES(cls):
        if cls._SYNTOOLS_DOWNLOAD_RETRIES is None:
            cls._SYNTOOLS_DOWNLOAD_RETRIES = int(os.environ.get('SYNTOOLS_DOWNLOAD_RETRIES', '10'))
        return cls._SYNTOOLS_DOWNLOAD_RETRIES

    @classmethod
    def SYNTOOLS_DOWNLOAD_WORKERS(cls):
        if cls._SYNTOOLS_DOWNLOAD_WORKERS is None:
            cls._SYNTOOLS_DOWNLOAD_WORKERS = int(os.environ.get('SYNTOOLS_DOWNLOAD_WORKERS', '20'))
        return cls._SYNTOOLS_DOWNLOAD_WORKERS

    @classmethod
    def SYNTOOLS_COPY_WORKERS(cls):
        if cls._SYNTOOLS_COPY_WORKERS is None:
            cls._SYNTOOLS_COPY_WORKERS = int(os.environ.get('SYNTOOLS_COPY_WORKERS', '20'))
        return cls._SYNTOOLS_COPY_WORKERS

    @classmethod
    def SYNTOOLS_LIST_WORKERS(cls):
        if cls._SYNTOOLS_LIST_WORKERS is None:
            cls._SYNTOOLS_LIST_WORKERS = int(os.environ.get('SYNTOOLS_LIST_WORKERS', '20'))
        return cls._SYNTOOLS_LIST_WORKERS

    @classmethod
    def SYNTOOLS_COMPARE_WORKERS(cls):
        if cls._SYNTOOLS_COMPARE_WORKERS is None:
            cls._SYNTOOLS_COMPARE_WORKERS = int(os.environ.get('SYNTOOLS_COMPARE_WORKERS', '20'))
        return cls._SYNTOOLS_COMPARE_WORKERS
