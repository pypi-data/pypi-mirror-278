# pkgpy-atp-dataset

The python package for manipulating datasets.

## Installation

## Keywords

- database
- dataset
- measurement, simulations, surveys
- datapoint

## Datatypes

- time series data (datapoints (time dependent), metadata, name, uuid)
- dataset:
  - timeseries (independent variables (datetime, timestamp, time(unit)))
  - multidimensional dataset
- dataset_ts(reference to time series data, metadata, name, uuid)
- dataset_spectrum (datapoints, metadata, name, uuid)

## Measurement

```YML
- name: string
- uuid: string(uuid)
- datatype_id: measurement
- metadata
  - name: string
  - uuid: string(uuid)
  - datetime: string[optional] # when the sample was created
  - device_id: string
  - device_uuid: string(uuid)
  - sample_id: string
  - sample_uuid: string(uuid)
  - subsample_id: string or ordered list[string]
  - parallel_id: string
  - location_id: string
  - location_uuid: string(uuid)
  - location_coordinates: {latitude: float, longitude: float, altitude: float[optional]}
  - measurement_type_id: string
  - measurement_type_uuid: string(uuid)
- data:
  - dict:
    - key: value or list
  - list:
    - dict:
      - key: value
- error
```

## Sample

```YML
- datatype_id: sample
- name: string
- uuid: string(uuid)

- metadata:
  - name: string
  - uuid: string(uuid)
  - datetime: string[optional] # when the sample was created
  - sample_id: string
  - location_id: string
  - location_uuid: string(uuid)
  - location_coordinates: {latitude: float, longitude: float, altitude: float[optional]}
  - ... # other metadata
- data:
  - properties: {}
  - labels: [] # list of labels
  - links: [] # links to other samples
  - measurement_dict: {}
  - measurement_list: []

- error
```
