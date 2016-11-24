#include "StdAfx.h"
#include "TPCollectorData.h"

TPCollectorArray g_aCollector;

CTPCollectorData::CTPCollectorData(void)
{
	TPCollector *stuCollector = new TPCollector;
	stuCollector->m_sName = _T("ÍøÒ×ÐÂÎÅ");
	stuCollector->m_sStartUrl = _T("http://www.ibm.com/developerworks/cn/linux/l-pythc/");

	g_aCollector.RemoveAll();
	g_aCollector.Add(stuCollector);
}

CTPCollectorData::~CTPCollectorData(void)
{
	for (int l = 0 ; l < g_aCollector.GetSize(); l ++)
	{
		delete g_aCollector[l];
		g_aCollector[l] = NULL;
	}
	g_aCollector.RemoveAll();
}
