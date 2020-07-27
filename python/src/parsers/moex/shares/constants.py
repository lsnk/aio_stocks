from ..constants import MOEX_API_BASE_URL


SHARES_AND_DR_URL = f'{MOEX_API_BASE_URL}/shares/boards/TQBR/securities.xml'
ETFS_URL = f'{MOEX_API_BASE_URL}/shares/boards/TQTF/securities.xml'


PARSING_URLS = {
    SHARES_AND_DR_URL: 'MOEX. Акции и ДР',
    ETFS_URL: 'MOEX. ETF',
}
