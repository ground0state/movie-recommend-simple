# movie-recommend-simple

## Install

Use Python 3.10.

```bash
conda create -n surprise python=3.10
conda activate surprise
```

```bash
pip install scikit-surprise
pip install flask pandas
```

## Download dataset

```bash
python download.py
```

## Train dataset

```bash
python train.py
```

## Deploy

```bash
python server.py
```
