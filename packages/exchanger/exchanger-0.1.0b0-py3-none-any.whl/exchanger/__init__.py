import requests
class CurrencyExchanger:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def get_exchange_rate(self, source_currency: str, targe_currency: str) -> float:
        if not source_currency:
            raise ValueError('Source currency must be provided')
        if not targe_currency:
            raise ValueError('Target currency must be provided')
        url = f'https://v6.exchangerate-api.com/v6/pair/{source_currency}/{targe_currency}'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(url, headers=headers)
        responsebody = response.json()
        return responsebody.get('conversion_rate')
