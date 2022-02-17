/*
 * Copyright (c) 2019 TAOS Data, Inc. <jhtao@taosdata.com>
 *
 * This program is free software: you can use, redistribute, and/or modify
 * it under the terms of the GNU Affero General Public License, version 3
 * or later ("AGPL"), as published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */
#ifndef TDENGINE_SCALAR_H
#define TDENGINE_SCALAR_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct SScalarCalcContext {

} SScalarCalcContext;

#define sclFatal(...)  qFatal(__VA_ARGS__)
#define sclError(...)  qError(__VA_ARGS__)
#define sclWarn(...)   qWarn(__VA_ARGS__)
#define sclInfo(...)   qInfo(__VA_ARGS__)
#define sclDebug(...)  qDebug(__VA_ARGS__)
#define sclTrace(...)  qTrace(__VA_ARGS__)

#define SCL_ERR_RET(c) do { int32_t _code = c; if (_code != TSDB_CODE_SUCCESS) { terrno = _code; return _code; } } while (0)
#define SCL_RET(c) do { int32_t _code = c; if (_code != TSDB_CODE_SUCCESS) { terrno = _code; } return _code; } while (0)
#define SCL_ERR_JRET(c) do { code = c; if (code != TSDB_CODE_SUCCESS) { terrno = code; goto _return; } } while (0)




#ifdef __cplusplus
}
#endif

#endif  // TDENGINE_SCALAR_H