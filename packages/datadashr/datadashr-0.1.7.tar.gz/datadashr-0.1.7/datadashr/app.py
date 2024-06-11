import panel as pn
import subprocess
import ollama
import webbrowser
import pandas as pd
from datadashr import DataDashr
from datadashr.llm.ollama import OllamaLLM
from datadashr.connectors.pandas import CSVConnector
from datadashr.config import *


# Theme configuration
pn.config.theme = 'default'
pn.extension('echarts')


class App:
    def __init__(self):
        self.allowed_models = ['codestral', 'mixtral']
        self.available_models = []

        self.llm_selector = pn.widgets.Select(name='Select LLM', options=self.available_models, value=None)
        self.cache_switch = pn.widgets.Switch(name='Enable Cache', value=True)
        self.verbose_switch = pn.widgets.Switch(name='Enable Verbose', value=False)
        self.vector_switch = pn.widgets.Switch(name='Enable Vector', value=False)
        self.file_input = pn.widgets.FileInput(name='Upload CSV', accept='.csv')
        self.cache_label = pn.pane.Str('Enable Cache')
        self.verbose_label = pn.pane.Str('Enable Verbose')
        self.vector_label = pn.pane.Str('Enable Vector')
        self.chat_interface = pn.chat.ChatInterface(callback=self.generate_response)

        self.df = None

        self.initialize_app()

    def initialize_app(self):
        if not self.verify_if_ollama_server_is_running() or not self.check_ollama_list():
            logger.error("Ollama server is not available. Please check the installation.")
            exit()

        self.available_models = self.check_accepted_models()
        if not self.available_models:
            logger.error("None of the accepted models are available.")
            exit()

        self.llm_selector.options = self.available_models
        self.llm_selector.value = self.available_models[0] if self.available_models else None

        self.setup_ui()
        self.setup_watchers()

        self.chat_interface.send("Hi! How can I help you?", user="Datadashr",
                                 avatar='https://www.datadashr.com/wp-content/uploads/2024/06/datadashr.png',
                                 respond=False)

    def get_allama_llm_list(self):
        models = ollama.list()
        return [model['name'] for model in models['models']]

    def verify_if_ollama_server_is_running(self):
        try:
            models = ollama.list()
            return True
        except Exception as e:
            logger.error(f"Ollama server is not running: {e}")
            return False

    def check_ollama_list(self):
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=True)
            if result.stdout:
                return True
            logger.error("Ollama server is not running")
            webbrowser.open('https://ollama.com/download')
            return False
        except subprocess.CalledProcessError as e:
            logger.error(f"Error checking ollama list: {e}")
            return False

    def check_accepted_models(self):
        models = self.get_allama_llm_list()
        if not models:
            logger.error("Nessun modello disponibile.")
            return []

        available_models = []
        logger.info(f"Models: {models}")

        normalized_models = {model.split(':')[0]: model for model in models}

        for model in self.allowed_models:
            logger.info(f"Checking model: {model}")
            if model in normalized_models:
                logger.info(f"Modello accettato: {model}")
                available_models.append(normalized_models[model])

        if not available_models:
            logger.error("Nessuno dei modelli accettati è disponibile.")
            return []

        return available_models

    def setup_ui(self):
        self.box_file = pn.WidgetBox('# Choose file', self.file_input, width=350, styles={'margin-bottom': '10px'})
        self.box_llm = pn.WidgetBox('# Choose LLM', self.llm_selector, width=350, styles={'margin-bottom': '10px'})
        self.box_switch = pn.WidgetBox('# Settings', self.cache_label, self.cache_switch, self.verbose_label,
                                       self.verbose_switch, self.vector_label, self.vector_switch, width=350,
                                       styles={'margin-bottom': '10px'})

    def setup_watchers(self):
        self.llm_selector.param.watch(self.update_datadashr, 'value')
        self.cache_switch.param.watch(self.update_datadashr, 'value')
        self.verbose_switch.param.watch(self.update_datadashr, 'value')
        self.vector_switch.param.watch(self.update_datadashr, 'value')
        self.file_input.param.watch(self.update_datadashr, 'value')

    def update_datadashr(self, event=None):
        selected_llm = self.llm_selector.value
        enable_cache = self.cache_switch.value
        enable_verbose = self.verbose_switch.value
        enable_vector = self.vector_switch.value

        if not self.file_input.value:
            logger.error("File CSV non caricato. Carica un file per continuare.")
            self.chat_interface.send("Please upload a CSV file to proceed.", user="Datadashr",
                                     avatar='https://www.datadashr.com/wp-content/uploads/2024/06/datadashr.png',
                                     respond=False)
            return

        file_path = 'uploaded_file.csv'
        with open(file_path, 'wb') as f:
            f.write(self.file_input.value)

        connector = CSVConnector(filepath=file_path)
        self.df = DataDashr(
            data_connector=connector,
            llm_instance=OllamaLLM(model=selected_llm, params={"temperature": 0.0}, verbose=enable_verbose),
            verbose=enable_verbose,
            enable_cache=enable_cache,
            enable_vector=enable_vector,
            format_type='panel'
        )

        try:
            self.df.df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                self.df.df = pd.read_csv(file_path, encoding='latin1')
            except UnicodeDecodeError:
                logger.error("Error decoding the CSV file. Try loading a file with a different encoding.")
                self.chat_interface.send("Error decoding the CSV file. Please upload a file with a different encoding.",
                                         user="Datadashr",
                                         avatar='https://www.datadashr.com/wp-content/uploads/2024/06/datadashr.png',
                                         respond=False)
                return

    def generate_response(self, contents: str, user: str, chat_interface: pn.chat.ChatInterface):
        if not self.df:
            chat_interface.send("Please upload a CSV file to start the analysis.", user="Datadashr",
                                avatar='https://www.datadashr.com/wp-content/uploads/2024/06/datadashr.png',
                                respond=False)
            return

        logger.info(f"Request: {contents}")
        response = self.df.chat(contents)
        chat_interface.send(response, user="Datadashr",
                            avatar='https://www.datadashr.com/wp-content/uploads/2024/06/datadashr.png', respond=False)

    def serve(self):
        settings_panel = pn.Column(
            self.box_file, self.box_llm, self.box_switch,
            styles={"padding": "15px", 'border': '1px solid white'}
        )

        chat_panel = pn.Column(
            self.chat_interface,
            sizing_mode='stretch_width',
            styles={"padding": "15px", 'border': '1px solid white'}
        )

        return pn.Column(
            pn.pane.SVG(
                "https://www.datadashr.com/wp-content/uploads/2024/06/datadashr.svg",
                height=30,
            ),
            pn.Row(settings_panel, chat_panel),
            sizing_mode='stretch_width',
            styles={"padding": "15px", 'border': '1px solid white'},
        )
