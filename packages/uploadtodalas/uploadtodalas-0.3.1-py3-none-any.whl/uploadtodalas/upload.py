import aiohttp
import asyncio
import os

from loguru import logger

class UploadToDalas():
    def __init__(self, api_key=None) -> None:
        
        self.upload_url:str="https://api.uploadgroup.site"
        self.chunk_size:int=5* 1024 * 1024

        self.pannel_url = "https://api.dalas.pw"
        self.api_key:str = api_key
        self.version = '0.3.1'
    async def version_test(self):
        """Служебный метод клиента `UploadToDalas`
        """  
        url = "https://pypi.org/pypi/uploadtodalas/json"
        try:
            async with aiohttp.ClientSession() as session: 
                async with session.get(url) as response:
                    version = (await response.json())['info']['version']
                    if version != self.version:
                        logger.error(f"Вы используете устаревшую версию пакета uploadtodalas {self.version}, актуальная версия {version}")
                        logger.warning(f"Возможны проблемы с совместимостью, пожалуйста обновите пакет используя команду:\nWindows: `pip install --upgrade uploadtodalas`\nLinux: `pip3 install --upgrade uploadtodalas --break-system-packages`")
                        return False
                    logger.success(f"Вы используете актуальную версию пакета uploadtodalas {self.version}")
            return True
        except Exception as e:
            logger.error(f'Ошибка при проверке версии: {e}')
            return True


    async def test_site(self, url):
        """Служебный метод клиента `UploadToDalas`
        """    
        try:
            logger.info(f"Тестируем доступность эндпоинта {url}")
            async with aiohttp.ClientSession() as session:
                    
                    async with session.get(url+"/docs") as response:
                        if response.status !=200:
                            logger.warning(f"Эндпоинт не доступен")
                            logger.error(f"Свяжитесь с поддержкой проекта Dalas , и сообщиете о недоступности эндпоинта, код эндпоинта {response.status}")
                            return False
                        logger.success("Эндпоинт доступен")
                        logger.info(f"Посетите {url+'/docs'}, для прочтения документации.")
                        return True
        except Exception as e:
            logger.warning(f"Проверка эндпоинта не удалась")
            logger.error(f"Свяжитесь с поддержкой проекта Dalas , и сообщиете об ошибке: {e}")
            return False


    async def upload_file_chunk(self,url, chunk, name, chunk_number, total_chunks):
        """Служебный метод клиента `UploadToDalas`
        """        
        try:
            c=0
            status_code = 400
            while c <5:
                data = aiohttp.FormData()
                data.add_field('file', chunk, filename=name, content_type='application/octet-stream')
                data.add_field('name', name)
                data.add_field('chunk', str(chunk_number))
                data.add_field('chunks', str(total_chunks))

                async with aiohttp.ClientSession() as session:
                        async with session.post(url, data=data) as response:
                            status_code=response.status
                            if status_code ==200:
                                logger.info(f"Chunk: {chunk_number+1}/{total_chunks} successfully sent, file: {name}")
                                return await response.json()
                await asyncio.sleep(1)
                c+=1
                logger.warning(f"upload attempts {c}/5")

            logger.error(f"Cant send chunk, check internet connection and contact support of project DALAS")
        except Exception as e:
            logger.error(f"Error while uploading chunk: {chunk_number}/{total_chunks}, file: {name}\n{e}")
        
    
    async def AsyncUploadToDalas(self, file_path:str, seller_id:int, shedul_in_hours:int=0):
        """
        Асинхронно загружает файл в Dalas.

        :`file_path`: Путь к файлу для загрузки.
        :`seller_id`: Идентификатор продавца.(можно узнать в боте 🌐 Мой профиль-->Ваш ID: 1111)
        :`shedul_in_hours`: Время задержки в часах перед проверкой, полезно для того чтобы загрузить файлы без отлеги сейчас а их проверка прошла после завершения отлеги (по умолчанию 0).
        """
        try:
            if not await self.test_site(url=self.upload_url):
                return
            if not await self.version_test():
                return
            if not os.path.exists(file_path):
                logger.error(f"Файл {file_path} не найден, проверьте указанный путь.")
                return

            file_size = os.path.getsize(file_path)
            total_chunks = (file_size // self.chunk_size) + (1 if file_size % self.chunk_size else 0)
            chunk_number = 0
            logger.success(f"Начинаем загрузку файла {os.path.basename(file_path)}")
            logger.info(f"Файл разделен на {total_chunks if total_chunks!=0 else 1} чанков, размер чанка {self.chunk_size/(1024 * 1024)} MB.")
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(self.chunk_size)
                    if not chunk:
                        break

                    url = f"{self.upload_url}/upload/{seller_id}_None/{shedul_in_hours}"
                    response = await self.upload_file_chunk(url, chunk, os.path.basename(file_path), chunk_number, total_chunks)
                    chunk_number += 1
                    # logger.info(response) 

                    if chunk_number == total_chunks:
                        # logger.success(f"File: {file_path} successfully sent")
                        logger.success(f"Файл: {file_path} успешно отправлен. ")
                        break

        except Exception as e:
            logger.error(f"Error while uploading file: {file_path}\n{e}")

    def SyncUploadToDalas(self, file_path: str, seller_id: int, shedul_in_hours: int = 0):
        """
        Синхронно загружает файл в Dalas, вызывая асинхронный метод AsyncUploadToDalas.

        :`file_path`: Путь к файлу для загрузки.
        :`seller_id`: Идентификатор продавца.(можно узнать в боте 🌐 Мой профиль-->Ваш ID: 1111)
        :`shedul_in_hours`: Время задержки в часах перед проверкой, полезно для того чтобы загрузить файлы без отлеги сейчас а их проверка прошла после завершения отлеги (по умолчанию 0).
        """
        try:
            asyncio.run(self.AsyncUploadToDalas(file_path=file_path, seller_id=seller_id, shedul_in_hours=shedul_in_hours))
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def PannelAsyncGetId(self, telegram_id:int=0, seller_id:int=0)->int:
        """
        Возвращает `int`: Seller id пользователя, `False` :bool - при ошибке, `None` - если пользователя с указанным ид не существует.

        Метод для панелей, для проверки необходим апи ключ, если у вас нет апи ключа используйте `AsyncUploadToDalas` или `SyncUploadToDalas`.

        Настоятельно рекомендуем валидировать ввод от пользователя(если таковой имеется), используя данную функцию.

        Вы также можете узнать есть ли у нас пользователь, передав его телеграм ид, что весьма удобно.
        
        Асинхронно проверяет\получает id пользователя в Dalas.

        Можно передать или seller_id(ид в боте) или telegram_id(ид в телеграм)

        :`telegram_id`: int  ид в телеграм.
        :`seller_id`: int ид в боте(необходим для загрузки).
        """
        try:
            if telegram_id >0 and seller_id >0:
                logger.error(f"Можно передать или seller_id(ид в боте) или telegram_id(ид в телеграм)")
                return False
            if telegram_id ==0 and seller_id ==0:
                logger.error(f"Нужно передать или seller_id(ид в боте) или telegram_id(ид в телеграм)")
                return False
            async with aiohttp.ClientSession() as session:
                    
                    async with session.post(self.pannel_url+f"/check_id/{self.api_key}/{telegram_id}/{seller_id}") as response:
                        if response.status ==400: 
                            logger.error(f"Неверный апи ключ\nЕсли вам нужна помощь, свяжитесь с поддержкой проекта Dalas.")
                            return False
                        if response.status == 404:
                            logger.error(f"Пользователь с {'telegram'if telegram_id>0 else 'seller'}_id равным {telegram_id if telegram_id>0 else seller_id} не найден.")
                            return None      
                        if response.status ==500: 
                            logger.error(f"Ошибка сервера. Свяжитесь с поддержкой проекта Dalas.")
                            return False        
                        if response.status == 200:
                            id_in_bot = int(await response.text())
                            # logger.debug(id_in_bot)
                            return id_in_bot

                        logger.error(f"Непредусмотренная ошибка. Свяжитесь с поддержкой проекта Dalas , и сообщиете о недоступности эндпоинта, код эндпоинта {response.status}, {await response.text()}")   
                        return False                     
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    async def PannelAsyncUpload(self, file_path:str, seller_id:int, shedul_in_hours:int=0, strict=True):
        """
        Метод для панелей, для загрузки необходим апи ключ, если у вас нет апи ключа используйте `AsyncUploadToDalas` или `SyncUploadToDalas`.
        
        Асинхронно загружает файл в Dalas.

        :`file_path`: Путь к файлу для загрузки.
        :`seller_id`: Идентификатор продавца.(можно узнать через `PannelAsyncGetId`)
        :`shedul_in_hours`: Время задержки в часах перед проверкой, полезно для того чтобы загрузить файлы без отлеги сейчас а их проверка прошла после завершения отлеги (по умолчанию 0).
        :`strict`: Валидация seller_id, проверка версий
        """  
        try:
            if not await self.test_site(url=self.pannel_url):
                return
            if self.api_key is None:
                logger.error("Необходимо предоставить апи ключ, при инициализации клиента\nесли у вас нет апи ключа используйте `AsyncUploadToDalas` или `SyncUploadToDalas`.")
                return
            if strict:
                logger.info(f"Валидация указанного seller_id: {seller_id}")
                if not await self.PannelAsyncGetId(seller_id=seller_id):
                    logger.error("Указанный seller_id не валиден, смотрите лог выше.")
                    return False
                if not await self.version_test():
                    return
            file_size = os.path.getsize(file_path)
            total_chunks = (file_size // self.chunk_size) + (1 if file_size % self.chunk_size else 0)
            chunk_number = 0
            logger.success(f"Начинаем загрузку файла {os.path.basename(file_path)}")
            logger.info(f"Файл разделен на {total_chunks if total_chunks!=0 else 1} чанков, размер чанка {self.chunk_size/(1024 * 1024)} MB.")
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(self.chunk_size)
                    if not chunk:
                        break
             

                    url = f"{self.pannel_url}/upload/{self.api_key}/{seller_id}/none/{shedul_in_hours}"
                    response = await self.upload_file_chunk(url, chunk, os.path.basename(file_path), chunk_number, total_chunks)
                    chunk_number += 1
                    

                    if chunk_number == total_chunks:
                        # logger.success(f"File: {file_path} successfully sent")
                        logger.info(response) 
                        logger.success(f"Файл: {file_path} успешно отправлен. ")
                        break

        except Exception as e:
            logger.error(f"Error while uploading file: {file_path}\n{e}")
    
