# ECMind blue client: Object Definition (objdef)

Helper modules for the `ecmind_blue_client` to ease the work with object definition APIs. See discussion here: https://hub.ecmind.ch/t/119

## Installation

`pip install ecmind_blue_client_objdef`

## Usage

```python
from ecmind_blue_client.tcp_client import TcpClient as Client
from ecmind_blue_client_objdef import object_definition

client = Client(hostname='localhost', port=4000, appname='test', username='root', password='optimal')
asobjdef = object_definition.load_object_definition(client)
for cabinet in asobjdef.cabinets:
    print(cabinet)
```

## Changes

### Version `0.0.3`

- Workaround and warn message for pages without internal name.

### Version `0.0.4`

- Workaround and warn message for tables without columns.

### Version `0.0.5`

- Workaround and warn message for tab pages without controls.

### Version `0.0.9`

- Add list addon support
- Add missing field types YES_NO, LETTERS_ONLY and ALPHA_DIGITS

### Version `0.1.0`

- Fix parsing of `dbfield`
- (Re-) add table_name to `Fields` & `TableFields`
- Fix/Remove redefining built-in `type` by renaming function parameter to `_type`

### Version `0.1.1`

- Deactivate automatic number and bool parsing in xml to dict function.
- Manually convert id/type/cotype/length fields to int. 

### Version `0.1.2`

- Add `row` to list of xml tags that are marked as list.
- Fix int casting for index elements of dropdown icon lists.