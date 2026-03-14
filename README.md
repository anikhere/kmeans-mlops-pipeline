# 🤖 KMeans MLOps Pipeline
 
> K-Means clustering algorithm built **from scratch** — no sklearn — deployed with a production-grade MLOps pipeline using Docker, GitHub Actions CI/CD, and AWS S3 artifact storage.
 
---
 
## 🏗️ Architecture
 
```
┌─────────────────────────────────────────────────────────────────┐
│                        Developer Machine                        │
│  kmeans.py + train.py  →  git push  →  GitHub                  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Actions Pipeline                      │
│                                                                 │
│   ┌──────────────────────────────────────┐                      │
│   │         CI: Test & Build             │                      │
│   │  ✓ Setup Python 3.10                 │                      │
│   │  ✓ Cache pip dependencies            │                      │
│   │  ✓ Install requirements              │                      │
│   │  ✓ Run train.py (smoke test)         │                      │
│   │  ✓ Upload artifacts → AWS S3         │                      │
│   │  ✓ Build Docker image                │                      │
│   └──────────────┬───────────────────────┘                      │
│                  │ needs: CI pass                               │
│   ┌──────────────▼───────────────────────┐                      │
│   │         CD: Deploy                   │                      │
│   │  ✓ Login to DockerHub                │                      │
│   │  ✓ Build Docker image                │                      │
│   │  ✓ Push :latest tag                  │                      │
│   │  ✓ Push :sha tag (versioned)         │                      │
│   └──────────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
┌──────────────────────┐       ┌─────────────────────────┐
│      DockerHub       │       │        AWS S3            │
│  kmeans-mlops:latest │       │  kmeans-mlops-bucket     │
│  kmeans-mlops:sha    │       │  └── outputs/            │
└──────────────────────┘       │       └── results.png    │
                               └─────────────────────────┘
```
 
---
 
## 🧠 Algorithm — Built From Scratch
 
K-Means clustering implemented with **zero sklearn** — only NumPy.
 
### How it works:
 
```
1. Initialize  →  randomly pick K points as centroids
2. Assign      →  label each point to nearest centroid (Euclidean distance)
3. Update      →  recalculate centroids as cluster means
4. Converge    →  repeat until centroids move less than tolerance (tol=1e-4)
```
 
### Implementation highlights:
 
| Component | Description |
|-----------|-------------|
| `_euclidean(a, b)` | Custom distance function — no `np.linalg.norm` |
| `_assign_clusters(X)` | Labels every point to nearest centroid |
| `_update_centroids(X, labels)` | Recalculates cluster centers via mean |
| `fit(X)` | Full training loop with convergence check |
| `predict(X)` | Assigns new data to learned clusters |
 
---
 
## 🛠️ Tech Stack
 
| Layer | Technology |
|-------|------------|
| Algorithm | Python, NumPy |
| Data Generation | scikit-learn `make_blobs` |
| Visualization | Matplotlib |
| Containerization | Docker (python:3.10-slim) |
| CI/CD | GitHub Actions |
| Artifact Storage | AWS S3 (boto3) |
| Image Registry | DockerHub |
| Secrets Management | GitHub Secrets + python-dotenv |
 
---
 
## 📁 Project Structure
 
```
kmeans-mlops-pipeline/
├── .github/
│   └── workflows/
│       └── main.yaml          # CI/CD pipeline
├── outputs/
│   └── results.png            # generated cluster plot
├── kmeans.py                  # K-Means algorithm from scratch
├── train.py                   # training script + S3 upload
├── aws_setup.py               # S3 bucket operations
├── dockerfile                 # production Docker image
├── requirements.txt           # pinned dependencies
└── README.md
```
 
---
 
## 🚀 Run Locally
 
### Prerequisites
- Python 3.10+
- Docker
- AWS account with S3 access
 
### 1. Clone the repo
```bash
git clone https://github.com/anikhere/kmeans-mlops-pipeline.git
cd kmeans-mlops-pipeline
```
 
### 2. Create virtual environment
```bash
python -m venv kmeans-venv
kmeans-venv\Scripts\activate      # Windows
source kmeans-venv/bin/activate   # Mac/Linux
```
 
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
 
### 4. Set up environment variables
Create a `.env` file:
```
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=ap-south-1
```
 
### 5. Train and visualize
```bash
python train.py
```
 
### 6. Run with Docker
```bash
docker build -t kmeans-mlops-pipeline .
docker run kmeans-mlops-pipeline
```
 
---
 
## ⚙️ CI/CD Pipeline
 
Every push to `main` triggers the full pipeline automatically.
 
### CI Job — Test & Build
```yaml
✓ Checkout code
✓ Setup Python 3.10
✓ Cache pip dependencies (hashFiles for smart invalidation)
✓ Install requirements
✓ Run train.py (smoke test — proves code works)
✓ Upload results.png to AWS S3
✓ Build Docker image with two tags
```
 
### CD Job — Deploy (runs only if CI passes)
```yaml
✓ Login to DockerHub
✓ Build Docker image
✓ Push :latest tag
✓ Push :<git-sha> tag (for versioned rollbacks)
```
 
### Docker Image Tags
```
anikhere/kmeans-mlops-pipeline:latest     → always points to newest
anikhere/kmeans-mlops-pipeline:<sha>      → frozen snapshot per commit
```
 
---
 
## ☁️ AWS S3 Integration
 
Artifacts are automatically uploaded to S3 after every training run.
 
```python
# Programmatic bucket operations via boto3
connect_to_s3()        # authenticated connection
create_s3_bucket()     # idempotent bucket creation
upload_to_s3()         # local → S3
download_from_s3()     # S3 → local
list_bucket()          # verify contents
```
 
**Bucket:** `kmeans-mlops-bucket-user` | **Region:** `ap-south-1` (Mumbai)
 
---
 
## 🔐 Secrets Management
 
| Secret | Where |
|--------|-------|
| `DOCKER_USERNAME` | GitHub Actions Secrets |
| `DOCKER_PASSWORD` | GitHub Actions Secrets (Access Token) |
| `AWS_ACCESS_KEY_ID` | GitHub Actions Secrets |
| `AWS_SECRET_ACCESS_KEY` | GitHub Actions Secrets |
| Local credentials | `.env` file (gitignored) |
 
> ⚠️ Never commit `.env` to version control. GitHub push protection is enabled on this repo.
 
---
 
## 📊 Results
 
The algorithm correctly identifies 3 clusters from 100 synthetic data points generated with `make_blobs`:
 
- **Red X markers** — learned centroids
- **Colored points** — cluster assignments (0, 1, 2)
- Convergence typically achieved in **< 20 iterations**
 
---
 
## 🗺️ Roadmap
 
- [ ] EC2 deployment for model serving
- [ ] FastAPI endpoint for real-time predictions  
- [ ] K-Means++ initialization
- [ ] Elbow method for optimal K selection
- [ ] MLflow experiment tracking
 
---
 
## 👤 Author
 
**Taha** — ML Engineer in progress  
Building production-grade ML systems from scratch.
 
[![GitHub](https://img.shields.io/badge/GitHub-anikhere-black?style=flat&logo=github)](https://github.com/anikhere)
 
---
 
> *"Built from scratch. Deployed to production. Zero shortcuts."*
