# Visão Geral

Este projeto fornece um conjunto de ferramentas para capturar regiões da tela e detectar texto dentro de imagens usando dois métodos diferentes de OCR (Reconhecimento Óptico de Caracteres): Google Cloud Vision API e Tesseract.

## Instalação

Para usar este projeto, você precisa instalar as dependências necessárias. Você pode fazer isso usando o poetry


```bash
poetry install
```

## Uso
### screenGrabber

Esta classe inicializa um aplicativo simples de captura de tela usando Tkinter.
Exemplo:

```python
from visionFusion.utils import ScreenGrabber

grabber = screenGrabber()
```

### visionai

Esta classe usa a API Google Cloud Vision para detectar texto em imagens de diferentes fontes.
Inicialização


```python
from pathlib import Path

# Inicialize com credenciais do Google Cloud e proxy opcional
vision = visionai(creds=Path('caminho/para/creds.json'), proxy='http://seu.proxy:porta')
```

#### Métodos:

- __detect_text_from_file(path: Path) -> Union[List, None]__

    Detecta texto em um arquivo de imagem.

    
    ```python
    textos = vision.detect_text_from_file(Path('caminho/para/imagem.png'))
    ```
- __detect_text_from_url(url: str) -> Union[List, None]__

    Detecta texto em uma imagem a partir de uma URL.

    
    ```python
    textos = vision.detect_text_from_url('https://exemplo.com/imagem.png')
    ```
- __detect_text_from_screen_region(coordenadas: Tuple[int]) -> Union[List, None]__

    Detecta texto em uma região específica da tela.

    
    ```python
    textos = vision.detect_text_from_screen_region((0, 0, 100, 100))
    ```

### tesseract

Esta classe usa Tesseract OCR para detectar texto em imagens de diferentes fontes.
Inicialização


```python
from pathlib import Path

Inicialize com o caminho do executável do Tesseract
tess = tesseract(tesseract_executable=Path('caminho/para/tesseract'))
```
#### Métodos:

- __detect_text_from_file(path: Path) -> Union[str, None]__

    Detecta texto em um arquivo de imagem.

    
    ```python
    texto = tess.detect_text_from_file(Path('caminho/para/imagem.png'))
    ```
- __detect_text_from_url(url: str) -> Union[str, None]__

    Detecta texto em uma imagem a partir de uma URL.

    
    ```python
    texto = tess.detect_text_from_url('https://exemplo.com/imagem.png')
    ```

- __detect_text_from_screen_region(coordenadas: Tuple[int]) -> Union[str, None]__

    Detecta texto em uma região específica da tela.

    
    ```python
    texto = tess.detect_text_from_screen_region((0, 0, 100, 100))
    ```

## Dependências:

- google-cloud-vision: Biblioteca cliente da API Google Cloud Vision.
- pillow: Biblioteca de imagens Python (PIL Fork).
- pytesseract: Wrapper Python para o Tesseract-OCR da Google.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Autor

Desenvolvido por Guilherme Eduardo Poças.

Sinta-se à vontade para entrar em contato com qualquer dúvida ou feedback!