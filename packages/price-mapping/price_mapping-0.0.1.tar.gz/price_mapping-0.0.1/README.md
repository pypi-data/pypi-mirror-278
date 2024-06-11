# Introduction
ESF calculation tool

# How to setup
Create your environment with conda
```
conda create -n <your_name> python=3.12 -y && conda activate <your_name>
```

Install with pip:
```
pip install core-tpl
```

ESF Calculation:
```
esf = ESFLogic(
    price_dict=price,
    data=df,
    col_route='route_',
    col_zone='zone_',
    col_weight='final_weight'
)
df = esf.run()
```
