ZPOC
===================================  
  ![](http://i.imgur.com/nHbRONh.jpg)
    
基于ZoomEye-Seebug-pocsuit的一键式自动化测试工具:-)
-----------------------------------  
Zpoc具备ZoomEye 和soudan的强大网络探索能力。并能够将数据存储指定文件。


    说明：ZoomEye 的API搜索是有限制的，shodan的结果是要付费的。【邪恶脸】

Zpoc具备基于pocsuit框架的poc库( ▼-▼ ),poc库期待你的完善。

	说明：难以想象，但你需要找某个漏洞时，工具会给你提示出相关的poc,that is  so cool

Zpoc具备基于pocsuit的poc快速化开发框架，后面会有更多的框架加入其中。

	说明：你还在为不会写poc,而惆怅吗？你还在为找不到测试用例，而悲伤吗？


    
### Zpoc项目功能简介：

    ZoomEye 的sdk 接口，包括登录，搜索，搜索结果的存储。（已经实现）
     
    结合pocsuit框架，实现快速进行poc测试（已经实现）
    
    poc库实现，漏洞的相关测试，以及poc和dork的智能提示（开发ing）

	基于整个Zpoc测试的深入学习，实现一键化和学习化（开发ing）

### 安装说明
- [安装说明](Zpoc/doc/install.md)	在 **doc/install.md**

####使用参数：
    项目现在暂时依赖于pocsuite库

    使用时，切换到src项目下，使用命令如下所示：

	python lock.py -q/--query=  #query数据，每个数据用逗号隔开
				   -d/--facets= #facet数据，每个数据用逗号隔开
				   -s/--search= #搜索类型：Web搜索或者host搜索，默认host搜索
				   -p/--page=   #页数默认是1
				   -r/--poc=    #PoC文件
				   -o/--port=   #由前一版本留下，如果`-q`中有port数据，则会被-o选项替换
				   -f/--script-file= #脚本文件，用来省略命令行参数填充
	
- 详细说明以及使用范例：
	- `python lock.py --help`

### 相关平台框架： 
> [Seebug ](https://www.seebug.org/)
>  
> > [ZoomEye ](https://www.zoomeye.org/)
>  
>  > > [shodan](https://www.shodan.io/)  
>  
> > > > [ Pocsuite](https://github.com/knownsec/Pocsuite)
  
