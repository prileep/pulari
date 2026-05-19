import pymysql

# This line tricks Django's version check
pymysql.version_info = (2, 2, 8, "final", 0)
pymysql.install_as_MySQLdb()