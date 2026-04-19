from flask import request, jsonify
from services import matriculas_service


def matricular():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição inválido.", "statusCode": 400}), 400

    aluno_id = data.get('aluno_id')
    curso_id = data.get('curso_id')

    if not aluno_id or not curso_id:
        return jsonify({"error": "Campos 'aluno_id' e 'curso_id' são obrigatórios.", "statusCode": 400}), 400

    try:
        matricula = matriculas_service.matricular_aluno(aluno_id, curso_id)
        return jsonify(matricula), 201
    except LookupError as e:
        return jsonify({"error": str(e), "statusCode": 404}), 404
    except ValueError as e:
        return jsonify({"error": str(e), "statusCode": 400}), 400


def cursos_do_aluno(aluno_id):
    try:
        cursos = matriculas_service.listar_cursos_do_aluno(aluno_id)
        return jsonify(cursos), 200
    except LookupError as e:
        return jsonify({"error": str(e), "statusCode": 404}), 404


def alunos_do_curso(curso_id):
    try:
        alunos = matriculas_service.listar_alunos_do_curso(curso_id)
        return jsonify(alunos), 200
    except LookupError as e:
        return jsonify({"error": str(e), "statusCode": 404}), 404


def cancelar_matricula(aluno_id, curso_id):
    try:
        matricula = matriculas_service.alterar_status_matricula(aluno_id, curso_id, 'cancelada')
        return jsonify(matricula), 200
    except LookupError as e:
        return jsonify({"error": str(e), "statusCode": 404}), 404
    except ValueError as e:
        return jsonify({"error": str(e), "statusCode": 400}), 400


def concluir_matricula(aluno_id, curso_id):
    try:
        matricula = matriculas_service.alterar_status_matricula(aluno_id, curso_id, 'concluida')
        return jsonify(matricula), 200
    except LookupError as e:
        return jsonify({"error": str(e), "statusCode": 404}), 404
    except ValueError as e:
        return jsonify({"error": str(e), "statusCode": 400}), 400
