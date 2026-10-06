from hhw.classify import classify_title


def test_r640_is_compute_server():
    x = classify_title("Dell PowerEdge R640 8SFF")
    assert "server" in x
    assert "proxmox_compute" in x


def test_xxv710_is_not_switch():
    x = classify_title("Intel XXV710-DA2 Dual Port 25GbE NIC")
    assert "network_adapter" in x
    assert "networking_component" in x
    assert "managed_switch" not in x


def test_hba_is_storage_component():
    x = classify_title("LSI 9300-8i SAS HBA")
    assert "storage_controller" in x
    assert "storage_component" in x


def test_enterprise_ups_is_power_protection():
    for title in (
        "APC Smart-UPS SMT1500I",
        "Eaton 9PX 3000i",
        "Vertiv Liebert GXT5 UPS",
    ):
        x = classify_title(title)
        assert "ups" in x
        assert "power_protection" in x
