import csv
from pathlib import Path

from scripts.utilities.manifest_ingestion import (
    manifest_rows,
    read_plantseg_metadata,
)


def test_read_plantseg_metadata(tmp_path: Path) -> None:
    metadata_path = tmp_path / "datasets" / "raw" / "plantseg" / "Metadatav2.csv"
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(
        "Name,Index,Plant,Disease,Resolution,Label file,Mask ratio,URL,Split\n"
        "apple_black_rot_1.jpg,0,Apple,apple black rot,640x480,apple_black_rot_1.png,0.04,http://example.com,Training\n",
        encoding="utf-8",
    )

    expected = {"apple_black_rot_1.jpg": "apple_black_rot_1.png"}
    assert read_plantseg_metadata(metadata_path=metadata_path) == expected


def test_manifest_rows_skips_plantseg_annotation_rows(tmp_path: Path, monkeypatch) -> None:
    inventory_dir = tmp_path / "outputs" / "inventory"
    inventory_dir.mkdir(parents=True)
    plantseg_inventory = inventory_dir / "plantseg_inventory.csv"
    plantseg_inventory.write_text(
        "image_id,dataset,relative_path,filename,crop,disease,extension,file_size_bytes,readable,width,height\n"
        "id1,PlantSeg,images/test/apple_black_rot_1.jpg,apple_black_rot_1.jpg,apple,black_rot,.jpg,1234,True,640,480\n"
        "id2,PlantSeg,annotations/test/apple_black_rot_1.png,apple_black_rot_1.png,apple,black_rot,.png,2345,True,268,172\n",
        encoding="utf-8",
    )

    monkeypatch.setattr("scripts.utilities.manifest_ingestion.DATASET_INVENTORY_PATHS", {
        "plantseg": plantseg_inventory,
    })
    monkeypatch.setattr("scripts.utilities.manifest_ingestion.PLANTSEG_METADATA_PATH", tmp_path / "datasets" / "raw" / "plantseg" / "Metadatav2.csv")
    (tmp_path / "datasets" / "raw" / "plantseg").mkdir(parents=True, exist_ok=True)
    (tmp_path / "datasets" / "raw" / "plantseg" / "Metadatav2.csv").write_text(
        "Name,Index,Plant,Disease,Resolution,Label file,Mask ratio,URL,Split\n"
        "apple_black_rot_1.jpg,0,Apple,apple black rot,640x480,apple_black_rot_1.png,0.04,http://example.com,Training\n",
        encoding="utf-8",
    )

    rows = list(manifest_rows())
    assert len(rows) == 1
    assert rows[0].image_id == "id1"
    assert rows[0].mask_path == "plantseg/annotations/apple_black_rot_1.png"
