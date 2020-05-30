import pytest

from baseapi.tagapi import tagapi


class Test_tag():
    tag = tagapi()
    test_data = tag.load_yml("../yaml/tag/test_setup.yml")

    @classmethod
    # @pytest.mark.param("old_name,new_name",test_data)该用法不可行
    def setup_class(cls):
        data = cls.tag.get_tag()
        for names in cls.test_data:
            for name in names:
                tag_id = cls.tag.base_jsonpath(data, f'$..tag[?(@.name=="{name}")].id')
                if tag_id:
                    cls.tag.delete_tag(tag_id=tag_id[0])

    @pytest.mark.parametrize("old_name,new_name", test_data)
    def test_all(self, old_name, new_name):
        for name in (old_name, new_name):
            tag_id = tagapi.base_jsonpath(self.tag.get_tag(), expr=f'$..tag[?(@.name=="{name}")].id')
            if tag_id:
                assert self.tag.delete_tag(tag_id[0])['errcode'] == 0
        assert self.tag.add_tag(tag_name=old_name)['errcode'] == 0
        tag_id = self.tag.base_jsonpath(self.tag.get_tag(), expr=f'$..tag[?(@.name=="{old_name}")].id')[0]
        assert self.tag.alter_tag(tag_id=tag_id, name=f'{new_name}')['errcode'] == 0

    def test_add_tag(self):
        assert self.tag.add_tag(tag_name="wangwu")['errcode'] == 0

    def test_alter_tag(self):
        tag_id = self.tag.base_jsonpath(self.tag.get_tag(), expr='$..tag[?(@.name=="wangwu")].id')[0]
        assert self.tag.alter_tag(tag_id=tag_id, name='zhangsan')['errcode'] == 0

    def test_get_tag(self):
        assert self.tag.get_tag()['errcode'] == 0

    def test_delete_tag(self):
        tag_id = self.tag.base_jsonpath(self.tag.get_tag(), expr='$..tag[?(@.name=="zhangsan")].id')[0]
        assert self.tag.delete_tag(tag_id=tag_id)['errcode'] == 0
