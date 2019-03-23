# 用途：
1. 爬取B站所有动漫评分
2. 根据条件自动关注动漫


# 使用方法：
1. 设置settings.py
（包括：数据库连接、线程数、请求间休息时间、查询条件）
2. 打开对应程序自动运行（bilibili.py为爬取，Bilibili_Anime_follow.py为自动关注）



# bilibili.py-程序逻辑：
1. 逐页进入动漫索引页面，获取单页所有动漫的url
2. 依次进入每个动漫页面获取信息


# Bilibili_Anime_follow.py-程序逻辑：
1. 进入bilibili登陆页面（有10秒的等待登陆时间，bilibili的登陆页面易失效，只能用手机扫码）
2. 获取mysql中对应评分的动漫网址
3. 逐个页面进入并自动关注（已关注则跳过）
