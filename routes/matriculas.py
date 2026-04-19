from flask import Blueprint
from controllers.matriculas_controller import (
    matricular, cursos_do_aluno,
    cancelar_matricula, concluir_matricula
)

matriculas_bp = Blueprint('matriculas', __name__)

matriculas_bp.route('/', methods=['POST'])(matricular)
matriculas_bp.route('/aluno/<int:aluno_id>/cursos', methods=['GET'])(cursos_do_aluno)
matriculas_bp.route('/aluno/<int:aluno_id>/curso/<int:curso_id>/cancelar', methods=['PATCH'])(cancelar_matricula)
matriculas_bp.route('/aluno/<int:aluno_id>/curso/<int:curso_id>/concluir', methods=['PATCH'])(concluir_matricula)
