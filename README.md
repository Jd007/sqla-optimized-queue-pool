### Optimized QueuePool for SQLAlchemy

An improved implementation of the default connection pool, QueuePool for SQLAlchemy. The default pool seems to cause database connections errors when connections have been idle for longer than MySQL's `wait_timeout` variable, because the pool's refresh timer does not update after creation. The connection will attempt to connect but MySQL has timed out the connection.

This optimized pool updates the refresh timer each time the connection is used. which is what MySQL does (i.e. a connection's timer is reset after each query with that connection). This ensures proper re-use of connections in the pool while avoiding the disconnect issue.

##### Requirements:

* Python 2.6.x or later
* SQLAlchemy 0.7.x or later

##### How to Use:

1. Add the optimized_queue_pool.py file to your project
2. Import OptimizedQueuePool from optimized_queue_pool
3. When creating a SQLAlchemy database engine, pass OptimizedQueuePool in with the poolclass argument
4. Note: in the engine creation call, make sure the pool_recycle argument is set to a value less than MySQL's global `wait_timeout` variable (you can find out by running SHOW GLOBAL VARIABLES LIKE 'wait_timeout' in MySQL)