"""
现在已经可以将data列表，转成一个树状列表，但是又有新的要求了：
1. 增加一个add_element方法，可以将一个新的element添加到树中，并动态调整树的结构
2. 参考print_tree方法，实现一个write_tree方法，写入到文件里面
请用python实现。
"""
import datetime
import lib.database_util as database_util
import json

data = [
    {
        "url": "https://sspai.com/series/291",
        "title": "生产力超频：用 Keynote 入门动画创意 - 少数派",
        "tabId": 697700581,
        "openerTabId": 697700578,
        "add_time": "08:01",
    },
    {
        "url": "https://sspai.com/series/292",
        "title": "生产力超频：用 PPT 做漂亮幻灯片 - 少数派",
        "tabId": 697700582,
        "openerTabId": 697700578,
        "add_time": "08:02",
    },
    {
        "url": "https://sspai.com/series/293",
        "title": "深入理解如何打造独特的个人品牌 - 少数派",
        "tabId": 697700583,
        "openerTabId": None,
        "add_time": "08:03",
    },
    {
        "url": "https://sspai.com/series/294",
        "title": "写作与表达，是如何提升你的思考能力的？ - 少数派",
        "tabId": 697700584,
        "openerTabId": None,
        "add_time": "08:04",
    },
    {
        "url": "https://sspai.com/series/295",
        "title": "知识管理，如何高效学习和输出知识？ - 少数派",
        "tabId": 697700585,
        "openerTabId": 697700582,
        "add_time": "08:05",
    },
    {
        "url": "https://sspai.com/series/296",
        "title": "如何养成一个高效率的工作习惯？ - 少数派",
        "tabId": 697700586,
        "openerTabId": 697700585,
        "add_time": "08:06",
    },
    {
        "url": "https://sspai.com/series/297",
        "title": "如何用工具和方法化解做事的焦虑和压力？ - 少数派",
        "tabId": 697700587,
        "openerTabId": 697700586,
        "add_time": "08:07",
    },
    {
        "url": "https://sspai.com/series/298",
        "title": "少数派的 2021：为你的数字生活带来好习惯 - 少数派",
        "tabId": 697700588,
        "openerTabId": 697700587,
        "add_time": "08:08",
    },
]


class TreeNode:
    def __init__(self, title, url, tabId, openerTabId, add_time, children=None):
        self.title = title
        self.url = url
        self.tabId = tabId
        self.openerTabId = openerTabId
        self.children = children or []
        self.add_time = add_time

    def add_child(self, node):
        self.children.append(node)

    def add_element(self, element):
        node = TreeNode(
            element["title"],
            element["url"],
            element["tabId"],
            element["openerTabId"],
            element["add_time"],
        )
        if element["tabId"] in self.get_nodes():
            return
        nodes = {self.tabId: self}
        for child in self.children:
            nodes.update(child.get_nodes())
        if element["openerTabId"] is None:
            self.add_child(node)
        elif element["openerTabId"] not in nodes:
            self.add_child(node)
        else:
            parent = nodes[element["openerTabId"]]
            parent.add_child(node)

    def get_nodes(self):
        nodes = {self.tabId: self}
        for child in self.children:
            nodes.update(child.get_nodes())
        return nodes

    def print_tree(self, file=None, level=0):
        prefix = "    " * level
        text = f"{prefix}- {self.add_time} [{self.title}]({self.url})\n"
        if file is None:
            print(text, end="")
        else:
            file.write(text)
        for child in self.children:
            child.print_tree(file, level + 1)

    def write_tree(self, filename):
        with open(filename, "w") as f:
            self.print_tree(file=f)

    def toJson(self):
        """
        Serialize this TreeNode to a JSON string
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def fromJson(jsonStr):
        """
        Deserialize a JSON string to a TreeNode object
        """

        def dict_to_node(node_dict):
            node = TreeNode(
                node_dict["title"],
                node_dict["url"],
                node_dict["tabId"],
                node_dict["openerTabId"],
                node_dict["add_time"],
            )
            for child_dict in node_dict["children"]:
                child_node = dict_to_node(child_dict)
                node.add_child(child_node)
            return node

        return dict_to_node(json.loads(jsonStr))


def build_tree(elements):
    nodes = {
        e["tabId"]: TreeNode(
            e["title"], e["url"], e["tabId"], e["openerTabId"], e["add_time"]
        )
        for e in elements
    }
    root = TreeNode("Chrome浏览记录", "https://google.com", 0, 0, "00:00")

    for e in elements:
        if e["openerTabId"] is None:
            root.add_child(nodes[e["tabId"]])
        elif e["openerTabId"] not in nodes:
            root.add_child(nodes[e["tabId"]])
        else:
            parent = nodes[e["openerTabId"]]
            parent.add_child(nodes[e["tabId"]])
    return root


def add_item(url, title, tabId, openerTabId, add_time):
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    k = f"md/ChromeHistory-{now}.md"
    # 从redis中获取树状列表
    obj_str = database_util.load_str(k)
    if obj_str == None:
        tree = build_tree([])
    else:
        tree = TreeNode.fromJson(obj_str)
    tree.add_element(
        {
            "url": url,
            "title": title,
            "tabId": tabId,
            "openerTabId": openerTabId,
            "add_time": add_time,
        }
    )
    v = tree.toJson()
    # 将树状列表写入到redis中
    database_util.save_str(k, v)
    tree.write_tree(k)
    print(
        f"添加树状节点成功: url={url}, title={title}, tabId={tabId}, openerTabId={openerTabId},add_time={add_time}"
    )
    tree.print_tree()


def test_build_tree():
    tree = build_tree(data)
    tree.write_tree("md/test_build_tree.md")
    new_element = {
        "url": "https://sspai.com/series/299",
        "title": "测试",
        "tabId": 697700589,
        "openerTabId": 697700588,
        "add_time": "09:01",
    }
    tree.add_element(new_element)
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    tree.write_tree(f"md/test_build_tree-{now}.md")


def test_add_item():
    add_item(
        "https://sspai.com/series/299", "测试网页标题0901", 697700589, 697700588, "09:01"
    )


def test_json():
    # Create a new tree
    root = TreeNode("Root", "/", 1, None)
    root.add_element(
        {
            "title": "Child 1",
            "url": "/1",
            "tabId": 2,
            "openerTabId": None,
            "add_time": "09:01",
        }
    )
    root.add_element(
        {
            "title": "Child 2",
            "url": "/2",
            "tabId": 3,
            "openerTabId": 2,
            "add_time": "09:02",
        }
    )
    root.add_element(
        {
            "title": "Child 3",
            "url": "/3",
            "tabId": 4,
            "openerTabId": 2,
            "add_time": "09:03",
        }
    )

    # Serialize the tree to JSON
    jsonStr = root.toJson()

    # Deserialize the JSON string to a new tree
    new_root = TreeNode.fromJson(jsonStr)

    # Print the new tree
    new_root.print_tree()


# test_json()
# test_build_tree()
# test_add_item()