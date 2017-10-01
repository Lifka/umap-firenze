# UMAP Km4City
This scripts performs the data ingestion and normalization for the car sharing platform car2go

### Notes
* Forked from https://github.com/MobilityPolito/UMAP
* Project for Km4City at Università degli Studi di Firenze - UniFI

### Requirements
* MongoDB running on the address specified in DataBaseProxy.py
* pandas python module
* pymongo python module

### Usage
If the requirements have been met, simply launch Ingestion and Normalization scripts with a Python interpreter. The ingestion and normalization scripts are meant to be runned as a daemon, constantly retrieving new data (for the ingestion) and normalizing it (normalization).

### Authors
- [Javier Izquierdo Vera (Lifka)](https://github.com/Lifka/) - [javierizquierdovera@gmail.com](mailto:javierizquierdovera@gmail.com)
- [Miguel Medina Ballesteros (Maximetinu)](https://github.com/Maximetinu/) - [maximetinu@gmail.com](mailto:maximetinu@gmail.com)

### License
Non-Profit Open Software License version 3.0 (NPOSL-3.0) https://opensource.org/licenses/NPOSL-3.0

