#Importar bibliotecas
#comece instalando a bilbioteca numpy
#apos, instale o cv2 de acordo com o comando descrito pois usando ele, que voce consegue usar comandos para reconhecomento facial

import numpy as np #pip install numpy
import cv2 #pip install opencv-contrib-python
import os 

def captura(largura, altura):
    #Classificadores
    classificador      = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  #pega os arquivos importados anteriormente no projeto
    classificador_olho = cv2.CascadeClassifier('haarcascade_eye.xml')     #pega os arquivos importados anteriormente no projeto

    #abrir a camera da maquina
    camera = cv2.VideoCapture(0) # 0 = camera principal, comeca no numero 0 e caso tenha mais cameras é so trocar o numero dentro para qual camera voce quer usar

    #Amostras da imagem do usuario
    #cada usuario tera uma amostra, uma base de dados de imagem do usuario, 
    amostra   = 1
    #precisa informar quantar imagem precisa, geralmente sao 25 amostras, ele aprende (treina) a diferenciar uma pessoa da outra
    n_amostas = 25

    #Recebe o ID do usuario
    id = input('Digite o ID do usuário: ')

    #Mensagem indicando captura de imagens 
    print('Capturando as imagens...')

    #loop 
    while True:
        conectado, imagem = camera.read()
        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        print(np.average(imagem_cinza))
        faces_detectadas = classificador.detectMultiScale(imagem_cinza, scaleFactor=1.5, minSize=(150,150))

        #identificar geometria das faces
        for (x, y, l, a) in faces_detectadas:
            cv2.rectangle(imagem, (x, y), (x + 1, y + a), (0, 0, 255), 2)
            regiao = imagem[y:y + a, x:x + l]
            regiao_cinza_olho = cv2.cvtColor(regiao, cv2.COLOR_BGR2GRAY)
            olhos_detectados = classificador_olho.detectMultiScale(regiao_cinza_olho)

        #identificar geometria dos codigos (4 pontos cardiais, leste, sul, norte, oeste)
            for (ox, oy, ol, oa) in olhos_detectados:
                cv2.rectangle(regiao, (ox, oy), (ox + ol, oy + oa), (0, 255, 0), 2)

                 # salva as imagens em um arquivo do sistema ao apertar a letra c
            if np.average(imagem_cinza) > 110 and amostra <= n_amostas:    
                imagem_face = cv2.resize(imagem_cinza[y:y + a, x:x + l], (largura, altura))
                cv2.imwrite(f'fotos/pessoa.{str(id)}.{str(amostra)}.jpg', imagem_face)
                print(f'[foto] {str(amostra)} capturada com seucesso.')
                amostra += 1
        
        cv2.imshow('Detectar faces', imagem)
        cv2.waitKey(1)

        #encerra o loop caso o numero de fotos do usuario tenha chegado a 25
        if (amostra >= n_amostas + 1):
            print('Faces capturadas com sucesso.')
            break
        elif cv2.waitKey(1) == ord('q'):
            print('Câmera encerrada.')
            break

    #encerra a captura 
    camera.release()
    cv2.destroyAllWindows() #fim da funcao
    
#programa principal
if __name__ == '__main__':
    #definir o tamanho da camera
    largura = 220
    altura  = 220

    while True:
    #menu
        print('0 - Sair do programa')
        print('1 - Captura imagem')

        opcao = input('Informe opção desejada: ')

        match opcao:
            case '0':
                print('Programa encerrado.')
                break

            case '1':
                captura(largura, altura)
                continue
            

                

