# Github Actions Rss (garss, 嘎RSS! 已收集{{rss_num}}个RSS源, 生成时间: {{ga_rss_datetime}})

信息茧房是指人们关注的信息领域会习惯性地被自己的兴趣所引导，从而将自己的生活桎梏于像蚕茧一般的「茧房」中的现象。

## 《嘎!RSS》🐣为打破信息茧房而生

![](./_media/ga-rss.png)

这个名为**嘎!RSS**的项目会利用免费的Github Actions服务, 提供一个内容全面的信息流, 让现代人的知识体系更广泛, 减弱信息茧房对现代人的影响, 让**非茧房信息流**造福人类~
[《嘎!RSS》永久开源页面: https://github.com/zhaoolee/garss](https://github.com/zhaoolee/garss)

## 主要功能
1. 收集RSS, 打造无广告内容优质的 **头版头条** 超赞新闻页
2. 利用Github Actions, 搜集全部RSS的头版头条新闻标题和超链接, 并自动更新到首页,当天最新发布的文章会出现🆕 标志

邮件内容区开始>
<h2>新获取{{new_num}}篇文章 生产时间 {{ga_rss_datetime}} 保质期24小时</h2>

{{news}}

<邮件内容区结束

## 已收集RSS列表

| 编号 | 名称 | 描述 | RSS  |  最新内容 |
| --- | --- | --- | --- |  --- |
| <h2 id="ai资讯">AI资讯</h2> |  |   |  |
| AI001 | OpenAI Blog | OpenAI 官方博客 | {{latest_content}}  |  [订阅地址](https://openai.com/blog/rss.xml) |
| AI002 | OpenAI News | OpenAI 官方新闻 | {{latest_content}}  |  [订阅地址](https://openai.com/news/rss.xml) |
| AI003 | Anthropic Blog | Anthropic 官方博客 | {{latest_content}}  |  [订阅地址](https://rsshub.rss3.workers.dev/anthropic/engineering) |
| AI004 | Google DeepMind | Google DeepMind 官方博客 | {{latest_content}}  |  [订阅地址](https://deepmind.google/blog/rss.xml) |
| AI005 | Google AI Blog | Google AI 资讯 | {{latest_content}}  |  [订阅地址](https://blog.google/technology/ai/rss/) |
| AI006 | Microsoft Research | 微软研究院官方博客 | {{latest_content}}  |  [订阅地址](https://www.microsoft.com/en-us/research/feed/) |
| AI007 | Microsoft DevBlogs | 微软开发者官方博客 | {{latest_content}}  |  [订阅地址](https://devblogs.microsoft.com/feed/) |
| AI008 | Hugging Face Blog | Hugging Face 官方博客 | {{latest_content}}  |  [订阅地址](https://huggingface.co/blog/feed.xml) |
| AI009 | Meta Research | Meta 研究动态 | {{latest_content}}  |  [订阅地址](https://research.facebook.com/feed/) |
| AI010 | Engineering at Meta | Meta 工程博客 | {{latest_content}}  |  [订阅地址](https://engineering.fb.com/feed/) |
| AI011 | NVIDIA Blog | NVIDIA 官方博客 | {{latest_content}}  |  [订阅地址](https://blogs.nvidia.com/feed/) |
| AI012 | AWS ML Blog | AWS Machine Learning 博客 | {{latest_content}}  |  [订阅地址](https://aws.amazon.com/blogs/machine-learning/feed/) |
| AI013 | 量子位 | AI 产业与产品资讯 | {{latest_content}}  |  [订阅地址](https://www.qbitai.com/feed) |
| AI014 | InfoQ | 中文技术与 AI 资讯 | {{latest_content}}  |  [订阅地址](https://www.infoq.cn/feed) |
| AI015 | MarkTechPost | AI 研究与工程资讯 | {{latest_content}}  |  [订阅地址](https://marktechpost.com/feed) |
| AI016 | TechCrunch AI | AI 创业与投融资动态 | {{latest_content}}  |  [订阅地址](https://techcrunch.com/category/artificial-intelligence/feed/) |
| AI017 | VentureBeat AI | AI 行业新闻 | {{latest_content}}  |  [订阅地址](https://venturebeat.com/category/ai/feed/) |
| AI018 | AI News | 国际 AI 新闻 | {{latest_content}}  |  [订阅地址](https://www.artificialintelligence-news.com/feed/) |
| AI019 | PaperWeekly | PaperWeekly 论文周报 | {{latest_content}}  |  [订阅地址](https://raw.githubusercontent.com/osnsyc/Wechat-Scholar/main/channels/gh_5138cebd4585.xml) |
| <h2 id="前端开发">前端开发</h2> |  |   |  |
| FE001 | React | React 官方博客 | {{latest_content}}  |  [订阅地址](https://react.dev/rss.xml) |
| FE002 | React Native | React Native 官方博客 | {{latest_content}}  |  [订阅地址](https://reactnative.dev/blog/atom.xml) |
| FE003 | Expo | Expo 官方博客 | {{latest_content}}  |  [订阅地址](https://blog.expo.dev/feed) |
| FE004 | CSS-Tricks | CSS 与前端工程实践 | {{latest_content}}  |  [订阅地址](https://css-tricks.com/feed/) |
| FE005 | web.dev | Google Web 平台与性能实践 | {{latest_content}}  |  [订阅地址](https://web.dev/feed.xml) |
| FE006 | MDN Blog | Web 标准与前端知识库博客 | {{latest_content}}  |  [订阅地址](https://developer.mozilla.org/en-US/blog/rss.xml) |
| FE007 | Chrome Developers Blog | Chrome 团队前端实践 | {{latest_content}}  |  [订阅地址](https://developer.chrome.com/blog/feed.xml) |
| FE008 | 美团技术团队博客 | 美团工程实践 | {{latest_content}}  |  [订阅地址](https://tech.meituan.com/feed/) |
| FE009 | 阮一峰的网络日志 | Web 技术与工程视角 | {{latest_content}}  |  [订阅地址](http://www.ruanyifeng.com/blog/atom.xml) |
| FE0010 | JavaScript Weekly | JavaScript 每周新闻 | {{latest_content}}  |  [订阅地址](https://cprss.s3.amazonaws.com/javascriptweekly.com.xml) |
| FE0011 | Smashing Magazine | 前端与设计工程深度文章 | {{latest_content}}  |  [订阅地址](https://www.smashingmagazine.com/feed/) |
| <h2 id="泛科技">泛科技</h2> |  |   |  |
| T001 | Hacker News | 高质量技术社区新闻流 | {{latest_content}}  |  [订阅地址](https://news.ycombinator.com/rss) |
| T002 | 奇客Solidot | 科技与开源资讯 | {{latest_content}}  |  [订阅地址](https://www.solidot.org/index.rss) |
| T003 | The Verge | 消费科技与产业新闻 | {{latest_content}}  |  [订阅地址](https://www.theverge.com/rss/index.xml) |
| T004 | Github Trending | Github 每周 Trending（全语言） | {{latest_content}}  |  [订阅地址](https://mshibanami.github.io/GitHubTrendingRSS/weekly/all.xml) |
| T005 | TechSpot | 硬件与科技新闻 | {{latest_content}}  |  [订阅地址](https://www.techspot.com/backend.xml) |
| T006 | Bloomberg Tech | 全球科技商业新闻 | {{latest_content}}  |  [订阅地址](https://feeds.bloomberg.com/technology/news.rss) |
| T007 | HelloGitHub 月刊 | 开源项目与技术月刊 | {{latest_content}}  |  [订阅地址](https://hellogithub.com/rss) |
| <h2 id="理财投资">理财投资</h2> |  |   |  |
| F001 | 雪球 | A 股、港股、美股投资社区 | {{latest_content}}  |  [订阅地址](https://xueqiu.com/hots/topic/rss) |
| F002 | 华尔街见闻 | 宏观、市场与交易资讯 | {{latest_content}}  |  [订阅地址](https://dedicated.wallstreetcn.com/rss.xml) |
| <h2 id="新闻热点">新闻热点</h2> |  |   |  |
| N001 | 虎嗅 | 商业与科技新闻 | {{latest_content}}  |  [订阅地址](https://www.huxiu.com/rss/0.xml) |
| N002 | 36kr | 创投与公司动态 | {{latest_content}}  |  [订阅地址](https://www.36kr.com/feed) |
| N003 | BBC 中文 | 国际综合新闻 | {{latest_content}}  |  [订阅地址](https://feeds.bbci.co.uk/zhongwen/simp/rss.xml) |
| <h2 id="数码产品">数码产品</h2> |  |   |  |
| D001 | 少数派 | 数码产品与效率工具 | {{latest_content}}  |  [订阅地址](https://sspai.com/feed) |
| D002 | 数字尾巴 | 数码产品评测与体验 | {{latest_content}}  |  [订阅地址](https://www.dgtle.com/rss/dgtle.xml) |
| D003 | 爱范儿 | 科技产品与互联网趋势 | {{latest_content}}  |  [订阅地址](https://www.ifanr.com/feed) |
| D004 | IT之家 | 国内外科技新品与行业快讯 | {{latest_content}}  |  [订阅地址](https://www.ithome.com/rss) |
| D005 | 小众软件 | 工具类软件与实用应用 | {{latest_content}}  |  [订阅地址](https://www.appinn.com/feed/) |

## 批量导入所有RSS订阅

OPML V2.0:  [https://raw.githubusercontent.com/zhaoolee/garss/main/zhaoolee_github_garss_subscription_list_v2.opml](https://raw.githubusercontent.com/zhaoolee/garss/main/zhaoolee_github_garss_subscription_list_v2.opml) 

OPML V2.0 备用CDN地址: [https://cdn.jsdelivr.net/gh/zhaoolee/garss/zhaoolee_github_garss_subscription_list_v2.opml](https://cdn.jsdelivr.net/gh/zhaoolee/garss/zhaoolee_github_garss_subscription_list_v2.opml)



> 如果RSS软件版本较老无法识别以上订阅,请使用[V1.0版本的OPML订阅信息](https://raw.githubusercontent.com/zhaoolee/garss/main/zhaoolee_github_garss_subscription_list_v1.opml) [V1.0版本的OPML订阅信息备用CDN地址](https://cdn.jsdelivr.net/gh/zhaoolee/garss/zhaoolee_github_garss_subscription_list_v1.opml)


## 如何定制自己的私人简报?

从 github.com/zhaoolee/garss.git 仓库, fork一份程序到自己的仓库

允许运行actions

![允许运行actions](https://cdn.fangyuanxiaozhan.com/assets/1630216112533FANcC1QY.jpeg)

在EditREADME.md中, 展示了zhaoolee已收集的RSS列表, 你可以参考每行的格式, 按行增删自己订阅的RSS

然后按照下图设置发件邮箱相关内容即可!

![](https://cdn.fangyuanxiaozhan.com/assets/1629970189283arACkBKe.png)

收件人请在 GitHub Secrets 中配置 `EMAIL_LISTS`

支持格式：
- `a@example.com,b@example.com`
- `a@example.com;b@example.com`
- 多行邮箱（每行一个）

设置完成后 在README.md文件的底部加个空格，并push，即可触发更新！

## 无法收到邮件怎么办

可以按照以下代码，自测一下自己的HOST, PASSWORD，USER 是否能顺利发邮件

```
!pip install yagmail

import yagmail

# 连接邮箱服务器
yag = yagmail.SMTP(user="填USER参数", password="填PASSWORD参数", host='填HOST参数')

# 邮箱正文
contents = ['今天是周末,我要学习, 学习使我快乐;', '<a href="https://www.python.org/">python官网的超链接</a>']

# 发送邮件
yag.send('填收件人邮箱', '主题:学习使我快乐', contents)
```

在线自测地址 [Colab： https://colab.research.google.com/](https://colab.research.google.com/)

![在线自测](https://i.v2ex.co/zQWM0V6b.png)

## 发送邮件的效果

![手机端优化后的邮件效果](https://cdn.fangyuanxiaozhan.com/assets/163039979740967wCT8RQ.jpeg)

![PC端优化后的邮件效果](https://cdn.fangyuanxiaozhan.com/assets/1630399693988c2tk8n7k.png)

## 微信交流群

[https://frp.v2fy.com/dynamic-picture/%E5%BE%AE%E4%BF%A1%E4%BA%A4%E6%B5%81%E7%BE%A4/qr.png](https://frp.v2fy.com/dynamic-picture/%E5%BE%AE%E4%BF%A1%E4%BA%A4%E6%B5%81%E7%BE%A4/qr.png)


## 广告位招租

![广告位招租](https://raw.githubusercontent.com/zhaoolee/ChineseBQB/master/README/zhaoolee-link.png)
