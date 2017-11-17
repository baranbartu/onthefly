from onthefly.backend import AbstractBackend


class FileBackend(AbstractBackend):
    def __init__(self, options, **kwargs):
        file_name = 'filebackendstorage.ini'
        try:
            file_storage = open(file_name, 'r')
        except IOError:
            file_storage = open(file_name, 'w')
        self.file_storage = file_storage
        super(FileBackend, self).__init__(options, **kwargs)

    def set(self, name, value):
        # name: DEBUG, value: True

        # DEBUG:True
        # STORAGE:Mysql
        # ...
        record = '%s:%s' % (name, value)
        self.file_storage.write(record)

    # TODO will be implemented later
