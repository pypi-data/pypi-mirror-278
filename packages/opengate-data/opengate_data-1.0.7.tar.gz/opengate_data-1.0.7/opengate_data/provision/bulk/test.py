from flatten_dict import flatten, unflatten
from pprint import pprint

dct = {
  "entities": [
    {
      "provision": {
        "administration": {
          "organization": {
            "_current": {
              "value": "base_organization"
            }
          },
          "channel": {
            "_current": {
              "value": "base_channel"
            }
          },
          "serviceGroup": {
            "_current": {
              "value": "emptyServiceGroup"
            }
          }
        },
        "device": {
          "identifier": {
            "_current": {
              "value": "device_1_id"
            }
          },
          "name": {
            "_current": {
              "value": "device_1_name"
            }
          },
          "description": {
            "_current": {
              "value": "device_1_description"
            }
          },
          "administrativeState": {
            "_current": {
              "value": "ACTIVE"
            }
          },
          "operationalStatus": {
            "_current": {
              "value": "NORMAL"
            }
          },
          "model": {
            "_current": {
              "value": {
                "manufacturer": "OpenGate",
                "name": "OpenGate",
                "version": "1.0"
              }
            }
          },
          "specificType": {
            "_current": {
              "value": "CONCENTRATOR"
            }
          },
          "serialNumber": {
            "_current": {
              "value": "32333-33334-122-1"
            }
          }
        }
      }
    }
  ]
}

     
flat = flatten(dct["entities"][0], reducer='underscore')

keys_to_modify = list(flat.keys())

for key in keys_to_modify:
    if '__' in key:
        new_key = key.replace('__', '_')
    if new_key != key:
        flat[new_key] = flat.pop(key)


pprint(flat)


def add_underscore_to_current_keys(d):
    for key in list(d.keys()):
        if isinstance(d[key], dict):
            add_underscore_to_current_keys(d[key])
        if key == 'current':
            d[f'_{key}'] = d.pop(key)
        
        
            
unflat = unflatten(flat, splitter='underscore')


add_underscore_to_current_keys(unflat)

pprint(unflat)




