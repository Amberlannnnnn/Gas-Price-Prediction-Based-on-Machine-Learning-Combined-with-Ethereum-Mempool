# Quickstart

The application connects to infura to get data from its ethereum full node. In order to do so the following env variables need to be setup (they can be placed in a `.env` file):
```.env
INFURA_URL=https://mainnet.infura.io/v3
INFURA_PROJECT=<your_project_id>
GECKO_URL=https://api.coingecko.com/api/v3
```

To start the app during development
```bash
# run the app
make run

# test health endpoint
curl http://localhost:5000/health

# get gasprice
wscat -c ws://localhost:5000/gasprice
```

### Build executable:
```bash
# build
make build