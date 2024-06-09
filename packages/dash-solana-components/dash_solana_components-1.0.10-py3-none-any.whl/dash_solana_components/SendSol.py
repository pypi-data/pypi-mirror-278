# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SendSol(Component):
    """A SendSol component.
SendSolTx component for sending Solana tokens.
@param {SendSolTxProps} props - The properties for the component.
@returns {JSX.Element} The rendered component.

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    Adds CSS class name(s).

- connection (dict; required):
    Connection element for wallet.

    `connection` is a dict with keys:

    - _buildArgs (required)

    - commitment (a value equal to: 'processed', 'confirmed', 'finalized', 'recent', 'single', 'singleGossip', 'root', 'max'; required):
        The default commitment used for requests.

    - confirmTransaction (dict; required)

        `confirmTransaction` is a dict with keys:


    - confirmTransactionUsingBlockHeightExceedanceStrategy (boolean | number | string | dict | list; required)

    - confirmTransactionUsingDurableNonceStrategy (boolean | number | string | dict | list; required)

    - confirmTransactionUsingLegacyTimeoutStrategy (boolean | number | string | dict | list; required)

    - getAccountInfo (required):
        Fetch all the account info for the specified public key.

    - getAccountInfoAndContext (required):
        Fetch all the account info for the specified public key,
        return with context.

    - getAddressLookupTable (required)

    - getBalance (required):
        Fetch the balance for the specified public key.

    - getBalanceAndContext (required):
        Fetch the balance for the specified public key, return with
        context.

    - getBlock (dict; required):
        Fetch a processed block from the cluster.
        @,deprecated,Instead, call `getBlock` using a
        `GetVersionedBlockConfig` by setting the
        `maxSupportedTransactionVersion` property.
        @,deprecated,Instead, call `getBlock` using a
        `GetVersionedBlockConfig` by setting the
        `maxSupportedTransactionVersion` property.
        @,deprecated,Instead, call `getBlock` using a
        `GetVersionedBlockConfig` by setting the
        `maxSupportedTransactionVersion` property.

        `getBlock` is a dict with keys:


    - getBlockHeight (required)

    - getBlockProduction (required)

    - getBlockSignatures (required):
        Fetch a list of Signatures from the cluster for a block,
        excluding rewards.

    - getBlockTime (required):
        Fetch the estimated production time of a block.

    - getBlocks (required):
        Fetch confirmed blocks between two slots.

    - getCancellationPromise (boolean | number | string | dict | list; required)

    - getClusterNodes (required):
        Return the list of nodes that are currently participating in
        the cluster.

    - getConfirmedBlock (required):
        Fetch a list of Transactions and transaction statuses from the
        cluster for a confirmed block. @,deprecated,Deprecated since
        v1.13.0. Please use ,{@link ,getBlock ,}, instead.

    - getConfirmedBlockSignatures (required):
        Fetch a list of Signatures from the cluster for a confirmed
        block, excluding rewards @,deprecated,Deprecated since Solana
        v1.8.0. Please use ,{@link ,getBlockSignatures ,}, instead.

    - getConfirmedSignaturesForAddress (required):
        Fetch a list of all the confirmed signatures for transactions
        involving an address within a specified slot range. Max range
        allowed is 10,000 slots. @,deprecated,Deprecated since v1.3.
        Please use ,{@link ,getConfirmedSignaturesForAddress2 ,},
        instead. @,param,address, ,queried address @,param,startSlot,
        ,start slot, inclusive @,param,endSlot, ,end slot, inclusive.

    - getConfirmedSignaturesForAddress2 (required):
        Returns confirmed signatures for transactions involving an
        address backwards in time from the provided signature or most
        recent confirmed block @,param,address, ,queried address
        @,param,options.

    - getConfirmedTransaction (required):
        Fetch a transaction details for a confirmed transaction
        @,deprecated,Deprecated since Solana v1.8.0. Please use
        ,{@link ,getTransaction ,}, instead.

    - getEpochInfo (required):
        Fetch the Epoch Info parameters.

    - getEpochSchedule (required):
        Fetch the Epoch Schedule parameters.

    - getFeeCalculatorForBlockhash (required):
        Fetch the fee calculator for a recent blockhash from the
        cluster, return with context @,deprecated,Deprecated since
        Solana v1.8.0. Please use ,{@link ,getFeeForMessage ,},
        instead.

    - getFeeForMessage (required):
        Fetch the fee for a message from the cluster, return with
        context.

    - getFirstAvailableBlock (required):
        Fetch the slot of the lowest confirmed block that has not been
        purged from the ledger.

    - getGenesisHash (required):
        Fetch the genesis hash.

    - getInflationGovernor (required):
        Fetch the cluster InflationGovernor parameters.

    - getInflationRate (required):
        Fetch the specific inflation values for the current epoch.

    - getInflationReward (required):
        Fetch the inflation reward for a list of addresses for an
        epoch.

    - getLargestAccounts (required):
        Fetch the 20 largest accounts with their current balances.

    - getLatestBlockhash (required):
        Fetch the latest blockhash from the cluster @,return.

    - getLatestBlockhashAndContext (required):
        Fetch the latest blockhash from the cluster @,return.

    - getLeaderSchedule (required):
        Fetch the leader schedule for the current epoch @,return.

    - getMinimumBalanceForRentExemption (required):
        Fetch the minimum balance needed to exempt an account of
        `dataLength` size from rent.

    - getMinimumLedgerSlot (required):
        Fetch the lowest slot that the node has information about in
        its ledger. This value may increase over time if the node is
        configured to purge older ledger data.

    - getMultipleAccountsInfo (required):
        Fetch all the account info for multiple accounts specified by
        an array of public keys.

    - getMultipleAccountsInfoAndContext (required):
        Fetch all the account info for multiple accounts specified by
        an array of public keys, return with context.

    - getMultipleParsedAccounts (required):
        Fetch all the account info for multiple accounts specified by
        an array of public keys, return with context.

    - getNonce (required):
        Fetch the contents of a Nonce account from the cluster.

    - getNonceAndContext (required):
        Fetch the contents of a Nonce account from the cluster, return
        with context.

    - getParsedAccountInfo (required):
        Fetch parsed account info for the specified public key.

    - getParsedBlock (dict; required):
        Fetch parsed transaction details for a confirmed or finalized
        block.

        `getParsedBlock` is a dict with keys:


    - getParsedConfirmedTransaction (required):
        Fetch parsed transaction details for a confirmed transaction
        @,deprecated,Deprecated since Solana v1.8.0. Please use
        ,{@link ,getParsedTransaction ,}, instead.

    - getParsedConfirmedTransactions (required):
        Fetch parsed transaction details for a batch of confirmed
        transactions @,deprecated,Deprecated since Solana v1.8.0.
        Please use ,{@link ,getParsedTransactions ,}, instead.

    - getParsedProgramAccounts (required):
        Fetch and parse all the accounts owned by the specified
        program id @,return.

    - getParsedTokenAccountsByOwner (required):
        Fetch parsed token accounts owned by the specified account
        @,return.

    - getParsedTransaction (required):
        Fetch parsed transaction details for a confirmed or finalized
        transaction.

    - getParsedTransactions (required):
        Fetch parsed transaction details for a batch of confirmed
        transactions.

    - getProgramAccounts (dict; required):
        Fetch all the accounts owned by the specified program id
        @,return.

        `getProgramAccounts` is a dict with keys:


    - getRecentBlockhash (required):
        Fetch a recent blockhash from the cluster @,return
        @,deprecated,Deprecated since Solana v1.8.0. Please use
        ,{@link ,getLatestBlockhash ,}, instead.

    - getRecentBlockhashAndContext (required):
        Fetch a recent blockhash from the cluster, return with context
        @,return @,deprecated,Deprecated since Solana v1.8.0. Please
        use ,{@link ,getLatestBlockhash ,}, instead.

    - getRecentPerformanceSamples (required):
        Fetch recent performance samples @,return.

    - getRecentPrioritizationFees (required):
        Fetch a list of prioritization fees from recent blocks.

    - getSignatureStatus (required):
        Fetch the current status of a signature.

    - getSignatureStatuses (required):
        Fetch the current statuses of a batch of signatures.

    - getSignaturesForAddress (required):
        Returns confirmed signatures for transactions involving an
        address backwards in time from the provided signature or most
        recent confirmed block @,param,address, ,queried address
        @,param,options.

    - getSlot (required):
        Fetch the current slot that the node is processing.

    - getSlotLeader (required):
        Fetch the current slot leader of the cluster.

    - getSlotLeaders (required):
        Fetch `limit` number of slot leaders starting from `startSlot`
        @,param,startSlot, ,fetch slot leaders starting from this slot
        @,param,limit, ,number of slot leaders to return.

    - getStakeActivation (required):
        Returns epoch activation information for a stake account that
        has been delegated.

    - getStakeMinimumDelegation (required):
        get the stake minimum delegation.

    - getSupply (required):
        Fetch information about the current supply.

    - getTokenAccountBalance (required):
        Fetch the current balance of a token account.

    - getTokenAccountsByOwner (required):
        Fetch all the token accounts owned by the specified account
        @,return.

    - getTokenLargestAccounts (required):
        Fetch the 20 largest token accounts with their current
        balances for a given mint.

    - getTokenSupply (required):
        Fetch the current supply of a token mint.

    - getTotalSupply (required):
        Fetch the current total currency supply of the cluster in
        lamports @,deprecated,Deprecated since v1.2.8. Please use
        ,{@link ,getSupply ,}, instead.

    - getTransaction (dict; required):
        Fetch a confirmed or finalized transaction from the cluster.
        @,deprecated,Instead, call `getTransaction` using a
        `GetVersionedTransactionConfig` by setting the
        `maxSupportedTransactionVersion` property.

        `getTransaction` is a dict with keys:


    - getTransactionConfirmationPromise (boolean | number | string | dict | list; required)

    - getTransactionCount (required):
        Fetch the current transaction count of the cluster.

    - getTransactions (dict; required):
        Fetch transaction details for a batch of confirmed
        transactions. Similar to  {@link  getParsedTransactions  }
        but returns a  {@link  TransactionResponse  } .   Fetch
        transaction details for a batch of confirmed transactions.
        Similar to  {@link  getParsedTransactions  }  but returns a
        {@link  * VersionedTransactionResponse } .
        @,deprecated,Instead, call `getTransactions` using a
        `GetVersionedTransactionConfig` by setting the
        `maxSupportedTransactionVersion` property.

        `getTransactions` is a dict with keys:


    - getVersion (required):
        Fetch the node version.

    - getVoteAccounts (required):
        Return the list of nodes that are currently participating in
        the cluster.

    - isBlockhashValid (required):
        Returns whether a blockhash is still valid or not.

    - onAccountChange (required):
        Register a callback to be invoked whenever the specified
        account changes @,param,publicKey, ,Public key of the account
        to monitor @,param,callback, ,Function to invoke whenever the
        account is changed @,param,commitment, ,Specify the commitment
        level account changes must reach before notification
        @,return,subscription id.

    - onLogs (required):
        Registers a callback to be invoked whenever logs are emitted.

    - onProgramAccountChange (required):
        Register a callback to be invoked whenever accounts owned by
        the specified program change @,param,programId, ,Public key of
        the program to monitor @,param,callback, ,Function to invoke
        whenever the account is changed @,param,commitment, ,Specify
        the commitment level account changes must reach before
        notification @,param,filters, ,The program account filters to
        pass into the RPC method @,return,subscription id.

    - onRootChange (required):
        Register a callback to be invoked upon root changes
        @,param,callback, ,Function to invoke whenever the root
        changes @,return,subscription id.

    - onSignature (required):
        Register a callback to be invoked upon signature updates
        @,param,signature, ,Transaction signature string in base 58
        @,param,callback, ,Function to invoke on signature
        notifications @,param,commitment, ,Specify the commitment
        level signature must reach before notification
        @,return,subscription id.

    - onSignatureWithOptions (required):
        Register a callback to be invoked when a transaction is
        received and/or processed. @,param,signature, ,Transaction
        signature string in base 58 @,param,callback, ,Function to
        invoke on signature notifications @,param,options, ,Enable
        received notifications and set the commitment level that
        signature must reach before notification @,return,subscription
        id.

    - onSlotChange (required):
        Register a callback to be invoked upon slot changes
        @,param,callback, ,Function to invoke whenever the slot
        changes @,return,subscription id.

    - onSlotUpdate (required):
        Register a callback to be invoked upon slot updates.  {@link
        SlotUpdate  } 's may be useful to track live progress of a
        cluster. @,param,callback, ,Function to invoke whenever the
        slot updates @,return,subscription id.

    - removeAccountChangeListener (required):
        Deregister an account notification callback
        @,param,clientSubscriptionId, ,client subscription id to
        deregister.

    - removeOnLogsListener (required):
        Deregister a logs callback. @,param,clientSubscriptionId,
        ,client subscription id to deregister.

    - removeProgramAccountChangeListener (required):
        Deregister an account notification callback
        @,param,clientSubscriptionId, ,client subscription id to
        deregister.

    - removeRootChangeListener (required):
        Deregister a root notification callback
        @,param,clientSubscriptionId, ,client subscription id to
        deregister.

    - removeSignatureListener (required):
        Deregister a signature notification callback
        @,param,clientSubscriptionId, ,client subscription id to
        deregister.

    - removeSlotChangeListener (required):
        Deregister a slot notification callback
        @,param,clientSubscriptionId, ,client subscription id to
        deregister.

    - removeSlotUpdateListener (required):
        Deregister a slot update notification callback
        @,param,clientSubscriptionId, ,client subscription id to
        deregister.

    - requestAirdrop (required):
        Request an allocation of lamports to the specified address
        ```typescript import { Connection, PublicKey, LAMPORTS_PER_SOL
        } from \"@solana/web3.js\";  (async () => {   const connection
        = new Connection(\"https://api.testnet.solana.com\",
        \"confirmed\");   const myAddress = new
        PublicKey(\"2nr1bHFT86W9tGnyvmYW4vcHKsQB3sVQfnddasz4kExM\");
        const signature = await connection.requestAirdrop(myAddress,
        LAMPORTS_PER_SOL);   await
        connection.confirmTransaction(signature); })(); ```.

    - rpcEndpoint (string; required):
        The RPC endpoint.

    - sendEncodedTransaction (required):
        Send a transaction that has already been signed, serialized
        into the wire format, and encoded as a base64 string.

    - sendRawTransaction (required):
        Send a transaction that has already been signed and serialized
        into the wire format.

    - sendTransaction (dict; required):
        Sign and send a transaction   Send a signed transaction
        @,deprecated,Instead, call ,{@link ,sendTransaction ,}, with a
        ,{@link ,* VersionedTransaction,}.

        `sendTransaction` is a dict with keys:


    - simulateTransaction (dict; required):
        Simulate a transaction @,deprecated,Instead, call ,{@link
        ,simulateTransaction ,}, with ,{@link ,*
        VersionedTransaction,}, and ,{@link ,SimulateTransactionConfig
        ,}, parameters.

        `simulateTransaction` is a dict with keys:


- publicKey (dict; required):
    Public key element for wallet.

    `publicKey` is a dict with keys:

    - __@toStringTag@858 (string; required)

    - encode (required)

    - equals (required):
        Checks if two publicKeys are equal.

    - toBase58 (required):
        Return the base-58 representation of the public key.

    - toBuffer (required):
        Return the Buffer representation of the public key in big
        endian.

    - toBytes (required):
        Return the byte array representation of the public key in big
        endian.

    - toJSON (required)

    - toString (optional):
        Return the base-58 representation of the public key.

- sendSolTx (string; required):
    Transaction signature."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_solana_components'
    _type = 'SendSol'
    @_explicitize_args
    def __init__(self, sendSolTx=Component.REQUIRED, connection=Component.REQUIRED, publicKey=Component.REQUIRED, setSendSolTx=Component.REQUIRED, connectionErr=Component.REQUIRED, sendTransaction=Component.REQUIRED, id=Component.UNDEFINED, className=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'connection', 'publicKey', 'sendSolTx']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'connection', 'publicKey', 'sendSolTx']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['connection', 'publicKey', 'sendSolTx']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(SendSol, self).__init__(**args)
