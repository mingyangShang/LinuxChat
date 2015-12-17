# <center>LinuxChat项目推进</center>

### 2015-11-30 完成后台技术选型
- 语言：Python

- 框架：Django


- 数据库：mysql＋radius
	
### 2015-12-02 开始数据库设计
- User(用户表)：

	||用户ID|昵称|密码|性别|个人签名
	|----|-----|---|---|---|---|
	|列名|_uid|nick|pwd|sex|sign|
	
	|列名|描述|类型|约束|
	|----|----|----|----|
	|_uid|用户ID|varchar(32)|主键，32位uuid|
	|nick|昵称|varchar(20)|20字数限制|
	|pwd|密码|varchar(32)|经md5加密|
	|sex|性别|char(1)|M（男）或 W（女）|
	|sign|个人签名|varchar(40)|40字数限制|
	
- ~~Friends(好友列表)：~~
	
	|列名|描述|类型|约束|
	|----|----|----|----|
	|uid|用户ID|varchar(32)|外键，参照User中的_uid|
	|friends|好友ID列表|string|以;分隔，每一项参照User中的_uid|
	
- Friends(好友列表)：

	|列名|描述|类型|约束|
	|----|----|----|----|
	|uid|用户ID|varchar(32)|外键，参照User中的_uid|
	|friend_id|好友ID|varchar(32)|外键，参照User中的_uid|
	
	
- Group(群组表)：

	|列名|描述|类型|约束|
	|----|----|---|----|
	|_gid|组id|varchar(32)|主键，32位uuid|
	|name|群组名称|varchar(20)|20字数限制|
	|owner|创建者|varchar(32)|外键，参照User表中的_id|
	|create_time|创建时间|long|格林尼治毫秒数|
	|max_num|最大支持人数|Integer|默认20|
	
- ~~Group_User(群组包含用户关系表)：~~

	|列名|描述|类型|约束|
	|----|----|---|----|
	|gid|群组id|varchar(32)|外键，参照Group表中的_gid|
	|members|成员id集合|string|以;分隔|
	
- ~~User_Group(用户所在群组关系表)：~~

	|列名|描述|类型|约束|
	|----|----|---|----|
	|uid|用户ID|varchar(32)|外键，参照User表中的_uid|
	|owners|群组ID集合|string|以;分隔|
	
- Members(群组用户关系表)
	
	|列名|描述|类型|约束|
	|----|----|---|----|
	|gid|群组ID|varchar(32)|主键，外键，参照Group表中的_gid|
	|uid|成员ID|varchar(32)|主键，外键，参照User表中的_uid|
	（）
	
- MsgType(消息类型表)：

	|列名|描述|类型|约束|
	|----|----|----|----|
	|_tid|消息类型ID|Integer|主键，递增|
	|type|消息类型|varchar(10)|默认含有text(普通文本),img(图片),link(链接),code(代码),face(表情),file(文件)

- Msg(消息表)：
	
	|列名|描述|类型|约束|
	|----|----|----|----|
	|_mid|消息ID|varchar(32)|主键，32位uuid|
	|from_user|发消息用户ID|varchar(32)|外键，参照User表中的_uid|
	|to_user|接收者ID|varchar(32)|外键，参照User表中的_id或|
	|to_group|接收组ID|varchar(32)|外键，参照Group表中的_gid|
	|type|消息类型|Integer|外键，参照MsgType中的_tid|
	|content|实际内容|text|图片存地址，表情存字符串，代码存元格式
	
	**注:<br />
	1.单独将消息类型建表是为了支持消息类型的扩展性，可以方便地新增消息类型从而支持新消息的格式化处理<br />
	2.弃用关系表（好友表，组群用户表）的列表拼凑属性，改为单独的id对应关系，虽然会造成部分冗余，但在更新，删除的时候能提高速度，查询只需第一次从数据中查询然后存至缓存数据库`radius`中，有更新回写（为保证一致性，抽为事务，并且先写数据库再写内存）**
	
### 2015-12-10 搭建好后台开发环境
virtualenv＋django+pillow

### 2015-12-12 完成命令行终端通讯demo

### 2015-12-15 完成数据库搭建，django中创建mysql表及CURD测试
1. mysql默认编码为latin，为使支持中文，需要修改数据默认编码
2. django中的外键反馈策略导致多外键时冲突，需加related_name区分
3. ImageField使用pillow库
4. 消息表的设计还是不太合理，如何设计这种包含多种类型字段的数据的表？？？

### 2015-12-17 完成Url，服务API设计
|url|用途|请求方式|参数|返回格式(外层json含有success键和error键，具体信息在data键对应值，以下不再列出success和error键)
|---|---|---|---|---|
|/user/register|注册|POST|{username,sex,pwd,sign}|{"data":"{}"}|
|/user/login|登录|POST|{username,pwd}|{"data":{"uid":<uuid>,"timestamp":<currenttime>,"cookie":"<random string>"}}|
|/user/delete|删除|POST|{uid}|{"data":"{}"}|
|/user/get|查询|POST|{uid}|{"data":{"name":<name>,"sex":<M or W>,sign:<sign>"}}|
|user/<uid>|查询|GET|{uid}|{"data":{"name":<name>,"sex":<M or W>,sign:<sign>"}|
|user/friend/invite|添加好友|POST|{from,to(name or uid)}|{"data:":{}}|
|user/friend/accept|同意好友邀请|POST|{from}|{"data":""}|
|user/friend/delete|删除好友|POST|{from,delete_friend}|{"data"":{}}|
|user/group/create|创建讨论组|POST|{from,group_name,members}|{"data":"{"gid":"<gid>","members":<[members]>}"}|
|user/group/exit|退出讨论组|POST|{from,group_id}|{"data":""}|
|user/group/members/add|添加组成员|POST|{from,gid,[member_id]}|{"data":""}|
|user/group/members/remove|删除组成员|POST|{from,gid,[member_id]}|{"data":""}|
|chat/group|查看组消息|POST|{from,gid,start_time,start_page,end_page}|{"data":"{"msg":<[msg]>}"}|
|chat/person|查看个人聊天消息|POST|{from,gid,start_time,start_page,end_page}|{"data":"{"msg":<[msg]>}}|





	
	