import pandas as pd

from .columns import GLADEDescriptor

def to_df(filename, cols=None, filter_fn=None, chunksize=200000, progress=None, **kwargs):
    """Parse the GlADE+ text file into a Pandas DataFrame.
    Uses Pandas.read_csv method.

    Parameters
    ----------
    filename : str
        The path to the GLADE+ text file
    cols : list
        The list of columns to extract from the file. See `GlADEDescriptor.get_columns`.
        If None, will return all columns. By default None.
    filter_fn : function
        A filter function to be executed on each DataFrame chunk. By default None.
    chunksize : int, optional
        The chunksize argument of read_csv. Defaults to 200000, which corresponds to roughly 100 iterations
    progress :  optional
        A progress bar decorator, such as tqdm.tqdm. By default None.

    Returns
    -------
    Pandas.DataFrame
        The DataFrame containing the extracted columns after filtering out the data
    """
    descriptor = GLADEDescriptor()
    all_columns = descriptor.get_columns(names=True)
    reader_args = dict(
        sep=" ",
        names=all_columns,
        usecols=cols,
        dtype=descriptor.column_dtypes,
        header=None,
        false_values=["null"],
        chunksize=chunksize,
        **kwargs,
    )
    chunks = []
    with pd.read_csv(filename, **reader_args) as reader:
        iterator = progress(reader) if progress else reader
        fn = filter_fn if filter_fn is not None else lambda x: x
        for chunk in iterator:
            chunks.append(fn(chunk))

        catalog = pd.concat(chunks, ignore_index=True)

    return catalog

def to_hdf5(filename, output_filename, hdf5_key, cols=None, filter_fn=None, chunksize=200000, progress=None, **kwargs):
    """Parse the GlADE+ text file onto an HDF5 file.
    Uses Pandas.read_csv method.

    Parameters
    ----------
    filename : str
        The path to the GLADE+ text file
    output_filename: str
        The path to the output file
    hdf5_key: str
        The hdf5 key to put the data
    cols : list
        The list of columns to extract from the file. See `GlADEDescriptor.get_columns`. 
        If None, will return all columns. By default None.
    filter_fn : function
        A filter function to be executed on each DataFrame chunk. By default None.
    chunksize : int, optional
        The chunksize argument of read_csv. Defaults to 200000, which corresponds to roughly 100 iterations
    progress :  optional
        A progress bar decorator, such as tqdm.tqdm. By default None.
    """
    descriptor = GLADEDescriptor()
    all_columns = descriptor.get_columns(names=True)
    reader_args = dict(
        sep=" ",
        names=all_columns,
        usecols=cols,
        dtype=descriptor.column_dtypes,
        header=None,
        false_values=["null"],
        chunksize=chunksize,
        **kwargs,
    )
    store = pd.HDFStore(filename, mode='w')
    with pd.read_csv(output_filename, **reader_args) as reader:
        iterator = progress(reader) if progress else reader
        fn = filter_fn if filter_fn is not None else lambda x: x
        for chunk in iterator:
            store.append(hdf5_key, fn(chunk))

    store.close()
