import redis
import time
 
if __name__ == '__main__':
    print('web start to work')
    rcon = redis.StrictRedis(host='localhost', db=5)
    task_queue = 'task:prodcons:task_queue'
    result_queue = 'task:prodcons:result_queue'
    try:
        while True:
            str_time = time.asctime()
            codes = ['Aron', 'Bob', 'Mike', 'John', 'Ian']
            str_codes = ','.join(codes)
            rcon.rpush(task_queue, str_codes)
            print("Task create: {}, at {}".format(str_codes, str_time))
            print('Now waiting crawler to feedback the data')
            start_time = time.time()
            codes_crawler_result = {}
            while start_time + 8 - time.time() > 0 :
                #time.sleep(20)
              code = rcon.blpop(result_queue, 1)
              if not code:
                continue
              code = code[1].decode('utf-8')
              codes_crawler_result[code] = rcon.get('ssxx_{}'.format(code))
              print('  Task Result from queue:', code , ' at ', time.asctime(), ' reulst is:', codes_crawler_result[code])
              if len(codes) == len(codes_crawler_result):
                print('  *All task result is OK now, break the while loop:', time.time() - start_time )
                break
            else:
              print(' ****only {} task result is ok: '.format(len(codes_crawler_result)), time.time() - start_time )
              
    except KeyboardInterrupt:
        pass
        
        
   
import redis
import time
import random
import asyncio

task_queue = 'task:prodcons:task_queue'
result_queue = 'task:prodcons:result_queue'
 
#class Task(object):
#    def __init__(self):
#        self.rcon = redis.StrictRedis(host='localhost', db=5)
#        self.queue = 'task:prodcons:queue'
# 
#    def product_task(self):
#        while True:
#            str_time = time.asctime()
#            task = self.rcon.rpush(self.queue, str_time)
#            coffee_time = random.randint(1,20)
#            print("Task create: {}, and will have a coffee for {}s".format(task, coffee_time))
#            time.sleep(coffee_time)
#

async def crawler(code):
  coffee_time = random.randint(1,10)
  await asyncio.sleep(coffee_time)
  rcon.setex('ssxx_{}'.format(code), 5, '{} result at {}'.format(code, time.asctime()))
  #rcon.set('ssxx_{}'.format(code), '{} result at {}'.format(code, time.asctime()))
  rcon.rpush(result_queue, code)
  print('Task {} result at {}'.format(code, time.asctime()), " it takes ", coffee_time, ' s')

def done_callback(futu):
    print('Done')
 
if __name__ == '__main__':
    print('crawler start to work')
    rcon = redis.StrictRedis(host='localhost', db=5)
    loop = asyncio.get_event_loop()
    cnt_task = 0
    try:
        while True:
            str_time = time.asctime()
            codes = rcon.blpop(task_queue, 1)
            if not codes:
              continue
            codes = codes[1].decode('utf-8').split(',')
            print('##Task from queue:', codes , ' at ', str_time)
            #tasks = [ crawler(code) for code in codes ]
            #loop.run_until_complete(crawler('1'))
            #futu = asyncio.ensure_future(crawler('1'))
            #futu.add_done_callback(done_callback)
            
            #loop.run_until_complete(futu)
            tasks = []
            for code in codes:
                futu = asyncio.ensure_future(crawler(code))
                futu.add_done_callback(done_callback)
                tasks.append(futu)
            loop.run_until_complete(asyncio.gather(*tasks))
            
            cnt_task = cnt_task + 1
            print("##All task done. {}".format(cnt_task))
    except KeyboardInterrupt:
        pass
