BASE_URL = 'https://iss.moex.com/iss/engines/stock/markets/bonds/boards'

CORP_BONDS_URL = f'{BASE_URL}/TQCB/securities.xml'
GOV_BONDS_URL = f'{BASE_URL}/TQOB/securities.xml'


PARSING_URLS = {
    CORP_BONDS_URL: 'MOEX. Корпоративные облигации',
    GOV_BONDS_URL: 'MOEX. Государственные облигации',
}
