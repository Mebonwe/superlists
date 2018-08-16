from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Chrome()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		#使用浏览器打开首页
		self.browser.get('http://localhost:8000')

		#浏览器的标题为To-Do
		self.assertIn("To-Do", self.browser.title)
		header_text =self.browser.find_element_by_tag_name('h1').text
		self.assertIn("To-Do", header_text)
		

		#输入一个待办事项
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		#文本框中输入内容
		inputbox.send_keys('Buy peacock feathers')
		#回车，页面更新
		#待办事项表格中显示1：Buy peacock feathers
		inputbox.send_keys(Keys.ENTER)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Buy peacock feathers' ,[row.text for row in rows])

		#页面中再次显示文本框，可输入其他待办事项
		#输入"Use peacock feathers to make a fly"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		#页面再次更新，显示两个待办事项
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Buy peacock feathers' ,[row.text for row in rows])
		self.assertIn('2: Use peacock feathers to make a fly', [row.text for row in rows])

		#判断网站是否记住待办清单
		#网站生成了一个唯一的URL
		#页面中有文字解说这个功能
		self.fail("Finish the test!")
		#访问指定的url，清单还在


if __name__ == '__main__':
	unittest.main(warnings="ignore")