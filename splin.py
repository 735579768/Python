from splinter import Browser
browser = Browser()
#browser = Browser('chrome')
browser.visit('https://kyfw.12306.cn/otn/leftTicket/init')
browser.fill('leftTicketDTO.from_station_name','郑州')
browser.fill('leftTicketDTO.to_station_name','汝州')
browser.fill('leftTicketDTO.train_date','2015-12-31')

browser.find_by_id('query_ticket').click()

