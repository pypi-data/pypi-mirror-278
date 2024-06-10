default_prompt_intro = """
           Ты - ассистент, отвечающий на вопросы. Давай точные ответы или, если не знаешь ответ, уточни запрос.
            """

# TODO: обернуть это и пути в ConfigProvider и передавать через конструктор
data_folder_path = "./.data"
databases_path = data_folder_path + "/database"
message_history_path = data_folder_path + "/message_history"
chat_files_path = data_folder_path + "/chat_files"
