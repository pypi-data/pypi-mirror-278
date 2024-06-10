import time
import concurrent.futures
import re
import openai
import threading
import os
import re
import openai

real_print=print
from lib.log_util import print

mock_status=0
# 会话类 
# 当前可用AK https://platform.openai.com/account/api-keys
# 当前账户余额 https://platform.openai.com/account/usage )
class Chat:

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", **kwargs):
        self.api_key = api_key
        self.model = model
        self.messages = []
        self.kwargs = kwargs
    
    def get_size(self):
        return len(self.messages)

    def request(self, text):
        print("Request Session:" + str(id(self)))
        print("Request length:" + str(len(self.messages)))
        print("Request Data:" + text)
        if mock_status==1:
            self.messages.append({"role": "user", "content": text})
            time.sleep(2)
            answer="这是回答-"+text
            self.messages.append({"role": "assistant", "content": answer})
            print("Response Data: " + answer)
            return answer
        self.messages.append({"role": "user", "content": text})
        completion = openai.ChatCompletion.create(
            api_key=self.api_key,
            model=self.model,
            messages=self.messages,
            **self.kwargs,
        )
        answer = completion.choices[0].message["content"]
        self.messages.append({"role": "assistant", "content": answer})
        print("Response Data: " + answer)
        return answer


# 会话管理类
class ChatManager:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.__api_key = api_key
        self.__model = model
        self.__lastSession = Chat(api_key=self.__api_key, model=self.__model)
        self.__lastNum = 0

    def __recentSession(self):
        if lastSession.get_size() > 10:
            print("当前会话已超过10次，重新建立一个新的会话")
            return newSession()
        return lastSession

    def __newSession(self):
        return Chat(api_key=self.__api_key, model=self.__model)

    def __request_task(session, question):
        result = session.request(question)
        return result

    def newQuestion(self,question):
        session = self.__newSession()
        return session.request(question)
        

    def continueQuestion(self,question="继续"):
         session = self.__recentSession()
         return session.request(question)


# 请求计时器，优化等待体验
class Timer:
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

    # 定义计时器函数
    def count_task(self,event):
        count = 0
        thread_name=threading.current_thread().getName()
        while not event.is_set():
            count += 1
            real_print(f"Count:{count} thread:{thread_name}", end="\r")
            time.sleep(1)
        real_print(end="\n")
        return count

    def request_with_timer(self,request_task, *args):
        # 提交计数器任务
        event = threading.Event()
        count_future = self.executor.submit(self.count_task, event)
        # 提交请求任务
        request_future = self.executor.submit(request_task, *args)
        # 获取请求的返回结果
        request_result = request_future.result()
        # 获取计数器返回结果
        event.set()
        count_result = count_future.result()
        thread_name=threading.current_thread().getName()
        print(f"Count Result:{str(count_result)} thread_name:{thread_name}")
        print(request_result)
        return request_result, count_result


def test_timer():
    question = """
    我想创建一个类：
- 用户类
  - 邮箱
  - 密码
  - 昵称
  - 头像
除了上面已经定义的类属性，还有id、create_time、update_time，这些属性是传入的，不要自动设置默认值。id名称不要加前缀。
用python实现，只保留init方法。
    """
    chatManager = ChatManager("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")
    timer = Timer()
    request_result, count_result = timer.request_with_timer(
        chatManager.newQuestion, question
    )
    assert count_result > 0
    if not mock_status:
        assert "class" in request_result


def test_session():
    api_key="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"
    session_1 = Chat(api_key=api_key, model="gpt-3.5-turbo")
    session_2 = Chat(api_key=api_key, model="gpt-3.5-turbo")
    if mock_status:
        session_1.request("数字1的后面是哪个数字?")
        session_2.request("数字101的后面是哪个数字?")
        session_1.request("再往后是哪个数字?") 
        session_2.request("再往后是哪个数字?")
    else:
        assert "2" in session_1.request("数字1的后面是哪个数字?")
        time.sleep(20)
        assert "102" in session_2.request("数字101的后面是哪个数字?")
        time.sleep(20)
        assert "3" in session_1.request("再往后是哪个数字?") 
        time.sleep(20)
        assert "103" in session_2.request("再往后是哪个数字?")
        time.sleep(20)

# test_session()