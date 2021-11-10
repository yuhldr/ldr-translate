# 填写你的appid 密钥，这个我自己的被人用的比较多，可能会有问题
# https://ripperhe.gitee.io/bob/#/service/translate/baidu
baidu_appid = '20211109000995303'
baidu_secretKey = 'qLFDFx7fLRrioaa6CTnk'

# OCR图片识别并翻译，按照下面的教程修改为自己的，一个人一月1000次
# https://cloud.baidu.com/doc/OCR/s/dk3iqnq51
baidu_ocr_api_key = "S1NHCzzzBhL2TUMx5iGpOSUu"
baidu_ocr_secret_key = "709INHX6GCLsAXXZPLhKGVMmra7bEwGl"

# 翻译api最小请求间隔
translate_span = 1.0

# 是否划词翻译，默认复制时翻译
translate_select = False

# 百度接口，默认翻译为中文
translate_to_language = 'zh'

translate_to_language_zh = [
    "中文",
    "文言文",
    "英语",
    "日语",
    "韩语",
    "德语",
    "法语",
]
