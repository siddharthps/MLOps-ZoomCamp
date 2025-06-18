```markdown
# Taxi Data Monitoring: Mage + PostgreSQL + Grafana

This project monitors data drift and missing values on NYC Taxi data using a Mage pipeline, stores metrics in PostgreSQL, and visualizes them in Grafana.

---

## 🧱 Components

- **Mage**: Executes data drift analysis using Evidently.
- **PostgreSQL**: Stores calculated metrics (`dummy_metrics` table).
- **Grafana**: Visualizes metrics via PostgreSQL datasource.

---

## 📂 Folder Structure

```

taxi\_monitoring/
├── mage/                            # Mage project
├── data/                            # .parquet files
│   ├── green\_tripdata\_2025-01.parquet
│   ├── green\_tripdata\_2025-02.parquet
│   └── reference.parquet
├── models/
│   └── lin\_reg.bin                  # Trained sklearn model
├── config/
│   └── grafana\_datasources.yaml    # Grafana datasource config
├── dashboards/                      # Grafana dashboards
├── docker-compose.yaml
├── requirements.txt

````

---

## 🐳 Docker Setup

```bash
docker-compose up --build
````

This starts the following services:

* PostgreSQL (`localhost:5432`)
* Adminer (`localhost:8080`)
* Grafana (`localhost:3000`)
* Mage (`localhost:6789`)

---

## 🧱 Mage Blocks

### `prep_db_` (Custom Block)

Creates `dummy_metrics` table in `test` database if not already present.

### `calculate_metrics` (Custom Block)

For each day in January 2025:

* Loads that day's taxi data
* Runs Evidently metrics: `prediction_drift`, `dataset_drift`, `missing_values`
* Saves the metrics to PostgreSQL

---

## 📊 Grafana Setup

### Datasource Config (`config/grafana_datasources.yaml`)

```yaml
apiVersion: 1

datasources:
  - name: PostgreSQL
    type: postgres
    access: proxy
    url: db:5432
    database: test
    user: postgres
    secureJsonData:
      password: example
    jsonData:
      sslmode: disable
```

### Dashboard Example

In Grafana, create a panel with this SQL:

```sql
SELECT 
  timestamp, prediction_drift 
FROM dummy_metrics 
ORDER BY timestamp
```

Use **Time series** visualization to display drift over time.

---

## ✅ Example Output Table

| Timestamp           | Prediction Drift | Drifted Columns | Missing Share |
| ------------------- | ---------------- | --------------- | ------------- |
| 2025-01-01 00:00:00 | 0.08             | 1               | 0.02          |

---

## 🛠 Requirements

These should go in `requirements.txt`:

```
mage
psycopg[binary]
evidently==0.6.7
pandas
joblib
pyarrow
scikit-learn
tqdm
requests
jupyter
```

---


---

## 🌐 Access URLs

* **Mage**: [http://localhost:6789](http://localhost:6789)
* **Adminer**: [http://localhost:8080](http://localhost:8080) (user: `postgres`, password: `example`)
* **Grafana**: [http://localhost:3000](http://localhost:3000) (user: `admin`, password: `admin`)


