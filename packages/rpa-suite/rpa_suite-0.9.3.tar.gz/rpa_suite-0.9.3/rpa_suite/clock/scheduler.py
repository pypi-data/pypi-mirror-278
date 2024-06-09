import schedule
import time
import subprocess

def run_python_script(script_path):
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script {script_path}: {e}")

def batch1():
    # Substitua 'script1.py' pelo caminho do primeiro script Python que deseja executar
    run_python_script('script1.py')

def batch2():
    # Substitua 'script2.py' pelo caminho do segundo script Python que deseja executar
    run_python_script('script2.py')

def batch3():
    # Substitua 'script3.py' pelo caminho do terceiro script Python que deseja executar
    run_python_script('script3.py')

print("Aguardando nova execução...")

# Horário para executar o primeiro batch (substitua com o horário desejado)
schedule.every().day.at("08:00").do(batch1)

# Horário para executar o segundo batch (substitua com o horário desejado)
schedule.every().day.at("12:00").do(batch2)

# Horário para executar o terceiro batch (substitua com o horário desejado)
schedule.every().day.at("16:00").do(batch3)

while True:
    schedule.run_pending()
    time.sleep(1)