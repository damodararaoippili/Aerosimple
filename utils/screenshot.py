import os,time
def capture_screenshot(browser,name='failed screen_shots'):
    folder = os.path.join(os.path.dirname(__file__),'..','Reports','Failed scripts_screenshots')
    os.makedirs(folder,exist_ok=True)

    time_stamp = time.strftime("%Y%m%d-%H%M%S")
    file_name = f"{name}_{time_stamp}.png"
    path = os.path.join(folder,file_name)
    browser.save_screenshot(path)
    return path