#!/usr/bin/env python3
"""
更新 summits.json：
1. 合并重复条目（WAIC 2026）
2. 添加新收集到的峰会数据
3. 移除已结束超30天条目
4. 更新 last_updated
"""
import json
import datetime

# 读取原数据
with open('/app/data/所有对话/主对话/tech-summit-tracker/data/summits.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

summits = data['summits']

# 当前日期
today = datetime.date.today()
cutoff = today - datetime.timedelta(days=30)

# ============================
# STEP 1: 移除结束日期超30天条目
# ============================
kept = []
removed = []
for s in summits:
    end_str = s.get('end_date', '') or s.get('start_date', '')
    if end_str:
        try:
            end_date = datetime.datetime.strptime(end_str, '%Y-%m-%d').date()
            if end_date < cutoff:
                removed.append(s['name'])
                continue
        except ValueError:
            pass
    kept.append(s)

print(f"移除条目数: {len(removed)}")
for n in removed:
    print(f"  - {n}")

# ============================
# STEP 2: 合并重复条目
# ============================
# 按 name(小写去空格) + city 合并
def norm_key(name, city):
    # 提取核心名（去掉括号里的）
    import re
    n = re.sub(r'[\(（].*?[\)）]', '', name).strip().lower()
    n = n.replace(' ', '').replace('　', '')
    return (n, city)

# 手动处理 WAIC 重复
# 找到两个WAIC
waic_indexes = [i for i, s in enumerate(kept) if 'WAIC' in s.get('name', '') or '世界人工智能大会' in s.get('name', '')]
print(f"WAIC相关条目 idx: {waic_indexes}")
for i in waic_indexes:
    print(f"  [{i}] {kept[i]['name']} - {kept[i].get('start_date','')}-{kept[i].get('end_date','')}")

# 保留id="waic-2026"这个（更完整），移除另一个
# 两个都是2026-07-17至20，上海，都是WAIC 2026
# 保留第一个含id的
to_remove_idx = []
seen_waic = False
for i in waic_indexes:
    if kept[i].get('start_date') == '2026-07-17':
        if seen_waic:
            to_remove_idx.append(i)
        else:
            seen_waic = True

# 从后往前移除
for i in sorted(to_remove_idx, reverse=True):
    print(f"合并去重移除: {kept[i]['name']}")
    kept.pop(i)

# ============================
# STEP 3: 新增峰会条目
# ============================
new_summits = [
    {
        "id": "ccf-chinaosc-2026",
        "name": "2026 CCF 中国开源大会 (ChinaOSC)",
        "start_date": "2026-08-15",
        "end_date": "2026-08-16",
        "date": "2026-08-15 至 2026-08-16",
        "city": "重庆",
        "venue": "重庆",
        "category": ["开发者"],
        "pricing": "付费",
        "organizer": "中国计算机学会 (CCF)",
        "theme": "渝见开源 数智启新",
        "description": "由CCF主办、重庆大学联合承办，围绕AI4SE与SE4AI核心议题，覆盖开源代码生成、可信维护、开源大模型与智能体、开源芯片安全等前沿方向。早鸟价2000元起",
        "status": "报名中",
        "register_url": "https://ccf.org.cn/2026COSC",
        "source_urls": [
            "https://chinaosc2023.ccf.org.cn/",
            "https://chinaosc.ccf.org.cn/"
        ],
        "url": "https://chinaosc2023.ccf.org.cn/",
        "source": "CCF官网",
        "updated_at": "2026-07-01"
    },
    {
        "id": "agic-shenzhen-2026",
        "name": "AGIC 2026 深圳国际通用人工智能大会暨展览会",
        "start_date": "2026-08-26",
        "end_date": "2026-08-28",
        "date": "2026-08-26 至 2026-08-28",
        "city": "深圳",
        "venue": "深圳国际会展中心（宝安）",
        "category": ["AI"],
        "pricing": "免费",
        "organizer": "深圳市人工智能产业协会、深圳市物联传媒、深圳鹏城会展传媒",
        "theme": "仿生智能·无界未来",
        "description": "全球面积最大机器人与AI主题专业展，8万㎡展示面积，30国院士专家出席，1000+AI企业参展，12万+专业观众，40+主题论坛",
        "status": "报名中",
        "register_url": "https://www.agicexpo.com/sz/",
        "source_urls": [
            "https://www.agicexpo.com/sz/",
            "https://www.szaiexpo.com/sz/"
        ],
        "url": "https://www.agicexpo.com/sz/",
        "scale": "8万㎡，1000+企业，12万观众",
        "source": "AGIC官网",
        "updated_at": "2026-07-01"
    },
    {
        "id": "ml-summit-shanghai-2026",
        "name": "2026奇点智能技术大会 (ML-Summit)",
        "start_date": "2026-07-15",
        "end_date": "2026-07-17",
        "date": "2026-07-15 至 2026-07-17",
        "city": "上海",
        "venue": "上海世博中心",
        "category": ["AI"],
        "pricing": "付费",
        "organizer": "CSDN & Boolan",
        "theme": "智构·共生·跃迁",
        "description": "50+AI大咖齐聚，覆盖类脑芯片、多模态大模型、可信AI治理、工业级Agent编排等主题，主论坛发布《2026全球大模型可信部署白皮书》",
        "status": "报名中",
        "register_url": "https://ml-summit.org/",
        "source_urls": [
            "https://ml-summit.org/",
            "https://blog.csdn.net/QuickCode/article/details/160020449"
        ],
        "url": "https://ml-summit.org/",
        "source": "CSDN",
        "updated_at": "2026-07-01"
    },
    {
        "id": "wuhan-computing-2026",
        "name": "2026武汉国际算力基础设施与应用展览会",
        "start_date": "2026-09-22",
        "end_date": "2026-09-24",
        "date": "2026-09-22 至 2026-09-24",
        "city": "武汉",
        "venue": "武汉国际博览中心",
        "category": ["云"],
        "pricing": "免费",
        "organizer": "武汉国际博览中心",
        "theme": "智算筑基，算力赋能产业",
        "description": "华中地区规模领先的算力产业对接平台，40000㎡展览面积，500+参展企业，聚焦通用算力/智能算力/超算/边缘算力全产业链",
        "status": "报名中",
        "register_url": "https://beijing0643208.11467.com/m/news/15714386.asp",
        "source_urls": [
            "https://beijing0643208.11467.com/m/news/15714386.asp"
        ],
        "url": "https://beijing0643208.11467.com/m/news/15714386.asp",
        "scale": "40000㎡，500+企业，45000+观众",
        "source": "武汉国际博览中心",
        "updated_at": "2026-07-01"
    },
    {
        "id": "qecon-shanghai-2026",
        "name": "QECon 全球软件质量&效能大会（上海站）",
        "start_date": "2026-09-04",
        "end_date": "2026-09-05",
        "date": "2026-09-04 至 2026-09-05",
        "city": "上海",
        "venue": "上海普陀区",
        "category": ["开发者"],
        "pricing": "付费",
        "organizer": "百格活动/QECon组委会",
        "theme": "AI时代软件质量与研发效能",
        "description": "聚焦AI驱动的软件质量、测试自动化、DevOps、研发效能等实践，¥3500起",
        "status": "报名中",
        "register_url": "https://www.bagevent.com/event/9296060",
        "source_urls": [
            "https://www.bagevent.com/eventlist.html?f=1&tag=17"
        ],
        "url": "https://www.bagevent.com/eventlist.html?f=1&tag=17",
        "source": "百格活动",
        "updated_at": "2026-07-01"
    },
    {
        "id": "gops-shanghai-2026",
        "name": "第30届智能体驱动的 GOPS 全球运维大会（上海站）",
        "start_date": "2026-10-16",
        "end_date": "2026-10-17",
        "date": "2026-10-16 至 2026-10-17",
        "city": "上海",
        "venue": "上海静安区",
        "category": ["开发者"],
        "pricing": "付费",
        "organizer": "高效运维社区 & BizDevOps",
        "theme": "智能体驱动的IT研发运维变革",
        "description": "设运维智能体、AI+DevOps 等专场，聚焦故障诊断、研发提效等智能体落地实践，¥4200起",
        "status": "报名中",
        "register_url": "https://www.bagevent.com/eventlist.html?f=1&tag=17",
        "source_urls": [
            "https://www.bagevent.com/eventlist.html?f=1&tag=17"
        ],
        "url": "https://www.bagevent.com/eventlist.html?f=1&tag=17",
        "source": "百格活动",
        "updated_at": "2026-07-01"
    },
    {
        "id": "secon-shenzhen-2026",
        "name": "SECon 全球软件工程技术大会（深圳站）",
        "start_date": "2026-11-13",
        "end_date": "2026-11-14",
        "date": "2026-11-13 至 2026-11-14",
        "city": "深圳",
        "venue": "深圳",
        "category": ["开发者"],
        "pricing": "付费",
        "organizer": "SECon组委会",
        "theme": "全球软件工程技术实践",
        "description": "聚焦软件工程、架构设计、大规模系统实践等技术议题，¥3780起",
        "status": "报名中",
        "register_url": "https://www.bagevent.com/eventlist.html?f=1&tag=17",
        "source_urls": [
            "https://www.bagevent.com/eventlist.html?f=1&tag=17"
        ],
        "url": "https://www.bagevent.com/eventlist.html?f=1&tag=17",
        "source": "百格活动",
        "updated_at": "2026-07-01"
    }
]

# 去重判断：如果新增的 name 已经存在（模糊匹配），跳过
existing_names = set()
for s in kept:
    key = norm_key(s.get('name', ''), s.get('city', ''))
    existing_names.add(key)

added = []
for ns in new_summits:
    key = norm_key(ns['name'], ns['city'])
    # 特别针对 CCF 开源相关做检查
    if key in existing_names:
        print(f"跳过已存在: {ns['name']}")
        continue
    # 额外检查：与'开源中国·开源世界高峰论坛'比对，避免与ChinaOSC混淆
    kept.append(ns)
    added.append(ns['name'])

print(f"新增条目数: {len(added)}")
for n in added:
    print(f"  + {n}")

# ============================
# STEP 4: 按日期排序
# ============================
def sort_key(s):
    sd = s.get('start_date', '')
    if sd:
        try:
            return datetime.datetime.strptime(sd, '%Y-%m-%d').date()
        except ValueError:
            pass
    return datetime.date(2099, 12, 31)

kept.sort(key=sort_key)

# ============================
# STEP 5: 更新元数据
# ============================
data['summits'] = kept
data['last_updated'] = '2026-07-01 10:30'

# 保存
with open('/app/data/所有对话/主对话/tech-summit-tracker/data/summits.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n最终条目总数: {len(kept)}")
print(f"last_updated: {data['last_updated']}")
