---
description: Revisa um arquivo de código em busca de bugs, problemas de segurança e melhorias, gerando um relatório em português.
allowed-tools: Read, Grep, Glob, mcp__ide__getDiagnostics
---

Faça uma revisão de código do seguinte arquivo ou trecho:

$ARGUMENTS

Estruture a revisão em seções:

## Bugs e erros
Liste problemas que causariam falhas em runtime. Se não houver, escreva "Nenhum encontrado."

## Segurança
Aponte vulnerabilidades (injeção, exposição de dados, etc.). Se não houver, escreva "Nenhum encontrado."

## Qualidade e manutenibilidade
Código duplicado, nomes pouco descritivos, complexidade desnecessária.

## Sugestões de melhoria
Melhorias opcionais com justificativa clara.

Seja direto. Cite linha e trecho quando relevante.
