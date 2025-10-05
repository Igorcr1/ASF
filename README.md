<h1><center>Trabalho de Análise de Sistemas Físicos</center></h1>
<img width="516" height="516" alt="image" src="https://github.com/user-attachments/assets/a12cc34d-bbe9-49f3-97b5-8743af5dc816" />
<hr></hr>
<h2>Ideia Geral:</h2>
<br>Utilizar-se do Numpy com matplotlib e control para plotar gráficos e fazer o trabalho relacionado a Control Systems Engineering.
<br>Serão utilizados 4 bibliotecas de ínicio: <b>Numpy</b>, <b>Matplotlib</b>,<b>Control</b> e <b>Sympy</b>.
<br> A utilização do Anaconda pode tornar o projeto mais fácil, mas vai depender do usuário. Quem for testar, pode simplesmente criar um ambiente isolado com venv ou usar as bibliotecas como serão dispostos aqui, utilize como achar melhor. (((Recomendável o uso do terminal, pois irá salvar na mesma pasta os resultados e gráficos)))
<h3>Instação no Windows: </h3>
<ul>
<li>Baixar o Anaconda no site: https://www.anaconda.com/download</li>
<li>No terminal do Windows com conda adicionar instalar: conda install -c conda-forge control</li>
<li>Como o Anaconda já é interativo, basta jogar os códigos aqui presente.</li>
</ul>
<br>
<h3>Instalação no Linux(Base Arch Linux):</h3>
<br>Aqui há a possibilidade de você usar um ambiente isolado venv para baixar as bibliotecas ou simplesmente baixar o anaconda também e usar o comando acima para baixar o control.
<br>Digamos que você quer ser <b>Hardcore</b> igual Jorge, então essa é a escolha perfeita para você.
<img width="505" height="379" alt="image" src="https://github.com/user-attachments/assets/ffa92656-db63-4023-8e9d-959d8b0bdf82" />
<ol>
<li>Primeiramente você vai setar alguma pasta para fazer isso, digamos que seja uma pasta que vc vai criar com mkdir no diretório ~ (ou seja, a pasta pessoal): mkdir Projeto</li>
<li>Entre na pasta Projeto com o cd:  cd Projeto</li>
<li>Agora você pode escolher: Instalar o ambiente isolado ou instalar tudo</li>
<li>Ambiente isolado: python -m venv . (ESSE PONTO NO FINAL VAI INSTALAR O AMBIENTE ISOLADO NO DIRETORIO ATUAL, no caso, projeto)</li>
<li>Ative o ambiente isolado: source bin/activate</li>
<li>Pronto agora você vai ver (Projeto) antes do terminal indicando que o ambiente isolado está habilitado.</li>
<li>Ultima parte: use o pip para instalar as dependências</li>
</ol>

```
pip install numpy
pip install matplotlib
pip install control
pip install sympy
```


<hr>
<h2>Exercício 2 - Sistema elétrico passivo</h2>
<img width="635" height="418" alt="image" src="https://github.com/user-attachments/assets/aea34ea8-b0dd-46aa-8ef1-a40cbc44b5aa" />
<br> Lei dos nós é a possibilidade para encontrar as tensões nodais, onde Vc(t) = Vo(t) e que Va(t) = Vi(t). 
<img width="635" height="418" alt="image" src="https://github.com/user-attachments/assets/b2d30641-8d08-4eb8-a825-739981f81e5d" />
<br> Para equacionar no sympy, os termos isolados serão ajustados juntos.
<br><b>Utilize os códigos na pasta de Exercício.</b>


