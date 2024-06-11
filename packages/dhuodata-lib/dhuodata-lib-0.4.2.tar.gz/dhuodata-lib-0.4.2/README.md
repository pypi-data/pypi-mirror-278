# DHuO LIb

## Board

![](assets/imgs/board.png)

## Features

### Login 

- [x] login
    - Auth.login
    - Auth.is_logged

![](assets/docs/src/login/login.png)

--- 
### Análise Exploratória / Persistencia / Aquisição de Dados

- [x] leitura de arquivos de bucket 
    - Dhuolib.read_from_bucket

- [x] leitura/escrita dataset Lake house
    - Dhuolib.execute_select
    - Dhuolib.execute_dml

![](assets/docs/src/persistencia/persistencia.png)

--- 
### Model registry

- [x] upload/download de modelos de ml
    - Dhuolib.create_experiment
    - Dhuolib.save_model
    - Dhuolib.load_model

![](assets/docs/src/model_registry/model_registry.png)

--- 
### Deploy

- [x] criar cluster no Dataflow
- [x] informar o dado de schedule e criação de aplicação Dataflow     
- [x] inserção de lista de dependencias: libs + zip + script.py
    - Dhuolib.depĺoy
    - config/deploy.yaml

> OCI - Oracle Function para uso do [Arquivo Compactado de Dependencia](https://docs.oracle.com/pt-br/iaas/data-flow/using/third-party-provide-archive.htm)

![](assets/docs/src/deploy/deploy.png)

--- 
### Prediction

- [ ] salvar dataset saída de modelo 
    - Dhuolib.save_predictions
    Scrip template: predict.py

    Execução: Oracle Function

![](assets/docs/src/feedback_status/feedback_status.png)

---
### Feedback dos steps do Pipeline para o usuário
- Dhuolib.pipeline_status_exec

![](ass)


### C4 Diagram
#### Context
 ![](assets/docs/src/c4/context/context.png)

#### Components
 ![](assets/docs/src/c4/components/components.png)


#### Containers
 ![](assets/docs/src/c4/containers/containers.png)


![](ass)

## Issues

#### 

- Definir padrões e nomes de buckets
- Expor o MLFLow para uso em VPN
- No log de experimentos não está contemplado:
    - Métricas
    - Hiperparâmetros
- Não estamos usaando a API do Dataflow para acompanhamento de status da execução
- Não estamos contemplando Feature Engineering
- Não estamos contemplando Etapas de Treinamento
- Não estamos contemplando o Feedback de execuções 100% remotas

## References

- https://docs.oracle.com/pt-br/iaas/data-flow/using/third-party-provide-archive.htm
- https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml
- https://plantuml.com/