#include "StdAfx.h"
#include "TPCollectorData.h"

TPCollectorArray g_aCollector;

CTPCollectorData::CTPCollectorData(void)
{
	TPCollector *stuCollector = new TPCollector;
	stuCollector->m_sName = _T("ÍøÒ×ÐÂÎÅ");
	stuCollector->m_sStartUrl = _T("http://news.163.com/16/1124/13/C6L2K0IP000187VE.html");

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
