###################################################################
#           Copyright (c) 2016 by TAOS Technologies, Inc.
#                     All rights reserved.
#
#  This file is proprietary and confidential to TAOS Technologies.
#  No part of this file may be reproduced, stored, transmitted,
#  disclosed or used in any form or by any means other than as
#  expressly provided by the written permission from Jianhui Tao
#
###################################################################

# -*- coding: utf-8 -*-

import random
import string
import os
import sys
import time
import taos
from util.log import tdLog
from util.cases import tdCases
from util.sql import tdSql
from util.dnodes import tdDnodes
from util.dnodes import *
from util.createdata import *
from util.where import *
import itertools
from itertools import product
from itertools import combinations
from faker import Faker
import subprocess

class TDTestCase:
    def caseDescription(self):
        '''
        case1<xyguo>:select * from stable where condition && select * from ( select front )
        case2<xyguo>:select * from stable where condition order by ts asc | desc && select * from ( select front )
        case3<xyguo>:select * from stable where condition order by ts limit && select * from ( select front )
        case4<xyguo>:select * from stable where condition order by ts limit offset && select * from ( select front )
        case5<xyguo>:
        case6<xyguo>:
        case7<xyguo>:
        case8<xyguo>:
        case9<xyguo>:
        case10<xyguo>:
        ''' 
        return

    def init(self, conn, logSql):
        tdLog.debug("start to execute %s" % __file__)
        tdSql.init(conn.cursor(), logSql)

        testcaseFilename = os.path.split(__file__)[-1]
        os.system("rm -rf query_new/%s.sql" % testcaseFilename )

    def run(self):
        tdSql.prepare()
        startTime = time.time() 

        db = "stable_db"
        tdCreateData.dropandcreateDB_random("%s" %db,1) 

        conn1 = taos.connect(host="127.0.0.1", user="root", password="taosdata", config="/etc/taos/")
        print(conn1)
        cur1 = conn1.cursor()
        tdSql.init(cur1, True)        
        cur1.execute('use "%s";' %db)
        sql = 'select * from stable_1 limit 5;'
        cur1.execute(sql)

        for i in range(2):
            try:
                testcaseFilename = os.path.split(__file__)[-1]
                taos_cmd1 = "taos -f query_new/%s.sql" % testcaseFilename
                _ = subprocess.check_output(taos_cmd1, shell=True).decode("utf-8")
                print(conn1)

                for i in range(2):
                    print(db)
                    cur1.execute('use "%s";' %db)                 

                    print("case1:select * from stable where condition && select * from ( select front )")
                    print("\n\n\n=========================================case1=========================================\n\n\n")

                    stable_where = tdWhere.stable_where()
                    sql1 = 'select * from stable_1;' 
                    for i in range(2,len(stable_where[2])+1):
                        qt_where = list(combinations(stable_where[2],i))
                        for qt_where in qt_where:
                            qt_where = str(qt_where).replace("(","").replace(")","").replace("'","").replace("\"","").replace(",","")
                            qt_in_where = stable_where[4]
                            sql2 = "select * from stable_1 where %s %s " %(qt_where,qt_in_where)
                            tdCreateData.dataequal('%s' %sql1 ,10,10,'%s' %sql2 ,10,10)
                            cur1.execute(sql2)

                            sql2 = "select * from (select * from stable_1 where %s %s ) " %(qt_where,qt_in_where)
                            tdCreateData.dataequal('%s' %sql1 ,10,10,'%s' %sql2 ,10,10)
                            cur1.execute(sql2)

                            sql2 = "select * from (select * from stable_1 ) where %s %s " %(qt_where,qt_in_where)
                            tdCreateData.dataequal('%s' %sql1 ,10,10,'%s' %sql2 ,10,10)
                            cur1.execute(sql2)

                    print("case2:select * from stable where condition order by ts asc | desc && select * from ( select front )")
                    print("\n\n\n=========================================case2=========================================\n\n\n")

                    stable_where = tdWhere.stable_where()
                    sql1 = 'select * from stable_1;' 
                    for i in range(2,len(stable_where[2])+1):
                        qt_where = list(combinations(stable_where[2],i))
                        for qt_where in qt_where:
                            qt_where = str(qt_where).replace("(","").replace(")","").replace("'","").replace("\"","").replace(",","")
                            qt_in_where = stable_where[4]
                            sql2 = "select * from stable_1 where tbname in ('table_1') and %s %s order by ts" %(qt_where,qt_in_where)
                            tdCreateData.dataequal('%s' %sql1 ,10,10,'%s' %sql2 ,10,10)
                            cur1.execute(sql2)

                            sql2 = "select * from (select * from stable_1 where tbname in ('table_1') and %s %s order by ts ) " %(qt_where,qt_in_where)
                            tdCreateData.dataequal('%s' %sql1 ,10,10,'%s' %sql2 ,10,10)
                            cur1.execute(sql2)

                            sql2 = "select * from (select * from stable_1  where tbname in ('table_1')) where %s %s order by ts " %(qt_where,qt_in_where)
                            tdCreateData.dataequal('%s' %sql1 ,10,10,'%s' %sql2 ,10,10)
                            cur1.execute(sql2)

                            sql2 = "select * from (select * from stable_1 ) where tbname in ('table_1') and %s %s order by ts " %(qt_where,qt_in_where)
                            tdSql.error(sql2)

                    print("case3:select * from stable where condition order by ts limit && select * from ( select front ) ")
                    print("\n\n\n=========================================case3=========================================\n\n\n")

                    stable_where = tdWhere.stable_where()
                    sql1 = 'select * from stable_1;' 
                    for i in range(2,len(stable_where[2])+1):
                        qt_where = list(combinations(stable_where[2],i))
                        for qt_where in qt_where:
                            qt_where = str(qt_where).replace("(","").replace(")","").replace("'","").replace("\"","").replace(",","")
                            qt_in_where = stable_where[4]
                            sql2 = "select * from stable_1 where tbname in ('table_1') and %s %s order by ts limit 10" %(qt_where,qt_in_where)
                            tdCreateData.dataequal('%s' %sql1 ,10,10,'%s' %sql2 ,10,10)
                            cur1.execute(sql2)

                            sql2 = "select * from (select * from stable_1 where tbname in ('table_1') and %s %s order by ts limit 10)" %(qt_where,qt_in_where)
                            tdCreateData.dataequal('%s' %sql1 ,10,10,'%s' %sql2 ,10,10)
                            cur1.execute(sql2)

                            sql2 = "select * from (select * from stable_1 where tbname in ('table_1')) where %s %s order by ts limit 10" %(qt_where,qt_in_where)
                            tdCreateData.dataequal('%s' %sql1 ,10,10,'%s' %sql2 ,10,10)
                            cur1.execute(sql2)

                            sql2 = "select * from (select * from stable_1) where tbname in ('table_1') and %s %s order by ts limit 10" %(qt_where,qt_in_where)
                            tdSql.error(sql2)

                    print("case4:select * from stable where condition order by ts limit offset && select * from ( select front )")
                    print("\n\n\n=========================================case4=========================================\n\n\n")

                    stable_where = tdWhere.stable_where()
                    sql1 = 'select * from stable_1 limit 10 offset 5;' 
                    for i in range(2,len(stable_where[2])+1):
                        qt_where = list(combinations(stable_where[2],i))
                        for qt_where in qt_where:
                            qt_where = str(qt_where).replace("(","").replace(")","").replace("'","").replace("\"","").replace(",","")
                            qt_in_where = stable_where[4]
                            sql2 = "select * from stable_1 where tbname in ('table_1') and %s %s order by ts limit 10 offset 5" %(qt_where,qt_in_where)
                            tdCreateData.dataequal('%s' %sql1 ,10,10,'%s' %sql2 ,10,10)
                            cur1.execute(sql2)

                            sql2 = "select * from (select * from stable_1 where tbname in ('table_1') and %s %s order by ts limit 10 offset 5)" %(qt_where,qt_in_where)
                            tdCreateData.dataequal('%s' %sql1 ,10,10,'%s' %sql2 ,10,10)
                            cur1.execute(sql2)

                            sql2 = "select * from (select * from stable_1 where tbname in ('table_1')) where %s %s order by ts limit 10 offset 5" %(qt_where,qt_in_where)
                            tdCreateData.dataequal('%s' %sql1 ,10,10,'%s' %sql2 ,10,10)
                            cur1.execute(sql2)

                            sql2 = "select * from (select * from stable_1) where tbname in ('table_1') and %s %s order by ts limit 10 offset 5" %(qt_where,qt_in_where)
                            tdSql.error(sql2)                                  

                    print("\n\n\n=======================================error case=======================================\n\n\n")
                    print("case1:select * from stable where condition interval | sliding | Fill && select * from ( select front )")
                    print("\n\n\n=========================================case1=========================================\n\n\n")

                    stable_where = tdWhere.stable_where()
                    sql1 = 'select * from stable_1 interval(3s) sliding(3n) Fill(NEXT);'  
                    for i in range(2,len(stable_where[2])+1):
                        q_where = list(combinations(stable_where[2],i))
                        for q_where in q_where:
                            q_where = str(q_where).replace("(","").replace(")","").replace("'","").replace("\"","").replace(",","")
                            q_in_where = stable_where[4]
                            time_window = stable_where[5]
                            sql2 = "select * from stable_1 where %s %s %s" %(q_where,q_in_where,time_window)
                            tdSql.error(sql2)

                            sql2 = "select * from (select * from stable_1 where %s %s %s)" %(q_where,q_in_where,time_window)
                            tdSql.error(sql2)

                            sql2 = "select * from (select * from stable_1) where %s %s %s" %(q_where,q_in_where,time_window)
                            tdSql.error(sql2)


            except Exception as e:
                raise e   

        endTime = time.time()
        print("total time %ds" % (endTime - startTime))
        
    def stop(self):
        tdSql.close()
        tdLog.success("%s successfully executed" % __file__)


tdCases.addWindows(__file__, TDTestCase())
tdCases.addLinux(__file__, TDTestCase())