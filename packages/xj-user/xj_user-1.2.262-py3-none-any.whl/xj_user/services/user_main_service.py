import sys
from django.forms import model_to_dict

from xj_user.utils.custom_tool import write_to_log
if 'xj_role' in sys.modules:
    from xj_role.services.user_group_service import UserGroupService
from ..models import Platform, UserSsoServe
from ..services.login_service import LoginService
from ..utils.utility_method import generate_password, replace_placeholders
from xj_user.services.user_relate_service import UserRelateToUserService


class UserMainService:

    @staticmethod
    def register(params):
        platform_id = params.get("platform_id", None)  # 平台。不应该支持ID传入，无法数据移植。20230507 by Sieyoo
        platform_code = params.get("platform_code", None)
        account = params.get('account', '')
        nickname = params.get('nickname', '')
        phone = params.get('phone', '')
        password = str(params.get('password', ''))

        if platform_code:
            platform_set = Platform.objects.filter(platform_code=platform_code).first()
            if not platform_set:
                return None, "platform不存在平台名称：" + platform_code
            platform_id = model_to_dict(platform_set)['platform_id']

        if platform_id:
            platform_set = Platform.objects.filter(platform_id=platform_id).first()
            if not platform_set:
                return None, "所属平台不存在"
            platform_code = model_to_dict(platform_set)['platform_code']

        account_serv, error_text = LoginService.check_account(account, platform_code, "REGISTER")
        if error_text:
            return None, error_text

        register_serv, register_error = LoginService.register_write(account, nickname, phone, platform_id,
                                                                    platform_code, password)
        if register_error:
            return None, register_error

        return register_serv, None

    """
     登录整合接口，支持以下几种登录方式：
          1、PASSWORD 账户密码登录
          2、SMS 短信验证码登录 （支持多账号登录*）
          3、WECHAT_APPLET 微信小程序授权登录
          4、WECHAT_WEB 微信公众号授权登录
          5、WECHAT_APP 微信APP授权登录

    """

    @staticmethod
    def login_integration_interface(params):
        data = {}
        # ----------------------------获取信息----------------------------------------
        # TODO platform_id字段 即将弃用，改为platform_code 20230507 by Sieyoo
        platform_id = params.get("platform_id", None)  # 平台。不应该支持ID传入，无法数据移植。20230507 by Sieyoo
        platform_code = params.get("platform_code", None)
        user_id = params.get("user_id", None)  # 用户id
        login_type = params.get("login_type", None)  # 支持的登录方式
        openid_code = params.get("openid_code", None) or params.get("code", None)  # 微信登录code
        phone_code = params.get("phone_code", None)  # 微信手机号code
        sms_code = params.get("sms_code", None)  # 短信验证码
        # sso_serve_id = params.get("sso_serve_id", None)  # 单点登录用户平台，弃用字段设计
        sso_serve_code = params.get("sso_serve_code", None)  # 单点登录用户平台
        phone = params.get("phone", None)  # 手机号
        other_params = params.get("other_params", None)
        account = params.get("account", None)  # 账户
        password = params.get("password", None)  # 密码
        bind_data = params.get("bind_data", None)  # 绑定的数据
        apple_logo = params.get("apple_logo", None)  # 苹果
        # ------------------------边界检查----------------------------------------------
        if not login_type:
            return None, "登录方式不能为空"
        if platform_code:
            platform_set = Platform.objects.filter(platform_code=platform_code).first()
            if not platform_set:
                return None, "platform不存在平台名称：" + platform_code
            platform_id = model_to_dict(platform_set)['platform_id']

        if platform_id:
            platform_set = Platform.objects.filter(platform_id=platform_id).first()
            if not platform_set:
                return None, "所属平台不存在"
            platform_code = model_to_dict(platform_set)['platform_code']

        # 平台ID不具有可识别性，禁止传此参数 by Sieyoo at 20231219
        # if sso_serve_id:
        #     sso_server_set = UserSsoServe.objects.filter(id=sso_serve_id).first()
        #     if not sso_server_set:
        #         return None, "单点登录平台不存在：" + str(sso_serve_id)
        #     sso_serve_id = model_to_dict(sso_server_set)['id']

        sso_serve_id = None
        if sso_serve_code:
            sso_server_set = UserSsoServe.objects.filter(sso_code=sso_serve_code).first()
            if not sso_server_set:
                return None, "单点登录平台不存在：" + sso_serve_code
            sso_serve_id = model_to_dict(sso_server_set)['id']
        # ------------------------登录类型判断----------------------------------------------

        if other_params is None:
            other_params = {}
        try:
            current_user, user_err = LoginService.type_judgment(
                login_type=login_type, account=account, phone=phone, password=password, platform_code=platform_code,
                sms_code=sms_code, user_id=user_id, openid_code=openid_code, phone_code=phone_code, bind_data=bind_data,
                apple_logo=apple_logo)
            print("> login_integration_interface: current_user, user_err:", current_user, user_err)
            if user_err:
                return None, user_err

            # 设计错误，严禁在函数之间传递实例（尤其是模型实例），转为字典对象 by Sieyoo at 20231219
            # if isinstance(current_user.get("user_info", None), list):
            #     return current_user, None
            # else:

            # 登录逻辑处理
            # data, err = LoginService.logical_processing(current_user.get("user_info", None),
            #                                             current_user.get("phone", None),
            #                                             current_user.get("appid", None),
            #                                             current_user.get("openid", None),
            #                                             current_user.get("unionid", None),
            #                                             platform_id,
            #                                             platform_code, other_params,
            #                                             current_user.get("wx_login_type", None))
            # if err:
            #     return None, err

        except Exception as e:
            write_to_log(
                prefix="登录异常",
                content='---用户登录异常：' + str(e) + '---',
                err_obj=e
            )

        # ------------------------登录逻辑处理的移植代码（LoginService.logical_processing）------------------------

        # 如果不存在则注册
        user_info = current_user.get("user_info", None)
        is_create = False
        if not user_info:
            user_info = LoginService.register_phone_account(phone=current_user.get("phone", None),
                                                                platform_code=platform_code)
            is_create = True

        # 检查单点登录信息（查询并创建）针对小程序、公众号、APP，同一微信平台绑定过的绑定
        if sso_serve_id:
            sso_set, sso_err = LoginService.sso_verify(
                sso_serve_id=sso_serve_id, user_id=user_info.get('id', ""), appid=current_user.get("appid", None),
                is_exist=True, sso_unicode=current_user.get("openid", None),
                union_code=current_user.get("unionid", None))
            if sso_err:
                return None, sso_err

        # TODO token可以考虑让各个子服务独立获取token，而不是公共生成Token，当然，这样设计好不好有待商考 20230507 by Sieyoo
        token = LoginService.make_token(user_info.get('id', ""), user_info.get("user_name", ""), platform_id,
                                        platform_code)
        password = generate_password(12)
        # 修改用户登录信息，绑定token
        auth_set, auth_err = LoginService.bind_token(user_id=user_info.get('id', ""), token=token,
                                                     is_create=is_create, password=password)
        if auth_err:
            return None, auth_err

        # 登录逻辑处理-------本代码方法注掉，平铺到下方
        # data, err = LoginService.logical_processing(current_user.get("user_info", None),
        #                                             current_user.get("phone", None),
        #                                             current_user.get("appid", None),
        #                                             current_user.get("openid", None),
        #                                             current_user.get("unionid", None),
        #                                             platform_id,
        #                                             platform_code, other_params,
        #                                             current_user.get("wx_login_type", None))
        # if err:
        #     return None, err

        wx_login_type = ""  # 登录类型
        # 代码理解：如果是新用户，注册成功并发送短信通知
        if is_create:
            # 注册成功后发送短信通知
            sms_data = {
                "phone": phone,
                "platform": 'ALi',
                "account": user_info.get("user_name", ""),
                "pwd": password,
                "type": "PWD"
            }

            if wx_login_type == "applet" or wx_login_type == "sms":
                sms_set, sms_err = SmsService.bid_send_sms(sms_data)
                if sms_err:
                    write_to_log(
                        prefix="首次登录写入用户详细信息异常",
                        content='---首次登录写入用户详细信息异常：' + str(sms_err) + '---',
                        err_obj=sms_err
                    )

            try:
                other_params.setdefault("user_id", user_info.get('id', ""))
                other_params.setdefault("score", "5")  # 用户评分初始化，镖行天下业务逻辑 TODO 后期业务抽离，路程控制
                data, detail_err = DetailInfoService.create_or_update_detail(other_params)
                if detail_err:
                    raise Exception(detail_err)
            except Exception as e:
                write_to_log(
                    prefix="首次登录写入用户详细信息异常",
                    content='---首次登录写入用户详细信息异常：' + str(e) + '---',
                    err_obj=e
                )
            # 用户第一次登录即注册，绑定用户的分组ID
            try:
                group_id = other_params.get("group_id")
                if group_id:
                    data, err = UserGroupService.user_bind_group(user_id=user_info.get('id', ""), group_id=group_id)
                    write_to_log(
                        prefix="group_id:" + str(other_params.get("group_id", "")) + "绑定部门ID异常",
                        content=err
                    )
            except Exception as err:
                write_to_log(
                    prefix="绑定部门ID异常",
                    content="group_id:" + str(other_params.get("group_id", "")),
                    err_obj=err
                )
        # 代码理解：否则是已注册过的用户，同时则将其邀请关系进行绑定？
        else:
            # 绑定用户关系 邀请关系和收益关系
            data, relate_err = UserRelateToUserService.bind_bxtx_relate(params=other_params, user_info=user_info)
            if relate_err:
                write_to_log(
                    prefix='绑定用户关系异常：' + str(relate_err),
                    content='当前用户ID:' + str(user_info.get("id", "")) + '\n detail_params:' + json.dumps(
                        other_params),
                    err_obj=relate_err
                )

        return {'token': "Bearer " + auth_set.token, 'user_info': user_info}, None
