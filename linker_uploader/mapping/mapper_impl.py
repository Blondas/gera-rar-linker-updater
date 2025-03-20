from linker_uploader.db2.db_connection import DBConnection

from linker_uploader.mapping.mapping_entry import MappingEntry
from linker_uploader.mapping.mapper import Mapper

class MapperImpl(Mapper):
    def __init__(
        self,
        _db_connection: DBConnection,
        table_name: str
    ) -> None:
        self._db2_connection = _db_connection
        self._query = (
        "SELECT "
        "src_tsm_server_name, "
        "src_tsm_filespace_name, "
        "scr_tsm_btch_filename, "
        "status, "
        "dst_agid_name "
        f"FROM {table_name}"
    )

    def get_mappings(self) -> list[MappingEntry]:
        rows = self._db2_connection.fetch_all(self._query)
        return [MappingEntry(*row) for row in rows]
        