# crm_votos

## Serviços que compõem a aplicação

Além do uWSGI, que é o servidor de aplicação utilizado (xxx) para disponibilizar a aplicação Django, o Athenas depende de outros serviços para o seu correto funcionamento. Tais serviços são executados como containers _Docker_ e suas configurações estão inclusas no projeto. São eles:

- [PostgreSQL v14.4](#postgresql)
- [Nginx v1.18.0(#nginx)

### PostgreSQL

Como banco de dados o sistema utiliza o PostgreSQL em sua versão 11.5. A imagem utilizada para este serviço foi construída a partir da imagem oficial na versão _alpine_. Em cima dela foi adicionado o suporte à extensão _plpython_ que é necessária para a execução de alguns relatórios que dependem de funções escritas em python.

Nome do serviço no docker-compose: `postgres`.
Porta utilizada: `5432`.

### Nginx

O Nginx foi a ferramenta escolhida para realizar o proxy de acesso aos demais serviços e servir arquivos estáticos. A versão utilizada atualmente é a 1.18.0 e a imagem oficial é utilizada como base para a construção da imagem aqui utilizada, que apenas copia arquivos de config e páginas de erros personalizadas.

Nome do serviço no docker-compose: `nginx`.
Porta utilizada: `80`.

## Instalação do Docker

Caso o Docker ainda não esteja instalado na máquina em que se deseja configurar o Athenas, faça-o seguindo as recomendações presentes na própria documentação da ferramenta de acordo com a versão do seu sistema operacional.

**Atenção**: _Após a instalação do Docker e adição do usuário corrente ao grupo docker (o que é mandatório para a perfeita execução dos demais passos), será necessário reiniciar a sessão para que as alterações surtam efeito._

Para testar se o Docker está instalado corretamente, tente executar o seguinte comando no terminal:

``` bash
docker ps
```

Caso você se depare com um erro informando que não tem permissão para conectar-se ao socket do Docker, provavelmente seu usuário não foi adicionado corretamente ao grupo `docker`. Certifique-se de concluir este passo antes de prosseguir.

