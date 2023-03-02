# -*- encoding:utf-8 -*-
import os
from djchoices import ChoiceItem
from djchoices import DjangoChoices
import decimal

# 所有数据表前缀:
MODEL_PREFIX = "matrix_"


# django-choices usage:
# defination: CONSTANT_NAME = ChoiceItem("db value", "label")
# as contant name: CoinType.BTC => 0
# as model choices: coin_type = IntegerField(choices=CoinType.choices)
# get label: CoinType.get_choice("db value").label


#########################################################
#            常量定义规范
# type:  (-1, 1,2,3...)
# status: (..-3, -2, -1, 1,2,3...)
#
#########################################################


class DemoFieldType(DjangoChoices):
    """自定义type

        - 默认值 -1
        - 类型值 >=1, (剔除0值)

    """
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    TYPE_01 = ChoiceItem(1, 'Type: 01')
    TYPE_02 = ChoiceItem(2, 'Type: 02')
    TYPE_03 = ChoiceItem(3, 'Type: 03')
    TYPE_04 = ChoiceItem(4, 'Type: 04')


class DemoFieldStatus(DjangoChoices):
    """自定义Status

        - 默认值 -1
        - 完成: 1
        - 失败: 0
        - 正常中间状态值: >1
        - 异常中介状态值: <-1

    """
    STAGE_F04 = ChoiceItem(-5, 'Stage: 04')  # 异常状态1
    STAGE_F03 = ChoiceItem(-4, 'Stage: 03')  # 异常状态1
    STAGE_F02 = ChoiceItem(-3, 'Stage: 02')  # 异常状态1
    STAGE_F01 = ChoiceItem(-2, 'Stage: 01')  # 异常状态1
    #
    # error-mid-status:
    #
    UNDEFINED = ChoiceItem(-1, 'Undefined')  # 默认值
    FAILED = ChoiceItem(0, 'FAILED')  # 失败
    COMPLETED = ChoiceItem(1, 'Completed')  # 完成
    #
    # ok-mid-status:
    #
    STAGE_01 = ChoiceItem(2, 'Stage: 01')  # 中间状态1
    STAGE_02 = ChoiceItem(3, 'Stage: 02')  # 中间状态2
    STAGE_03 = ChoiceItem(4, 'Stage: 03')  # 中间状态3
    STAGE_04 = ChoiceItem(5, 'Stage: 04')  # 中间状态4


#########################################################
#            auth part
#########################################################

# 用户注册状态:
class UserStatus(DjangoChoices):
    UNDEFINED = ChoiceItem("undefined", 'Undefined')
    ENABLED = ChoiceItem("enabled", 'Enabled')
    DISABLED = ChoiceItem("disabled", 'Disabled')
    ENGINE_COMPLETED = ChoiceItem("engine_completed", 'Engine Completed')


# 用户角色:
class UserRoleType(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    CUSTOMER = ChoiceItem(0, 'Customer')  # 客户
    ROBOT = ChoiceItem(1, 'Robot')  # 交易程序: 机器人
    #
    ADMIN = ChoiceItem(2, 'Staff: Admin')  # 员工: 管理员
    DEV = ChoiceItem(3, 'Staff: Dev')  # 员工: 开发人员
    #
    SALES = ChoiceItem(4, 'Staff: Sales')  # 员工: 销售
    CUSTOMER_SERVICE = ChoiceItem(5, 'Staff: Customer Service ')  # 员工: 客服
    FINANCIAL = ChoiceItem(6, 'Staff: Financial')  # 员工: 财务


# 用户注册方式:
class UserRegisterType(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    EMAIL = ChoiceItem(0, 'Email')
    SMS = ChoiceItem(1, 'SMS')
    GOOGLE_2FA = ChoiceItem(2, 'Google 2FA')
    OTHER = ChoiceItem(3, 'Other Way')


# 用户注册码状态:
class UserRegisterCodeStatus(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')  # 未定义
    PENDING = ChoiceItem(0, 'Pending: Available')  # 待激活(未登录)
    COMPLETED = ChoiceItem(1, 'Completed: Assigned')  # 已激活(密码覆写)


# 用户帐号状态:
class UserAccountStatus(DjangoChoices):
    DISABLED = ChoiceItem(-3, 'Disabled')  # 禁用
    DELETED = ChoiceItem(-2, "Deleted")  # 删除
    UNDEFINED = ChoiceItem(-1, 'Undefined')  # 未定义
    ENABLED = ChoiceItem(0, 'Enabled All')  # 完全激活
    EXCHANGE_ENABLED = ChoiceItem(1, 'Stage1: Exchange Account Enabled')  # 交易所账号激活
    ENGINE_ENABLED = ChoiceItem(2, 'Stage2: Engine Account Enabled')  # 引擎账号激活


# 旧 leaf 用户迁移状态:
class UserMigrationStatus(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')  # 未定义
    PENDING = ChoiceItem(0, 'Enabled All')  # 待激活(未登录)
    COMPLETED = ChoiceItem(1, 'Final Completed')  # 已激活(密码覆写)


# 注册方式:
class RegisterType(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    EMAIL = ChoiceItem(0, 'EMAIL')
    SMS = ChoiceItem(1, 'SMS')


# 2fa device status:
class TOTPDeviceStatus(DjangoChoices):
    DELETED = ChoiceItem(-2, "Deleted")
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    REGISTERED = ChoiceItem(0, "Registered")
    ACTIVATED = ChoiceItem(1, 'Activated')


#########################################################
#            transaction part
#########################################################


# 法币类型
class FiatType(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    CNY = ChoiceItem(0, 'CNY')
    USD = ChoiceItem(1, 'USD')
    EUR = ChoiceItem(2, 'EU')
    HKD = ChoiceItem(3, 'HKD')
    JPY = ChoiceItem(4, 'JPY')


# 用户银行卡账户类型
class AccountType(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    DEPOSIT = ChoiceItem(0, 'deposit')
    WITHDRAW = ChoiceItem(1, 'withdraw')


FiatServiceChargeMin = {
    FiatType.USD: (10000, 30, 0.003)
}


# 人民币开户行:
class FiatBankCNY(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    ABC = ChoiceItem(0, "ABC")


# 美元开户行:
class FiatBankUSD(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')


# 港币开户行:
class FiatBankHKD(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')


# 日元开户行:
class FiatBankJPY(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')


class CoinType(DjangoChoices):
    """
    BTC = (0,'BTC')
    ETC = (1,'ETC')
    ETH = (2,'ETH')
    BCH = (3,'BCH')
    ICO = (4,'ICO')
    REP = (5,'REP')
    LTC = (6,'LTC')
    DASH = (7,'DASH')
    MONA = (8,'MONA')
    """
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    BTC = ChoiceItem(0, 'BTC')
    ETC = ChoiceItem(1, 'ETC')
    ETH = ChoiceItem(2, 'ETH')
    BCH = ChoiceItem(3, 'BCH')
    ICO = ChoiceItem(4, 'ICO')
    REP = ChoiceItem(5, 'REP')
    LTC = ChoiceItem(6, 'LTC')
    DASH = ChoiceItem(7, 'DASH')
    MONA = ChoiceItem(8, 'MONA')
    USDT = ChoiceItem(9, 'USDT')


class CurrencyType(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, "Undefined")
    COIN_TYPE = ChoiceItem(1, "Coin Type")
    FIAT_TYPE = ChoiceItem(2, "Fiat Type")


class MarketFeeType(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, "Undefined")
    SALE = ChoiceItem(1, "Sale")
    BUY = ChoiceItem(2, "Buy")


class CoinSeries(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    BTC_SERIES = ChoiceItem(0, 'BTC series')
    ETC_SERIES = ChoiceItem(1, 'ETC series')
    ETH_SERIES = ChoiceItem(2, 'ETH series')
    BCH_SERIES = ChoiceItem(3, 'BCH series')
    ICO_SERIES = ChoiceItem(4, 'ICO series')
    REP_SERIES = ChoiceItem(5, 'REP series')
    LTC_SERIES = ChoiceItem(6, 'LTC series')
    DASH_SERIES = ChoiceItem(7, 'DASH series')
    MONA_SERIES = ChoiceItem(8, 'MONA series')
    USDT_SERIES = ChoiceItem(9, 'USDT, series')


class IdImgStatus(DjangoChoices):
    NULL = ChoiceItem(0, 'null')
    PENDING = ChoiceItem(1, 'pending')
    INVALID = ChoiceItem(2, 'invalid')
    VERIFIED = ChoiceItem(3, 'verified')


class ComplianceLockStatus(DjangoChoices):
    UNLOCKED = ChoiceItem(0, 'unlocked')
    LOCKED = ChoiceItem(1, 'locked')
    UNTRIGGERED = ChoiceItem(2, 'untriggered')


class Gender(DjangoChoices):
    MALE = ChoiceItem(0, 'male')
    FEMALE = ChoiceItem(1, 'female')


class TransactionStatus(DjangoChoices):
    """链上交易状态

    """
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    UNCONFIRMED = ChoiceItem(0, 'Unconfirmed')
    PENDING = ChoiceItem(1, 'Pending')
    BEFORE_COMPLETED = ChoiceItem(4, 'Before completed')
    COMPLETED = ChoiceItem(2, 'Completed')
    FAILED = ChoiceItem(3, 'Failed')


class DepositStatus(DjangoChoices):
    """充值状态:

    """
    UN_REVIEW = ChoiceItem(-4, 'Un review')  # 未审核
    ENGINE_FAILED = ChoiceItem(-3, 'Failed')  # 交易引擎通知失败
    FAILED = ChoiceItem(-2, 'Failed')                     # 失败
    UNDEFINED = ChoiceItem(-1, 'Undefined')               # 未定义
    #
    COMPLETED = ChoiceItem(0, 'Final Completed')          # 最终完成状态
    #
    CHAIN_PENDING = ChoiceItem(1, 'Chain Pending')        # 链上: pending
    CHAIN_COMPLETED = ChoiceItem(2, 'Chain Completed')    # 链上: 完成
    #
    ENGINE_PENDING = ChoiceItem(3, 'Engine Pending')      # 交易引擎: pending
    ENGINE_COMPLETED = ChoiceItem(4, 'Engine Completed')  # 交易引擎: complete


class FiatDepositStatus(DjangoChoices):
    """法币充值状态:

    """
    SIMPLES_DECLINED = ChoiceItem(-4, 'simplex declined')
    REJECT = ChoiceItem(-3, 'Reject')  # 审核拒绝
    FAILED = ChoiceItem(-2, 'Failed')                     # 失败
    UNDEFINED = ChoiceItem(-1, 'Undefined')               # 未定义
    COMPLETED = ChoiceItem(0, 'Final Completed')          # 最终完成状态
    #
    UN_REVIEW = ChoiceItem(1, 'Un review')  # 待审核
    REVIEWED = ChoiceItem(2, 'Reviewed')                 # 审核完成
    #
    ENGINE_PENDING = ChoiceItem(3, 'Engine Pending')      # 交易引擎: pending
    ENGINE_COMPLETED = ChoiceItem(4, 'Engine Completed')  # 交易引擎: complete
    #
    SIMPLEX_PENDING = ChoiceItem(5, 'simples pending')    # simples: pending
    SIMPLES_APPROVED = ChoiceItem(6, 'simples approved')


class FiatDepositType(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    BANK_TRANSFER = ChoiceItem(0, 'bank transfer')
    SIMPLEX = ChoiceItem(1, 'simplex')


class FiatDepositAllowStatus(DjangoChoices):

    REVIEWED = ChoiceItem(2, 'Reviewed')                 # 审核完成
    REJECT = ChoiceItem(-3, 'Reject')                 # 审核拒绝


class EngineResponseCode(DjangoChoices):
    """Engine Response 返回码:

        "0": Operation Success
        "1": Invalid Params
        "-1": Operation Failed
        "99": System Error;
        "12" TRANSACTION ID IS NOT UNIQUE
    """

    INVALID_PARAMS = ChoiceItem(1, 'Invalid Params')  # 参数错误
    OPT_FAILED = ChoiceItem(-1, 'Operation Failed')  # Operation Failed
    SYSTEM_FAILED = ChoiceItem(99, 'System Error')  # System Error
    REQNO_FAILED = ChoiceItem(12, 'TRANSACTION ID IS NOT UNIQUE')  # request no 重复
    #
    COMPLETED = ChoiceItem(0, 'Final Completed')  # succ
    #
    FAILED = ChoiceItem(-2, 'Failed')  # 未知失败
    UNDEFINED = ChoiceItem(-99, 'Undefined')  # 未定义


class WithdrawStatus(DjangoChoices):
    """提现状态:

    """
    STAGE_F01 = ChoiceItem(-8, 'XXX F1')
    #
    VALIDATE_FAILED = ChoiceItem(-10, 'Invalid Address') # 内部提现地址类型不匹配
    WALLET_FAILED = ChoiceItem(-7, 'Block Failed')  # 区块连通知失败
    ENGINE_FAILED = ChoiceItem(-6, 'Engine Failed')  # 交易引擎通知失败
    REVIEW_FAILED = ChoiceItem(-5, 'Admin Verify Failed')  # 人工审核: 失败
    VERIFY_FAILED = ChoiceItem(-4, 'User Verify Failed')  # 用户审核: 失败, 超过一天时间未确认状态
    #
    USER_REVOKE = ChoiceItem(-3, 'User Revoke')  # 用户撤单
    FAILED = ChoiceItem(-2, 'Failed')  # 失败
    UNDEFINED = ChoiceItem(-1, 'Undefined')  # 未定义
    COMPLETED = ChoiceItem(0, 'Final Completed')  # 最终完成状态
    #
    VERIFY_PENDING = ChoiceItem(1, 'User Verify Pending')      # 用户审核: Pending
    VERIFY_COMPLETED = ChoiceItem(2, 'User Verify Completed')  # 用户审核: Completed
    #
    REVIEW_PENDING = ChoiceItem(3, 'Admin  Verify Pending')  # 客服人工审核: Pending
    REVIEW_COMPLETED = ChoiceItem(4, 'Admin Verify Completed')  # 客服人工审核: Completed
    #
    OUT_MONEY_COMPLETED = ChoiceItem(9, 'Fiance  Verify Pending')  # 财务出款: Completed
    OUT_MONEY_FAILED = ChoiceItem(-9, 'Fiance Verify Failed')  # 财务出款失败: Completed
    #
    ENGINE_PENDING = ChoiceItem(5, 'Engine Pending')  # 交易引擎: Pending
    ENGINE_COMPLETED = ChoiceItem(6, 'Engine Completed')  # 交易引擎: Completed
    #
    CHAIN_PENDING = ChoiceItem(7, 'Chain Pending')  # 链上: Pending
    CHAIN_COMPLETED = ChoiceItem(8, 'Chain Completed')  # 链上: 完成
    #
    # STAGE_01 = ChoiceItem(9, 'XXX 1')
    # STAGE_02 = ChoiceItem(10, 'XXX 2')
    # STAGE_03 = ChoiceItem(11, 'XXX 3')


class CryptoWithdrawAllowStatus(DjangoChoices):
    REVIEW_FAILED = ChoiceItem(-5, 'Admin Verify Failed')  # 人工审核: 失败
    REVIEW_COMPLETED = ChoiceItem(4, 'Admin Verify Completed')  # 客服人工审核: Completed


class FiatWithdrawAllowStatus(DjangoChoices):
    REVIEW_FAILED = ChoiceItem(-5, 'Admin Verify Failed')  # 人工审核: 失败
    REVIEW_COMPLETED = ChoiceItem(4, 'Admin Verify Completed')  # 客服人工审核: Completed


class FiatWithdrawFianceAllowStatus(DjangoChoices):
    OUT_MONEY_COMPLETED = ChoiceItem(9, 'Admin  Verify Pending')  # 财务出款: Completed
    OUT_MONEY_FAILED = ChoiceItem(-9, 'Admin  Verify Pending')  # 财务出款失败: Completed


class WithdrawRequestVerifyReason(DjangoChoices):
    """客服审核失败原因

    """
    UNDEFINED = ChoiceItem(-1, 'Undefined')  # 未定义
    ERROR_01 = ChoiceItem(1, 'ERROR_01 1')
    ERROR_02 = ChoiceItem(2, 'ERROR_02 1')
    ERROR_03 = ChoiceItem(3, 'ERROR_03 1')
    ERROR_04 = ChoiceItem(4, 'ERROR_04 1')
    ERROR_05 = ChoiceItem(5, 'ERROR_05 1')


class WithDrawWalletCode(DjangoChoices):
    """充值--Engine出错的返回码:
        ACCEPTED = 0
        WORKING_IN_PROGRESS = 1
        TRANSACTION_CREATED = 2
        FAILED = 3

    """
    COMPLETED = ChoiceItem(2, 'TRANSACTION_CREATED Final Completed')  # succ
    #
    FAILED = ChoiceItem(3, 'Failed')  # 失败
    UNDEFINED = ChoiceItem(-3, 'Undefined')


class TransactionType(DjangoChoices):
    """交易产生的类型(触发方)

    """
    UNDEFINED = ChoiceItem(-1, 'Undefined')  # 未定义
    WITHDRAW = ChoiceItem(0, 'Withdraw')  # 矿工手续费(系统支付)
    DEPOSIT = ChoiceItem(1, 'Deposit')  # 矿工手续费(用户支付)
    SWAP_ERC_TOKEN_FROM_TX_ADDR = ChoiceItem(2, 'Swap ERC Token: From User Tx Address')  # 矿工手续费(系统支付)
    SWAP_ERC_TOKEN_FROM_COLD_WALLET = ChoiceItem(3, 'Swap ERC Token: from Cold Wallet')  # 矿工手续费(系统支付)
    TX_FAILED = ChoiceItem(4, 'Transaction Failed')  # 矿工手续费(系统支付)


class SecEventType(DjangoChoices):
    LOGIN = ChoiceItem(0, 'login')
    CHANGE_PASSWORD = ChoiceItem(1, 'change_password')


# available transitions:
#               -> RECEIVED     : user request
# RECEIVED      -> UNVERIFIED   : send_engine_withdraw_request
# UNVERIFIED    -> VERIFIED     : _on_verified
# VERIFIED      -> SENT         : send_blockchain_withdraw_request
# RECEIVED      -> CANCELED     : cancel_withdraw_request
# UNVERIFIED    -> CANCELED     : send_engine_deposit_back_request


class DepositType(DjangoChoices):
    """充值记录产生的原因

    """
    UNDEFINED = ChoiceItem(-1, 'Undefined')  # 未定义
    CHAIN_TX = ChoiceItem(0, 'Chain Transaction')  # 链上交易
    CHAIN_FORK = ChoiceItem(1, 'Chain Fork')  # 链上分叉
    SYS_REWARD = ChoiceItem(2, 'SYS Reward')  # 系统赠送(奖励)发币
    SYS_REFUND = ChoiceItem(3, 'Cancel Withdraw, SYS Refund')  # 用户撤销提现, 系统退款(重新产生一笔充值)


class DepositAddressStatus(DjangoChoices):
    """充值地址的状态:

    """
    DISABLE = ChoiceItem(-2, 'Disable')  # 被禁用
    UNDEFINED = ChoiceItem(-1, 'Undefined')  # 未定义
    UNCONFIRMED = ChoiceItem(0, 'Unconfirmed')  # 待确认(等确认数)
    USABLE = ChoiceItem(1, 'Usable')  # 可用地址(未分配)
    ASSIGNED = ChoiceItem(2, 'Assigned')  # 已分配


class WithdrawAddressStatus(DjangoChoices):
    """提现地址的状态

    """
    DISABLE = ChoiceItem(-2, 'Disable')      # 被禁用
    UNDEFINED = ChoiceItem(-1, 'Undefined')  # 未定义
    NORMAL = ChoiceItem(0, "Normal")  # 正常使用


class UserIdStatus(DjangoChoices):
    """无效的UserID 默认值
    - 替代 NULL 值

    """
    UNDEFINED = ChoiceItem(-1, 'Undefined')  # 未定义


class VerificationType(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    VCODE = ChoiceItem(0, 'Mail vcode')
    MANUAL = ChoiceItem(1, 'Manual')


class VerificationStatus(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    CREATED = ChoiceItem(0, 'Created')
    SENT = ChoiceItem(1, 'Verification message sent')
    VERIFIED = ChoiceItem(2, 'Verified')
    SKIPPED = ChoiceItem(3, 'Skipped')


class VerificationPurpose(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    WITHDRAW = ChoiceItem(0, 'Withdraw')


class ApiKeyStatus(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    ACTIVE = ChoiceItem(0, "Active")


class ApiKeyPermission(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    READ = ChoiceItem(0, "Read")
    WRITE = ChoiceItem(1, "Write")
    ADMIN = ChoiceItem(2, "Admin")


class UserMembersPointsSource(DjangoChoices):
    USERACTIVATE = ChoiceItem(101, "User Activate")
    USERLOGIN = ChoiceItem(102, "User Login")
    FIRST_DEPOSIT = ChoiceItem(103, "first_deposit")
    FIRST_TRADE = ChoiceItem(104, "first_trade")
    PASS_KYC = ChoiceItem(105, "kyc_verify")
    TRADE_REBATE = ChoiceItem(106, 'Trade Rebate')
    FIRST_INVITE = ChoiceItem(107, 'first_invite')
    INVITEE_TRADE_REBATE = ChoiceItem(108, 'invitee_trade_rebate')


UserActivityPoint = {
    101: 1000,
    103: 3000,
    105: 3000,
    107: 3000,
}


class UserDistributorType(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, "Unidefined")
    USER = ChoiceItem(1, "User")
    SUPER_AGENT = ChoiceItem(2, "SuperAgent")
    AGENT = ChoiceItem(3, "Agent")


# User account will be locked after x failed login attempts.
LOGIN_ATTEMPTS_LIMIT = 15

# Confirmation thresholds for each coin. If the confirmations reach the
# threshold, the trasaction on chain will be treated completed.

# 确认数 - 最小限额
CONFIRM_LIMIT = {
    CoinType.BTC: 6,
    CoinType.ETC: 6,
    CoinType.ETH: 12,
    CoinType.BCH: 6,
    CoinType.ICO: 6,
    CoinType.REP: 6,
    CoinType.LTC: 6,
    CoinType.DASH: 6,
    CoinType.MONA: 6,
    CoinType.USDT: 6,
}

# Indicate which series a coin belongs to.
COIN_SERIES = {
    CoinType.BTC: CoinSeries.BTC_SERIES,
    CoinType.BCH: CoinSeries.BCH_SERIES,
    CoinType.ETC: CoinSeries.ETC_SERIES,
    CoinType.ETH: CoinSeries.ETH_SERIES,
    CoinType.ICO: CoinSeries.ICO_SERIES,
    CoinType.REP: CoinSeries.ETH_SERIES,
    CoinType.LTC: CoinSeries.LTC_SERIES,
    CoinType.DASH: CoinSeries.DASH_SERIES,
    CoinType.MONA: CoinSeries.MONA_SERIES,
    CoinType.USDT: CoinSeries.USDT_SERIES,
}

COIN_SERIES_LABEL = {
    "BTC": CoinSeries.BTC_SERIES,
    "BCH": CoinSeries.BCH_SERIES,
    "ETC": CoinSeries.ETC_SERIES,
    "ETH": CoinSeries.ETH_SERIES,
    "ICO": CoinSeries.ICO_SERIES,
    "REP": CoinSeries.ETH_SERIES,
    "LTC": CoinSeries.LTC_SERIES,
    "DASH": CoinSeries.DASH_SERIES,
    "MONA": CoinSeries.MONA_SERIES,
    "USDT": CoinSeries.USDT_SERIES,
}

# label group:
ETH_LABEL_GROUP = ['ETC', 'ETH']
BTC_LABEL_GROUP = ["BTC", "BCH", "LTC", "DASH", "MONA", "USDT"]

# Group for BTC and ETH
BTC_GROUP = [
    CoinType.BTC,
    CoinType.BCH,
    CoinType.ICO,
    CoinType.REP,
    CoinType.LTC,
    CoinType.DASH,
    CoinType.MONA,
    CoinType.USDT,
]

ETH_GROUP = [
    CoinType.ETC,
    CoinType.ETH,
]

# kyc:
UPLOAD_FILE_TYPE = ('doc', 'docx', 'pdf')
UPLOAD_IMAGE_TYPE = ('jpg', 'png', 'gif', 'jpeg')
# 上传文件的限制大小
UPLOAD_FILE_SIZE = 20 * 1024 * 1024
# 压缩后图片的纵向分辨率
UPLOAD_IMAGE_HEIGHT = 2160
# 是否开启合同自动生成功能
IS_UPLOAD_DOCX = False
# 合同文件模板的路径
INDIVIDUAL_APP_1 = 'apps/user_kyc/libs/KYC L2 agreement_20180608.docx'
INDIVIDUAL_APP_2 = 'apps/user_kyc/libs/KYC L3 agreement_20180608.docx'
ENTERPRISE_APP_1 = 'apps/user_kyc/libs/Terms & Conditions 13 April 2018.docx'


class UserVIPLevel(DjangoChoices):
    """用户 VIP 等级:

    """
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    LV0 = ChoiceItem(0, "Level 0")
    LV1 = ChoiceItem(1, "Level 1")
    LV2 = ChoiceItem(2, "Level 2")
    LV3 = ChoiceItem(3, "Level 3")
    LV4 = ChoiceItem(4, "Level 4")
    LV5 = ChoiceItem(5, "Level 5")
    LV6 = ChoiceItem(6, "Level 6")
    LV7 = ChoiceItem(7, "Level 7")
    LV8 = ChoiceItem(8, "Level 8")
    LV9 = ChoiceItem(9, "Level 9")


# 加密货币-提现手续费-基础费率
CRYPTO_WITHDRAW_FEE_BASE_RATE = 0.0001
# 加密货币-提现-基础最小限额
CRYPTO_WITHDRAW_MIN_BASE_LIMIT = 0.001
# 提现最大上限:
CRYPTO_WITHDRAW_MAX_BASE_LIMIT = 0.1

# 数字货币-提现-手续费-基准费率
WITHDRAW_FEE_RATE = {
    CoinType.BTC: CRYPTO_WITHDRAW_FEE_BASE_RATE * 10,
    CoinType.BCH: CRYPTO_WITHDRAW_FEE_BASE_RATE * 1,
    CoinType.ETH: CRYPTO_WITHDRAW_FEE_BASE_RATE * 100,
    CoinType.ETC: CRYPTO_WITHDRAW_FEE_BASE_RATE * 100,
    CoinType.LTC: CRYPTO_WITHDRAW_FEE_BASE_RATE * 10,
    CoinType.DASH: CRYPTO_WITHDRAW_FEE_BASE_RATE * 20,
    CoinType.MONA: CRYPTO_WITHDRAW_FEE_BASE_RATE * 10,
    CoinType.USDT: CRYPTO_WITHDRAW_FEE_BASE_RATE * 100000,
}

# 数字货币-提现-最小限额
WITHDRAW_MIN_LIMIT = {
    CoinType.BTC: CRYPTO_WITHDRAW_MIN_BASE_LIMIT * 10,
    CoinType.BCH: CRYPTO_WITHDRAW_MIN_BASE_LIMIT * 10,
    CoinType.ETH: CRYPTO_WITHDRAW_MIN_BASE_LIMIT * 15,
    CoinType.ETC: CRYPTO_WITHDRAW_MIN_BASE_LIMIT * 500,
    CoinType.LTC: CRYPTO_WITHDRAW_MIN_BASE_LIMIT * 100,
    CoinType.DASH: CRYPTO_WITHDRAW_MIN_BASE_LIMIT * 20,
    CoinType.MONA: CRYPTO_WITHDRAW_MIN_BASE_LIMIT * 100,
    CoinType.USDT: CRYPTO_WITHDRAW_MIN_BASE_LIMIT * 200000,
}

# 数字货币-提现-最大限额
WITHDRAW_MAX_LIMIT = {
    CoinType.BTC: CRYPTO_WITHDRAW_MAX_BASE_LIMIT * 0.5,
    CoinType.BCH: CRYPTO_WITHDRAW_MAX_BASE_LIMIT * 10,
    CoinType.ETH: CRYPTO_WITHDRAW_MAX_BASE_LIMIT * 5,
    CoinType.ETC: CRYPTO_WITHDRAW_MAX_BASE_LIMIT * 200,
    CoinType.LTC: CRYPTO_WITHDRAW_MAX_BASE_LIMIT * 80,
    CoinType.DASH: CRYPTO_WITHDRAW_MAX_BASE_LIMIT * 10,
    CoinType.MONA: CRYPTO_WITHDRAW_MAX_BASE_LIMIT * 1000,
    CoinType.USDT: CRYPTO_WITHDRAW_MAX_BASE_LIMIT * 10000000,
}

#
USD_DEPOSIT_FEE_BASE_RATE = decimal.Decimal('0.001')

# 法币提现最小限额
FIAT_WITHDRAW_MIN_LIMIT = {
    FiatType.CNY: 0,
    FiatType.USD: 0,
    FiatType.EUR: 0,
    FiatType.HKD: 0,
    FiatType.JPY: 0,
}


# 法币提现最大限额
FIAT_WITHDRAW_MAX_LIMIT = {
    FiatType.CNY: 0,
    FiatType.USD: 0,
    FiatType.EUR: 0,
    FiatType.HKD: 0,
    FiatType.JPY: 0,
}


WALLET_HASH_FEILD = {
    0: 'BTC',
    1: 'ETC',
    2: 'ETH',
    3: 'BCH',
    4: 'ICO',
    5: 'REP',
    6: 'LTC',
    7: 'DASH',
    8: 'MONA',
    9: 'USDT',
}


class ApiPermissionType(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    List = ChoiceItem(1, "List")
    Create = ChoiceItem(2, "Create")


class ApiPermissionTypeFront(DjangoChoices):
    UNDEFINED = ChoiceItem(-1, 'Undefined')
    List = ChoiceItem(1, "Get")
    Create = ChoiceItem(2, "Post")


class UserKYCType(DjangoChoices):
    INDIVIDUAL = ChoiceItem(0, 'Individual')
    ENTERPRISE = ChoiceItem(1, 'Enterprise')


# withdraw daily limit by kyc level
WITHDRAW_DAILY_LIMIT = {
    '1': {
        'BTC': 2,
        'ETH': 20,
        'LTC': 100,
        'BCH': 10,
        'USD': 0,
        'USDT': 2000,
    },
    '2':
        {
            'BTC': 10,
            'ETH': 100,
            'LTC': 500,
            'BCH': 50,
            'USD': 0,
            'USDT': 10000,
        },
    '3': {
        'BTC': 100,
        'ETH': 1000,
        'LTC': 5000,
        'BCH': 500,
        'USD': 50000,
        'USDT': 50000,
    },
    '4': {
        'BTC': 100,
        'ETH': 1000,
        'LTC': 5000,
        'BCH': 500,
        'USD': 100000,
        'USDT': 100000,
    },

}


# #  积分活动枚举
# class UserActivityType(DjangoChoices):
#     FIRST_DEPOSIT = ChoiceItem(1, "first_deposit")
#     FIRST_TRADE = ChoiceItem(2, "first_trade")
#     KYC_VERIFY = ChoiceItem(3, "kyc_verify")

DEPOSIT_LOWER_BOUND = {
    'USD': decimal.Decimal('500'),
    'BTC': decimal.Decimal('0.1'),
    'ETH': decimal.Decimal('1'),
    'BCH': decimal.Decimal('0.5'),
    'LTC': decimal.Decimal('5'),
    'USDT': decimal.Decimal('500'),
}


# 返佣类型
RateType = ['share', 'direct', 'indirect', 'supers', 'normal']

# 返佣范围 (min,max)
RateTypeRange = {
    "share": (0, 100),
    "direct": (0, 100),
    "indirect": (0, 100),
    "supers": (10, 15),
    "normal": (5, 10),
}

# 每人每天产生最大积分
MAX_POINTS_DAILY = decimal.Decimal('100000')


# 审核类型
class VerifyType(DjangoChoices):
    AUTOMIC_ACCESS = ChoiceItem(0, "automic_access")
    STAFF_ACCESS = ChoiceItem(1, "staff_access")
