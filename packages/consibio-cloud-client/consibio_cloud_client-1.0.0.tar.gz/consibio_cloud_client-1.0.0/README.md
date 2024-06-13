# consibio-cloud-client

## Data Client for Consibio Cloud

### Installation

To install the package, run the following command:

```bash
pip install consibio-cloud-client
```

### Usage

See the [examples](https://github.com/Consibio/consibio-cloud-python-client/tree/main/examples) folder for examples on how to use the client.

You'll need a Consibio Cloud account, to use the client.

The client can be imported with: `from consibio_cloud_client import Client, Project`

Initialize the client with `client = Client()`, login and initialize the `Project` with `project = Project(client)`, and get the datalog in `DataFrame` with `df = project.get_datalog()`.

#### `Client`

The `Client` exposes the following methods:

- `auth_valid`: to check if the authentication is valid
- `auth_login`: to login with the credentials
- `auto_output`: to get the output of the last command

The Client stores the session token in a `secrets.json` file.

#### `Project`

The `Project` exposes the following methods:

- `get_devices`: to get the devices, will return object with the devices
- `get_elements`: to get the elements, will return object with the elements
- `get_datalog`: to get the datalog, will return a `Datalog` object

The `Project` will use the `Client` to get the data, to remember to initialize the `Client` before initializing the `Project`, and login with the `auth_login` method, too.

#### `DataFrame`

The `get_datalog` method on the `Project` returns a `DataFrame` object, where you can use:

- `plot`: to plot the data, by providing `project=project`, it will render the element title and color the line, too.
- `get_data`: to get the data, each value in a `SingleValue` object
- `get_raw`: to get the raw data
- `get_pandas_df`: to get the Pandas DataFrame
- `add_many`: to add multiple elements to the datalog
- `add`: to add a single element to the datalog
- `remove_element`: to remove an element from the datalog
- `remove_specific`: to remove a specific element from the datalog, with a specific timestamp

#### `SingleValue`

The `SingleValue` object has the following methods:

- `get_element_id`: to get the element id
- `get_value`: to get the value
- `get_timestamp`: to get the timestamp

## Development

### Nox

Nox is a Python automation tool that automates testing in multiple Python environments, packaging, and more.

To install nox, run the following command:

```bash
pip install nox
```

To run the `tests` session, run the following command:

```bash
python3 -m nox -s tests
```

To run the `lint` session, run the following command:

```bash
python3 -m nox -s lint
```

It's recommended to use autopep8 to format the code. Install the extension in VS Code, and use the Workspace settings, which can be found in the `.vscode` folder.
