import webbrowser

def open_in_browser(site,browser):
	webbrowser.get(browser).open_new_tab(site)
