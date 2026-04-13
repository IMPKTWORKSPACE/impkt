# Pipeline Manager — IMPKT

Mueve leads entre las 6 etapas del pipeline.

## Uso

```bash
# Resumen del pipeline
python tools/pipeline-manager/pipeline.py summary

# Listar leads en una etapa
python tools/pipeline-manager/pipeline.py ls --stage mila-to-lena

# Crear lead nuevo
python tools/pipeline-manager/pipeline.py create --name "Restaurante El Faro" --stage mila-to-lena

# Mover lead entre etapas
python tools/pipeline-manager/pipeline.py move --lead restaurante-el-faro --from mila-to-lena --to lena-to-sofia

# Descartar lead
python tools/pipeline-manager/pipeline.py discard --lead restaurante-el-faro --from lena-to-sofia --reason "No responde hace 30 dias"

# Archivar lead
python tools/pipeline-manager/pipeline.py archive --lead restaurante-el-faro --from finn-to-nova
```

## Pipeline stages

```
mila-to-lena     (leads generados por Mila)
lena-to-sofia    (prospectos calificados por Lena)
sofia-to-finn    (deals cerrados por Sofia)
finn-to-nova    (proyectos entregados por Finn)
archive          (leads frios, en espera)
lost             (leads descartados)
```

## Equivalencia con agentes

| Etapa | Agente | Significado |
|-------|--------|------------|
| mila-to-lena | Mila | Genero el lead |
| lena-to-sofia | Lena | Califico y descubrió |
| sofia-to-finn | Sofia | Cerro el deal |
| finn-to-nova | Finn | Entregó el proyecto |
| archive | - | Lead frio, no сейчас |
| lost | - | Descartado |
