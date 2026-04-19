from config.database import get_connection


def listar_alunos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nome, email, created_at FROM alunos ORDER BY id")
    alunos = cursor.fetchall()
    cursor.close()
    conn.close()
    return alunos


def buscar_aluno_por_id(aluno_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nome, email, created_at FROM alunos WHERE id = %s", (aluno_id,))
    aluno = cursor.fetchone()
    cursor.close()
    conn.close()
    return aluno


def criar_aluno(nome, email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Verifica email duplicado
    cursor.execute("SELECT id FROM alunos WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        raise ValueError("Email já cadastrado.")

    cursor.execute(
        "INSERT INTO alunos (nome, email) VALUES (%s, %s)",
        (nome, email)
    )
    conn.commit()
    novo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return buscar_aluno_por_id(novo_id)


def atualizar_aluno(aluno_id, nome, email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Verifica se aluno existe
    cursor.execute("SELECT id FROM alunos WHERE id = %s", (aluno_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return None

    # Verifica email duplicado (outro aluno)
    cursor.execute("SELECT id FROM alunos WHERE email = %s AND id != %s", (email, aluno_id))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        raise ValueError("Email já cadastrado por outro aluno.")

    cursor.execute(
        "UPDATE alunos SET nome = %s, email = %s WHERE id = %s",
        (nome, email, aluno_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return buscar_aluno_por_id(aluno_id)


def deletar_aluno(aluno_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM alunos WHERE id = %s", (aluno_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return False

    cursor.execute("DELETE FROM alunos WHERE id = %s", (aluno_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return True
