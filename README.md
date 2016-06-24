# ZPoc#场景：
  通过此工具来完成zoomeye的数据库查询，获取查询结果并存储，用于poc检测使用

#需求：
  1. 支持zoomeye的api查询
  2. 支持自动登录，保存tooken功能，并保证tooken生效
  3. 支持web查询和host查询，资源使用情况查询
  4. 支持输入参数生成配置文件（默认保存zoomeye 10页的查询结果）
      ip列表
      域名列表
  5. 封装成python类。可以在此基础上扩展；（后续功能）
  	  内置dork库
  	  
#接口
	登录登出接口
	web查询接口
	host查询接口
	资源查询接口
	查询结果保存接口
	pocsuit调用接口
	pocsuit结果保存接口
	dork查询接口？是否可以归类到host，web查询接口

