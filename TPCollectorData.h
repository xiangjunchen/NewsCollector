#pragma once

struct TPCollector 
{
	CString m_sName;
	CString m_sStartUrl;
};
typedef CArray<TPCollector *,TPCollector *&> TPCollectorArray;


class CTPCollectorData
{
public:
	CTPCollectorData(void);
	~CTPCollectorData(void);
};
