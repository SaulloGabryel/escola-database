from flask import request, jsonify
from services import cursos_service


def listar():
    cursos = cursos_service.listar_cursos()
    return jsonify(cursos), 200


def buscar(curso_id):
    curso = cursos_service.buscar_curso_por_id(curso_id)
    if not curso:
        return jsonify({"error": "Curso não encontrado.", "statusCode": 404}), 404
    return jsonify(curso), 200


def criar():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição inválido.", "statusCode": 400}), 400

    titulo = data.get('titulo', '').strip()
    descricao = data.get('descricao', '').strip() or None

    if not titulo:
        return jsonify({"error": "Campo 'titulo' é obrigatório.", "statusCode": 400}), 400

    curso = cursos_service.criar_curso(titulo, descricao)
    return jsonify(curso), 201


def atualizar(curso_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição inválido.", "statusCode": 400}), 400

    titulo = data.get('titulo', '').strip()
    descricao = data.get('descricao', '').strip() or None

    if not titulo:
        return jsonify({"error": "Campo 'titulo' é obrigatório.", "statusCode": 400}), 400

    curso = cursos_service.atualizar_curso(curso_id, titulo, descricao)
    if not curso:
        return jsonify({"error": "Curso não encontrado.", "statusCode": 404}), 404
    return jsonify(curso), 200


def deletar(curso_id):
    deletado = cursos_service.deletar_curso(curso_id)
    if not deletado:
        return jsonify({"error": "Curso não encontrado.", "statusCode": 404}), 404
    return jsonify({"message": "Curso deletado com sucesso."}), 200
