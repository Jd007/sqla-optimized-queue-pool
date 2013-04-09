### Optimized QueuePool for SQLAlchemy

An improved implementation of the default connection pool, QueuePool for SQLAlchemy.

##### Requirements:

* Python 2.6.x or later
* SQLAlchemy 0.7.x or later

##### How to Use:

1. Add the optimized_queue_pool.py file to your project
2. Import OptimizedQueuePool from optimized_queue_pool
3. When creating a SQLAlchemy database engine, pass OptimizedQueuePool in with the poolclass argument