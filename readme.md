
# 🔐 Crypto Wallet Scanner

This Python script performs high-speed generation and analysis of cryptocurrency wallet keys and addresses to check for matches against a provided database.

## 📦 Requirements

All required packages are listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
````

Ensure that `requirements.txt` is in the **same folder** as `wallet_scanner.py`.

## ⚙️ Configuration

Edit the `config.py` file to set the following parameters:

```python
TARGET_CRYPTO = "DOGE"  # Options: "DOGE", "LTC", "BTC"

DATABASE_DIR = {
    "DOGE": "Database/doge/",
    "LTC": "Database/ltc/",
    "BTC": "Database/btc/"
}
```

## 🚀 Usage

```bash
python wallet_scanner.py [options]
```

### Options

| Argument        | Description                                                    | Default                |
| --------------- | -------------------------------------------------------------- | ---------------------- |
| `cpu_count`     | Number of CPU cores to use                                     | Number of system cores |
| `substring`     | Minimum length of address to save to output                    | `8`                    |
| `keep_scanning` | Continue scanning even after a match is found (`true`/`false`) | `false`                |

### Example

Run using 4 CPU cores, address substring length of 10, and continue scanning even after a match:

```bash
python wallet_scanner.py cpu_count=4 substring=10 keep_scanning=true
```

## 🗃️ Output

If a match is found, details will be saved to `wallet-info.txt`. The file includes:

* Private Key
* Public Key
* Wallet Address
* WIF (Wallet Import Format)

## 🛑 Stopping

To stop scanning manually, press `CTRL+C`.

---

Feel free to contribute improvements or optimizations via pull requests!
