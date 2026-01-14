#vars
NOME_AGENTE="rotorres_agent"
GIT_TOKEN="your_git_token_here"

#criando virtual env python
uv venv venv
sleep 10
source venv/bin/activate

#instalando adk
uv pip install google-adk

#criando o agente com adk
adk create $NOME_AGENTE
#Choose a model for the root agent: 1. gemini-2.5-flash
#Choose a backend: 2. Vertex AI

#copia o conteúdo do agent.py.sample para o arquivo agent.py, e o conteúdo do .env.sample para o .env no folder do agente
cat agent.py.sample > $NOME_AGENTE/agent.py
cat .env.sample > $NOME_AGENTE/.env
(echo "\nGIT_TOKEN=$GIT_TOKEN") >> $NOME_AGENTE/.env

#rodando o agente
adk run $NOME_AGENTE