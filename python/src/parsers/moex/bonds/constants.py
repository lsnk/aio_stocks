from parsers.moex.constants import MOEX_API_BASE_URL


CORP_BONDS_URL = f'{MOEX_API_BASE_URL}/bonds/boards/TQCB/securities.xml'
GOV_BONDS_URL = f'{MOEX_API_BASE_URL}/bonds/boards/TQOB/securities.xml'
EUR_BONDS_URL = f'{MOEX_API_BASE_URL}/bonds/boards/TQOD/securities.xml'


PARSING_URLS = {
    CORP_BONDS_URL: 'MOEX. Корпоративные облигации',
    GOV_BONDS_URL: 'MOEX. Государственные облигации',
    EUR_BONDS_URL: 'MOEX. Еврооблигации',
}
