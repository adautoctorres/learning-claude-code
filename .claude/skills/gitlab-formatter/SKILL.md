---
name: gitlab-formatter
description: Formata atividades para lançar no GitLab usando templates de markdown estruturados. Use esta skill sempre que o usuário quiser criar uma issue, merge request, épico ou qualquer outra atividade GitLab — mesmo que ele não diga explicitamente "GitLab" mas mencione bug, feature, MR, épico, tarefa, história de usuário ou "quero abrir uma issue". A skill identifica o tipo certo de template e produz o markdown pronto para colar no GitLab.
---

# GitLab Formatter

Você ajuda o usuário a formatar atividades para o GitLab de forma estruturada, usando templates de markdown prontos.

## Fluxo de trabalho

### 1. Identificar o tipo de atividade

Se o usuário não informou o tipo, pergunte de forma direta:

> "Que tipo de atividade você quer criar? Bug, Feature, Merge Request ou Épico?"

Mapeamento das respostas para os templates em `assets/`:

| Tipo             | Template                  |
|------------------|---------------------------|
| Bug / Erro       | `assets/template-bug.md`  |
| Feature / Tarefa | `assets/template-feature.md` |
| Merge Request    | `assets/template-mr.md`   |
| Épico            | `assets/template-epic.md` |

Se o usuário já trouxe um contexto claro na descrição (ex: "tem um erro no login"), prefira inferir o tipo e confirmar antes de perguntar.

### 2. Carregar o template

Leia o arquivo de template correspondente. Os campos entre `{chaves}` são placeholders — você vai preenchê-los com as informações fornecidas pelo usuário.

**Atenção:** Quando o usuário fornecer seus próprios templates (em `assets/`), eles têm prioridade sobre os exemplos. Sempre liste os arquivos disponíveis em `assets/` antes de escolher o template — pode haver templates customizados com nomes diferentes.

### 3. Coletar informações

Com base no template carregado, identifique quais campos são obrigatórios e quais têm valores padrão razoáveis.

- Se o usuário já forneceu a descrição da atividade (via argumento ou mensagem), extraia as informações diretamente do texto dele — não pergunte o que já foi dito.
- Para campos que faltam e são importantes (título, descrição, critérios de aceite), pergunte de forma concisa e agrupe as perguntas em uma única mensagem.
- Campos opcionais como `/assign`, `/label` e `/milestone` podem ser deixados com placeholder `{campo}` se o usuário não souber ou não quiser preencher agora.

### 4. Preencher e entregar o template

Substitua todos os `{placeholders}` com as informações coletadas. Se algum campo não foi informado e não há um valor razoável a inferir, mantenha o placeholder visível para que o usuário saiba que precisa completar depois.

Entregue o resultado como um bloco de código markdown (````markdown`) para facilitar a cópia.

Ao final, pergunte:
> "Quer ajustar algo? Posso reformular seções, adicionar critérios de aceite ou adaptar o tom."

## Templates disponíveis

Os templates de exemplo estão em `assets/`. Quando o usuário trouxer seus próprios templates, eles devem ser adicionados nessa mesma pasta. Antes de cada uso, liste os arquivos em `assets/` para identificar o que está disponível.

| Arquivo                   | Quando usar                                      |
|---------------------------|--------------------------------------------------|
| `template-bug.md`         | Erros, falhas, comportamentos inesperados        |
| `template-feature.md`     | Novas funcionalidades, melhorias, histórias      |
| `template-mr.md`          | Merge requests, pull requests                    |
| `template-epic.md`        | Épicos, iniciativas maiores com várias issues    |

## Dicas de qualidade

- **Título**: prefira o padrão `[TIPO] Verbo + objeto` (ex: `[BUG] Login falha com email inválido`).
- **Critérios de aceite**: sejam testáveis — "o sistema exibe mensagem X quando Y" é melhor que "funcionar corretamente".
- **Quick actions GitLab** (`/label`, `/assign`, `/milestone`): inclua apenas se o usuário souber os valores; caso contrário, deixe o placeholder.
- Se o usuário descrever a atividade de forma narrativa (ex: "tá dando erro quando o usuário tenta logar com email errado"), transforme isso em linguagem de issue — objetivo, direto, com passos claros.
