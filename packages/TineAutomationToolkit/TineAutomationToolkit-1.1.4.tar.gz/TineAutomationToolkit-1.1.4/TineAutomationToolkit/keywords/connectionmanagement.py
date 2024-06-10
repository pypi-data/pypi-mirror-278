# -*- coding: utf-8 -*-

import robot

from robot.libraries.BuiltIn import BuiltIn
from TineAutomationToolkit.utils.applicationcache import ApplicationCache
from AppiumLibrary.keywords._logging import _LoggingKeywords

cache_app = BuiltIn()
method_cache_app = ApplicationCache()
log = _LoggingKeywords()

class ConnectionManagement:

    def __init__(self):
        #เนื่องจากปัญหาเรื่องโครงสร้าง structure เลยยังไม่สามารถใช้ได้
        # self._bi = BuiltIn()
        pass
    #KeyWord
    
    def native_close_application_session(self,alias=None):
        """Close Application And Quit Seesion

        =========================================================
        
        ปิดแอพปัจจุบันและปิดเซสชัน"""
        driver = self._current_application()
        log._debug('Closing application with session id %s' % self._current_application().session_id)
        method_cache_app.register(driver,alias)
        method_cache_app.close_all()

    def native_background_application(self, seconds=5):
        """
        Puts the application in the background on the device for a certain
        duration.

        =========================================================

        วางแอปพลิเคชันไว้ในพื้นหลังของอุปกรณ์เป็นระยะเวลาหนึ่ง.
        """
        self._current_application().background_app(seconds)
        
    def native_activate_application(self, app_id):
        """
        Activates the application if it is not running or is running in the background.
        Args:
         - app_id - BundleId for iOS. Package name for Android.

        New in AppiumLibrary v2

        =========================================================

        
        เปิดใช้งานแอปพลิเคชันหากมันไม่ได้รันอยู่หรือรันอยู่ในพื้นหลัง
        อาร์กิวเมนต์:
        - app_id - BundleId สำหรับ iOS, ชื่อแพ็คเกจสำหรับ Android.
        """
        self._current_application().activate_app(app_id)

    def native_terminate_application(self, app_id):
        """
        Terminate the given app on the device

        Args:
         - app_id - BundleId for iOS. Package name for Android.

        New in AppiumLibrary v2

        =========================================================
        
        ยุติแอปพลิเคชันที่กำหนดไว้บนอุปกรณ์แต่ยัง active อยู่ในระบบ
        สามารถเปิดต่อได้

        อาร์กิวเมนต์:  

        app_id - BundleId สำหรับ iOS, ชื่อแพ็คเกจสำหรับ Android.
        ใหม่ใน AppiumLibrary เวอร์ชัน 2
        """
        return self._current_application().terminate_app(app_id)
    
    def native_get_window_height(self):
        """Get current device height.

        Example:
        | ${width}       | Get Window Width |
        | ${height}      | Get Window Height |
        | Click A Point  | ${width}         | ${height} |

        New in AppiumLibrary 1.4.5
        """
        return self._current_application().get_window_size()['height']
    
    def native_get_window_width(self):
        """Get current device width.

        Example:
        | ${width}       | Get Window Width |
        | ${height}      | Get Window Height |
        | Click A Point  | ${width}          | ${height} |

        New in AppiumLibrary 1.4.5
        """
        return self._current_application().get_window_size()['width']
    
    def commond_install_app(self, app_path, app_package):
        """ *******Not available wait for update flutter*******
        Install App via Appium
        
        Android .

        - app_path - path to app (.apk)
        - app_package - package of install app to verify

        Ios .

        - app_path - path to app (.app | .ipa)
        - bundleId - package of install app to verify
        """
        driver = self._current_application()
        driver.install_app(app_path)
        return driver.is_app_installed(app_package)
    
    
    
    #PRIVATE_FUNCTION
        
    def _current_application(self):
        """Return the instance of the current application
        From AppiumFlutterLibrary

        =========================================================

        คืนค่าอินสแตนซ์ของแอปพลิเคชันปัจจุบัน
        จาก AppiumFlutterLibrary
        """
        return cache_app.get_library_instance('AppiumFlutterLibrary')._current_application()
        # return self._bi.get_library_instance('AppiumFlutterLibrary')._current_application()

    def get_source(self):
        """Returns the entire source of the current page.
        
        =========================================================

        ฟังก์ชันนี้จะส่งคืนสตริงที่มีซอร์สโค้ด HTML ของหน้าเว็บที่กำลังแสดงอยู่ในเบราว์เซอร์ในขณะนั้น 
        ซึ่งสามารถนำไปใช้ในการตรวจสอบหรือวิเคราะห์โครงสร้างหรือเนื้อหาของหน้าเว็บได้
        """
        return self._current_application().page_source
        