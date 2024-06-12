class MobileCmdConst:
    class App:
        CLEAR_APP = 'mobile: clearApp'
        ACTIVATE_APP = 'mobile: activateApp'
        TERMINATE_APP = 'mobile: terminateApp'

    class Permission:
        SET_PERMISSION_ANDROID = 'mobile: changePermissions'
        GET_PERMISSION_ANDROID = 'mobile: getPermissions'
        SET_PERMISSION_IOS = 'mobile: setPermission'
        GET_PERMISSION_IOS = 'mobile: getPermission'

    class Gesture:
        SCROLL = 'mobile: scroll'
        CLICK = 'mobile: clickGesture'
        LONG_CLICK = 'mobile: longClickGesture'
