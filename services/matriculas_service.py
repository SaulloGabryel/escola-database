from config.database import get_connection

MAX_MATRICULAS_ATIVAS = 5


def matricular_aluno(aluno_id, curso_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Verifica se aluno existe
    cursor.execute("SELECT id FROM alunos WHERE id = %s", (aluno_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise LookupError("Aluno não encontrado.")

    # Verifica se curso existe
    cursor.execute("SELECT id FROM cursos WHERE id = %s", (curso_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise LookupError("Curso não encontrado.")

    # Verifica matrícula duplicada (ativa ou concluída no mesmo curso)
    cursor.execute(
        "SELECT id FROM matriculas WHERE aluno_id = %s AND curso_id = %s AND status != 'cancelada'",
        (aluno_id, curso_id)
    )
    if cursor.fetchone():
        cursor.close()
        conn.close()
        raise ValueError("Aluno já está matriculado neste curso.")

    # Verifica limite de matrículas ativas
    cursor.execute(
        "SELECT COUNT(*) as total FROM matriculas WHERE aluno_id = %s AND status = 'ativa'",
        (aluno_id,)
    )
    resultado = cursor.fetchone()
    if resultado['total'] >= MAX_MATRICULAS_ATIVAS:
        cursor.close()
        conn.close()
        raise ValueError(f"Aluno atingiu o limite de {MAX_MATRICULAS_ATIVAS} matrículas ativas.")

    cursor.execute(
        "INSERT INTO matriculas (aluno_id, curso_id, status) VALUES (%s, %s, 'ativa')",
        (aluno_id, curso_id)
    )
    conn.commit()
    novo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return buscar_matricula_por_id(novo_id)


def buscar_matricula_por_id(matricula_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT m.id, m.aluno_id, m.curso_id, m.status, m.created_at,
               a.nome as aluno_nome, c.titulo as curso_titulo
        FROM matriculas m
        JOIN alunos a ON a.id = m.aluno_id
        JOIN cursos c ON c.id = m.curso_id
        WHERE m.id = %s
        """,
        (matricula_id,)
    )
    matricula = cursor.fetchone()
    cursor.close()
    conn.close()
    return matricula


def listar_cursos_do_aluno(aluno_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id FROM alunos WHERE id = %s", (aluno_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise LookupError("Aluno não encontrado.")

    cursor.execute(
        """
        SELECT c.id, c.titulo, c.descricao, m.status, m.created_at as matricula_em
        FROM matriculas m
        JOIN cursos c ON c.id = m.curso_id
        WHERE m.aluno_id = %s
        ORDER BY m.created_at DESC
        """,
        (aluno_id,)
    )
    cursos = cursor.fetchall()
    cursor.close()
    conn.close()
    return cursos


def listar_alunos_do_curso(curso_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id FROM cursos WHERE id = %s", (curso_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise LookupError("Curso não encontrado.")

    cursor.execute(
        """
        SELECT a.id, a.nome, a.email, m.status, m.created_at as matricula_em
        FROM matriculas m
        JOIN alunos a ON a.id = m.aluno_id
        WHERE m.curso_id = %s
        ORDER BY m.created_at DESC
        """,
        (curso_id,)
    )
    alunos = cursor.fetchall()
    cursor.close()
    conn.close()
    return alunos


def alterar_status_matricula(aluno_id, curso_id, novo_status):
    """Cancela ou conclui uma matrícula."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, status FROM matriculas WHERE aluno_id = %s AND curso_id = %s",
        (aluno_id, curso_id)
    )
    matricula = cursor.fetchone()

    if not matricula:
        cursor.close()
        conn.close()
        raise LookupError("Matrícula não encontrada.")

    if matricula['status'] == 'cancelada':
        cursor.close()
        conn.close()
        raise ValueError("Matrícula já está cancelada.")

    if matricula['status'] == 'concluida' and novo_status == 'concluida':
        cursor.close()
        conn.close()
        raise ValueError("Matrícula já está concluída.")

    cursor.execute(
        "UPDATE matriculas SET status = %s WHERE id = %s",
        (novo_status, matricula['id'])
    )
    conn.commit()
    matricula_id = matricula['id']
    cursor.close()
    conn.close()
    return buscar_matricula_por_id(matricula_id)
