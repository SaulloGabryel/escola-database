from config.database import get_connection


def listar_cursos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, titulo, descricao, created_at FROM cursos ORDER BY id")
    cursos = cursor.fetchall()
    cursor.close()
    conn.close()
    return cursos


def buscar_curso_por_id(curso_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, titulo, descricao, created_at FROM cursos WHERE id = %s", (curso_id,))
    curso = cursor.fetchone()
    cursor.close()
    conn.close()
    return curso


def criar_curso(titulo, descricao=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cursos (titulo, descricao) VALUES (%s, %s)",
        (titulo, descricao)
    )
    conn.commit()
    novo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return buscar_curso_por_id(novo_id)


def atualizar_curso(curso_id, titulo, descricao=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM cursos WHERE id = %s", (curso_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return None

    cursor.execute(
        "UPDATE cursos SET titulo = %s, descricao = %s WHERE id = %s",
        (titulo, descricao, curso_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return buscar_curso_por_id(curso_id)


def deletar_curso(curso_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM cursos WHERE id = %s", (curso_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return False

    cursor.execute("DELETE FROM cursos WHERE id = %s", (curso_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return True
