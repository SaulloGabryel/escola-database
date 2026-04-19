from flask import request, jsonify
from services import alunos_service


def listar():
    alunos = alunos_service.listar_alunos()
    return jsonify(alunos), 200


def buscar(aluno_id):
    aluno = alunos_service.buscar_aluno_por_id(aluno_id)
    if not aluno:
        return jsonify({"error": "Aluno não encontrado.", "statusCode": 404}), 404
    return jsonify(aluno), 200


def criar():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição inválido.", "statusCode": 400}), 400

    nome = data.get('nome', '').strip()
    email = data.get('email', '').strip()

    if not nome:
        return jsonify({"error": "Campo 'nome' é obrigatório.", "statusCode": 400}), 400
    if not email:
        return jsonify({"error": "Campo 'email' é obrigatório.", "statusCode": 400}), 400
    if '@' not in email:
        return jsonify({"error": "Email inválido.", "statusCode": 400}), 400

    try:
        aluno = alunos_service.criar_aluno(nome, email)
        return jsonify(aluno), 201
    except ValueError as e:
        return jsonify({"error": str(e), "statusCode": 400}), 400


def atualizar(aluno_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição inválido.", "statusCode": 400}), 400

    nome = data.get('nome', '').strip()
    email = data.get('email', '').strip()

    if not nome:
        return jsonify({"error": "Campo 'nome' é obrigatório.", "statusCode": 400}), 400
    if not email:
        return jsonify({"error": "Campo 'email' é obrigatório.", "statusCode": 400}), 400
    if '@' not in email:
        return jsonify({"error": "Email inválido.", "statusCode": 400}), 400

    try:
        aluno = alunos_service.atualizar_aluno(aluno_id, nome, email)
        if not aluno:
            return jsonify({"error": "Aluno não encontrado.", "statusCode": 404}), 404
        return jsonify(aluno), 200
    except ValueError as e:
        return jsonify({"error": str(e), "statusCode": 400}), 400


def deletar(aluno_id):
    deletado = alunos_service.deletar_aluno(aluno_id)
    if not deletado:
        return jsonify({"error": "Aluno não encontrado.", "statusCode": 404}), 404
    return jsonify({"message": "Aluno deletado com sucesso."}), 200
