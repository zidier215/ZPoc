####依赖库
- pycurl, certifi

####依赖库安装方法
- pip  install  pycurl
- pip  install  certifi

####支持框架
- **pocsuite** `pip install pocsuite`

####支持参数
  >-d  dork

  >-p  page     获取查询的第几页
  
  >-o  port     查询端口
  
  >-r  poc.py   待验证的poc脚本文件

####使用方法
	python lock.py -d app,os -p 1 -o 21 -r xxx.py
####错误防止
1. **Windows用户**请确保`pocsuite`框架的执行路径被加入至系统**环境变量**中

2. **×nix用户**确保搜索路径中能搜索到框架的存在

3. 或者可以选择将本程序文件夹 `Zpoc`放于`pocsuite`框架的文件夹内
####注意事项
- 请使用浏览器/Markdown阅读器打开本页面
- 后续将扩展支持的框架
