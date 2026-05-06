class LoggerMixin:
    def log(self, message):
        print(f"[{self.__class__.__name__} LOG]: {message}")

class Database(LoggerMixin):
    def connect(self):
        self.log("Conectando a la base de datos MySQL...")

class API(LoggerMixin):
    def get_data(self):
        self.log("Solicitando datos del endpoint...")

# Prueba
db = Database()
db.connect()
