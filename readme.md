

# Rodando migrations


## Ao alterar algum model na aplicação e rodar o comando:
```bash
alembic revision --autogenerate -m "Migration Message"
```

## Será criado um arquivo de revisão, que ao rodar: 
```bash
alembic upgrade head
```

## Será de fato aplicado ao banco de dados