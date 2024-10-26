# Sistema de Monitoramento de Vagas de Estacionamento

Este projeto utiliza OpenCV para monitorar vagas de estacionamento em um vídeo. Ele processa cada frame do vídeo para detectar se uma vaga está ocupada ou livre, exibindo o resultado em tempo real.

## Descrição

O código processa um vídeo de estacionamento para identificar o estado de ocupação de cada vaga. A detecção é feita por meio de um limiar de pixels brancos, onde um valor acima de 3000 indica que a vaga está ocupada. As vagas livres são destacadas em verde e as ocupadas em vermelho, com um contador exibindo o número de vagas livres em tempo real.

### Funcionamento

1. **Conversão em Escala de Cinza**: Cada frame é convertido para uma escala de cinza para facilitar o processamento.
2. **Threshold Adaptativo**: Um threshold adaptativo é aplicado para distinguir áreas de interesse (vagas).
3. **Filtros e Dilatação**: Um filtro de suavização e uma operação de dilatação ajudam a melhorar a precisão na contagem de pixels.
4. **Contagem de Pixels Brancos**: Para cada vaga, a quantidade de pixels brancos determina se a vaga está ocupada (>= 3000 pixels) ou livre (< 3000 pixels).

## Requisitos

Para rodar este projeto, você precisará das seguintes bibliotecas:

- OpenCV
- NumPy

Para instalar as dependências, execute:
```bash
pip install opencv-python numpy
```

## Estrutura do Código

- **Coordenadas das Vagas**: As coordenadas de cada vaga são definidas manualmente no código.
- **Processamento do Vídeo**: O vídeo é carregado e processado frame a frame.
- **Exibição em Tempo Real**: As vagas são destacadas no vídeo com retângulos coloridos (verde para vagas livres, vermelho para vagas ocupadas) e um contador de vagas livres é exibido no canto superior esquerdo.

## Como Usar

1. Coloque o vídeo que deseja analisar na pasta do projeto e ajuste o caminho do arquivo no código, se necessário.
2. Execute o script:

   ```bash
   python nome_do_arquivo.py
   ```

3. A janela de vídeo mostrará o status de cada vaga e o total de vagas livres. Para sair, pressione a tecla **'q'**.

## Estrutura de Diretórios

```
├── CTI/
│   └── video.mp4          # O vídeo a ser processado
└── script.py              # O script Python principal
```

## Exemplo de Saída

Durante a execução, o código exibirá:
- **Vídeo Original** com as vagas destacadas (retângulos verdes/vermelhos).
- **Contador de Vagas Livres** no canto superior esquerdo.

## Ajustes e Limitações

- **Parâmetros de Vaga**: As coordenadas e o limiar de ocupação (3000 pixels) podem precisar ser ajustados para outros vídeos ou cenários.
- **Iluminação**: Variações de iluminação podem afetar a precisão do threshold adaptativo.

## Contribuição

Sinta-se à vontade para contribuir com melhorias ou sugestões para o código. 

## Licença

Este projeto está sob a licença MIT.
```
