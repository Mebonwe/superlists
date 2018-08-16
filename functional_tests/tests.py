from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Chrome()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self,row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		#使用浏览器打开首页
		self.browser.get(self.live_server_url)

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
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		self.check_for_row_in_list_table('1: Buy peacock feathers')

		#页面中再次显示文本框，可输入其他待办事项
		#输入"Use peacock feathers to make a fly"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		#页面再次更新，显示两个待办事项
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

		#用户B访问了网站
		##使用心得浏览器会话
		##确保用户A的信息不会从cokkie中泄漏出来
		self.browser.quit()
		self.browser = webdriver.Chrome()

		# 用户B访问首页
		# 用户B看不到用户A的清单
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('to make a fly', page_text)

		# 用户B新输入一个新的待办事项
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)

		#用户B获得自己唯一的URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		#当前页面不会展示用户A的待办清单
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)
