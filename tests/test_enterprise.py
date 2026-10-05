from hhw.enterprise import parse_enterprise_title


def test_r640_dense_config():
    x = parse_enterprise_title(
        'Dell R640 2x Xeon Gold 6230 256GB DDR4 HBA330 10x 2.5" SFF NVMe 25GbE'
    )
    assert x["cpu_count"] == 2
    assert x["memory_gb"] == 256
    assert x["drive_bays"]["count"] == 10
    assert x["drive_bays"]["size_in"] == 2.5
    assert x["nvme_capable_or_present"] is True
    assert x["storage_controller"].upper() == "HBA330"
    assert x["network_max_gbps"] == 25


def test_tb_memory_and_lff():
    x = parse_enterprise_title("PowerEdge R740xd 1.5TB DDR4 12 LFF H740P 10GbE")
    assert x["memory_gb"] == 1536
    assert x["drive_bays"]["count"] == 12
    assert x["drive_bays"]["size_in"] == 3.5
    assert x["storage_controller"].upper() == "H740P"
