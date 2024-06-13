from pistol_magazine import List, Datetime, Float, Timestamp


def test_list():
    list = List()
    # Default [str, int, float], e.g. ['involve', 6642899413184882178, 65.23]
    print(list.mock())

    expect_format = [
        Datetime(Datetime.D_FORMAT_YMD, days=2),
        Timestamp(Timestamp.D_TIMEE10, days=2),
        Float(left=2, right=4, unsigned=True)
    ]
    print(List(expect_format).mock(to_json=True))  # e.g. ["2024-06-09 11:49:51", 1717730470, 68.1601] <JSON>
