# pytech
  
Python package providing technical indicators and patterns implemented in C++.  
  
## 安装  
  
`pip install pytech-zp`  
  
## 说明
  
pytech 包中包含 pytech 模块和 getpricedata 模块。pytech 模块提供了技术指标和买卖信号的实现，getETFprice 模块提供了获取 ETF 数据的功能。其中 getETFprice 模块有以下依赖包：

pandas  
numpy  
pyodbc

同时需安装 ODBC Driver 17 for SQL Server。安装方法如下：
1. 打开网址：https://learn.microsoft.com/zh-cn/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16
2. 选择版本17，不要选择版本18
3. 64位下载：下载 Microsoft ODBC Driver 17 for SQL Server (x64)
https://go.microsoft.com/fwlink/?linkid=2266337
4. 32位下载：下载 Microsoft ODBC Driver 17 for SQL Server (x86)
https://go.microsoft.com/fwlink/?linkid=2266446
5. 双击下载好的文件安装即可

## getpricedata 模块的使用方法如下：
```python
from getpricedata import Params,GetETFprice
gparams = Params()
getETF = GetETFprice(gparams)
# getETFprice(ETFcode,startDate,endDate)
# ETFcode: ETF代码，例如'510300.SH'
# startDate: 开始日期，例如'2021-01-01'
# endDate: 结束日期，例如'2021-01-31'
# df 为 pandas 的 DataFrame 类型
# 输出位 [最高价，最低价，收盘价，开盘价，成交量，日期]
# [H, L, C, O, V, t]
df = getETF.getETFprice('510300.SH', '2021-01-01', '2021-01-31')
# 获取到当前最新日期的数据
from datetime import datetime
ETFcode = '510300.SH'
startDate = '2016-01-01'
endDate = datetime.now().date().strftime('%Y-%m-%d')
df = getETF.getETFprice(ETFcode, startDate, endDate)
```

## pytech 模块的使用方法如下：  
pytech 模块提供了技术指标函数和买卖信号函数。其中买卖信号函数通过类 Params 来设置参数，通过类 Signal 来获取买卖信号。 

Params 类包含了技术指标买卖信号的默认参数，可以通过修改 Params 类的属性来修改参数。

Params 类需要手动设置必要的价格数据，例如开盘价、最高价、最低价、收盘价、成交量。这些数据在类中默认为空值。

使用 Signal 类的函数需要首先实例化 Params 类，然后再调用 Signal 类的函数，通过设置 Params 类的价格属性来向 Signal 类传递价格数据。

Signal 类的函数返回一个 bool 类型的列表，列表的长度与价格数据的长度相同，列表的元素为 true 或 false，true 表示满足，false 表示不满足条件。
```python  
from pytech import pytech  
  
# 获取技术指标的买卖信号
params = pytech.Params()
signals = pytech.Signals()
params.C = df['C']
result = signals.MACDcrossup(params)

# 直接使用技术指标计算指标值
rDIF,rDEA,rMACD = pytech.MACD(params.C,12,26,9)
```
可以使用 help 来查看 pytech 包中的函数说明，例如：
```python
from pytech import pytech
help(pytech)
help(pytech.Signals.MACDcrossup) 
```
## 买卖信号函数列表如下：

- `MAcrossup(Params& params), params.C, params.MAdx, params.MAcx`
- `MAcrossdown(Params& params), params.C, params.MAdx, params.MAcx`
- `MAlong(Params& params), params.C, params.MAdx, params.MAcx`
- `MAshort(Params& params), params.C, params.MAdx, params.MAcx`
- `EMAcrossup(Params& params), params.C, params.EMAdx, params.EMAcx`
- `EMAcrossdown(Params& params), params.C, params.EMAdx, params.EMAcx`
- `EMAlong(Params& params), params.C, params.EMAdx, params.EMAcx`
- `EMAshort(Params& params), params.C, params.EMAdx, params.EMAcx`
- `WMAcrossup(Params& params), params.C, params.WMAdx, params.WMAcx`
- `WMAcrossdown(Params& params), params.C, params.WMAdx, params.WMAcx`
- `WMAlong(Params& params), params.C, params.WMAdx, params.WMAcx`
- `WMAshort(Params& params), params.C, params.WMAdx, params.WMAcx`
- `MACDcrossup(Params& params), params.C, params.MACDdx, params.MACDcx, params.MACDdea`
- `MACDcrossdown(Params& params), params.C, params.MACDdx, params.MACDcx, params.MACDdea`
- `ATRxy(Params& params), params.H, params.L, params.C, params.ATRzq, params.ATR1bs`
- `ATRqj(Params& params), params.H, params.L, params.C, params.ATRzq, params.ATR2xj, params.ATR2sj`
- `ASIcrossup(Params& params), params.H, params.L, params.C, params.O, params.ASIn, params.ASIm`
- `ASIcrossdown(Params& params), params.H, params.L, params.C, params.O, params.ASIn, params.ASIm`
- `ASIupbreakthrough(Params& params), params.H, params.L, params.C, params.O, params.ASIn, params.ASIm, params.ASItpzq`
- `ASIdownbreakthrough(Params& params), params.H, params.L, params.C, params.O, params.ASIn, params.ASIm, params.ASItpzq`
- `ROCcrossup(Params& params), params.C, params.ROCn`
- `ROCcrossdown(Params& params), params.C, params.ROCn`
- `RSIcrossup(Params& params), params.C, params.RSIdx, params.RSIcx`
- `RSIcrossdown(Params& params), params.C, params.RSIdx, params.RSIcx`
- `AROONupgrade(Params& params), params.C, params.AROONz, params.AROONzq`
- `AROONupless(Params& params), params.C, params.AROONz, params.AROONzq`
- `AROONdowngrade(Params& params), params.C, params.AROONz, params.AROONzq`
- `AROONdownless(Params& params), params.C, params.AROONz, params.AROONzq`
- `BOLLbreakup(Params& params), params.C, params.BOLLn`
- `BOLLbreakdown(Params& params), params.C, params.BOLLn`
- `BOLLlocalup(Params& params), params.C, params.BOLLn`
- `BOLLlocaldown(Params& params), params.C, params.BOLLn`
- `Kentner_ATRbreakup(Params& params), params.C, params.H, params.L, params.Kentner_ATRn, params.Kentner_ATRbs, params.Kentner_ATRmid`
- `Kentner_ATRbreakdown(Params& params), params.C, params.H, params.L, params.Kentner_ATRn, params.Kentner_ATRbs, params.Kentner_ATRmid`
- `Kentner_ATRoverup(Params& params), params.C, params.H, params.L, params.Kentner_ATRn, params.Kentner_ATRbs, params.Kentner_ATRmid`
- `Kentner_ATRbelowdown(Params& params), params.C, params.H, params.L, params.Kentner_ATRn, params.Kentner_ATRbs, params.Kentner_ATRmid`
- `KDJcrossup(Params& params), params.H, params.L, params.C, params.KDJrsv, params.KDJk, params.KDJd`
- `KDJcrossdown(Params& params), params.H, params.L, params.C, params.KDJrsv, params.KDJk, params.KDJd`
- `KDJlong(Params& params), params.H, params.L, params.C, params.KDJrsv, params.KDJk, params.KDJd`
- `KDJshort(Params& params), params.H, params.L, params.C, params.KDJrsv, params.KDJk, params.KDJd`
- `BBIcrossup(Params& params), params.C, params.BBIn1, params.BBIn2, params.BBIn3, params.BBIn4`
- `BBIcrossdown(Params& params), params.C, params.BBIn1, params.BBIn2, params.BBIn3, params.BBIn4`
- `BBIlong(Params& params), params.C, params.BBIn1, params.BBIn2, params.BBIn3, params.BBIn4`
- `BBIshort(Params& params), params.C, params.BBIn1, params.BBIn2, params.BBIn3, params.BBIn4`
- `WRoverbuy(Params& params), params.H, params.L, params.C, params.WRn, params.WRoverbuywr1`
- `WRoversell(Params& params), params.H, params.L, params.C, params.WRn, params.WRoversellwr1`
- `MFIcrossup(Params& params), params.H, params.L, params.C, params.V, params.MFIzq, params.MFIjxzq`
- `MFIcrossdown(Params& params), params.H, params.L, params.C, params.V, params.MFIzq, params.MFIjxzq`
- `OBVpriceup(Params& params), params.C, params.V, params.OBVn`
- `OBVpricedown(Params& params), params.C, params.V, params.OBVn`
- `CCIoverbuy(Params& params), params.H, params.L, params.C, params.CCIn`
- `CCIoversell(Params& params), params.H, params.L, params.C, params.CCIn`
- `TRIXcrossup(Params& params), params.C, params.TRIXzq, params.TRIXjxzq`
- `TRIXcrossdown(Params& params), params.C, params.TRIXzq, params.TRIXjxzq`
- `TRIXlong(Params& params), params.C, params.TRIXzq, params.TRIXjxzq`
- `TRIXshort(Params& params), params.C, params.TRIXzq, params.TRIXjxzq`
- `MTMcrossup(Params& params), params.C, params.MTMzq, params.MTMjxzq`
- `MTMcrossdown(Params& params), params.C, params.MTMzq, params.MTMjxzq`
- `DMAIcorossup(Params& params), params.C, params.DMAn1, params.DMAn2, params.DMAm`
- `DMAIcorossdown(Params& params), params.C, params.DMAn1, params.DMAn2, params.DMAm`
- `DMIcrossup(Params& params), params.H, params.L, params.C, params.DMIn`
- `DMIcrossdown(Params& params), params.H, params.L, params.C, params.DMIn`