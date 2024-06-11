<div align="center">

# PKG-SUPPORT-RESISTANCE

![Github Actions](https://github.com/pdm-project/pdm/workflows/Tests/badge.svg)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
</div>

## Description
Collection of algorithms to calculate supports and resistances in financial markets.

## Installation
```js
pip install pkg_support_resistance
```

## Quick usage
Here's an example to get the gist of using the package.

### VanillaSupportResistance algorithms:
```python
from pkg_support_resistance import VanillaSupportResistance


input_data = {
    "open": [
        42780, 42834.94, 42961.83, 43070.3, 43139.4, 43303.82, 43115.57,
        43163.67, 43065.25, 42680.34, 42232.62, 42147.35, 42142.36, 42254.69,
        42369.76, 42333, 42178.39, 42203.58, 42443.2, 42459.92, 42546.45
    ],
    "close": [
        42834.94, 42961.84, 43069.98, 43139.4, 43303.82, 43115.58, 43163.66,
        43065.25, 42680.34, 42232.61, 42147.35, 42142.37, 42254.69, 42369.76,
        42333, 42178.39, 42203.58, 42443.19, 42459.91, 42546.46, 42559.31
    ],
    "high": [
        42901.1, 42986.06, 43160.86, 43159.74, 43333, 43400, 43170.7,
        43234.16, 43092.28, 42802.13, 42393.9, 42303, 42387.46, 42434.54,
        42396.01, 42344.24, 42308.54, 42479.99, 42548.69, 42670.17, 42590.9
    ],
    "low": [
        42730.03, 42795.41, 42914.13, 42988, 43115, 43100.73, 42983.61,
        43000.99, 42641.17, 42156.94, 42098, 41942, 42051.99, 42156.49,
        42203, 42078.63, 42173.02, 42145.3, 42370, 42459.91, 42460.87
    ],
    "volume": [
        173.63661, 169.47648, 298.77136, 221.9715, 398.10382, 277.8895,
        249.64196, 229.9978, 478.65775, 1188.13786, 793.69658, 955.58978,
        428.43125, 378.42146, 260.78176, 396.55715, 245.59294, 357.44034,
        478.28118, 477.66581, 280.79704
    ]
}

sr_result: list[dict] = VanillaSupportResistance.exec_pipeline(input_data=input_data, cluster_threshold=1)

print(sr_result)
```

### KMeansSupportResistance algorithms (data ingestion by json file):
```python
from pkg_support_resistance import KMeansSupportResistance


input_file_path = "/src/pkg_support_resistance/data_set/example.json"
# Open json file
with open(input_file_path, "r") as file:
    input_data = json.load(file)

sr_result: list[dict] = KMeansSupportResistance.exec_pipeline(input_data=input_data, n_clusters=9)

print(sr_result)
```

> [!IMPORTANT]
> ## Supported Algorithms
> | Supported Algorithms   | `Operational`   |
> |:-----------------------|:------------------|
> | `Vanilla`             | ✅                |
> | `Kmeans Clustering`               | ❌                |

----

## Input example:
```javascript
To see in: "/src/pkg_support_resistance/data_set/example.json"
```

## Output example (Using VanillaSupportResistance algorithm and dataset from '/dataset/example.json'):
```javascript
[
   {
      "pivotPrice": 48184.0,
      "limitsUp": 48495.0,
      "limitsDown": 47347.53,
      "score": 67,
      "accumulatedVolume": 44687.15635
   },
   {
      "pivotPrice": 47534.34,
      "limitsUp": 47874.98,
      "limitsDown": 46763.68,
      "score": 41,
      "accumulatedVolume": 23864.294279999995
   },
   {
      "pivotPrice": 45000.0,
      "limitsUp": 45000.0,
      "limitsDown": 44700.0,
      "score": 8,
      "accumulatedVolume": 6010.54166
   },
   {
      "pivotPrice": 43996.5,
      "limitsUp": 44141.37,
      "limitsDown": 43100.0,
      "score": 40,
      "accumulatedVolume": 17909.42211
   },
   {
      "pivotPrice": 43473.45,
      "limitsUp": 43580.0,
      "limitsDown": 42697.01,
      "score": 37,
      "accumulatedVolume": 18501.36496
   },
   {
      "pivotPrice": 42819.86,
      "limitsUp": 42850.0,
      "limitsDown": 42041.7,
      "score": 15,
      "accumulatedVolume": 6355.429050000001
   },
   {
      "pivotPrice": 42259.58,
      "limitsUp": 42787.38,
      "limitsDown": 42017.33,
      "score": 24,
      "accumulatedVolume": 12506.830009999998
   },
   {
      "pivotPrice": 41619.99,
      "limitsUp": 42365.48,
      "limitsDown": 41115.0,
      "score": 91,
      "accumulatedVolume": 42944.990900000004
   },
   {
      "pivotPrice": 41071.29,
      "limitsUp": 41157.26,
      "limitsDown": 40753.88,
      "score": 8,
      "accumulatedVolume": 4474.11918
   }
]
```

### pivotPrice:
Support/resistance line.

### limitsUp/limitsDown:
Support/resistance zone.

### Score, support/resistance score:
If the score is high it means that many candles have been traded in that area with a high volume being traded, on the other hand a low score may be due to the fact that it is not a highly traded area or that it belongs to a higher maximum or lower minimum (very important zones, but not surpassed in the short term and low negotiation).

### accumulatedVolume:
Accumulated volume traded in the consolidated zone between limitsUp/limitsDown.

## Graph of the 'pivotPrice' S/R (Using VanillaSupportResistance algorithm and dataset from '/dataset/example.json'):
<img src="assets/plot_sr_output.png">
