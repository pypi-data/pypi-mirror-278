# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class WalletContextProvider(Component):
    """A WalletContextProvider component.
Wallet Context Provider.
This is a wrapper for apps that provides wallet context throughout the app.
It must be used at the root of the app to provide wallet connections to all child components.

Keyword arguments:

- children (a list of or a singular dash component, string or number; required):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    Adds CSS class name(s).

- network (a value equal to: 'devnet', 'mainnet', 'testnet'; required):
    The network for the wallet.  This prop specifies the network for
    the wallet. It can be 'devnet', 'mainnet', or 'testnet'.

- rpcEndpoint (string; optional):
    The custom RPC endpoint for the wallet.  This prop specifies a
    custom RPC endpoint for the wallet. If it's not provided, the
    default endpoint for the specified network will be used."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_solana_components'
    _type = 'WalletContextProvider'
    @_explicitize_args
    def __init__(self, children=None, network=Component.REQUIRED, rpcEndpoint=Component.UNDEFINED, id=Component.UNDEFINED, className=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'network', 'rpcEndpoint']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'network', 'rpcEndpoint']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['network']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        if 'children' not in _explicit_args:
            raise TypeError('Required argument children was not specified.')

        super(WalletContextProvider, self).__init__(children=children, **args)
