import threading
import time

########### Thread ###########
def run_thread(func, **kwargs):
    """
    주어진 함수를 백그라운드 스레드에서 실행하고, 결과를 result_container에 저장합니다.
    
    :param func: 백그라운드에서 실행할 함수
    :param kwargs: 함수에 전달할 키워드 인수
    :return: 함수 실행 결과와 상태를 담는 딕셔너리
    """
    
    result_container = {'done': False, 'result': None, 'error': None}
    
    def wrapper():
        try:
            result = func(**kwargs)
            result_container['result'] = result
        except Exception as e:
            result_container['error'] = str(e)
        finally:
            result_container['done'] = True

    # 백그라운드에서 실행할 스레드 생성
    thread = threading.Thread(target=wrapper)
    result_container['thread'] = thread
    
    # 스레드를 데몬으로 설정 (메인 프로그램 종료 시 강제 종료)
    thread.daemon = True
    
    # 스레드 시작
    thread.start()
    
    return result_container


def run_thread_multi(func, kwargs_list=[], sleep=0.05):
    """
    동일한 함수를 여러 인자로 백그라운드 스레드에서 여러 번 실행하고, 결과를 저장합니다.
    
    :param func: 백그라운드에서 실행할 함수
    :param kwargs_list: 각 호출에 사용할 키워드 인수들의 리스트
    :param sleep: 각 스레드의 상태를 확인할 대기 시간 (초)
    :return: 각 호출의 결과와 상태를 담는 딕셔너리
    """
    
    result_container = {'done': False, 'result': None, 'error': None}
    
    def wrapper():
        try:
            result = []
            for kwargs in kwargs_list:
                result.append(run_thread(func, **kwargs))
            result_container['result'] = result

            while True:
                done = True
                for a_result in result:
                    if not a_result['done']:
                        done = False
                        break
                if done:
                    result_container['done'] = True
                    break
                time.sleep(sleep)
        except Exception as e:
            result_container['error'] = str(e)
        finally:
            result_container['done'] = True
   
    # 백그라운드에서 실행할 스레드 생성
    thread = threading.Thread(target=wrapper)
    result_container['thread'] = thread
        
    # 스레드를 데몬으로 설정 (메인 프로그램 종료 시 강제 종료)
    thread.daemon = True
    
    # 스레드 시작
    thread.start()
    
    return result_container


def thread_join(result_container, max_time=60, sleep=0.05):
    """
    주어진 시간 내에 백그라운드 스레드가 완료될 때까지 대기합니다.
    
    :param result_container: 스레드의 결과와 상태를 담고 있는 딕셔너리
    :param max_time: 최대 대기 시간 (초)
    :param sleep: 각 스레드의 상태를 확인할 대기 시간 (초)
    :return: 완료된 스레드의 결과와 상태를 담은 딕셔너리
    """
    
    s_time = time.time()
    while not result_container['done']:
        if time.time() - s_time > max_time:
            raise Exception(f"max_time : {max_time} sec")
        time.sleep(sleep)
    return result_container
