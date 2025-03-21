import sqlite3

class NewsStorage:
    def __init__(self, db_path="news_database.db"):
        """
        Inicializa la conexión a la base de datos.
        
        Args:
            db_path (str): Ruta al archivo de la base de datos SQLite
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Establece la conexión con la base de datos SQLite"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  
            self.cursor = self.connection.cursor()
            print(f"Conexión exitosa a la base de datos: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
    
    def _create_tables(self):
        """Crea las tablas necesarias si no existen"""
        try:
            # Tabla principal de noticias
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Titulo TEXT NOT NULL,
                URL TEXT UNIQUE NOT NULL,
                Autor TEXT,
                Fecha TEXT DEFAULT CURRENT_TIMESTAMP,
                Imagen_url TEXT,
                Descripcion TEXT
            )
            ''')
            
            
            self.connection.commit()
            print("Tablas creadas correctamente")
        except sqlite3.Error as e:
            print(f"Error al crear las tablas: {e}")
    
    def save_news(self, news_items):
        """
        Guarda una lista de noticias en la base de datos
        
        Args:
            news_items (list): Lista de diccionarios con los datos de las noticias
            
        Returns:
            tuple: (int, int) - (total de noticias, noticias nuevas guardadas)
        """
        if not news_items:
            return (0, 0)
        
        new_count = 0
        try:
            for item in news_items:
                # Verificar si la noticia ya existe por URL
                self.cursor.execute("SELECT id FROM news WHERE URL = ?", (item.get('url'),))
                existing = self.cursor.fetchone()
                
                if not existing:
                    self.cursor.execute('''
                    INSERT INTO news (Titulo, URL, Autor, Fecha, Imagen_url, Descripcion)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        item.get('title', 'No disponible'),
                        item.get('url', ''),
                        item.get('author', 'No disponible'),
                        item.get('date', 'No disponible'),
                        item.get('image_url', 'No disponible'),
                        item.get('headline', 'No disponible'),
                    ))
                    new_count += 1
            
            self.connection.commit()
            return (len(news_items), new_count)
        except sqlite3.Error as e:
            print(f"Error al guardar noticias: {e}")
            self.connection.rollback()
            return (len(news_items), 0)
    
    
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if self.connection:
            self.connection.close()
            print("Conexión a la base de datos cerrada")