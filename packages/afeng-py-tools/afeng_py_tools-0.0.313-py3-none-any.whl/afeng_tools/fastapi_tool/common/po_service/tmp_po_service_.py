from afeng_tools.fastapi_tool.common.po_service.base_po_service import PoService


class TmpSortPoService(PoService):
    """
    使用示例：tmp_sort_po_service = TmpSortPoService(app_info.db_code, TmpSortInfoPo)
    """
    _table_name_ = "tmp_sort_info"

    def delete_by_unique_code(self, unique_code: str):
        """通过唯一码删除"""
        return self.delete(self.model_type.unique_code == unique_code)

    def add_in_list(self, unique_code: str, in_data_list: list):
        """添加in列表"""
        tmp_po_list = []
        for index, tmp_in_data in enumerate(in_data_list):
            tmp_po_list.append(self.model_type(
                type_code='default',
                unique_code=unique_code,
                sort_value=str(tmp_in_data),
                sort_index=(index + 1)
            ))
        return self.add_batch(tmp_po_list)
