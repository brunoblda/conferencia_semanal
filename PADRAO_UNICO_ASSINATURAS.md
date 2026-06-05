# Padrão Único de Assinaturas (DDD + Clean Architecture)

Este documento define um padrão único para assinaturas, nomes e responsabilidades por camada.
Objetivo: manter consistência arquitetural no projeto e reduzir acoplamento entre domínio, aplicação e infraestrutura.

## 1. Regra Central

Em todos os fluxos:

- `Request Adapter` traduz entrada externa para `InputDTO`
- `Controller.handle(input_dto)` orquestra caso de uso e presenter
- `UseCase.execute(input_dto)` aplica regra de negócio
- `Presenter.present(output_dto)` monta resposta de interface
- `Composer.build()` faz wiring e retorna `controller.handle`

## 2. Assinaturas Canônicas

### 2.1 Request Adapter

```python
class CompararPiRequestAdapter:
    def adapt(self, raw_request: dict) -> CompararPiInput:
        ...
```

### 2.2 Controller

```python
class CompararPiController:
    def handle(self, input_dto: CompararPiInput) -> ResponseFormat:
        ...
```

### 2.3 Use Case

```python
class CompararPiSeof:
    def execute(self, input_dto: CompararPiInput) -> CompararPiOutput:
        ...
```

### 2.4 Presenter

```python
class CompararPiPresenter:
    def present(self, output_dto: CompararPiOutput) -> ResponseFormat:
        ...
```

### 2.5 Composer

```python
class CompararPiSeofComposer:
    def build(self):
        return controller.handle
```

## 3. Convenção de Nomes

Para cada caso de uso `<NomeCaso>`:

- Input DTO: `<NomeCaso>Input`
- Output DTO: `<NomeCaso>Output`
- Use case: `<NomeCaso>.execute(...)`
- Controller: `<NomeCaso>Controller.handle(...)`
- Presenter: `<NomeCaso>Presenter.present(...)`
- Composer: `<nome_caso>_composer.build()`

Exemplo:

- `CompararPiInput`
- `CompararPiOutput`
- `CompararPiSeof.execute(...)`
- `CompararPiController.handle(...)`
- `CompararPiPresenter.present(...)`
- `comparar_pi_seof_composer.build()`

## 4. Responsabilidades por Camada

### 4.1 Domain

- Entidades e regras de domínio
- Interfaces de domínio (portas internas)
- Sem dependência de framework, UI, banco, PDF, pandas/tabula

### 4.2 Use Cases (Application)

- Orquestra regra de aplicação
- Usa interfaces (portas), não detalhes concretos
- Retorna `OutputDTO` estruturado
- Não formata saída de UI, arquivo ou protocolo

### 4.3 Adapters

- Controllers (entrada)
- Presenters (saída)
- Request adapters
- Traduzem dados entre bordas e aplicação

### 4.4 Infra

- Implementações concretas de portas
- PDF, filesystem, tabula, APIs externas, etc.
- Nunca importado por `domain`

### 4.5 Main (Composition Root)

- Apenas wiring de dependências
- Escolhe implementações concretas
- Constrói controller + use case + presenter

## 5. Contratos de Qualidade (obrigatórios)

1. Todo `Controller` expõe `handle(...)`
2. Todo `UseCase` expõe `execute(...)`
3. Todo fluxo possui `InputDTO` e `OutputDTO`
4. `UseCase` não retorna texto final formatado para UI/PDF
5. `Presenter` é o único responsável por formatação final de resposta
6. `Composer` não contém regra de negócio
7. Assinaturas de interfaces e implementações devem ser idênticas

## 6. Exemplo de Fluxo Completo

```python
# main/composer/comparar_pi_seof_composer.py

def build_comparar_pi_seof_handler():
    request_adapter = CompararPiRequestAdapter()
    use_case = CompararPiSeof(utils_gateway, comparador_gateway)
    presenter = CompararPiPresenter()
    controller = CompararPiController(use_case, presenter)
    return request_adapter, controller.handle
```

```python
# ponto de entrada (UI/CLI)

request_adapter, handle = build_comparar_pi_seof_handler()
input_dto = request_adapter.adapt(raw_request)
response = handle(input_dto)
```

## 7. Checklist de Refatoração por Fluxo

Use esta lista para cada fluxo (SEOF, SIAFI, etc.):

1. Criar `InputDTO` e `OutputDTO`
2. Ajustar `UseCase.execute(input_dto) -> output_dto`
3. Remover formatação de saída de dentro do use case
4. Criar/ajustar `Presenter.present(output_dto)`
5. Ajustar `Controller.handle(input_dto)` para usar presenter
6. Ajustar `Composer.build()` para retornar `handle`
7. Validar interfaces x implementações
8. Adicionar testes de use case e controller

## 8. Anti-padrões a Evitar

- `UseCase` gerando string final para relatório/UI
- Interface com assinatura diferente da implementação
- `domain` importando libs técnicas (PDF, pandas, tabula, framework)
- `controller` contendo regra de negócio
- `composer` executando lógica além de wiring

## 9. Observações para o Projeto Atual

Para o estado atual do projeto, priorize nesta ordem:

1. Corrigir divergências de assinatura de interfaces
2. Padronizar `handle` (controller) e `execute` (use case)
3. Extrair formatação de resposta dos use cases de comparação para presenters
4. Consolidar DTOs de entrada e saída por caso de uso
5. Cobrir fluxos principais com testes automatizados

---

Última atualização: 2026-06-05
