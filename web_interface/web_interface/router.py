class Rout():
    web_apps={'authorization', 'charts', 'devices', 'setpoints'}
    def db_for_read(self, model):
        if model._meta.app_label in self.web_apps:
            return 'logs'
        return None