import os # para mexer com arquivos (excluir os audios)
from gtts import gTTS
import pygame # tocar audios
import datetime
import io # trabalhar com imagens
from flask import Flask, flash, render_template, request, redirect, send_file, url_for, session, abort # interações com bd
import psycopg2 # interações com bd
from functools import wraps

app = Flask(__name__)
app.secret_key = 'chave_secreta'

DB_HOST = 'localhost'
DB_NAME = 'DbOmni+'
DB_USER = 'postgres'
DB_PASSWORD = 'pg482'

# conectar com bd
def connect_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# func que faz o controle de usuarios em determinadas abas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'tipo_usuario' not in session or session['tipo_usuario'] not in ['admin', 'funcionario']:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

# rota index
@app.route('/')
def index():
    return redirect(url_for('cadastro'))

# cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        tipo_usuario = request.form['tipo_usuario']

        # insert d novo user
        conn = connect_db()
        if conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)",
                    (nome, email, senha, tipo_usuario)
                )
                conn.commit()
            conn.close()
            return redirect(url_for('login'))
    return render_template('cadastro.html')

# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        # verifica o banco
        conn = connect_db()
        if conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, tipo_usuario FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
                user = cur.fetchone()
                if user:
                    # inicia sessão e salva id nela
                    session['usuario_id'] = user[0]
                    # mesma coisa que em cima mas com o tipo de user
                    session['tipo_usuario'] = user[1]  
                    return redirect(url_for('home'))
                else:
                    return "Credenciais inválidas", 401
            conn.close()
    return render_template('login.html')

# home
@app.route('/home')
def home():
    return render_template('home.html')

# logout
@app.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('login')) 

# chat completo com setores sendo adicionados manualmente pelo user
@app.route('/chat')
@login_required
def chat():
    conn = connect_db()
    problemas = []
    setores = [] # guardando os setores em lista
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, titulo, descricao, data_reportado FROM problemas WHERE resolvido = FALSE")
            problemas = cur.fetchall()
            
            # busca os setores
            cur.execute("SELECT id, nome FROM setores")
            setores = cur.fetchall()
        conn.close()
    return render_template('chat.html', problemas=problemas, setores=setores)

# relatar problema
@app.route('/relatar-problema', methods=['GET', 'POST'])
def relatar_problema():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        imagem = request.files['imagem']

        # validando campos obgrigatorios
        if not titulo or not descricao or not imagem:
            return "Todos os campos são obrigatórios!", 400
        
        # salvando imagem no bd
        if imagem:
            imagem_byte = imagem.read()

            # inserir problema
            conn = connect_db()
            if conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO problemas (titulo, descricao, imagem, usuario_id, data_reportado) VALUES (%s, %s, %s, %s, %s)",
                        (titulo, descricao, imagem_byte, session['usuario_id'], datetime.datetime.now())
                    )
                    conn.commit()
                conn.close()
                return redirect(url_for('home'))
    return render_template('relatar_problema.html')

# obter a imagem
@app.route('/problema/<int:problema_id>/imagem')
def get_image(problema_id):
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT imagem FROM problemas WHERE id = %s", (problema_id,))
            img_data = cur.fetchone()
            if img_data and img_data[0]:
                return send_file(io.BytesIO(img_data[0]), mimetype='image/png')
    return "Imagem não encontrada", 404

# resolver problema
@app.route('/resolver_problemas', methods=['POST'])
@login_required
def resolver_problemas():
    problema_ids = request.form.getlist('problemas_resolvidos') 
    if not problema_ids:
        flash('Nenhum problema selecionado para resolver.', 'warning')  
        return redirect(url_for('chat'))
    
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            for problema_id in problema_ids:
                cur.execute("UPDATE problemas SET resolvido = TRUE WHERE id = %s", (problema_id,))
            conn.commit()  
        conn.close()  
    flash('Problemas resolvidos atualizados com sucesso!', 'success')
    return redirect(url_for('chat'))  

# func que gera o audio e toca ele
def tocar_audio_setor(setor, mensagem):
    nome_arquivo = f"audio_{setor}.mp3"
    try:
        # gera o audio
        tts = gTTS(mensagem, lang='pt-br')
        tts.save(nome_arquivo)
        
        # inicia o pygame para tocar audio
        pygame.mixer.init()
        pygame.mixer.music.load(nome_arquivo)
        pygame.mixer.music.play()

        # espera acabar o audio
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # finaliza o mixer dps q acaba o audio
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        
    except Exception as e:
        print(f"Erro ao tocar o áudio do setor {setor}: {e}")
    
    finally:
        # remove arquivo de audio dps que ele é usado
        if os.path.exists(nome_arquivo):
            try:
                os.remove(nome_arquivo)
                print(f"Arquivo {nome_arquivo} deletado com sucesso.")
            except Exception as e:
                print(f"Erro ao deletar o arquivo {nome_arquivo}: {e}")
        

# verificar problemas - tocar audios
@app.route('/verificar_problemas', methods=['POST'])
def verificar_problemas():
    problema_ids = request.form.getlist('problemas_verificados')
    conn = connect_db()

    if conn:
        with conn.cursor() as cur:
            for problema_id in problema_ids:
                # pega setor selecionado
                setor_id = request.form.get(f'setor_{problema_id}')

                # seta como o setor selecionado
                cur.execute("SELECT nome FROM setores WHERE id = %s", (setor_id,))
                setor = cur.fetchone()[0]

                # atuliza o problema no BD
                cur.execute("""
                    UPDATE problemas 
                    SET visualizado = TRUE, setor_id = %s 
                    WHERE id = %s
                """, (setor_id, problema_id))

                # toca o que for selecionado no setor
                tocar_audio_setor(setor, f"Problema verificado: {setor}")
            
            conn.commit()
        conn.close()

    return redirect(url_for('chat'))

# buscar problemas pelo nome / titulo
@app.route('/buscar_problemas', methods=['POST'])
@login_required
def buscar_problemas():
    titulo_busca = request.form.get('busca_problema', '').strip()  # remove espaços extras
    conn = connect_db()
    problemas = []
    
    if conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, titulo, descricao, data_reportado 
                FROM problemas 
                WHERE titulo ILIKE %s
            """, (f'%{titulo_busca}%',))  # busca mais flexível com curingas
            problemas = cur.fetchall()
        conn.close()
    
    return render_template('chat.html', problemas=problemas)

# add setores / selects para os audios
@app.route('/adicionar_setor', methods=['POST'])
@login_required
def adicionar_setor():
    novo_setor = request.form['novo_setor']
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO setores (nome) VALUES (%s)", (novo_setor,))
            conn.commit()
        conn.close()

    return redirect(url_for('chat'))

# excluir um setor
@app.route('/excluir_setor/<int:setor_id>', methods=['POST'])
@login_required
def excluir_setor(setor_id):
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            # deleta o setor com base no id fornecido
            cur.execute("DELETE FROM setores WHERE id = %s", (setor_id,))
            conn.commit()
        conn.close()
        flash('Setor excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir o setor.', 'danger')
    
    return redirect(url_for('chat'))

if __name__ == '__main__':
    app.run(debug=True)
