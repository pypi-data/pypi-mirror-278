import requests, json, os, traceback
from datetime import datetime, timezone, date
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class AutomaxiaApi:

    def __init__(self, url =''):
        self.url = 'http://plataforma-api.automaxia.com.br'
        if url != '':
            self.url = url
        self.headers = {'Authorization': 'Bearer ','Content-Type': 'application/json'}

    def convert_bytes(self,num):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0

    def file_size(self,file_path):
        if os.path.isfile(file_path):
            file_info = os.stat(file_path)
            return self.convert_bytes(file_info.st_size)

    def gera_token_acesso(self, constante_virtual):
        try:
            self.config = self.get_automacao_by_constante_virtual_json(constante_virtual)
            
            if 'detail' in self.config:
                return self.config['detail']

            self.nome_worker = self.config['tx_nome']
            self.config['tx_json'] = self.config['tx_json'].replace("'",'"')
            self.config = json.loads(self.config['tx_json'])
            self.set_config(tokenacesso='', url=self.config['url'])
            retorno = self.login(_user=self.config['username'], _pass=self.config['password'], client_id='worker')
            
            if 'detail' in retorno:
                return retorno['detail']
            else:
                self.tokenacesso = retorno['access_token']                
                self.set_config(tokenacesso=self.tokenacesso, url=self.config['url'])
                return [self.tokenacesso, self.config['url']]
        except Exception as error:
            return self.trata_error_traceback(traceback.format_exc())

    def set_config(self, tokenacesso='', url = ''):
        if url != '':
            self.url = url

        self.headers = {'Authorization': 'Bearer ' + tokenacesso,'Content-Type': 'application/json'}

    def login(self, _user='', _pass='', client_id='worker'):
        try:
            if _user is None or _pass is None:
                return None
            
            headers = {}

            url = str(self.url)+"/login"
            payload = {"username": f"{_user}", "password": f"{_pass}", "client_id":f"{client_id}"}

            self.headers = {'Content-Type': 'application/json'}
            self.headersFiles = {'Content-Type': 'application/octet-stream'}

            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            response = response.json()
            if 'access_token' in response:
                self.tokenacesso = response['access_token']
                self.headers = {'Authorization': 'Bearer ' + self.tokenacesso,'Content-Type': 'application/json'}
                self.headersFiles = {'Authorization': 'Bearer ' + self.tokenacesso,'Content-Type': 'application/octet-stream'}
            else:
                self.tokenacesso = response['detail']
            return response
        except Exception as error:
            return self.trata_error_traceback(traceback.format_exc())

    def pega_dados_configuracao(self, config = '/config_ex.json'):
        try:
            dir_json = os.getcwd() + config
            with open(dir_json, 'r', encoding='utf_8_sig') as f:
                arq_json = json.load(f)
            return arq_json
        except Exception as error:
            return self.trata_error_traceback(traceback.format_exc())

    def ler_arquivo(self, arquivo):
        dados = []
        if os.path.isfile(arquivo):
            with open(arquivo, 'r', encoding='utf_8_sig') as f:
                try:
                    dados = json.load(f)
                except:
                    dados = []
        return dados

    def grava_logs_local(self, conteudo):
        try:
            arquivo = "logs_" + str(date.today()).replace('-','')+'.txt'
            dir_logs = os.getcwd() + "/arquivos/logs/"+arquivo

            os.makedirs(os.getcwd() + "/arquivos/logs", exist_ok=True)

            with open(dir_logs, "a", encoding='utf_8_sig') as outfile:
                outfile.write(conteudo+chr(13))
            return True
        except Exception as error:
            print(error)

    def grava_arquivo_logs(self, json_error, arquivo = ''):
        if arquivo == '':
            arquivo = "logError_" + str(date.today()).replace('-','')+'.json'
        dir_logs = os.getcwd() + "/arquivos/logs/"+arquivo

        os.makedirs(os.getcwd() + "/arquivos/logs", exist_ok=True)

        #print(dir_logs)
        dados_json = self.ler_arquivo(dir_logs)
        
        conteudo = []
        if dados_json != '':
            dados_json.append(json_error)
            conteudo = dados_json
        else:
            conteudo.append(json_error)

        conteudo = str(conteudo).replace('"', '\\"')
        conteudo = str(conteudo).replace("'", '"')
        conteudo = str(conteudo).replace(': "None"', ': null')
        conteudo = str(conteudo).replace(": None", ': null')
        
        with open(dir_logs, "w", encoding='utf_8_sig') as outfile:
            outfile.write(str(conteudo))

    def trata_error_traceback(self, traceback):
        error = traceback.split('Traceback')[-1]
        self.grava_arquivo_logs(f"""{error}""")
        return error

    def start_tarefa(self,payload):
        try:        
            url = str(self.url)+"/tarefa/start/"

            payload = json.dumps(payload)

            response = self.post(url, payload)
            return response
        except Exception as erro:
            return self.trata_error_traceback(traceback.format_exc())

    def stop_automacao(self, tarefa_id, bo_status_code = 200, tx_resumo = 'ExecuÃ§Ã£o finalizada pela automaÃ§Ã£o'):
        try:        
            url = str(self.url)+"/tarefa/stop/"

            payload = {
                "tarefa_id": tarefa_id,
                "dt_fim": str(datetime.now(timezone.utc)),
                "bo_status_code": bo_status_code,
                "tx_resumo": tx_resumo
            }
            payload = json.dumps(payload)

            if tarefa_id:
                response = self.put(url, payload)
                return response
            return {'detail':False}
        except Exception as erro:
            return self.trata_error_traceback(traceback.format_exc())
        
    def historico_tarefa_txjson(self,payload):
        try:        
            url = str(self.url)+"/tarefa/historico-tarefa/tx-json"

            payload = json.dumps(payload)

            response = self.post(url, payload)
            return response
        except Exception as erro:
            return self.trata_error_traceback(traceback.format_exc())

    def get_start_automacao(self, automacao_id):
        url = str(self.url)+"/tarefa/automacao/"+str(automacao_id)
        response = self.get(url)
        return response

    def get_usuario_by_worker(self, tx_ip_mac, nu_cpf):
        url = str(self.url)+"/automacao/worker/"+str(nu_cpf)+'/'+str(tx_ip_mac)
        response = self.get(url)
        return response

    def get_download_script(self, tarefa_id):
        url = str(self.url)+"/downloadScripts/"+str(tarefa_id)
        response = self.getFiles(url)
        return response

    def get_tarefa_by_automacao(self, automacao_id, tx_ip_mac):
        url = str(self.url)+"/tarefa/worker/"+str(automacao_id)+"/"+str(tx_ip_mac)
        response = self.get(url)
        return response

    def get_tarefa_by_id(self, tarefa_id):
        url = str(self.url)+"/tarefa/"+str(tarefa_id)
        response = self.get(url)
        return response

    def get_configuracao_by_tarefa(self, tx_nome, tarefa_id):
        url = str(self.url)+f"/configuracao?tx_nome={tx_nome}&tarefa_id={tarefa_id}&bo_status=True"
        response = self.get(url)
        return response
    
    def get_configuracao_by_chave(self, tx_chave, tarefa_id):
        url = str(self.url)+f"/configuracao/{tx_chave}/{tarefa_id}"
        response = self.get(url)
        return response
    
    def get_tarefa_by_constante_virtual(self, constante_virtual):
        url = str(self.url)+"/tarefa/constante_virtual/"+str(constante_virtual)
        response = self.get(url)
        return response

    def get_automacao_by_id(self, automacao_id):
        url = str(self.url)+"/automacao/"+str(automacao_id)
        response = self.get(url)
        return response

    def get_logs_by_id_historico(self, historico_tarefa_id):
        url = str(self.url)+"/logs/historico-tarefa/"+str(historico_tarefa_id)
        response = self.get(url)
        return response
    
    def get_historico_tarefa_by_id(self, historico_tarefa_id):
        url = str(self.url)+"/tarefa/historico-tarefa/"+str(historico_tarefa_id)
        response = self.get(url)
        return response

    def get_automacao_by_id_json(self, automacao_id):
        url = str(self.url)+"/automacao/worker/"+str(automacao_id)
        response = self.get(url)
        return response

    def get_automacao_by_constante_virtual_json(self, constante_virtual):
        url = str(self.url)+"/automacao/worker/constante/"+str(constante_virtual)
        response = self.get(url)
        return response

    def get_cofre_senha_by_cliente(self, tx_nome, setor_id):
        url = str(self.url)+"/cofresenha/"+str(tx_nome)+"/"+str(setor_id)
        response = self.get(url)
        return response

    def gravar_logs(self, historico_tarefa_id, tx_descricao, status='success', json_dados=''):
        url = str(self.url)+"/logs/"

        payload = {
            "historico_tarefa_id": historico_tarefa_id,
            "tx_status": f"{status}",
            "tx_descricao": f"""{str(tx_descricao)}""",
            "tx_json": f"""{str(json_dados)}"""
        }
        if historico_tarefa_id:
            payload = json.dumps(payload)
            response = self.post(url, payload)
            return response
        return False

    def gravar_log_execucao(self, payload):
        url = str(self.url)+"/logs/"
        
        payload = json.dumps(payload)

        response = self.post(url, payload)
        return response

    def gravar_download_worker(self, payload):
        url = str(self.url)+"/worker/"
        payload = json.dumps(payload)
        response = self.post(url, payload)
        return response
    
    def gravar_elasticsearch(self, payload):
        url = str(self.url)+"/logs/elasticsearch/"
        payload = json.dumps(payload)
        response = self.post(url, payload)
        return response

    def grava_historico_tarefa(self, payload):
        url = str(self.url)+"/historico-tarefa/"
        payload = json.dumps(payload)
        response = self.post(url, payload)
        return response

    def gravar_dados_negocial(self, payload):
        url = str(self.url)+"/dadosnegocial/"

        payload = json.dumps(payload)
        
        response = self.post(url, payload)
        return response

    def get_controle_execucao_tarefa(self, tarefa_id):
        url = str(self.url)+"/controleexecucao/"+str(tarefa_id)
        response = self.get(url)
        return response
    
    def get_controle_execucao_chave(self, tarefa_id, tx_chave):
        url = str(self.url)+"/controleexecucao/chave/"+str(tarefa_id)+"/"+str(tx_chave)
        response = self.get(url)
        return response
    
    def get_controle_execucao_situacao(self, tarefa_id, tx_situacao):
        url = str(self.url)+"/controleexecucao/situacao/"+str(tarefa_id)+"/"+str(tx_situacao)
        response = self.get(url)
        return response

    def gravar_controle_execucao(self, payload):
        url = str(self.url)+"/controleexecucao/"

        payload = json.dumps(payload)
        
        response = self.post(url, payload)
        return response

    def atualiza_controle_execucao(self, payload):
        url = str(self.url)+"/controleexecucao/"

        payload = json.dumps(payload)
        
        response = self.put(url, payload)
        return response

    def atualiza_situacao_tarefa(self, payload):
        url = str(self.url)+"/tarefa/situacao/"

        payload = json.dumps(payload)
        
        response = self.put(url, payload)
        return response

    def atualizar_dados_negocial(self, payload):
        url = str(self.url)+"/dadosnegocial/"

        payload = json.dumps(payload)

        response = self.put(url, payload)
        return response

    def atualizar_data_script(self, script_id, dt_download = ''):
        url = str(self.url)+"/script/dt_download?script_id="+str(script_id)+"&dt_download="+str(dt_download)
        response = self.put(url, [])
        return response

    def atualiza_worker(self, payload):
        url = str(self.url)+"/worker/arquitetura/"
        
        payload = json.dumps(payload)

        response = self.put(url, payload)
        return response

    def get(self, url):
        try:
            response = requests.request("GET", url, headers=self.headers, data="", verify=False)
            if response.status_code in [200, 201]:
                return response.json()
            return {'detail':False, 'status_code': response.status_code}
        except Exception as error:
            return self.trata_error_traceback(traceback.format_exc())

    def getFiles(self, url):
        try:
            response = requests.request("GET", url, headers=self.headersFiles, stream=True, verify=False)
            return response
        except Exception as error:
            return self.trata_error_traceback(traceback.format_exc())

    def put(self, url, payload):
        try:
            response = requests.request("PUT", url, headers=self.headers, data=payload, verify=False)
            if response.status_code in [200, 201]:
                return response.json()
            return {'detail':False, 'status_code': response.status_code}
        except Exception as error:
            return self.trata_error_traceback(traceback.format_exc())

    def post(self, url, payload):
        try:
            response = requests.request("POST", url, headers=self.headers, data=payload, verify=False)
            if response.status_code in [200, 201]:
                if( 'detail' not in response.json() and response.json() is not None and 'Traceback' not in response.json()):
                    if 'id' in response.json():
                        response = {'message': 'Registro inserido com sucesso!', 'id': response.json()['id']}
                    else:
                        response = {'message': 'Registro inserido com sucesso!'}
                else:
                    response = response.json()
                return response
            return {'detail':False, 'status_code': response.status_code}
        except Exception as error:
            return self.trata_error_traceback(traceback.format_exc())