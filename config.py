# Configuration for the crypto key scanning script

TARGET_CRYPTO = "DOGE"  # Options: DOGE, LTC, BTC

DATABASE_DIR = {
    "DOGE": "Database/doge/",
    "LTC":  "Database/ltc/",
    "BTC":  "Database/btc/",
}

CRYPTO_PARAMS = {
    "DOGE": {
        "address_prefix": "1E",
        "wif_prefix": "9E",
    },
    "LTC": {
        "address_prefix": "30",
        "wif_prefix": "B0",
    },
    "BTC": {
        "address_prefix": "00",
        "wif_prefix": "80",
    }
}
