
from unittest import skip
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
	@skip
	def test_cannot_add_empty_list_items(self):
		# 用户A访问首页，不小心提交了空的待办事项
		# 输入框中没有输入内容就点击了enter键
		# 首页刷新，显示错误信息
		# 提示待办事项不能为空
		# 输入某些文字，再次提交，成功
		# 再次提交空的待办事项
		# 再次显示错误信息
		# 输入文字之后显示正常
		self.fail("write me!")
