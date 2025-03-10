class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        self.detalles = (titulo, autor)  # Tupla inmutable para título y autor
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        return f"{self.detalles[0]} por {self.detalles[1]} (ISBN: {self.isbn}, Categoría: {self.categoria})"


class Usuario:
    def __init__(self, nombre, usuario_id):
        self.nombre = nombre
        self.usuario_id = usuario_id
        self.libros_prestados = []  # Lista de libros actualmente prestados

    def __str__(self):
        return f"Usuario: {self.nombre} (ID: {self.usuario_id})"


class Biblioteca:
    def __init__(self):
        self.libros_disponibles = {}  # Diccionario: ISBN -> Objeto Libro
        self.usuarios_registrados = set()  # Conjunto de IDs de usuario
        self.prestamos = {}  # Diccionario: ID usuario -> Lista de libros prestados

    def agregar_libro(self, libro):
        if libro.isbn in self.libros_disponibles:
            print("El libro ya está en la biblioteca.")
        else:
            self.libros_disponibles[libro.isbn] = libro
            print(f"Libro agregado: {libro}")

    def eliminar_libro(self, isbn):
        if isbn in self.libros_disponibles:
            del self.libros_disponibles[isbn]
            print(f"Libro con ISBN {isbn} eliminado.")
        else:
            print("El libro no está en la biblioteca.")

    def registrar_usuario(self, usuario):
        if usuario.usuario_id in self.usuarios_registrados:
            print("El usuario ya está registrado.")
        else:
            self.usuarios_registrados.add(usuario.usuario_id)
            self.prestamos[usuario.usuario_id] = []
            print(f"Usuario registrado: {usuario}")

    def dar_de_baja_usuario(self, usuario_id):
        if usuario_id in self.usuarios_registrados:
            if not self.prestamos[usuario_id]:
                self.usuarios_registrados.remove(usuario_id)
                del self.prestamos[usuario_id]
                print(f"Usuario con ID {usuario_id} dado de baja.")
            else:
                print("El usuario tiene libros prestados y no puede ser dado de baja.")
        else:
            print("El usuario no está registrado.")

    def prestar_libro(self, usuario_id, isbn):
        if usuario_id not in self.usuarios_registrados:
            print("El usuario no está registrado.")
            return
        if isbn not in self.libros_disponibles:
            print("El libro no está disponible.")
            return
        libro = self.libros_disponibles.pop(isbn)
        self.prestamos[usuario_id].append(libro)
        print(f"Libro prestado: {libro} a usuario ID {usuario_id}")

    def devolver_libro(self, usuario_id, isbn):
        if usuario_id not in self.prestamos or not self.prestamos[usuario_id]:
            print("El usuario no tiene libros prestados.")
            return
        for libro in self.prestamos[usuario_id]:
            if libro.isbn == isbn:
                self.prestamos[usuario_id].remove(libro)
                self.libros_disponibles[isbn] = libro
                print(f"Libro devuelto: {libro}")
                return
        print("El usuario no tiene prestado este libro.")

    def buscar_libro(self, titulo=None, autor=None, categoria=None):
        resultados = [libro for libro in self.libros_disponibles.values()
                      if (titulo is None or titulo.lower() in libro.detalles[0].lower())
                      and (autor is None or autor.lower() in libro.detalles[1].lower())
                      and (categoria is None or categoria.lower() == libro.categoria.lower())]
        return resultados

    def listar_libros_prestados(self, usuario_id):
        if usuario_id not in self.prestamos or not self.prestamos[usuario_id]:
            print("El usuario no tiene libros prestados.")
            return
        for libro in self.prestamos[usuario_id]:
            print(libro)

# Prueba del sistema
if __name__ == "__main__":
    biblioteca = Biblioteca()

    # Agregar libros
    libro1 = Libro("1984", "George Orwell", "Ficción", "123456")
    libro2 = Libro("Cien años de soledad", "Gabriel García Márquez", "Realismo Mágico", "654321")
    biblioteca.agregar_libro(libro1)
    biblioteca.agregar_libro(libro2)

    # Registrar usuario
    usuario1 = Usuario("Juan Pérez", "U001")
    biblioteca.registrar_usuario(usuario1)

    # Prestar libro
    biblioteca.prestar_libro("U001", "123456")
    
    # Listar libros prestados
    biblioteca.listar_libros_prestados("U001")
    
    # Devolver libro
    biblioteca.devolver_libro("U001", "123456")
    
    # Buscar libros disponibles
    resultados = biblioteca.buscar_libro(titulo="Cien años")
    for libro in resultados:
        print(f"Libro encontrado: {libro}")
