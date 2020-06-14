from datascroller import command_line

path = 'example_path.csv'


def get_args(input_args):

    parser = command_line.create_parser()
    args = parser.parse_args(input_args)
    return vars(args)


def test_default():

    expected = {'filepath': path,
                'sep': ',',
                'encoding': None,
                'nrows': None,
                'chunksize': None}

    assert expected == get_args([path])


def test_options():

    sep = '|'
    encoding = 'utf-16'
    nrows = 1000
    chunksize = 1000
    args = [path, '--sep', sep, '--encoding', encoding, '--nrows', str(nrows), '--chunksize', str(chunksize)]

    expected = {'filepath': path,
                'sep': sep,
                'encoding': encoding,
                'nrows': nrows,
                'chunksize': chunksize}

    assert expected == get_args(args)
