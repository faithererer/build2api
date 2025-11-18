import time
from playwright.sync_api import TimeoutError


def keep_alive_task(page, logger, config):
    """
    定时执行Google搜索以保持cookies活跃
    """
    keep_alive_config = config.get('keep_alive', {})
    if not keep_alive_config.get('enabled', False):
        return
    
    interval = keep_alive_config.get('interval', 3600)  # 默认1小时
    search_query = keep_alive_config.get('search_query', 'hello')
    cookie_file = config.get('cookie_file', 'unknown')
    
    # 记录下次执行时间
    next_run = time.time() + interval
    logger.info(f"[{cookie_file}] keepAlive任务已启动，间隔{interval}秒")
    
    return next_run, interval, search_query, cookie_file


def check_keep_alive(page, logger, next_run, interval, search_query, cookie_file):
    """
    检查是否需要执行keepAlive任务
    """
    current_time = time.time()
    if current_time >= next_run:
        try:
            logger.info(f"[{cookie_file}] 执行keepAlive搜索任务...")
            
            # 创建新标签页进行搜索
            context = page.context
            search_page = context.new_page()
            search_url = f"https://www.google.com/search?q={search_query}"
            search_page.goto(search_url, timeout=30000)
            search_page.wait_for_timeout(2000)  # 等待2秒
            
            # 关闭搜索标签页
            search_page.close()
            
            logger.info(f"[{cookie_file}] keepAlive搜索完成")
            
        except TimeoutError:
            logger.warning(f"[{cookie_file}] keepAlive搜索超时")
        except Exception as e:
            logger.error(f"[{cookie_file}] keepAlive搜索失败: {e}")
        
        # 返回下次执行时间
        return current_time + interval
    
    return next_run