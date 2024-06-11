import os
import tempfile
import pytesseract
from pathlib import Path

from google.cloud import vision
from requests import get
from PIL import ImageGrab, Image

from typing import Optional, Tuple, Union, List

class visionai():
    
    def __init__(self, creds: Optional[Path] = None, proxy: Optional[str] = None) -> None:
        
        self.creds = creds
        self.proxy = proxy

        if self.proxy:
             os.environ['HTTP_PROXY'] = self.proxy
             os.environ['HTTPS_PROXY'] = self.proxy
            
        if self.creds:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(self.creds)
        else:  
            if os.getenv('GOOGLE_APPLICATION_CREDENTIALS') is None:
                raise Exception('the visionai class requires that "creds" or the environment variable "GOOGLE_APPLICATION_CREDENTIALS" be defined')

        self.client = vision.ImageAnnotatorClient()

    def detect_text_from_file(self, path: Path) -> Union[List, None]:
        '''
            A função detect_text_from_file é responsável por detectar texto em uma imagem fornecida através de um caminho de arquivo. Essa função utiliza a API do Google Cloud Vision para realizar a detecção de texto em imagens. 
            
            Parâmetros:
                path: Path
                Descrição: O caminho para o arquivo de imagem no sistema de arquivos. Deve ser uma instância da classe Path da biblioteca pathlib.

            Retorno:
                Union[List, None]
                Descrição: Retorna uma lista contendo os textos detectados na imagem, sem duplicatas, ou None caso ocorra algum erro durante o processo de detecção.
        '''

        texts_dect = []

        try:
            with open(path, 'rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)

            response = self.client.text_detection(image=image)
            texts = response.text_annotations
            if response.error.message:
                return None

            for text in texts:
                x = '{}'.format(text.description)
                texts_dect.append(x)

            return list(set(texts_dect))

        except Exception as exc:
            return None

    def detect_text_from_url(self, url: str)-> Union[List, None]:
        '''
            A função detect_text_from_url é responsável por detectar texto em uma imagem obtida a partir de uma URL fornecida. Essa função utiliza a biblioteca de requests para baixar a imagem e a API do Google Cloud Vision para realizar a detecção de texto. 
            
            Parâmetros:
                url: str
                Descrição: Uma string contendo a URL da imagem na web. A URL deve apontar para um arquivo de imagem compatível (JPEG ou PNG).

            Retorno:
                Union[List, None]
                Descrição: Retorna uma lista contendo os textos detectados na imagem, sem duplicatas, ou None caso ocorra algum erro durante o processo de detecção.
        '''

        response = get(url)

        if not response.headers['content-type'] in ['image/jpeg', 'image/jpg', 'image/png']:
            raise Exception('url content-type is not allowed')

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp.write(response.content)

        return self.detect_text_from_file(tmp.name)

    def detect_text_from_screen_region(self, coordenadas:Tuple[int]) -> Union[List, None]:
        '''
        A função detect_text_from_screen_region é responsável por detectar texto em uma região específica da tela capturada. Essa função utiliza a biblioteca PIL (Python Imaging Library) para capturar a tela e a API do Google Cloud Vision para realizar a detecção de texto. 
        
        Parâmetros:
            coordenadas: Tuple[int]
            Descrição: Uma tupla de quatro inteiros que define a região da tela a ser capturada. A tupla deve seguir o formato (left, top, right, bottom).

        Retorno
            Union[List, None]
            Descrição: Retorna uma lista contendo os textos detectados na imagem capturada da tela, sem duplicatas, ou None caso ocorra algum erro durante o processo de detecção.
        '''

        image = ImageGrab.grab(bbox=coordenadas)
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            image.save(tmp.name)

        return self.detect_text_from_file(tmp.name)


class tesseract():
    
    def __init__(self, tesseract_executable: Optional[Path] = None, proxy: Optional[str] = None) -> None:
        
        self.tesseract_executable = tesseract_executable
        self.proxy = proxy

        if self.proxy:
             os.environ['HTTP_PROXY'] = self.proxy
             os.environ['HTTPS_PROXY'] = self.proxy

        
        if self.tesseract_executable:
            pytesseract.pytesseract.tesseract_cmd = str(self.tesseract_executable)
        else:  
            if os.getenv('TESSERACT_EXECUTABLE') is None:
                raise Exception('the tesseract class requires that "tesseract_executable" or the environment variable "TESSERACT_EXECUTABLE" be defined')
            else:
                pytesseract.pytesseract.tesseract_cmd = os.getenv['TESSERACT_EXECUTABLE']


    def detect_text_from_file(self, path: Path) -> Union[str, None]:
        '''
        A função detect_text_from_file é responsável por detectar texto em uma imagem fornecida através de um caminho de arquivo. Essa função utiliza a biblioteca Pillow (PIL) para abrir a imagem e o pytesseract para realizar a detecção de texto. 
        
        Parâmetros:
            path: Path
            Descrição: O caminho para o arquivo de imagem no sistema de arquivos. Deve ser uma instância da classe Path da biblioteca pathlib.

        Retorno:
            Union[str, None]
            Descrição: Retorna uma string contendo o texto detectado na imagem ou None caso ocorra algum erro durante o processo de detecção.
        '''
        try:
            image = Image.open(path)
            result = pytesseract.image_to_string(image)
            return result
        except Exception as exc:
            print(exc)
            return None
        

    def detect_text_from_url(self, url: str)-> Union[str, None]:
        '''
        A função detect_text_from_url é responsável por detectar texto em uma imagem obtida a partir de uma URL fornecida. Essa função utiliza a biblioteca requests para baixar a imagem e o pytesseract para realizar a detecção de texto. 
        
        Parâmetros:
            url: str
            Descrição: Uma string contendo a URL da imagem na web. A URL deve apontar para um arquivo de imagem compatível (JPEG ou PNG).

        Retorno:
            Union[str, None]
            Descrição: Retorna uma string contendo o texto detectado na imagem ou None caso ocorra algum erro durante o processo de detecção.
        '''

        response = get(url)

        if not response.headers['content-type'] in ['image/jpeg', 'image/jpg', 'image/png']:
            raise Exception('url content-type is not allowed')

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp.write(response.content)

        return self.detect_text_from_file(tmp.name)
    
    def detect_text_from_screen_region(self, coordenadas:Tuple[int]) -> Union[List, None]:
        '''
        A função detect_text_from_screen_region é responsável por detectar texto em uma região específica da tela capturada. Essa função utiliza a biblioteca Pillow (PIL) para capturar a tela e o pytesseract para realizar a detecção de texto. 
        
        Parâmetros:
            coordenadas: Tuple[int]
            Descrição: Uma tupla de quatro inteiros que define a região da tela a ser capturada. A tupla deve seguir o formato (left, top, right, bottom).

        Retorno:
            Union[List, None]
            Descrição: Retorna uma lista contendo os textos detectados na imagem capturada da tela ou None caso ocorra algum erro durante o processo de detecção.
        '''

        image = ImageGrab.grab(bbox=coordenadas)
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            image.save(tmp.name)

        return self.detect_text_from_file(tmp.name)
    
    
