from datascroller import command_line

path = 'example_path.csv'


def get_args(input_args):

    parser = command_line.create_parser()
    args = parser.parse_args(input_args)
    return vars(args)


def test_default():

    expected = {'csv_filepath': path,
                'sep': ',',
                'encoding': None}

    assert expected == get_args([path])


def test_options():

    sep = '|'
    encoding = 'utf-16'
    args = [path, '--sep', sep, '--encoding', encoding]

    expected = {'csv_filepath': path,
                'sep': sep,
                'encoding': encoding}

    assert expected == get_args(args)
