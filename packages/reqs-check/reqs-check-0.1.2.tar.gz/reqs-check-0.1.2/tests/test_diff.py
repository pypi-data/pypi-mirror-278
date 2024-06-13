from reqs_check.diff import compare_requirements, filter_differences
from reqs_check.utils import parse_requirements


def test_parse_requirements(tmp_path):
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("pandas>=1.1.5\nnumpy==1.19.5\nscipy~=1.5.4")

    result = parse_requirements(req_file)
    expected = {"pandas": ">=1.1.5", "numpy": "==1.19.5", "scipy": "~=1.5.4"}
    assert result == expected


def test_compare_requirements(tmp_path):
    req_file1 = tmp_path / "requirements1.txt"
    req_file1.write_text("pandas>=1.1.5\nnumpy==1.19.5\nscipy~=1.5.4")

    req_file2 = tmp_path / "requirements2.txt"
    req_file2.write_text("pandas==1.1.5\nnumpy==1.19.3\nmatplotlib==3.3.4")

    df = compare_requirements([str(req_file1), str(req_file2)])

    expected_columns = ["Package", str(req_file1), str(req_file2)]
    assert list(df.columns) == expected_columns
    assert "pandas" in df["Package"].values
    assert "numpy" in df["Package"].values
    assert "scipy" in df["Package"].values
    assert "matplotlib" in df["Package"].values
    assert df.loc[df["Package"] == "pandas", str(req_file1)].values[0] == ">=1.1.5"
    assert df.loc[df["Package"] == "pandas", str(req_file2)].values[0] == "==1.1.5"
    assert (
        df.loc[df["Package"] == "matplotlib", str(req_file1)].values[0] == "Not Present"
    )


def test_filter_differences(tmp_path):
    req_file1 = tmp_path / "requirements1.txt"
    req_file1.write_text("pandas==1.1.5\nnumpy==1.19.5\nscipy~=1.5.4")

    req_file2 = tmp_path / "requirements2.txt"
    req_file2.write_text("pandas==1.1.5\nnumpy==1.19.3\nmatplotlib==3.3.4")

    df = compare_requirements([str(req_file1), str(req_file2)])
    filtered_df = filter_differences(df)

    assert "pandas" not in filtered_df["Package"].values
    assert "numpy" in filtered_df["Package"].values
    assert "scipy" in filtered_df["Package"].values
