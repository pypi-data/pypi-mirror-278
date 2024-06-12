import json
import requests
from aiohttp import ClientSession


class RadiometerAPI:
    def __init__(self, server_address: str, token: str, verify_ssl: bool, session: ClientSession = None):
        if not server_address.endswith('/'):
            server_address += '/'
        self.__server_address = server_address
        self.__token = token
        self.__verify_ssl = verify_ssl
        self.__session = session
        self.__headers = {"Authorization": f'Bearer {self.__token}'}

        self.__devices_path = 'devices'
        self.__patients_path = 'patients'
        self.__measurements_path = 'measurements'
        self.__measurements_with_data_path = 'measurements-with-data'
        self.__measurement_path = 'measurement'
        self.__measurement_with_data_path = 'measurement-with-data'
        self.__calibrations_path = 'calibrations'

    def get_server_address(self) -> str:
        return self.__server_address

    def get_token(self) -> str:
        return self.__token

    def set_server_address(self, server_address: str) -> None:
        if not server_address.endswith('/'):
            server_address += '/'
        self.__server_address = server_address

    def set_token(self, token: str) -> None:
        self.__token = token
        self.__headers = {"Authorization": f'Bearer {self.__token}'}

    def set_session(self, session: ClientSession) -> None:
        self.__session = session

    def set_ssl_verification(self, verify_ssl: bool) -> None:
        self.__verify_ssl = verify_ssl

    def get_devices(self) -> list:
        devices = requests.get(f'{self.__server_address}{self.__devices_path}',
                               headers=self.__headers, verify=self.__verify_ssl)
        return json.loads(devices.content)

    async def get_devices_async(self) -> list:
        if self.__session is None:
            raise AttributeError('Session is None')
        async with self.__session.get(f'{self.__server_address}{self.__devices_path}',
                                      headers=self.__headers, ssl=self.__verify_ssl) as response:
            data = await response.read()
            return json.loads(data)

    def get_patients(self) -> list:
        patients = requests.get(f'{self.__server_address}{self.__patients_path}',
                                headers=self.__headers, verify=self.__verify_ssl)
        return json.loads(patients.content)

    async def get_patients_async(self) -> list:
        if self.__session is None:
            raise AttributeError('Session is None')
        async with self.__session.get(f'{self.__server_address}{self.__patients_path}',
                                      headers=self.__headers, ssl=self.__verify_ssl) as response:
            data = await response.read()
            return json.loads(data)

    def get_measurements(self) -> list:
        measurements = requests.get(f'{self.__server_address}{self.__measurements_path}',
                                    headers=self.__headers, verify=self.__verify_ssl)
        return json.loads(measurements.content)

    async def get_measurements_async(self) -> list:
        if self.__session is None:
            raise AttributeError('Session is None')
        async with self.__session.get(f'{self.__server_address}{self.__measurements_path}',
                                      headers=self.__headers, ssl=self.__verify_ssl) as response:
            data = await response.read()
            return json.loads(data)

    def get_measurements_with_data(self) -> list:
        measurements = requests.get(f'{self.__server_address}{self.__measurements_with_data_path}',
                                    headers=self.__headers, verify=self.__verify_ssl)
        return json.loads(measurements.content)

    async def get_measurements_with_data_async(self) -> list:
        if self.__session is None:
            raise AttributeError('Session is None')
        async with self.__session.get(f'{self.__server_address}{self.__measurements_with_data_path}',
                                      headers=self.__headers, ssl=self.__verify_ssl) as response:
            data = await response.read()
            return json.loads(data)

    def get_measurement(self, measurement_id: int) -> bytes:
        measurement = requests.get(f'{self.__server_address}{self.__measurement_path}/{measurement_id}',
                                   headers=self.__headers, verify=self.__verify_ssl)
        return json.loads(measurement.content)

    async def get_measurement_async(self, measurement_id: int) -> bytes:
        if self.__session is None:
            raise AttributeError('Session is None')
        async with self.__session.get(f'{self.__server_address}{self.__measurement_path}/{measurement_id}',
                                      headers=self.__headers, ssl=self.__verify_ssl) as response:
            data = await response.read()
            return json.loads(data)

    def get_measurement_with_data(self, measurement_id: int) -> bytes:
        measurement = requests.get(f'{self.__server_address}{self.__measurement_with_data_path}/{measurement_id}',
                                   headers=self.__headers, verify=self.__verify_ssl)
        return json.loads(measurement.content)

    async def get_measurement_with_data_async(self, measurement_id: int) -> bytes:
        if self.__session is None:
            raise AttributeError('Session is None')
        async with self.__session.get(f'{self.__server_address}{self.__measurement_with_data_path}/{measurement_id}',
                                      headers=self.__headers, ssl=self.__verify_ssl) as response:
            data = await response.read()
            return json.loads(data)

    def get_calibrations(self) -> list:
        calibrations = requests.get(f'{self.__server_address}{self.__calibrations_path}',
                                    headers=self.__headers, verify=self.__verify_ssl)
        return json.loads(calibrations.content)

    async def get_calibrations_async(self) -> list:
        if self.__session is None:
            raise AttributeError('Session is None')
        async with self.__session.get(f'{self.__server_address}{self.__calibrations_path}',
                                      headers=self.__headers, ssl=self.__verify_ssl) as response:
            data = await response.read()
            return json.loads(data)
