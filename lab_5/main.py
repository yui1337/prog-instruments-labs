import argparse
import logging
import os.path

from crypto.hybrid import Hybrid
from logger_config import setup_logging
from const import USER_SETTINGS_FILE, ROOT_DIR
from fileshandler import FilesHandler


logger = logging.getLogger(__name__)

def get_arg() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", type=str, help=""
                                                       "Changes mode of script:"
                                                       "generate - generates keys"
                                                       "encrypt - encrypts ur txt"
                                                       "decrypt - decrypts ur txt")
    arguments = parser.parse_args()
    return arguments.mode

def main() -> int:
    setup_logging()

    logger.info("Программа запущена.")
    try:
        mode = get_arg()
        logger.info(f"Выбранный режим работы программы: {mode}")

        settings = FilesHandler.get_json(USER_SETTINGS_FILE)

        logger.info(f"Загружены настройки из файла {USER_SETTINGS_FILE}")

        for name, path in settings.items():
            path = os.path.join(ROOT_DIR, path)
            settings[name] = path

        hybrid = Hybrid()
        match mode:
            case "generate":
                logger.info("Начинается генерация ключей")

                hybrid.generate_keys(settings["public_key"],
                                    settings["private_key"],
                                    settings["symmetric_key"]
                                     )

                logger.info(f"Ключи успешно сгенерированы и сохранены"
                            f" в {settings["public_key"]}, \n"
                            f"{settings["private_key"]}, \n"
                            f"{settings["symmetric_key"]}.")

            case "encrypt":
                logger.info(f"Начинается шифрование текста из файла"
                            f"{settings["plain_text"]} с сохранением"
                            f"в файл {settings["encrypted_text"]}")


                hybrid.encrypt_data(settings["plain_text"],
                                    settings["private_key"],
                                    settings["symmetric_key"],
                                    settings["encrypted_text"]
                                    )

                logger.info("Текст успешно зашифрован и сохранён"
                            " в указанный файл")

            case "decrypt":
                logger.info(f"Начинается дешифрование текста из файла"
                            f"{settings["encrypted_text"]} с сохранением"
                            f"в файл {settings["decrypted_text"]}")

                hybrid.decrypt_data(settings["encrypted_text"],
                                    settings["private_key"],
                                    settings["symmetric_key"],
                                    settings["decrypted_text"]
                                    )

                logger.info("Текст успешно дешифрован в указанный файл")

            case _:
                logger.error(f"Выбран некорректный режим работы: {mode}")
                return 1

        logger.info("Программа выполнена успешно.")
        return 0

    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {e.filename}", exc_info=True)
        return 1

    except KeyError as e:
        logger.error(f"Отсутствует ключ в настройках: {e}", exc_info=True)
        return 1

    except ValueError as e:
        logger.error(f"Некорректное значение: {e}", exc_info=True)
        return 1

    except PermissionError as e:
        logger.error(f"Нет доступа к файлу: {e}", exc_info=True)
        return 1

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit(main())

