import requests

# 获取access_token GET https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/mp-access-token/getAccessToken.html
wx_token_url = 'https://api.weixin.qq.com/cgi-bin/token'
# 小程序登录 GET https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html
wx_login_url = "https://api.weixin.qq.com/sns/jscode2session"
# 获取手机号 POST (小程序) https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-info/phone-number/getPhoneNumber.html
wx_get_phone_url = "https://api.weixin.qq.com/wxa/business/getuserphonenumber"
# 换取网页授权 access_token GET https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html
wx_token_wbe_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'


def get_openid(wechat_type, params):
    """
    :param appid（微信的唯一标识）:
    :param secret（微信的appsecret）:
    :param code（openid登录的code）:
    :return:(err,data)
    """
    appid = params.get("appid", "")
    secret = params.get("secret", "")
    openid_code = params.get("openid_code", "") or params.get("code", "")  # 旧名code，不易读，新名称改为openid_code. Sieyoo
    phone_code = params.get("phone_code", "")
    phone = ""
    if wechat_type == "WECHAT_APPLET":
        access_token_url = wx_token_url
        userinfo_url = wx_login_url
    elif wechat_type == "WECHAT_WEB":
        userinfo_url = wx_token_wbe_url
    elif wechat_type == "WECHAT_APP":
        userinfo_url = wx_token_wbe_url

    if not appid or not secret or not openid_code:
        return None, f"缺少参数: {'appid' if not appid else 'secret' if not secret else 'openid_code'}! " \
                     f"File: wechat.py, Method: get_openid()"

    # print("wechat.py get_openid: appid, secret, openid_code, phone_code:", appid, secret, openid_code, phone_code)

    # 获取 Access token
    if wechat_type == "WECHAT_APPLET":
        get_access_token = requests.get(access_token_url, params={'appid': appid,
                                                                  'secret': secret,
                                                                  'grant_type': "client_credential"}, timeout=3,
                                        verify=False, headers={'content-type': 'application/json'}).json()
        # print("get_openid get_access_token:", get_access_token)
        if get_access_token.get("errcode", None):
            return None, str(get_access_token)

    # 获取用户基本信息
    wechat_user_info = requests.get(userinfo_url, params={'appid': appid,
                                                       'secret': secret,
                                                       # 'code': openid_code,
                                                       'js_code': openid_code,
                                                       'grant_type': "authorization_code"}, timeout=3,
                                 verify=False, headers={'content-type': 'application/json'}).json()
    # print("get_openid wechat_user_info:", wechat_user_info)
    if wechat_user_info.get("errcode", None):
        return None, str(wechat_user_info)

    # 获取用户手机号（只支持小程序）
    # print("wechat.py get_openid: phone_code, get_access_token:", phone_code, get_access_token)
    if phone_code:
        get_phone = requests.post(wx_get_phone_url + "?access_token={}".format(get_access_token.get('access_token')),
                                  json={'code': phone_code}, timeout=3,
                                  verify=False, headers={'content-type': 'application/json'}).json()
        # print("get_openid get_phone:", get_phone)
        if get_phone.get("errcode", None):
            return None, str(get_phone)
        phone = get_phone['phone_info']['phoneNumber']

    user_info = {
        "openid": wechat_user_info.get("openid", None),
        "unionid": wechat_user_info.get("unionid", None) if wechat_user_info.get("unionid", None) else "",
        "phone": phone
    }
    return user_info, None
