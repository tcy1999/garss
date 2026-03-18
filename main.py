import feedparser
import time
import os
import re
import pytz
import html
from datetime import datetime
import yagmail
import requests
import markdown
import json
import shutil
from urllib.parse import urlparse
from email.utils import parsedate_to_datetime
from multiprocessing import Pool,  Manager



def extract_entry_date(entry, feed=None):
    for key in ("published_parsed", "updated_parsed"):
        parsed_value = entry.get(key)
        if parsed_value:
            return time.strftime("%Y-%m-%d", parsed_value)

    for key in ("published", "updated", "pubDate"):
        raw_value = entry.get(key)
        if raw_value:
            try:
                return parsedate_to_datetime(raw_value).strftime("%Y-%m-%d")
            except Exception:
                pass

    if feed:
        feed_meta = feed.get("feed", {})
        for key in ("published_parsed", "updated_parsed"):
            parsed_value = feed_meta.get(key)
            if parsed_value:
                return time.strftime("%Y-%m-%d", parsed_value)
        for key in ("published", "updated", "pubDate"):
            raw_value = feed_meta.get(key)
            if raw_value:
                try:
                    return parsedate_to_datetime(raw_value).strftime("%Y-%m-%d")
                except Exception:
                    pass

    return datetime.today().strftime("%Y-%m-%d")


def strip_html(raw_text):
    text = re.sub(r"<[^>]+>", " ", raw_text or "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_entry_description(entry):
    for key in ("summary", "description", "subtitle"):
        value = entry.get(key, "")
        if value:
            return strip_html(value)

    content_list = entry.get("content", [])
    if isinstance(content_list, list) and len(content_list) > 0:
        first_content = content_list[0]
        if isinstance(first_content, dict):
            value = first_content.get("value", "")
            if value:
                return strip_html(value)

    return ""


def normalize_title_for_dedupe(title):
    normalized = (title or "").strip().lower()
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def make_mail_title(title, description, min_title_len=20, max_desc_len=80):
    clean_title = re.sub(r"\s+", " ", (title or "").strip())
    if len(clean_title) >= min_title_len:
        return clean_title

    clean_desc = re.sub(r"\s+", " ", (description or "").strip())
    if not clean_desc:
        return clean_title

    if len(clean_desc) > max_desc_len:
        clean_desc = clean_desc[:max_desc_len].rstrip() + "..."
    return clean_title + " - " + clean_desc


def parse_feed_rows(edit_readme_md):
    feed_rows = []
    current_category = "未分类"
    for line in edit_readme_md.splitlines():
        if "<h2 id=" in line and "</h2>" in line:
            category_match = re.search(r'<h2 id="[^"]*">(.*?)</h2>', line)
            if category_match:
                current_category = category_match.group(1).strip()

        if "{{latest_content}}" not in line or "[订阅地址](" not in line:
            continue

        row_match = re.match(
            r"\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*\{\{latest_content\}\}\s*\|\s*\[订阅地址\]\((.*?)\)\s*\|",
            line.strip()
        )

        if row_match:
            feed_rows.append({
                "raw": line,
                "code": row_match.group(1).strip(),
                "name": row_match.group(2).strip(),
                "description": row_match.group(3).strip(),
                "link": row_match.group(4).strip(),
                "category": current_category
            })
            continue

        link_match = re.search(r"\[订阅地址\]\((.*?)\)", line)
        if not link_match:
            continue
        feed_rows.append({
            "raw": line,
            "code": "",
            "name": "",
            "description": "",
            "link": link_match.group(1).strip(),
            "category": current_category
        })

    return feed_rows


def get_rss_info(feed_url, index, rss_info_list):
    result = {"result": []}
    request_success = False
    # 如果请求出错,则重新请求,最多五次
    for i in range(3):
        if(request_success == False):
            try:
                headers = {
                    # 设置用户代理头(为狼披上羊皮)
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                    "Content-Encoding": "gzip"
                }
                # 三次分别设置8, 16, 24秒钟超时
                feed_response = requests.get(feed_url,  timeout= (i+1)*8 ,headers = headers)
                feed_response.raise_for_status()
                feed_url_content = feed_response.content
                feed = feedparser.parse(feed_url_content)
                feed_entries = feed.get("entries", [])
                feed_entries_length = len(feed_entries)
                print("==feed_url=>>", feed_url, "==len=>>", feed_entries_length)
                for entrie in feed_entries:
                    title = entrie.get("title", "")
                    link = entrie.get("link", "")
                    if not title or not link:
                        continue
                    date = extract_entry_date(entrie, feed)
                    description = extract_entry_description(entrie)

                    title = title.replace("\n", "")
                    title = title.replace("\r", "")

                    result["result"].append({
                        "title": title,
                        "link": link,
                        "date": date,
                        "description": description
                    })
                request_success = True
            except Exception as e:
                print(feed_url+"第+"+str(i)+"+次请求出错==>>",e)
                pass
        else:
            pass

    rss_info_list[index] = result["result"]
    print("本次爬取==》》", feed_url, "<<<===", index, result["result"])
    # 剩余数量
    remaining_amount = 0

    for tmp_rss_info_atom in rss_info_list:
        if(isinstance(tmp_rss_info_atom, int)):
            remaining_amount = remaining_amount + 1
            
    print("当前进度 | 剩余数量", remaining_amount, "已完成==>>", len(rss_info_list)-remaining_amount)
    return result["result"]
    


def send_mail(email, title, contents):
    # 判断secret.json是否存在
    user = ""
    password = ""
    host = ""
    try:
        if(os.environ["USER"]):
            user = os.environ["USER"]
        if(os.environ["PASSWORD"]):
            password = os.environ["PASSWORD"]
        if(os.environ["HOST"]):
            host = os.environ["HOST"]
    except:
        print("无法获取github的secrets配置信息,开始使用本地变量")
        if(os.path.exists(os.path.join(os.getcwd(),"secret.json"))):
            with open(os.path.join(os.getcwd(),"secret.json"),'r') as load_f:
                load_dict = json.load(load_f)
                user = load_dict["user"]
                password = load_dict["password"]
                host = load_dict["host"]
                # print(load_dict)
        else:
            print("无法获取发件人信息")
    
    # 连接邮箱服务器
    # yag = yagmail.SMTP(user=user, password=password, host=host)
    yag = yagmail.SMTP(user = user, password = password, host=host)
    # 发送邮件
    yag.send(email, title, contents)

def replace_readme():
    new_edit_readme_md = ["", ""]
    current_date_news_by_category = {}


    
    # 读取EditREADME.md
    print("replace_readme")
    new_num = 0
    with open(os.path.join(os.getcwd(),"EditREADME.md"),'r') as load_f:
        edit_readme_md = load_f.read();



        new_edit_readme_md[0] = edit_readme_md
        feed_rows = parse_feed_rows(edit_readme_md)
        # 填充统计RSS数量
        new_edit_readme_md[0] = new_edit_readme_md[0].replace("{{rss_num}}", str(len(feed_rows)))
        # 填充统计时间
        ga_rss_datetime = datetime.fromtimestamp(int(time.time()),pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
        new_edit_readme_md[0] = new_edit_readme_md[0].replace("{{ga_rss_datetime}}", str(ga_rss_datetime))

        # 使用进程池进行数据获取，获得rss_info_list
        feed_rows_len = len(feed_rows)
        rss_info_list = Manager().list(range(feed_rows_len))
        print('初始化完毕==》', rss_info_list)

        

        # 创建一个最多开启8进程的进程池
        po = Pool(8)

        for index, feed_row in enumerate(feed_rows):
            # 获取link
            link = feed_row["link"]
            po.apply_async(get_rss_info,(link, index, rss_info_list))


        # 关闭进程池,不再接收新的任务,开始执行任务
        po.close()

        # 主进程等待所有子进程结束
        po.join()
        print("----结束----", rss_info_list)


        today_str = datetime.today().strftime("%Y-%m-%d")
        seen_today_titles = set()

        for index, feed_row in enumerate(feed_rows):
            # 获取link
            link = feed_row["link"]
            category_name = feed_row["category"]
            # 生成超链接
            rss_info = rss_info_list[index]
            latest_content = ""
            parse_result = urlparse(link)
            scheme_netloc_url = str(parse_result.scheme)+"://"+str(parse_result.netloc)
            latest_content = "[暂无法通过爬虫获取信息, 点击进入源网站主页]("+ scheme_netloc_url +")"

            # 加入到索引
            try:
                for rss_info_atom in rss_info:
                    if (rss_info_atom["date"] == today_str):
                        title_key = normalize_title_for_dedupe(rss_info_atom.get("title", ""))
                        if title_key in seen_today_titles:
                            continue
                        seen_today_titles.add(title_key)
                        new_num = new_num + 1
                        category_list = current_date_news_by_category.setdefault(category_name, [])
                        category_list.append({
                            "title": make_mail_title(
                                rss_info_atom.get("title", ""),
                                rss_info_atom.get("description", "")
                            ),
                            "link": rss_info_atom["link"],
                            "index": new_num
                        })

            except:
                print("An exception occurred")
            

                
            if(len(rss_info) > 0):
                rss_info[0]["title"] = rss_info[0]["title"].replace("|", "\|")
                rss_info[0]["title"] = rss_info[0]["title"].replace("[", "\[")
                rss_info[0]["title"] = rss_info[0]["title"].replace("]", "\]")

                latest_content = "[" + "‣ " + rss_info[0]["title"] + ( " 🆕 " + rss_info[0]["date"] if (rss_info[0]["date"] == datetime.today().strftime("%Y-%m-%d")) else " \| " + rss_info[0]["date"] ) +"](" + rss_info[0]["link"] +")"  

            if(len(rss_info) > 1):
                rss_info[1]["title"] = rss_info[1]["title"].replace("|", "\|")
                rss_info[1]["title"] = rss_info[1]["title"].replace("[", "\[")
                rss_info[1]["title"] = rss_info[1]["title"].replace("]", "\]")

                latest_content = latest_content + "<br/>[" + "‣ " +  rss_info[1]["title"] + ( " 🆕 " + rss_info[0]["date"] if (rss_info[0]["date"] == datetime.today().strftime("%Y-%m-%d")) else " \| " + rss_info[0]["date"] ) +"](" + rss_info[1]["link"] +")"

            # 生成after_info
            after_info = feed_row["raw"].replace("{{latest_content}}", latest_content)
            print("====latest_content==>", latest_content)
            # 替换edit_readme_md中的内容
            new_edit_readme_md[0] = new_edit_readme_md[0].replace(feed_row["raw"], after_info)
    
    current_date_news_index = []
    for category_name, category_items in current_date_news_by_category.items():
        if len(category_items) == 0:
            continue
        current_date_news_index.append(
            "<h3 style='margin:18px 0 8px;color:#584D49;'>" + html.escape(category_name) + "</h3>"
        )
        for item_index, item in enumerate(category_items):
            line_style = "line-height:3;background-color:#F7FAFF;" if (item_index % 2) == 0 else "line-height:3;"
            current_date_news_index.append(
                "<div style='" + line_style + "' ><a href='" + item["link"] + "' " +
                'style="line-height:2;text-decoration:none;display:block;color:#584D49;">' +
                "🆕 ‣ " + html.escape(item["title"]) + " | 第" + str(item["index"]) + "篇" +
                "</a></div>"
            )

    # 替换EditREADME中的索引
    new_edit_readme_md[0] = new_edit_readme_md[0].replace("{{news}}", "".join(current_date_news_index))
    # 替换EditREADME中的新文章数量索引
    new_edit_readme_md[0] = new_edit_readme_md[0].replace("{{new_num}}", str(new_num))
    # 添加CDN
    new_edit_readme_md[0] = new_edit_readme_md[0].replace("./_media", "https://cdn.jsdelivr.net/gh/zhaoolee/garss/_media")
        
    # 将新内容
    with open(os.path.join(os.getcwd(),"README.md"),'w') as load_f:
        load_f.write(new_edit_readme_md[0])
    

    mail_re = r'邮件内容区开始>([.\S\s]*)<邮件内容区结束'
    reResult = re.findall(mail_re, new_edit_readme_md[0])
    new_edit_readme_md[1] = reResult

    
    return new_edit_readme_md

# 将README.md复制到docs中

def cp_readme_md_to_docs():
    shutil.copyfile(os.path.join(os.getcwd(),"README.md"), os.path.join(os.getcwd(), "docs","README.md"))
    
def cp_media_to_docs():
    if os.path.exists(os.path.join(os.getcwd(), "docs","_media")):
        shutil.rmtree(os.path.join(os.getcwd(), "docs","_media"))	
    shutil.copytree(os.path.join(os.getcwd(),"_media"), os.path.join(os.getcwd(), "docs","_media"))

def get_email_list():
    # 仅支持 CI/CD 环境变量（例如 GitHub Actions secrets: EMAIL_LISTS）
    # 支持格式: a@x.com,b@y.com 或按行分隔
    env_email_lists = os.environ.get("EMAIL_LISTS", "").strip()
    if env_email_lists:
        parts = re.split(r"[\n,;]+", env_email_lists)
        return [p.strip() for p in parts if p.strip()]
    return []

# 创建opml订阅文件

def create_opml():

    result = "";
    result_v1 = "";

    # <outline text="CNET News.com" description="Tech news and business reports by CNET News.com. Focused on information technology, core topics include computers, hardware, software, networking, and Internet media." htmlUrl="http://news.com.com/" language="unknown" title="CNET News.com" type="rss" version="RSS2" xmlUrl="http://news.com.com/2547-1_3-0-5.xml"/>

    with open(os.path.join(os.getcwd(),"EditREADME.md"),'r') as load_f:
        edit_readme_md = load_f.read();

        ## 将信息填充到opml_info_list
        opml_info_text_list =  re.findall(r'.*\{\{latest_content\}\}.*\[订阅地址\]\(.*\).*' ,edit_readme_md);

        for opml_info_text in opml_info_text_list:


            # print('==', opml_info_text)

            opml_info_text_format_data = re.match(r'\|(.*)\|(.*)\|(.*)\|(.*)\|.*\[订阅地址\]\((.*)\).*\|',opml_info_text)

            # print("data==>>", opml_info_text_format_data)

            # print("总信息", opml_info_text_format_data[0].strip())
            # print("编号==>>", opml_info_text_format_data[1].strip())
            # print("text==>>", opml_info_text_format_data[2].strip())
            # print("description==>>", opml_info_text_format_data[3].strip())
            # print("data004==>>", opml_info_text_format_data[4].strip())
            print('##',opml_info_text_format_data[2].strip())
            print(opml_info_text_format_data[3].strip())
            print(opml_info_text_format_data[5].strip())
            

            opml_info = {}
            opml_info["text"] = opml_info_text_format_data[2].strip()
            opml_info["description"] = opml_info_text_format_data[3].strip()
            opml_info["htmlUrl"] = opml_info_text_format_data[5].strip()
            opml_info["title"] = opml_info_text_format_data[2].strip()
            opml_info["xmlUrl"] = opml_info_text_format_data[5].strip()

            # print('opml_info==>>', opml_info);
            


            opml_info_text = '<outline  text="{text}" description="{description}" htmlUrl="{htmlUrl}" language="unknown" title="{title}" type="rss" version="RSS2" xmlUrl="{xmlUrl}"/>'

            opml_info_text_v1 = '      <outline text="{title}" title="{title}" type="rss"  \n            xmlUrl="{xmlUrl}" htmlUrl="{htmlUrl}"/>'

            opml_info_text =  opml_info_text.format(
                text=opml_info["text"], 
                description=opml_info["description"], 
                htmlUrl = opml_info["htmlUrl"],
                title=opml_info["title"],
                xmlUrl=opml_info["xmlUrl"]
            )

            opml_info_text_v1 =  opml_info_text_v1.format(
                htmlUrl = opml_info["htmlUrl"],
                title=opml_info["title"],
                xmlUrl=opml_info["xmlUrl"]
            )

            result = result + opml_info_text + "\n"

            result_v1 = result_v1 + opml_info_text_v1 + "\n"
    
    zhaoolee_github_garss_subscription_list = "";
    with open(os.path.join(os.getcwd(),"rss-template-v2.txt"),'r') as load_f:
        zhaoolee_github_garss_subscription_list_template = load_f.read();
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        date_created = datetime.utcnow().strftime(GMT_FORMAT);
        date_modified = datetime.utcnow().strftime(GMT_FORMAT);
        zhaoolee_github_garss_subscription_list = zhaoolee_github_garss_subscription_list_template.format(result=result, date_created=date_created, date_modified=date_modified);
        # print(zhaoolee_github_garss_subscription_list);

    # 将内容写入
    with open(os.path.join(os.getcwd(),"zhaoolee_github_garss_subscription_list_v2.opml"),'w') as load_f:
        load_f.write(zhaoolee_github_garss_subscription_list)

    zhaoolee_github_garss_subscription_list_v1 = ""
    with open(os.path.join(os.getcwd(),"rss-template-v1.txt"),'r') as load_f:
        zhaoolee_github_garss_subscription_list_template = load_f.read();
        zhaoolee_github_garss_subscription_list_v1 = zhaoolee_github_garss_subscription_list_template.format(result=result_v1);
        # print(zhaoolee_github_garss_subscription_list_v1);

    # 将内容写入
    with open(os.path.join(os.getcwd(),"zhaoolee_github_garss_subscription_list_v1.opml"),'w') as load_f:
        load_f.write(zhaoolee_github_garss_subscription_list_v1)




        
    # print(result)

def create_json():
    result = {"garssInfo": []}
    with open(os.path.join(os.getcwd(),"EditREADME.md"),'r') as load_f:
        edit_readme_md = load_f.read();
        ## 将信息填充到opml_info_list
        opml_info_text_list =  re.findall(r'.*\{\{latest_content\}\}.*\[订阅地址\]\(.*\).*' ,edit_readme_md);
        for opml_info_text in opml_info_text_list:
            opml_info_text_format_data = re.match(r'\|(.*)\|(.*)\|(.*)\|(.*)\|.*\[订阅地址\]\((.*)\).*\|',opml_info_text)
            opml_info = {}
            opml_info["description"] = opml_info_text_format_data[3].strip()
            opml_info["title"] = opml_info_text_format_data[2].strip()
            opml_info["xmlUrl"] = opml_info_text_format_data[5].strip()
            result["garssInfo"].append(opml_info)
    with open("./garssInfo.json","w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

def main():
    create_json()
    create_opml()
    readme_md = replace_readme()
    content = markdown.markdown(readme_md[0], extensions=['tables', 'fenced_code'])
    cp_readme_md_to_docs()
    cp_media_to_docs()
    email_list = get_email_list()

    mail_re = r'邮件内容区开始>([.\S\s]*)<邮件内容区结束'
    reResult = re.findall(mail_re, readme_md[0])

    try:
        send_mail(email_list, "嘎!RSS订阅", reResult)
    except Exception as e:
        print("==邮件设信息置错误===》》", e)


if __name__ == "__main__":
    main()
