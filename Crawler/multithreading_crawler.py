import threading
from abc import ABCMeta, abstractmethod


class TaskManager(metaclass=ABCMeta):

    def __init__(self):
        self.thread_lock = threading.Lock()

    @abstractmethod
    def acquire_task(self):
        """
        threads acquire tasks from here.\n
        if there aren't any tasks, this method should return None.
        """
        pass

    @abstractmethod
    def do_task(self, task):
        """
        this method tell the thread how to do the task.
        :return:
        """
        pass

    def run(self):
        print('please input the number of thread you want to use:', end='')
        thread_num = eval(input())
        if thread_num <= 0:
            print('please input a number bigger than zero!')
        else:
            thread_list = []
            for i in range(thread_num):
                thread_list.append(MultithreadingCrawler(i, self, self.thread_lock))
                thread_list[i].start()

            for i in range(thread_num):
                thread_list[i].join()


class MultithreadingCrawler(threading.Thread):

    def __init__(self, thread_id: int, task_manager: TaskManager, thread_lock: threading.Lock):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.flag = True
        self.task_manager = task_manager
        self.tread_lock = thread_lock

    def run(self):
        print('thread starts! thread_id: ', self.thread_id)
        while self.flag:
            # Mutex。 互斥访问acquire_task()方法
            self.tread_lock.acquire()
            # the thread acquire task from taskManager. 获取任务
            self.task = self.task_manager.acquire_task()
            self.tread_lock.release()
            # 如果没有获得任务，线程就结束
            if not self.task:
                self.flag = False
                continue
            # do task! 开始任务
            print('thread', self.thread_id, 'starts to do the task:', self.task)
            self.task_manager.do_task(self.task)
            print('thread', self.thread_id, 'finish to do the task:', self.task)
        print('thread ends! thread_id: ', self.thread_id)
