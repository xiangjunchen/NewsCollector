#pragma once
#include "Python.h"

class CTPVcPython
{
public:
	CTPVcPython(void);
	~CTPVcPython(void);
	
	void* LoadPythonFile(CString sPlugin);
	void* GetFunctionProc(CString sFuntionName,void *pPlugin);
	void* ProcPythonDemo();

	CString  CollectorFromUrl(CString sUrl);

};
