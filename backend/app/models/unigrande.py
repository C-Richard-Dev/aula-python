from tortoise import fields, models

class PeriodoLetivo(models.Model):
    id = fields.IntField(pk=True)
    ano = fields.IntField() # ano que pode ser 2020, 2025
    semestre = fields.IntField() # semestre que pode ser 1 ou 2
    data_inicio = fields.DateField()
    data_fim = fields.DateField()

    class Meta:
        table = "periodos_letivos"
        unique_together = (("ano", "semestre"),)
        indexes = (("ano", "semestre"),)


class Professor(models.Model):
    id = fields.IntField(pk=True)  # DT_PROF
    matricula = fields.IntField(null=True)  # MAT_PROF
    nome = fields.CharField(max_length=50)

    class Meta:
        table = "professores"


class Curso(models.Model):
    id = fields.IntField(pk=True)  # COD_CURSO
    nome = fields.CharField(max_length=40)
    total_creditos = fields.IntField()
    professor = fields.ForeignKeyField("models.Professor", related_name="cursos")

    class Meta:
        table = "cursos"


class Disciplina(models.Model):
    id = fields.IntField(pk=True)  # COD_DISC
    nome = fields.CharField(max_length=50)
    creditos = fields.IntField()
    tipo = fields.CharField(max_length=1)  # obrigatória ou optativa
    horas_obrig = fields.IntField()
    limite_faltas = fields.IntField()

    class Meta:
        table = "disciplinas"


class Matriz(models.Model):
    id = fields.IntField(pk=True)  # pode ser chave artificial
    curso = fields.ForeignKeyField("models.Curso", related_name="matrizes")
    disciplina = fields.ForeignKeyField("models.Disciplina", related_name="matrizes")
    periodo = fields.IntField()

    class Meta:
        table = "matrizes"
        unique_together = (("curso", "disciplina"),)


class Turma(models.Model):
    id = fields.IntField(pk=True)  # pode ser artificial
    ano = fields.IntField()
    semestre = fields.IntField()
    disciplina = fields.ForeignKeyField("models.Disciplina", related_name="turmas")
    professor = fields.ForeignKeyField("models.Professor", related_name="turmas")
    vagas = fields.IntField()

    class Meta:
        table = "turmas"
        indexes = (("ano", "semestre"),)


class Aluno(models.Model):
    id = fields.IntField(pk=True)  # MAT_ALU
    nome = fields.CharField(max_length=50)
    total_creditos = fields.IntField()
    data_nascimento = fields.DateField()
    media_geral = fields.DecimalField(max_digits=4, decimal_places=2, null=True)
    curso = fields.ForeignKeyField("models.Curso", related_name="alunos")

    class Meta:
        table = "alunos"


class Matricula(models.Model):
    id = fields.IntField(pk=True)  # artificial
    ano = fields.IntField()
    semestre = fields.IntField()
    aluno = fields.ForeignKeyField("models.Aluno", related_name="matriculas")
    disciplina = fields.ForeignKeyField("models.Disciplina", related_name="matriculas")

    nota_1 = fields.DecimalField(max_digits=4, decimal_places=2, null=True)
    nota_2 = fields.DecimalField(max_digits=4, decimal_places=2, null=True)
    nota_3 = fields.DecimalField(max_digits=4, decimal_places=2, null=True)

    faltas_q1 = fields.IntField(null=True)
    faltas_q2 = fields.IntField(null=True)
    faltas_q3 = fields.IntField(null=True)

    class Meta:
        table = "matriculas"
        indexes = (("ano", "semestre"),)


class Historico(models.Model):
    id = fields.IntField(pk=True)  # artificial
    ano = fields.IntField()
    semestre = fields.IntField()
    aluno = fields.ForeignKeyField("models.Aluno", related_name="historicos")
    disciplina = fields.ForeignKeyField("models.Disciplina", related_name="historicos")

    situacao = fields.CharField(max_length=2)  # AP/RE/...
    media = fields.DecimalField(max_digits=4, decimal_places=2, null=True)
    faltas = fields.IntField(null=True)

    class Meta:
        table = "historicos"
        indexes = (("ano", "semestre"),)